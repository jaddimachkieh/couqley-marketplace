# Couqley Cowork Package

Restaurant analytics for Couqley French Bistro: sales, menu engineering, break-even, payroll, and marketing. Uses Omega POS data.

## Installation

1. Open **Claude Desktop** and launch **Claude Cowork**
2. Go to **Plugins** (click "+")
3. Add the plugin from the [plugin directory](https://claude.com/plugins-for/cowork) or GitHub: `jaddimachkieh/couqley-marketplace`
4. Create `reports/` and `outputs/` in your project folder (see below)

## Project Setup

```bash
mkdir reports outputs
```

- Put Omega POS reports (CSV, Excel) in `reports/`
- Dashboards save to `outputs/`
- Report types: REP_S_00001 (sales), REP_S_00506 (menu engineering), accounting Excel, payroll Excel
- Mapping Sheet for break-even is bundled — no setup needed

## Skills

| Skill | Input | Output |
|-------|-------|--------|
| **brand** | — | Brand and financial reporting guidelines |
| **sales** | REP_S_00001 CSV | Top items, group performance, slow movers |
| **menu-engineer** | REP_S_00506 CSV | Boston Matrix, Challenge items |
| **breakeven** | Accounting Excel | P&L, break-even, 12-month forecast |
| **payroll** | Payroll Excel | Department breakdown, top earners |
| **marketing** | Sales + menu-engineer | Social calendar, promo designs |
| **omega-extract** | — | Browser guide for Omega POS downloads |

## Example Prompts

- "Download the latest sales report from Omega"
- "Analyze this month's sales and suggest marketing ideas"
- "Run a Boston Matrix analysis on our menu"
- "Break-even forecast for this year"
- "Create a 4-week social media calendar"
- "Build a marketing summary dashboard"

## Troubleshooting

**Module not found?** `pip install pandas pdfplumber openpyxl`

**Reports folder missing?** Run `mkdir reports outputs` in your project folder

**Dashboards not rendering?** Open the HTML file in a modern browser (Chrome, Firefox, Safari)

**Need help?** Ask Claude — it knows this package.
