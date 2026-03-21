---
name: couqley-breakeven
description: Break-even forecast analysis. Upload an Accounting Excel file and get monthly P&L, break-even point, and 12-month forecast dashboard. Uses the Chart of Accounts mapping sheet for accurate account classification.
---

# Break-Even Analysis

## Trigger
User uploads an Accounting Excel file (.xlsx) and asks for break-even analysis, financial forecast, or P&L summary.

## Input
- **File:** Accounting Excel (.xlsx) exported from Omega POS
- **Expected columns:** DATE, M DOLLAR (debits), D DOLLAR (credits), HISAB_NAME (account name), SAB NUMBER or HISAB_NUMBER (account number)
- **Mapping file (bundled):** `reference/Mapping Sheet.xlsx` in plugin — Chart of Accounts with IS Family classifications (auto-loaded from plugin)

## Workflow

**Paths:** Look for reports in the project's `reports/` folder. Save dashboards to `outputs/`. Mapping Sheet is bundled in the plugin (`reference/Mapping Sheet.xlsx`).

1. Save uploaded file to `reports/` folder
2. Run `scripts/parse.py` → `parse_excel_accounting(xlsx_path)` or `format_accounting_excel(xlsx_path)`
   - Automatically loads bundled `reference/Mapping Sheet.xlsx` (Chart of Accounts) and joins on account number
   - Each transaction is enriched with `report_type`, `is_family`, and `bs_cat`
3. Run `scripts/analyze.py` → `break_even_forecast(df)` → returns analysis dict
   - Uses IS Family for exact Revenue / COGS / OpEx classification
   - Falls back to keyword matching if mapping sheet is missing
4. Populate `templates/dashboard.html` with analysis data
5. Save output to `outputs/` folder
6. Present business impact summary first, then offer dashboard

## Output
- Branded HTML dashboard with revenue vs expenses chart, cumulative break-even, forecast
- Expense breakdown by IS Family (e.g., Food Cost, Staff Cost, Rent)
- Executive summary: "Based on [X] months of data, monthly profit averages $[Y] with break-even [status]"

## Scripts (local to this skill)
- `scripts/parse.py` — Parses Accounting Excel files with mapping sheet integration
- `scripts/analyze.py` — Break-even calculation, monthly aggregation, 12-month forecast

## Key Functions

### parse.py
- `load_account_mapping(mapping_path)` → DataFrame with account_number, report_type, is_family, bs_cat
- `parse_excel_accounting(xlsx_path, mapping_path=None)` → DataFrame enriched with mapping columns
- `format_accounting_excel(xlsx_path, mapping_path=None)` → Cleaned DataFrame with standardized names + mapping

### analyze.py
- `categorize_from_is_family(is_family)` → 'Revenue' | 'COGS' | 'Operating Expense' | 'Other' (primary method)
- `categorize_account(account_name)` → Same categories via keyword matching (fallback)
- `break_even_forecast(df, forecast_months=12)` → dict with historical_monthly, forecast_monthly, break_even_months, chart_data, summary, summary_text, expense_breakdown

## Account Classification

### Primary: Mapping Sheet (IS Family)
The bundled Mapping Sheet classifies accounts by their IS Family:

- **Revenue:** Food Sales, Beverage Sales, Kiosk Sales, Other Revenues
- **COGS:** Food Cost, Beverage Cost, COGS Branches Adjustment, Kiosk COS, F&B Transfers
- **Operating Expense:** Staff Cost, Rent & Related Charges, DOE, Marketing & Promotion Activities, Electricity & Generator, Maintenance & Repairs, Delivery Cost, Professional Services, and 14 more families
- **Filtered out:** Balance Sheet (BS) accounts are excluded from P&L

### Fallback: Keyword Matching
When no mapping sheet is available, accounts are classified by name keywords (less accurate).

### Join Logic
- Accounting Excel column `SAB NUMBER` (or `HISAB_NUMBER`) → Mapping Sheet column `Account #`
- Account numbers are cleaned of `_x000D_\n` Excel XML artifacts before joining
- Unmatched transactions fall back to keyword classification

## Forecast Model
- Uses last 3 months of historical data as baseline
- Applies compound growth rate for revenue and expenses
- Growth rates auto-calculated from trends or manually specified
- Capped at ±20% monthly growth for realistic projections
- COGS/OpEx forecast split uses actual historical ratio (not hardcoded)

## Dashboard Components
- Status banner (Profitable/At Risk/Below Break-Even)
- Key metrics grid (avg revenue, expenses, net, cumulative)
- Historical vs Forecast comparison cards
- Monthly Revenue vs Expenses line chart (Chart.js)
- Cumulative Break-Even analysis chart
- Key insight cards with positive/warning indicators

## Brand Compliance
- Colors: Cream (#F7F3E9), Red (#CC3333), Gold (#BF9966)
- Typography: Georgia serif, professional financial presentation
- Charts: Brand colors, clear labels, tooltips with $ formatting
