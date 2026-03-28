---
name: couqley-payroll
description: Payroll analysis. Upload a Payroll Excel file and get department breakdown, top earners, cost trends, and branded dashboard.
---

# Payroll Analysis

## Trigger
User uploads or references a Payroll Excel file (.xlsx) and asks for payroll analysis, labor costs, or staffing breakdown.

## Input
- **File:** Payroll Excel (.xlsx) from Omega POS
- **Format:** Headers typically at row 4; columns include Name, Dep (department), and numeric salary/cost columns

If no file is provided, ask: "Please upload your Payroll Excel file (.xlsx) to get started."

## Workflow

1. **Read the file** — Read the Excel content directly; locate the header row (look for "Name" and "Dep" columns, often at row 4)
2. **Parse employees** — Extract: employee name, department, total compensation/cost columns
3. **Analyze:**
   - **Department breakdown** — total cost, employee count, average cost, % of total payroll per department
   - **Top 10 earners** — name, department, amount, % of dept total
   - **Payroll KPIs** — total headcount, total payroll, average per employee, highest-cost department
   - **Insights** — concentration warnings, distribution balance, cost anomalies
4. **Generate HTML dashboard** — Save to working folder as `Couqley_Payroll_[date].html`
5. **Present summary first**

## Output

### Executive Summary (always first)
"[X] employees across [Y] departments. Total payroll: $[Z]. Largest department: [dept] at $[A] ([%] of total). Average cost per employee: $[B]."

### HTML Dashboard
Generate a complete, self-contained HTML file with:
- **Brand colors:** Cream `#F7F3E9`, Red `#CC3333`, Gold `#BF9966`
- **Sections:**
  1. Header with Couqley French Bistro branding
  2. KPI cards (total employees, total payroll, avg per employee, top department)
  3. Department breakdown table (dept, employees, total cost, avg cost, % of payroll)
  4. Department costs doughnut chart (Chart.js CDN)
  5. Top 10 employees table (name, department, cost)
  6. Key insights cards (3–5 observations: concentration warnings, outliers)
- Save as `Couqley_Payroll_Analysis_[YYYY-MM].html`

## Brand Compliance
- Cream `#F7F3E9` backgrounds, Red `#CC3333` headers, Gold `#BF9966` borders
- Table headers: white text on red background
- Currency: $1,234 format
- Professional, discreet tone (payroll is sensitive data)
