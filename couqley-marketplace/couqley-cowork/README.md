# Couqley Cowork Plugin

Restaurant analytics for Couqley French Bistro. Sales analysis, menu engineering (Boston Matrix), break-even forecast, payroll, and marketing. Upload Omega POS reports (CSV/Excel) to your project's `reports/` folder and get branded dashboards.

## Prerequisites

- Omega POS reports exported as CSV or Excel
- Reports: REP_S_00001 (sales), REP_S_00506 (menu engineering), accounting Excel, payroll Excel
- For break-even: optional `reference/Mapping Sheet.xlsx` for Chart of Accounts mapping

## Installation (Claude Code)

```bash
# Add marketplace
/plugin marketplace add github:jaddimachkieh/couqley-marketplace

# Install the plugin
/plugin install couqley-cowork@couqley-marketplace
```

## Quick Start

1. Select or create a project folder
2. Ensure `reports/` and `outputs/` directories exist
3. Upload Omega POS CSVs (sales, menu engineering) or Excel (accounting, payroll) to `reports/`
4. Ask Claude to analyze: "Analyze my sales data", "Run Boston Matrix on menu", "Break-even forecast", etc.
5. Dashboards save to `outputs/`

## Skills Included

| Skill | Input | Output |
|-------|-------|--------|
| **brand** | — | Brand guidelines (reference) |
| **sales** | REP_S_00001 CSV | Top items, group performance, slow movers |
| **menu-engineer** | REP_S_00506 CSV | Boston Matrix, Challenge items, marketing plays |
| **breakeven** | Accounting Excel | P&L, break-even, 12-month forecast |
| **payroll** | Payroll Excel | Department breakdown, top earners |
| **marketing** | Uses sales + menu-engineer outputs | Social calendar, promo designs |
| **omega-extract** | — | Browser guide for Omega POS report extraction |
| **cfo** | — | Financial reporting standards (extends brand) |

## Data Flow

```
reports/ (CSV, Excel) → skills parse & analyze → outputs/ (HTML dashboards)
```

Brand colors: Cream #F7F3E9, Red #CC3333, Gold #BF9966.
