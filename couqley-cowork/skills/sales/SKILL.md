---
name: couqley-sales
description: Sales performance analysis. Upload a Sales Report CSV (REP_S_00001) and get top items, group breakdown, slow movers, and branded dashboard.
disable-model-invocation: true
---

# Sales Analysis

## Trigger
User uploads or references a Sales Report CSV (REP_S_00001 from Omega POS) and asks for sales analysis, trends, or performance breakdown.

## Input
- **File:** Sales Report CSV (REP_S_00001_sales.csv or similar) — uploaded or in working folder
- **Key columns:** Item name, quantity sold, total revenue/amount, group/category, division

If no file is provided, ask: "Please upload your Omega POS Sales Report CSV (REP_S_00001) to get started."

## Workflow

1. **Read the file** — Read the CSV content directly from the uploaded file or working folder
2. **Parse the data** — Identify columns for: item name, quantity, revenue, group/category
3. **Analyze:**
   - **Top 10 items** by revenue and by quantity
   - **Group performance** — revenue and % of total per category
   - **Slow movers** — bottom 25% by revenue
   - **Promotion candidates** — high margin / low volume items
   - **Key KPIs** — total revenue, total items, average item revenue, top group
4. **Generate HTML dashboard** — Use the brand colors and structure below, save to working folder as `Couqley_Sales_[date].html`
5. **Present summary first** — Lead with the executive insight before offering the dashboard

## Output

### Executive Summary (always first)
"Total revenue of $[X] across [Y] items. Top performer: [item] at $[Z] ([%] of revenue). Strongest group: [group]."

### HTML Dashboard
Generate a complete, self-contained HTML file with:
- **Brand colors:** Cream background `#F7F3E9`, Red headers `#CC3333`, Gold accents `#BF9966`
- **Font:** Georgia serif
- **Sections:**
  1. Header with Couqley French Bistro branding
  2. KPI cards row (total revenue, total items, top item, top group)
  3. Top 10 items table (name, quantity, revenue, % of total) — red header row
  4. Group performance table (group, revenue, %, item count)
  5. Slow movers table (bottom performers flagged for review)
  6. Key insights cards (3–5 actionable observations)
- **Charts:** Use Chart.js CDN for bar chart (top items revenue) and doughnut (group breakdown)
- Save file to working folder outputs as `Couqley_Sales_Analysis_[YYYY-MM].html`

## Brand Compliance
- Cream `#F7F3E9` backgrounds, Red `#CC3333` headers, Gold `#BF9966` borders
- Table headers: white text on red background
- Data rows: black text on cream/white
- Currency format: $1,234 (commas, no decimals unless cents matter)
- Warm, professional tone in insights
