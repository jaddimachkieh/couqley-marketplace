---
name: couqley-menu-engineer
description: Menu engineering analysis using Boston Matrix methodology. Upload a Menu Engineering CSV (REP_S_00506) and get Challenge item marketing plays, profit optimization, and branded dashboard.
---

# Menu Engineering Analysis

## Trigger
User uploads or references a Menu Engineering CSV (REP_S_00506 from Omega POS) and asks for menu analysis, optimization, or marketing plays.

## Input
- **File:** Menu Engineering CSV (REP_S_00506_SMRY.csv or similar)
- **Key columns:** Item name, group/category, quantity sold, price, profit margin %, total profit/revenue

If no file is provided, ask: "Please upload your Omega POS Menu Engineering CSV (REP_S_00506) to get started."

## Boston Matrix Classification
Classify each item using median popularity and median margin as thresholds:

| Category | Popularity | Margin | Strategy |
|----------|-----------|--------|----------|
| **Stars** | High | High | Protect, promote, flagship |
| **Workhorses** | High | Low | Raise price, reduce cost, bundle |
| **Challenge Items** | Low | High | Primary marketing focus — high ROI opportunity |
| **Dogs** | Low | Low | Consider removal or repositioning |

## Workflow

1. **Read the file** — Read CSV content directly
2. **Parse items** — Extract: item name, group, quantity sold, price, profit margin %, total profit
3. **Calculate thresholds** — Median quantity = popularity threshold; median margin % = margin threshold
4. **Classify all items** into Boston Matrix quadrants
5. **Identify Challenge Items** — Low popularity + high margin = maximum ROI opportunity
6. **Generate marketing plays** for top Challenge items (server scripts, social hooks, bundle ideas)
7. **Profit optimization** — Model 30% volume increase on Challenge items → projected profit gain
8. **Generate HTML dashboard** — Save to working folder
9. **Present summary first**

## Output

### Executive Summary (always first)
"[X] items analyzed. [Y] Challenge items identified with $[Z] profit potential at 30% volume increase. [N] Stars performing strongly. [M] Dogs flagged for review."

### Marketing Plays (for each top Challenge item)
- **Social media hook** — sensory-focused post angle
- **Server upsell script** — 1–2 sentence recommendation
- **Bundle suggestion** — pair with a Star or Workhorse
- **Menu positioning** — placement/description tip

### HTML Dashboard
Generate a complete, self-contained HTML file with:
- **Brand colors:** Cream `#F7F3E9`, Red `#CC3333`, Gold `#BF9966`
- **Sections:**
  1. Header with Couqley French Bistro branding
  2. KPI cards (total items, Challenge count, Stars count, avg margin %)
  3. Boston Matrix scatter chart — X: popularity %, Y: margin % (Chart.js CDN, color-coded quadrants)
  4. Challenge Items table (name, group, qty sold, price, margin %, total profit) sorted by profit potential
  5. Marketing plays section — top 5 Challenge items with action plans
  6. Profit optimization chart — current vs projected (30% volume lift)
  7. Stars table — items to protect
  8. Dogs table — items to review for removal
  9. Key insights cards (3–5 strategic recommendations)
- Save as `Couqley_MenuEngineering_[YYYY-MM].html`

## Brand Compliance
- Cream `#F7F3E9` backgrounds, Red `#CC3333` headers, Gold `#BF9966` accents
- Warm, inviting marketing language
- French bistro aesthetic in all copy suggestions
