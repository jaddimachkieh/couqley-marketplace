---
name: couqley-trends
description: Daily trends and busy-time forecast analysis. Upload a Transactions by Date CSV (REP_S_00002) and get hourly heatmaps, day-of-week patterns, delivery vs dine-in split, avg check by hour, 7-day forecast, and staffing recommendations.
disable-model-invocation: true
---

# Daily Trends & Forecast Analysis

## Trigger
User uploads or references a Transactions by Date CSV (REP_S_00002 from Omega POS) and asks for trends, busy times, forecast, or operational insights.

## Input
- **File:** Transactions by Date CSV (rep_s_00002_trans.csv or similar)
- **Key columns:** Invoice #, Date, Close Time, Table #, Cust.#, Amount, Discount, Tax, Pay By, Total

If no file is provided, ask: "Please upload your Omega POS Transactions by Date CSV (REP_S_00002) to get started."

## Parsing Rules

### Rows to Keep
Keep only rows where:
- Column 0 is a numeric invoice number
- Column 11 (Total) is greater than 0.00
- Table number does not equal 600, 800, or 1000

### Rows to Skip
Skip any row where column 0 contains:
- "Invoice #" (repeated header)
- "Branch:" (branch label)
- "Total" (footer summary — "Total For:", "Total:", etc.)
- "Gross" / "Net" / "Tax" / "Service" / "Discount" (summary labels)
- "Copyright" / "www." / "<div" / "Error" (artifacts)
- A date string like "30-Mar-2026" in a page-break line

### Last-Page Column Shift
On the final page, an extra empty column appears between Close Time and Table #. Detect this: if the value at index 3 is empty/blank, shift — Table # = index 4, Cust.# = index 5, Print# = index 6, Amount = index 7, Service = index 8, Discount = index 9, Tax = index 10, Pay By = index 11, Total = index 12.

