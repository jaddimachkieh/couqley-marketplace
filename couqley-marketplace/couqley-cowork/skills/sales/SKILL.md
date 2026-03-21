---
name: couqley-sales
description: Sales performance analysis. Upload a Sales Report CSV (REP_S_00001) and get top items, group breakdown, slow movers, and branded dashboard.
---

# Sales Analysis

## Trigger
User uploads a Sales Report CSV (REP_S_00001 from Omega POS) and asks for sales analysis, trends, or performance breakdown.

## Input
- **File:** Sales Report CSV (REP_S_00001_sales.csv or similar)
- **Format:** CSV from Omega POS

## Workflow

**Paths:** Look for reports in the project's `reports/` folder. Save dashboards to `outputs/`.

1. Save uploaded file to `reports/` folder
2. Run `scripts/parse.py` → `parse_sales_csv(csv_path)` → returns DataFrame
3. Run `scripts/analyze.py` → multiple analysis functions → returns metrics, rankings, insights
4. Populate `templates/dashboard.html` with analysis data
5. Save output to `outputs/` folder
6. Present business impact summary first, then offer dashboard

## Output
- Branded HTML dashboard with top items, group performance, slow movers
- Executive summary: "Total revenue of $[X] across [Y] items. Top performer: [item] at $[Z]"

## Scripts (local to this skill)
- `scripts/parse.py` — Parses REP_S_00001 Sales CSV format
- `scripts/analyze.py` — Top items, group performance, slow movers, insights

## Key Functions
- `parse_sales_csv(csv_path)` → DataFrame with item_name, quantity, total_amount, group, division
- `top_items(df, n=10, by='revenue')` → top N items by revenue or quantity
- `group_performance(df)` → group-level breakdown with pct_of_total
- `slow_movers(df, percentile=25)` → underperforming items
- `promotion_candidates(df, top_n=15)` → scored promotion list
- `revenue_metrics(df)` → KPI dict
- `generate_insights(df)` → natural-language insights list
- `quick_summary(df)` → one-liner for chat
