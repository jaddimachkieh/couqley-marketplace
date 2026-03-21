---
name: couqley-payroll
description: Payroll analysis. Upload a Payroll Excel file and get department breakdown, top earners, cost trends, and branded dashboard.
---

# Payroll Analysis

## Trigger
User uploads a Payroll Excel file (.xlsx) and asks for payroll analysis, labor costs, or staffing breakdown.

## Input
- **File:** Payroll Excel (.xlsx) from Omega POS
- **Format:** Headers at row 4, columns include Name, Dep (department), and numeric salary columns

## Workflow

**Paths:** Look for reports in the project's `reports/` folder. Save dashboards to `outputs/`.

1. Save uploaded file to `reports/` folder
2. Run `scripts/parse.py` → `parse_excel_payroll(xlsx_path)` or `format_payroll_excel(xlsx_path)` → returns DataFrame
3. Run `scripts/analyze.py` → `payroll_analysis(df)` → returns analysis dict
4. Populate `templates/dashboard.html` with analysis data
5. Save output to `outputs/` folder
6. Present business impact summary first, then offer dashboard

## Output
- Branded HTML dashboard with department breakdown, top earners, cost charts
- Executive summary: "[X] employees across [Y] departments. Total payroll: $[Z]"

## Scripts (local to this skill)
- `scripts/parse.py` — Parses Payroll Excel files (handles row-4 headers, Name/Dep cleanup)
- `scripts/analyze.py` — Department breakdown, employee rankings, cost metrics, insights

## Key Functions
- `parse_excel_payroll(xlsx_path)` → DataFrame with Name, Dep, and salary columns
- `format_payroll_excel(xlsx_path)` → Cleaned DataFrame
- `payroll_analysis(df)` → dict with department_breakdown, top_employees, metrics, insights, summary_text

## Analysis Details

### Department Breakdown
- Total cost per department
- Employee count per department
- Average cost per employee per department
- Percentage of total payroll

### Employee Rankings
- Top 10 highest-paid employees
- Department and position information
- Cost relative to department total

### Insights Generated
- Department cost concentration warnings
- Top earner identification
- Distribution balance assessment

## Dashboard Components
- Key metrics grid (employees, total payroll, avg cost, monthly avg)
- Department breakdown cards with cost and percentage
- Department costs doughnut chart (Chart.js)
- Top positions by cost bar chart
- Monthly payroll trends line chart
- Top 10 employees list
- Key insight cards

## Brand Compliance
- Colors: Cream (#F7F3E9), Red (#CC3333), Gold (#BF9966)
- Typography: Georgia serif, professional financial presentation
- Charts: Brand colors, clear labels, tooltips with $ formatting