### Field Parsing
- **Date:** Parse "01-Jan-2026" → datetime object; extract `day_of_week` (Mon–Sun)
- **Close Time:** Parse "21:34" → extract `hour` as integer (0–23)
- **Table #:** Integer. Classify: 1–299 = "dine-in", 300–399 = "delivery"
- **Covers (Cust.#):** Integer
- **Total:** Float. Skip rows where Total == 0.00
- **avg_check:** Total / Covers (skip if Covers == 0)

## Analysis Workflow

### Step 1 — Parse & Clean
Apply all parsing rules above. Print row count after cleaning: "Parsed [N] transactions from [start date] to [end date]."

### Step 2 — Hourly Heatmap Data
Group by `hour × day_of_week`. For each cell calculate:
- Transaction count
- Total revenue
- Total covers

Identify the top-3 peak windows (highest transaction count) and note them for the insights section.

### Step 3 — Daily Trends
Group by `date`. Calculate per day:
- Transaction count
- Total revenue
- Total covers
- Avg check size (total revenue / total covers)

If data spans 2+ weeks, calculate week-over-week revenue change %.

### Step 4 — Day-of-Week Patterns
Group by `day_of_week`. Calculate averages across all days of that type:
- Avg daily transactions
- Avg daily revenue
- Avg daily covers

Rank Mon–Sun from busiest to slowest by avg revenue.

### Step 5 — Delivery vs Dine-In
Separate `channel == "delivery"` vs `channel == "dine-in"`. For each:
- Total transactions
- Total revenue + % of overall
- Avg check size
- Top 3 peak hours by transaction count

### Step 6 — Avg Check by Hour
Group by `hour`. Calculate:
- Avg check size (total revenue / total covers)
- Total covers

Flag hours where avg check > overall avg check as "premium hours". Flag hours where covers are high but avg check is below overall avg as "value hours".

### Step 7 — Staffing Recommendations
From the hourly heatmap data (Step 2), extract top-5 day+hour windows by cover count. Generate one plain-language recommendation per window:
- Format: "Ensure full [floor/bar] team on [Day] between [Hour]–[Hour+2] (avg [N] covers/hour)"
- Use "floor team" for dine-in peak windows
- Add a general note: "Delivery orders peak at [top delivery hour] — ensure kitchen capacity"

### Step 8 — 7-Day Forecast
For each of the next 7 calendar days (starting tomorrow):
- Determine its day_of_week
- Look up the historical avg covers and avg revenue for that day_of_week from Step 4
- Project: `forecast_covers = avg_covers`, `forecast_revenue = avg_revenue`
- Label each row: date, day_of_week, projected_covers, projected_revenue

Add this note to the forecast section: "Estimates based on historical day-of-week averages. Accuracy improves with more months of data."

### Step 9 — Key Insights
Generate 4–5 plain-language observations, for example:
- "Saturday evenings (8–11pm) drive [X]% of weekly revenue"
- "Delivery accounts for [X]% of transactions but [Y]% of revenue"
- "Tuesday is the slowest day — avg $[X] revenue vs $[Y] on Saturday"
- "The peak avg check ($[X]/cover) occurs at [hour] — guests spending most at [time]"
- "Week-over-week revenue [increased/decreased] by [X]%" (if multi-week data)

## Output

### Executive Summary (always first)
"[N] transactions analyzed from [start] to [end]. Total revenue: $[X] across [Y] covers. Busiest day: [Day] (avg $[Z]/day). Peak hour: [H]:00. Delivery: [D]% of revenue."

### HTML Dashboard
Generate a complete, self-contained HTML file. Save as `Couqley_Trends_[YYYY-MM].html` in the working folder outputs directory.

**Brand colors:** Cream `#F7F3E9`, Red `#CC3333`, Gold `#BF9966`, Georgia serif font

**Dashboard sections in order:**

#### 1. Header
- "Couqley French Bistro" in red
- "Daily Trends & Forecast" subtitle
- Report period: "01 Jan 2026 – 31 Jan 2026" | Branch name

#### 2. KPI Cards Row (5 cards)
| Card | Value |
|------|-------|
| Total Revenue | $245,472 |
| Total Covers | 5,691 |
| Avg Check Size | $43.13 |
| Busiest Day | Saturday |
| Peak Hour | 9 PM |

#### 3. Hourly Heatmap
- Chart.js matrix/heatmap: X-axis = hours (12pm–12am+), Y-axis = days (Mon–Sun)
- Cell color intensity = transaction count (light cream → deep red gradient)
- Tooltip shows: "[Day] [Hour]: [N] transactions, $[X] revenue"
- If Chart.js matrix plugin not available, use a styled HTML table with inline background-color per cell calculated as `rgba(204,51,51, opacity)` where opacity = count / max_count

#### 4. Daily Revenue & Covers — Line Chart
- Dual-axis line chart (Chart.js)
- Left axis: daily revenue (red line)
- Right axis: daily covers (gold dashed line)
- X-axis: dates in the range
- Title: "Daily Performance"

#### 5. Day-of-Week Patterns — Bar Chart
- Horizontal bar chart (Chart.js)
- Y-axis: Mon, Tue, Wed, Thu, Fri, Sat, Sun (sorted busiest→slowest)
- X-axis: avg daily revenue
- Color: red bars with gold border
- Title: "Average Revenue by Day of Week"

#### 6. Delivery vs Dine-In
Two-column layout:
- Left: Doughnut chart (Chart.js) — revenue share dine-in vs delivery
- Right: Stats table

| Metric | Dine-In | Delivery |
|--------|---------|----------|
| Transactions | N | N |
| Revenue | $X | $X |
| % of Total | X% | X% |
| Avg Check | $X | $X |
| Peak Hour | Xpm | Xpm |

#### 7. Avg Check Size by Hour — Bar Chart
- Bar chart (Chart.js): X-axis = hours, Y-axis = avg check in $
- Bars above overall avg: red fill
- Bars below overall avg: gold fill
- Horizontal dashed line at overall avg check
- Annotate "premium hours" and "value hours" in the title/subtitle

#### 8. 7-Day Forecast Table
Styled table with gold header row:

| Date | Day | Projected Covers | Projected Revenue |
|------|-----|-----------------|-------------------|
| 31 Mar | Mon | 42 | $4,850 |
| ... | ... | ... | ... |

Footer note in italics: "Estimates based on Jan 2026 day-of-week averages. Accuracy improves with additional months of data."

#### 9. Staffing Recommendations
Card with red header "Staffing Recommendations":
- Bullet list from Step 7
- Gold border, cream background

#### 10. Key Insights
3–5 cards from Step 9, gold border, each with a one-line header and 1–2 sentence observation.

## Brand Compliance
- Cream `#F7F3E9` backgrounds, Red `#CC3333` headers/accents, Gold `#BF9966` borders
- Table headers: white text on red background
- Data rows: black text on alternating cream/white
- Currency: $1,234 format (commas, no decimals unless cents matter)
- Warm, operational tone — written for a restaurant manager, not a data analyst
