---
name: couqley-breakeven
description: Break-even forecast analysis. Upload an Accounting Excel file and get monthly P&L, break-even point, and 12-month forecast dashboard.
---

# Break-Even Analysis

## Trigger
User uploads or references an Accounting Excel file (.xlsx) and asks for break-even analysis, financial forecast, or P&L summary.

## Input
- **File:** Accounting Excel (.xlsx) exported from Omega POS
- **Key columns:** DATE, M DOLLAR (debits), D DOLLAR (credits), HISAB_NAME (account name), SAB NUMBER or HISAB_NUMBER (account number)

If no file is provided, ask: "Please upload your Omega POS Accounting Excel file (.xlsx) to get started."

## Account Classification
Classify accounts into P&L categories using the account name (HISAB_NAME):

- **Revenue:** Food Sales, Beverage Sales, Kiosk Sales, Other Revenues — use Credit (D DOLLAR)
- **COGS:** Food Cost, Beverage Cost, Kiosk COS, F&B Transfers — use Debit (M DOLLAR)
- **Operating Expense:** Staff Cost, Rent, Electricity, Maintenance, Marketing, Delivery, Professional Services, and similar — use Debit (M DOLLAR)
- **Exclude:** Balance Sheet accounts (assets, liabilities, equity)

## Workflow

1. **Read the file** — Read the Excel content directly from the uploaded file or working folder
2. **Parse transactions** — Extract date, account name, debit (M DOLLAR), credit (D DOLLAR)
3. **Classify accounts** — Map each account to Revenue / COGS / Operating Expense using name keywords
4. **Aggregate monthly** — Sum Revenue, COGS, OpEx by month; calculate Gross Profit and Net Profit
5. **Calculate break-even** — Month where cumulative net profit crosses zero
6. **12-month forecast** — Project forward using last 3 months average growth rate (cap at ±20%/month)
7. **Generate HTML dashboard** — Save to working folder as `Couqley_Breakeven_[date].html`
8. **Present summary first**

## Output

### Executive Summary (always first)
"Based on [X] months of data, average monthly revenue is $[Y] with average expenses of $[Z], yielding a net of $[N]. Break-even [achieved in month X / projected for month Y]."

### HTML Dashboard
Generate a complete, self-contained HTML file with:
- **Brand colors:** Cream `#F7F3E9`, Red `#CC3333`, Gold `#BF9966`
- **Sections:**
  1. Header with Couqley French Bistro branding and status banner (Profitable / At Risk / Below Break-Even)
  2. KPI cards (avg monthly revenue, avg monthly expenses, avg net profit, break-even status)
  3. Monthly P&L table (month, revenue, COGS, gross profit, OpEx, net profit)
  4. Revenue vs Expenses line chart (Chart.js CDN)
  5. Cumulative net profit chart showing break-even crossing point
  6. Expense breakdown by category (% of total OpEx)
  7. 12-month forecast table (Historical vs Projected)
  8. Key insights cards (3–5 observations)
- Save as `Couqley_Breakeven_Analysis_[YYYY-MM].html`

## Brand Compliance
- Cream `#F7F3E9` backgrounds, Red `#CC3333` headers, Gold `#BF9966` accents
- Profitable = green indicator, At Risk = amber, Below Break-Even = red
- Currency: $1,234 format
- Professional financial tone
