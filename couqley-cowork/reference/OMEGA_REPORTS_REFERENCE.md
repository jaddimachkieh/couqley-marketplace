# Omega POS Reports Reference

## Overview

Omega POS (https://cms.omegasoftware.ca/) is Couqley's point-of-sale system. Reports are exported as **CSV files** (which are PDF-to-CSV exports) and **Excel files** for accounting/payroll.

## Report Types & Real Column Structure

### 1. Menu Engineering WorkSheet (REP_S_00506)

**File format:** CSV exported from PDF
**Parser:** `pdf_parser.parse_menu_engineering_csv(csv_path)`
**Example file:** `REP_S_00506_SMRY.csv`

#### CSV Layout
```
Row 0: "Couqley Gemayzeh"
Row 1: "Menu Engineering WorkSheet"
Row 2: Date, Year/Month info, Page X of Y
Row 3: Column Headers
Row 4+: Data rows interspersed with Group/Menu/Category labels and page breaks
```

#### Column Structure (18 columns, 0-indexed)

| Index | Header | Type | Description |
|-------|--------|------|-------------|
| 0 | Menu Item | text | Item name (e.g., "Bistro Burger", "Carafe Bordeaux Superieur") |
| 1 | Qty | float | Quantity sold (can have commas: "1,058.00") |
| 2 | Popularity | float | Popularity as decimal percentage (e.g., 0.01, 4.23, 7.40) |
| 3 | (literal) | "%" | Always "%" — skip this column |
| 4 | Item cost | float | Unit cost per item |
| 5 | Item Sell Price | float | Unit selling price |
| 6 | (empty) | — | Empty column — skip |
| 7 | Item Profit | float | Unit profit (Sell Price - Cost) |
| 8 | Tot. Cost | float | Total cost (Qty × Item Cost) |
| 9 | Tot Revenue | float | Total revenue (Qty × Sell Price), can have commas |
| 10 | Tot Profit | float | Total profit (Tot Revenue - Tot Cost) |
| 11 | PL1 | float | Price level 1 reference |
| 12 | Profit | text | Profit margin level: "High" or "Low" |
| 13 | Popularit | text | Popularity level: "High" or "Low" |
| 14 | (empty) | — | Empty column — skip |
| 15 | Menu Item | text | Category: "Star", "Challenge", "Workhorse", or "Dog" |
| 16 | (empty) | — | Empty column — skip |
| 17 | Menu | text | Menu type (always "Tables") |

#### Menu Engineering Categories (Boston Matrix)
- **Star** — High profit margin, High popularity → Protect and promote
- **Challenge** — High profit margin, Low popularity → Market aggressively (PRIMARY MARKETING TARGET)
- **Workhorse** — Low profit margin, High popularity → Maintain volume, optimize margin
- **Dog** — Low profit margin, Low popularity → Consider removing or repositioning

#### Item Groups (from real data)
Apero, Beers, Boeuf, By the Glass & Carafe, Cocktails, Cold Drinks, Dessert, Formulas, Gin/Vodka, Hot Drinks, Kids Menu, Ladies Night, Les Sauces, Modifier, Plats Principaux, Prosecco, Red Wine (Europe/France/Lebanon), Rose Wine, Salades, Side Orders, Specials, Spirits/Digestif, Starters, Tequila, Weekday Lunch OFFER, Whiskey, White Wine (Europe/France/Lebanon)

#### CSV Artifacts to Filter
- Page break lines: "Page X of Y"
- Repeated header rows on each page
- "Year: YYYY - Month: M" lines
- "Copyright © Omega Software" lines
- "www.omegapos.com" lines
- HTML error artifacts: `<div>`, `<footer>`, "Error Occured", "Cannot modify"
- "REP_S_XXXXX" report ID lines
- Category/Group/Menu label rows (parsed as metadata, not data)

#### Output DataFrame Columns (after parsing)
```
menu_item, quantity, popularity, item_cost, item_sell_price, item_profit,
total_cost, total_revenue, total_profit, profit_margin (High/Low),
popularity_level (High/Low), category (Star/Challenge/Workhorse/Dog),
menu, group, profit_margin_pct (calculated)
```

---

### 2. Sales Report (REP_S_00001)

**File format:** CSV exported from PDF
**Parser:** `pdf_parser.parse_sales_csv(csv_path)`
**Example file:** `REP_S_00001 sales.csv`

This report contains detailed transaction-level sales data. Format is similar to the menu engineering report but with different column structure focused on transaction details.

---

### 3. Accounting Data (Excel)

**File format:** `.xlsx`
**Parser:** `pdf_parser.parse_excel_accounting(xlsx_path)` or `data_formatter.format_accounting_excel(xlsx_path)`
**Example file:** `Accounting Data YTD June 2025.xlsx`

#### Column Structure (headers already in row 0, UPPERCASE)

| Column | Type | Description |
|--------|------|-------------|
| COMP | text | Company identifier (e.g., "Q2025") |
| TYPE | text | Transaction type (e.g., "JVOPEN" for journal voucher) |
| KAID | integer | Transaction ID — groups related line items |
| NUMREC | numeric | Record/line number within a transaction |
| HISAB_NUMBER | text | Account code (chart of accounts) |
| DATE | timestamp | Transaction date |
| MD | text | Debit/Credit indicator ("C" or "D") |
| M DOLLAR | numeric | **Debit amount in USD** (expenses, assets increase) |
| D DOLLAR | numeric | **Credit amount in USD** (revenue, liabilities increase) |
| M LL | numeric | Debit in Lebanese Lira |
| D LL | numeric | Credit in Lebanese Lira |
| SHAREH | text | Shareholder/partner identifier |
| DEP | integer | Department code |
| HISAB_NAME | text | **Account name** (e.g., "Revenue", "Food Purchases", "Salaries") |

**Key relationships:**
- `KAID` groups multiple rows into one double-entry transaction
- `M DOLLAR` (debits) and `D DOLLAR` (credits) are mutually exclusive per row
- Revenue accounts: credits in D DOLLAR (look for HISAB_NAME containing "revenue", "sales", "income")
- Expense accounts: debits in M DOLLAR (look for "expense", "cost", "salary", "purchase")

**Used by:** `break_even_forecast.py` for monthly break-even analysis

---

### 4. Payroll Data (Excel)

**File format:** `.xlsx`
**Parser:** `pdf_parser.parse_excel_payroll(xlsx_path)` or `data_formatter.format_payroll_excel(xlsx_path)`
**Example file:** `Payroll Data 2025.xlsx`

#### Special Format
- Headers are at **row 4** (not row 0)
- Actual column names are at **row index 1** after skiprows=4 (look for "Name" in the row)
- Data starts after the column name row
- Clean: remove rows where Name or Dep is NaN

#### Key Columns (after formatting)

| Column | Type | Description |
|--------|------|-------------|
| SQ | integer | Employee sequence/ID |
| Name | text | Employee full name |
| Dep | text | Department: Kitchen, Floor, Cleaning, Bar, Support |
| Position | text | Job title: Head Chef, Sous Chef, Chef de Partie, Team Leader, etc. |
| Monthly | numeric | Base monthly salary |
| Cost | numeric | **Total cost per employee** (primary cost metric) |
| Tax | numeric | Income tax amount |
| NSSF | numeric | Social security contribution |
| Transport | numeric | Transportation allowance |
| Family Allowance | numeric | Family benefit |
| Month / Month_Num | text/int | Pay period |

**69 employees across 5 departments:** Kitchen (43%), Floor (37%), Cleaning (11%), Bar (5%), Support (4%)

---

### 5. Transactions by Date (REP_S_00002)

**File format:** CSV exported from PDF
**Parser:** Follow inline parsing rules in `couqley-trends` skill
**Example file:** `rep_s_00002_trans.csv`

#### CSV Layout
```
Row 0: "Couqley Gemayzeh" (branch name)
Row 1: "Transactions by Date"
Row 2: Print date, From Date, To Date, Page X of Y
Row 3: Column headers
Row 4: "Branch: Couqley Gemayzeh"
Row 5+: Data rows interspersed with page-break lines and repeated headers
Footer: Summary totals, copyright line, HTML error artifact
```

#### Column Structure (13 columns, 0-indexed)

| Index | Header | Type | Description |
|-------|--------|------|-------------|
| 0 | Invoice # | int | Transaction ID |
| 1 | Date | text | DD-Mon-YYYY (e.g., "01-Jan-2026") |
| 2 | Close Time | text | HH:MM — when the table bill was closed |
| 3 | Table # | int | Table identifier (see classification below) |
| 4 | Cust.# | int | Number of covers/guests at the table |
| 5 | Print# | int | Number of receipt prints |
| 6 | Amount | float | Pre-tax, pre-discount subtotal |
| 7 | Service | float | Service charge |
| 8 | Discount | float | Discount applied |
| 9 | Tax | float | Tax amount (≈11%) |
| 10 | Pay By | text | Payment method ("Cash $", "Toters", etc.) |
| 11 | Total | float | Final amount paid |
| 12 | (empty) | — | Trailing empty column — skip |

#### Last-Page Anomaly
On the final PDF page, an extra empty column is inserted between Close Time (index 2) and Table # (index 3), shifting all subsequent columns right by one. Detect this by checking if the value at index 3 is empty — if so, use index 4 for Table # and shift all remaining columns accordingly.

#### Table Classification
| Range | Channel |
|-------|---------|
| 1–299 | Dine-in |
| 300–399 | Toters delivery |
| 600, 800, 1000 | Special/comp — exclude from analysis |

#### CSV Artifacts to Filter
- Page break lines: "Page X of Y"
- Repeated header rows ("Invoice #,Date,Close Time...")
- Branch label rows ("Branch: Couqley Gemayzeh")
- Print date rows ("30-Mar-2026,,From Date:...")
- Footer summary rows ("Total For:", "Total:", "Gross Sales:", "Net Revenue:", "Net Sales:", "Total Tax:", "Total Service:", "Total Discount:")
- Copyright line ("Copyright © Omega Software")
- URL line ("www.omegapos.com")
- HTML error artifact (`<div>`, `<footer>`, "Error Occured", "Cannot modify")
- $0.00 Total transactions (comps/voids — exclude from all analysis)

#### Output DataFrame Columns (after parsing)
```
invoice (int), date (datetime), hour (int, 0-23),
day_of_week (str: "Mon"–"Sun"), table (int), covers (int),
amount (float), service (float), discount (float), tax (float),
pay_by (str), total (float),
channel (str: "dine-in" or "delivery"),
avg_check (float: total / covers, null if covers == 0)
```

---

## Parsing Quick Reference

```python
from scripts.pdf_parser import (
    parse_menu_engineering_csv,  # Menu engineering CSV → DataFrame
    parse_sales_csv,             # Sales CSV → DataFrame
    parse_excel_accounting,      # Accounting Excel → DataFrame
    parse_excel_payroll,         # Payroll Excel → DataFrame
    parse_omega_report,          # Auto-detect and parse any file
    batch_parse                  # Parse all files in a directory
)

from scripts.menu_analyzer import (
    menu_marketing_engine,       # Full marketing analysis for Challenge items
    generate_menu_engineering_matrix,  # Boston Matrix classification
    calculate_profit_optimization     # What-if profit scenarios
)

from scripts.break_even_forecast import (
    break_even_forecast          # Monthly break-even from accounting data
)
```

## Analysis Patterns

### Menu Marketing (Primary Use Case)
1. Parse: `df = parse_menu_engineering_csv("reports/REP_S_00506_SMRY.csv")`
2. Analyze: `results = menu_marketing_engine(df, top_n=20)`
3. Results include: Challenge items, marketing plays, bundles, pricing, social hooks, server scripts, profit optimization

### Break-Even Forecast
1. Parse: `df = parse_excel_accounting("reports/Accounting Data YTD June 2025.xlsx")`
2. Forecast: `results = break_even_forecast(df, forecast_months=12)`
3. Results include: Historical monthly, forecast monthly, chart data, summary

### Top Items & Trends
1. Parse: `df = parse_menu_engineering_csv("reports/REP_S_00506_SMRY.csv")`
2. Filter Stars: `stars = df[df['category'] == 'Star'].sort_values('total_revenue', ascending=False)`
3. Top sellers: Regular Couqley Steak Frites ($46K revenue), Large Couqley Steak Frites ($35K), Pain Perdu ($5.9K)
