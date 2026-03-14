# Market Intelligence Platform

Boardroom-ready market research in minutes. Enter a market, get a structured intelligence report — no lengthy prompting required.

Runs parallel AI-driven web search across Tavily and Exa, synthesises results with Claude, and exports polished PDF reports.

---

## What it does

| Tool | Output |
|---|---|
| **Market Scan** | Market sizing, structure, competitive landscape, customer segments, technology trends, geography, and strategic opportunities |
| **Competitor Analysis** | Deep-dive profiles: business model, GTM motion, financials, strengths/weaknesses, benchmarking matrix, and recommendations |
| **Innovation Case Studies** | 5 curated case studies from the market with impact analysis, outcomes, and client relevance assessment |

Reports are generated in ~5 minutes and exported as PDFs.

---

## Stack

- **Backend** — FastAPI + Python, async parallel research via Tavily and Exa, Claude for synthesis, PDF generation via xhtml2pdf/Jinja2
- **Frontend** — Next.js 14, TypeScript, Tailwind CSS
- **AI** — Claude (`claude-sonnet`) for structured report synthesis, Tavily for real-time web search, Exa for semantic/analyst-report search

---

## Prerequisites

- Python 3.11+
- Node.js 18+
- API keys: [Anthropic](https://console.anthropic.com/settings/keys), [Tavily](https://app.tavily.com/) (required), [Exa](https://exa.ai/) (optional, recommended)

---

## Setup

### 1. Clone and configure

```bash
git clone https://github.com/your-username/market-scan.git
cd market-scan
```

Copy the environment files and fill in your API keys:

```bash
cp .env.example .env
cp frontend/.env.local.example frontend/.env.local
```

`.env` (backend):
```env
ANTHROPIC_API_KEY=sk-ant-...
TAVILY_API_KEY=tvly-...
EXA_API_KEY=...          # optional but recommended
```

`frontend/.env.local`:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 2. Backend

```bash
pip install -r requirements.txt
python -m backend.main
```

Backend runs at `http://localhost:8000`. API docs at `http://localhost:8000/docs`.

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:3000`.

---

## Project structure

```
backend/
  api/          # FastAPI route handlers (market_scan, competitor, casestudy)
  core/         # Config and settings
  pdf/          # PDF renderer, charts, HTML templates
  schemas/      # Pydantic request/response models
  services/     # Research orchestration and report builders
frontend/
  app/          # Next.js pages
  components/   # UI components and report views
  hooks/        # Job polling hook
  lib/          # API client and types
.tmp/           # Temporary files (auto-generated, gitignored)
.env.example    # Backend environment template
```

---

## How it works

1. User submits a scan request (market name, time period, optional context)
2. Backend generates 30+ targeted search queries and fires them in parallel
3. Tavily returns real-time web results; Exa surfaces analyst reports and whitepapers
4. Results are deduplicated and batched; Claude synthesises each report section concurrently
5. Structured JSON is returned to the frontend for live rendering
6. User can download the full report as a PDF

---

## API keys and costs

| Service | Free tier | Used for |
|---|---|---|
| Anthropic Claude | Pay-per-use | Report synthesis |
| Tavily | 1,000 searches/month | Real-time web search |
| Exa | 1,000 searches/month | Semantic / analyst search |

A single full market scan uses roughly 30–40 Tavily queries and 5–10 Exa queries.
