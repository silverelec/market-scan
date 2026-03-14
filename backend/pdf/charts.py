"""
Matplotlib chart generators → base64-encoded PNG strings for PDF embedding.
"""

import base64
import io
from typing import Optional


def _b64(fig) -> str:
    """Convert matplotlib figure to base64 PNG string."""
    import matplotlib
    matplotlib.use("Agg")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    buf.seek(0)
    data = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    return data


SLATE_900 = "#0f172a"
SLATE_700 = "#334155"
SLATE_400 = "#94a3b8"
SLATE_200 = "#e2e8f0"
AMBER_500 = "#f59e0b"
EMERALD_600 = "#059669"
ROSE_600 = "#e11d48"
SKY_600 = "#0284c7"


def tam_sam_som_chart(tam: Optional[float], sam: Optional[float], som: Optional[float]) -> str:
    """Horizontal bar chart for TAM / SAM / SOM."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np

    values = [v for v in [tam, sam, som] if v is not None]
    labels = ["labels"]
    label_map = {"TAM": tam, "SAM": sam, "SOM": som}
    filtered = {k: v for k, v in label_map.items() if v is not None}
    if not filtered:
        return ""

    fig, ax = plt.subplots(figsize=(7, 2.5))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    colors = [SLATE_700, AMBER_500, EMERALD_600]
    bars = ax.barh(list(filtered.keys()), list(filtered.values()),
                   color=colors[:len(filtered)], height=0.5)

    for bar, val in zip(bars, filtered.values()):
        ax.text(bar.get_width() + max(filtered.values()) * 0.01, bar.get_y() + bar.get_height() / 2,
                f"${val:.1f}B", va="center", fontsize=10, color=SLATE_900, fontweight="bold")

    ax.set_xlabel("USD Billions", color=SLATE_400, fontsize=9)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(colors=SLATE_700, labelsize=10)
    ax.set_xlim(0, max(filtered.values()) * 1.25)
    ax.xaxis.label.set_color(SLATE_400)
    for spine in ax.spines.values():
        spine.set_color(SLATE_200)
    plt.tight_layout()
    result = _b64(fig)
    plt.close(fig)
    return result


def market_growth_chart(historical: list, forecast: list) -> str:
    """Line chart: historical + forecast market size."""
    import matplotlib.pyplot as plt

    if not historical and not forecast:
        return ""

    fig, ax = plt.subplots(figsize=(8, 3.5))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    if historical:
        h_years = [d.get("year") or d["year"] if isinstance(d, dict) else d.year for d in historical]
        h_vals = [d.get("value_usd_bn") or d["value_usd_bn"] if isinstance(d, dict) else d.value_usd_bn for d in historical]
        ax.plot(h_years, h_vals, color=SLATE_700, linewidth=2.5, marker="o", markersize=5, label="Historical")

    if forecast:
        f_years = [d.get("year") or d["year"] if isinstance(d, dict) else d.year for d in forecast]
        f_vals = [d.get("value_usd_bn") or d["value_usd_bn"] if isinstance(d, dict) else d.value_usd_bn for d in forecast]
        # Connect to last historical point
        if historical:
            connect_year = h_years[-1]
            connect_val = h_vals[-1]
            ax.plot([connect_year] + f_years, [connect_val] + f_vals,
                    color=AMBER_500, linewidth=2.5, marker="o", markersize=5,
                    linestyle="--", label="Forecast")
        else:
            ax.plot(f_years, f_vals, color=AMBER_500, linewidth=2.5, marker="o", markersize=5,
                    linestyle="--", label="Forecast")

    ax.set_ylabel("USD Billions", color=SLATE_400, fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors=SLATE_700, labelsize=9)
    for spine in ax.spines.values():
        spine.set_color(SLATE_200)
    ax.legend(fontsize=9, framealpha=0)
    ax.yaxis.label.set_color(SLATE_400)
    plt.tight_layout()
    result = _b64(fig)
    plt.close(fig)
    return result


def regional_bar_chart(regions: list) -> str:
    """Horizontal bar chart of regional market sizes."""
    import matplotlib.pyplot as plt

    filtered = [r for r in regions if (r.get("market_size_usd_bn") if isinstance(r, dict) else getattr(r, "market_size_usd_bn", None))]
    if not filtered:
        return ""

    names = [r.get("region") if isinstance(r, dict) else r.region for r in filtered]
    values = [r.get("market_size_usd_bn") if isinstance(r, dict) else r.market_size_usd_bn for r in filtered]
    colors = [AMBER_500 if i == 0 else SLATE_700 for i in range(len(names))]

    fig, ax = plt.subplots(figsize=(7, max(2.5, len(names) * 0.5 + 1)))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    bars = ax.barh(names, values, color=colors, height=0.55)
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + max(values) * 0.01, bar.get_y() + bar.get_height() / 2,
                f"${val:.1f}B", va="center", fontsize=9, color=SLATE_900)

    ax.set_xlabel("USD Billions", color=SLATE_400, fontsize=9)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(colors=SLATE_700, labelsize=9)
    ax.set_xlim(0, max(values) * 1.3)
    for spine in ax.spines.values():
        spine.set_color(SLATE_200)
    plt.tight_layout()
    result = _b64(fig)
    plt.close(fig)
    return result


def market_share_pie(players: list) -> str:
    """Pie chart of market share."""
    import matplotlib.pyplot as plt

    filtered = [p for p in players
                if (p.get("market_share_pct") if isinstance(p, dict) else getattr(p, "market_share_pct", None))]
    if not filtered:
        return ""

    names = [p.get("name") if isinstance(p, dict) else p.name for p in filtered[:7]]
    values = [p.get("market_share_pct") if isinstance(p, dict) else p.market_share_pct for p in filtered[:7]]

    palette = [SLATE_900, SLATE_700, AMBER_500, EMERALD_600, SKY_600, ROSE_600, SLATE_400]

    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor("white")
    wedges, texts, autotexts = ax.pie(
        values, labels=None, autopct="%1.1f%%",
        colors=palette[:len(values)], startangle=90,
        pctdistance=0.8, wedgeprops={"linewidth": 1, "edgecolor": "white"},
    )
    for at in autotexts:
        at.set_fontsize(8)
        at.set_color("white")

    ax.legend(wedges, names, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=9, framealpha=0)
    plt.tight_layout()
    result = _b64(fig)
    plt.close(fig)
    return result


def capability_radar_chart(rows: list, companies: list) -> str:
    """Radar chart for capability benchmarking."""
    import matplotlib.pyplot as plt
    import numpy as np

    if not rows:
        return ""

    rating_map = {"Leading": 4, "Strong": 3, "Average": 2, "Weak": 1}
    dimensions = ["product_performance", "innovation_technology", "brand_strength",
                  "pricing_competitiveness", "distribution_reach", "partnerships_ecosystem", "customer_experience"]
    dim_labels = ["Product", "Innovation", "Brand", "Pricing", "Distribution", "Partnerships", "CX"]
    N = len(dim_labels)
    angles = [n / float(N) * 2 * 3.14159 for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("white")

    colors_palette = [AMBER_500, SLATE_700, EMERALD_600, SKY_600, ROSE_600]

    for i, row in enumerate(rows[:5]):
        name = row.get("company") if isinstance(row, dict) else row.company
        vals = []
        for dim in dimensions:
            raw_val = row.get(dim) if isinstance(row, dict) else getattr(row, dim, "Average")
            vals.append(rating_map.get(raw_val, 2))
        vals += vals[:1]
        ax.plot(angles, vals, color=colors_palette[i % len(colors_palette)], linewidth=1.5, label=name)
        ax.fill(angles, vals, color=colors_palette[i % len(colors_palette)], alpha=0.05)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dim_labels, size=9, color=SLATE_700)
    ax.set_ylim(0, 4)
    ax.set_yticks([1, 2, 3, 4])
    ax.set_yticklabels(["Weak", "Avg", "Strong", "Leading"], size=7, color=SLATE_400)
    ax.grid(color=SLATE_200, linewidth=0.5)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=8, framealpha=0)
    plt.tight_layout()
    result = _b64(fig)
    plt.close(fig)
    return result
