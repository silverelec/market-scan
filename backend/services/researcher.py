"""
Shared research service: parallel Tavily + Exa queries.

Usage:
    results = await run_research(queries, request)
    # results: dict[str, list[SearchResult]]
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Any

from tavily import AsyncTavilyClient
from anthropic import AsyncAnthropic

from backend.core.config import get_settings
from backend.schemas.request import ScanRequest

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    url: str
    title: str
    content: str          # Full text (Tavily) or snippet (Exa)
    published_date: str   # ISO date string or empty
    source: str           # "tavily" | "exa"
    score: float = 0.0


async def _tavily_search(
    client: AsyncTavilyClient,
    query: str,
    days: int,
    max_results: int,
) -> list[SearchResult]:
    """Single Tavily search, returns SearchResult list."""
    try:
        response = await client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            days=days,
            include_raw_content=False,
        )
        results = []
        for r in response.get("results", []):
            results.append(SearchResult(
                url=r.get("url", ""),
                title=r.get("title", ""),
                content=r.get("content", ""),
                published_date=r.get("published_date", ""),
                source="tavily",
                score=r.get("score", 0.0),
            ))
        return results
    except Exception as e:
        logger.warning(f"Tavily search failed for '{query}': {e}")
        return []


async def _exa_search(
    query: str,
    start_date: str,
    max_results: int,
) -> list[SearchResult]:
    """Single Exa semantic search."""
    try:
        import exa_py
        settings = get_settings()
        client = exa_py.Exa(api_key=settings.exa_api_key)

        # Exa is sync — run in thread pool
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.search_and_contents(
                query,
                num_results=max_results,
                start_published_date=start_date,
                text=True,
                highlights=False,
            ),
        )
        results = []
        for r in response.results:
            results.append(SearchResult(
                url=r.url,
                title=r.title or "",
                content=(r.text or "")[:2000],  # cap at 2k chars
                published_date=r.published_date or "",
                source="exa",
                score=r.score or 0.0,
            ))
        return results
    except Exception as e:
        logger.warning(f"Exa search failed for '{query}': {e}")
        return []


def _deduplicate(results: list[SearchResult]) -> list[SearchResult]:
    """Remove duplicate URLs, preferring higher-scored results."""
    seen: dict[str, SearchResult] = {}
    for r in sorted(results, key=lambda x: x.score, reverse=True):
        if r.url and r.url not in seen:
            seen[r.url] = r
    return list(seen.values())


def format_results_as_markdown(results: list[SearchResult], max_chars: int = 8000) -> str:
    """Format search results as markdown for Claude prompts."""
    lines = []
    total_chars = 0
    for i, r in enumerate(results, 1):
        entry = f"[{i}] **{r.title}** ({r.published_date})\nURL: {r.url}\n{r.content}\n"
        if total_chars + len(entry) > max_chars:
            break
        lines.append(entry)
        total_chars += len(entry)
    return "\n---\n".join(lines) if lines else "No search results available."


async def run_research(
    queries: dict[str, list[str]],
    request: ScanRequest,
    exa_queries: list[str] | None = None,
) -> dict[str, list[SearchResult]]:
    """
    Run all Tavily queries (and optionally Exa queries) in parallel.

    Args:
        queries: {group_key: [query_string, ...]}
        request: ScanRequest with time period info
        exa_queries: optional list of Exa semantic queries (appended to "exa" key)

    Returns:
        {group_key: [SearchResult, ...]}
    """
    settings = get_settings()
    tavily_client = AsyncTavilyClient(api_key=settings.tavily_api_key)

    # Build flat list of (group_key, query, source) coroutines
    tasks: list[tuple[str, asyncio.Task]] = []

    for group_key, query_list in queries.items():
        for query in query_list:
            task = asyncio.create_task(
                _tavily_search(
                    tavily_client,
                    query,
                    days=request.tavily_days,
                    max_results=settings.tavily_results_per_query,
                )
            )
            tasks.append((group_key, task))

    # Add Exa queries if enabled and provided
    exa_tasks: list[asyncio.Task] = []
    if settings.exa_enabled and exa_queries:
        for query in exa_queries:
            exa_task = asyncio.create_task(
                _exa_search(
                    query,
                    start_date=request.exa_start_date,
                    max_results=settings.exa_results_per_query,
                )
            )
            exa_tasks.append(exa_task)

    # Await all Tavily tasks
    await asyncio.gather(*[t for _, t in tasks], return_exceptions=True)

    # Collect results by group
    results: dict[str, list[SearchResult]] = {k: [] for k in queries}
    for group_key, task in tasks:
        if not task.exception():
            results[group_key].extend(task.result())

    # Collect Exa results into "exa" group
    if exa_tasks:
        await asyncio.gather(*exa_tasks, return_exceptions=True)
        exa_results: list[SearchResult] = []
        for task in exa_tasks:
            if not task.exception():
                exa_results.extend(task.result())
        results["exa"] = _deduplicate(exa_results)

    # Deduplicate within each group
    for key in results:
        results[key] = _deduplicate(results[key])

    return results


def get_claude_client() -> AsyncAnthropic:
    settings = get_settings()
    return AsyncAnthropic(api_key=settings.anthropic_api_key)
