# Couqley Cowork Package

Restaurant analytics for Couqley French Bistro: sales, menu engineering, break-even, payroll, and marketing. Uses Omega POS data.

## Installation

This repository is a **plugin marketplace**, not a single plugin folder. Skills live under `couqley-cowork/skills/`. You must add the marketplace, then install the **`couqley-cowork`** plugin (not the repo root).

1. Open **Claude Desktop** and launch **Claude Cowork**
2. Go to **Plugins** (click "+")
3. **Add the marketplace** from GitHub: `jaddimachkieh/couqley-marketplace` (or use **Add marketplace** / `/plugin marketplace add` with that repo URL, depending on your Cowork UI)
4. **Install the plugin** named **`couqley-cowork`** from marketplace **`couqley-marketplace`** (in Claude Code this is `/plugin install couqley-cowork@couqley-marketplace`). If you only attach the repo as one plugin without that step, the app may treat the **repository root** as the plugin root — there is no `skills/` there, so skills will not load.
5. Alternatively: browse the [Cowork plugin directory](https://claude.com/plugins-for/cowork) and install **couqley-cowork** if listed, or **upload** the `couqley-cowork` folder (the directory that contains `skills/` and `.claude-plugin/plugin.json`), not the whole monorepo zip.
6. Create `reports/` and `outputs/` in your project folder (see below)

## Project Setup

```bash
mkdir reports outputs
```

- Put Omega POS reports (CSV, Excel) in `reports/`
- Dashboards save to `outputs/`
- Report types: REP_S_00001 (sales), REP_S_00506 (menu engineering), accounting Excel, payroll Excel
- Mapping Sheet for break-even is bundled — no setup needed

## Skills

Invoke plugin skills with slash commands using each skill’s **`name`** from `SKILL.md` frontmatter (for example `/couqley-sales`, `/couqley-brand`). Short names like `/sales` are not registered unless the frontmatter says so.

| Slash (name in SKILL.md) | Input | Output |
|--------------------------|-------|--------|
| `/couqley-brand` | — | Brand and financial reporting guidelines |
| `/couqley-sales` | REP_S_00001 CSV | Top items, group performance, slow movers |
| `/couqley-menu-engineer` | REP_S_00506 CSV | Boston Matrix, Challenge items |
| `/couqley-breakeven` | Accounting Excel | P&L, break-even, 12-month forecast |
| `/couqley-payroll` | Payroll Excel | Department breakdown, top earners |
| `/couqley-marketing` | Sales + menu-engineer | Social calendar, promo designs |
| `/couqley-omega-extract` | — | Browser guide for Omega POS downloads |

## Example Prompts

- "Download the latest sales report from Omega"
- "Analyze this month's sales and suggest marketing ideas"
- "Run a Boston Matrix analysis on our menu"
- "Break-even forecast for this year"
- "Create a 4-week social media calendar"
- "Build a marketing summary dashboard"

## Troubleshooting

**Skills or slash commands missing?** You likely installed the **repository root** as the plugin. Reinstall using the marketplace flow above so the enabled plugin root is **`couqley-cowork`** (the folder that contains `skills/`). Confirm the plugin is enabled in Cowork’s plugin list.

**Module not found?** `pip install pandas pdfplumber openpyxl`

**Reports folder missing?** Run `mkdir reports outputs` in your project folder

**Dashboards not rendering?** Open the HTML file in a modern browser (Chrome, Firefox, Safari)

**Validate locally (Claude Code CLI):** `claude plugin validate /path/to/couqley-cowork`

**Need help?** Ask Claude — it knows this package.
