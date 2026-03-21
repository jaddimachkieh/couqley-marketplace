# Couqley Marketplace Design

**Date:** 2026-03-21  
**Goal:** Restructure Couqley skills as a Claude Code plugin marketplace, fix inconsistencies, and enable distribution via `/plugin marketplace add` + `/plugin install`.

**Reference:** [doc-radar-marketplace](https://github.com/peekwez/doc-radar-marketplace) structure; [Claude Code Plugin Docs](https://code.claude.com/docs/en/plugins); [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).

---

## Target Structure

```
couqley-marketplace/                    # Repo root (can be couqley-cowork or new repo)
├── .claude-plugin/
│   └── marketplace.json               # Catalog of plugins
├── couqley-cowork/                    # Main plugin (one plugin for all skills)
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── skills/                        # All Couqley skills
│   │   ├── brand/
│   │   │   └── SKILL.md
│   │   ├── sales/
│   │   │   ├── SKILL.md
│   │   │   ├── scripts/
│   │   │   │   ├── parse.py
│   │   │   │   └── analyze.py
│   │   │   └── templates/
│   │   │       └── dashboard.html
│   │   ├── menu-engineer/
│   │   ├── breakeven/
│   │   ├── payroll/
│   │   ├── marketing/
│   │   ├── omega-extract/
│   │   └── cfo/                       # Renamed from cfo-skills
│   ├── reference/                     # Shared reference docs
│   │   ├── OMEGA_REPORTS_REFERENCE.md
│   │   └── ...
│   └── README.md
├── reference/                         # Workspace-level (reports/, outputs/ live in project)
│   ├── OMEGA_REPORTS_REFERENCE.md
│   └── OMEGA_LOGIN_GUIDE.md
├── reports/                           # User data (gitignored or .gitkeep)
├── outputs/
├── .claude/
│   └── CLAUDE.md                      # Cowork instructions
└── README.md
```

**Constraint:** Claude Code copies each plugin into a cache. Paths must stay inside the plugin directory. So `skills/sales/scripts/` and `skills/sales/templates/` must live inside `couqley-cowork/`.

---

## Inconsistency Fixes

### 1. couqley-marketing Script References (Broken)

**Current:** References `scripts/pdf_parser.py`, `scripts/sales_analyzer.py`, `scripts/menu_analyzer.py` which do not exist. Actual parsers live in couqley-sales and couqley-menu-engineer.

**Fix:**
- Update couqley-marketing to describe it as an **orchestrator** that uses outputs from `couqley-sales` and `couqley-menu-engineer`.
- Data flow: User uploads CSV → couqley-sales or couqley-menu-engineer parses & analyzes → couqley-marketing consumes findings for content generation (social calendar, promo design, email copy).
- Remove references to pdf_parser.py and sales_analyzer.py. Instead: "Use parsed data from couqley-sales (top items, group performance, slow movers) and couqley-menu-engineer (Challenge items, Boston Matrix) as input."
- Keep marketing templates (marketing_summary.html, social_calendar.html, promo_design.html) in couqley-marketing; they render insights from other skills.

### 2. Brand Duplication (couqley-brand vs cfo-skills)

**Current:** Both define brand colors, typography, logo usage. cfo-skills adds financial reporting standards.

**Fix:**
- **couqley-brand** = canonical visual/tone guidelines (colors, typography, logo, tone of voice).
- **couqley-cfo** (renamed from cfo-skills): References couqley-brand for visuals; keeps only financial-specific content (scenario tables, EBITDA format, chart colors for Bear/Base/Target, number formatting).
- Add 1–2 lines in couqley-cfo: "For visual identity (colors, typography, logo), follow couqley-brand. This skill extends with financial reporting standards."

### 3. Naming: cfo-skills → couqley-cfo

- Align with `couqley-*` prefix for consistency.
- Skill name in SKILL.md frontmatter: `couqley-cfo`.

### 4. Data Source Clarity

- couqley-marketing and README describe PDF workflow; actual data is CSV (REP_S_00001, REP_S_00506) and Excel (accounting, payroll).
- Update marketing skill and README to say: "Upload CSV (sales, menu engineering) or Excel (accounting, payroll) to `reports/`. Skills parse from there."
- Keep omega-extract as the way to obtain reports from Omega POS (PDF or CSV); downstream skills accept CSV/Excel.

---

## Marketplace Configuration

### `.claude-plugin/marketplace.json`

```json
{
  "name": "couqley-marketplace",
  "owner": { "name": "[Your Name / Couqley]" },
  "metadata": {
    "description": "Restaurant analytics for Couqley French Bistro — sales, menu engineering, break-even, payroll, marketing. Omega POS integration.",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "couqley-cowork",
      "source": "./couqley-cowork",
      "description": "Couqley French Bistro analytics: sales analysis, menu engineering (Boston Matrix), break-even forecast, payroll, marketing. Upload Omega POS CSVs/Excel to reports/, get branded dashboards.",
      "version": "1.0.0",
      "author": { "name": "[Your Name]" }
    }
  ]
}
```

### `couqley-cowork/.claude-plugin/plugin.json`

```json
{
  "name": "couqley-cowork",
  "description": "Restaurant analytics for Couqley French Bistro. Sales analysis, menu engineering, break-even, payroll, marketing. Upload Omega POS reports (CSV/Excel) to reports/ folder.",
  "version": "1.0.0",
  "author": { "name": "[Your Name]" },
  "keywords": ["restaurant", "omega", "pos", "sales", "menu-engineering", "breakeven", "payroll", "marketing", "couqley"]
}
```

---

## Skill Path Conventions

For plugins, paths are relative to the **plugin root** (e.g. `couqley-cowork/`). When a user opens a project with `reports/` and `outputs/`, the agent must resolve:

- **reports/** → project root `reports/` (user data)
- **outputs/** → project root `outputs/`
- **scripts/** → `skills/{skill}/scripts/` (inside plugin)
- **templates/** → `skills/{skill}/templates/` (inside plugin)

Update each analysis skill to document: "Look for reports in the project's `reports/` folder. Save dashboards to `outputs/`."

---

## Installation (Client Flow)

From [doc-radar-marketplace](https://github.com/peekwez/doc-radar-marketplace):

```
/plugin marketplace add github:[org]/couqley-marketplace
/plugin install couqley-cowork@couqley-marketplace
```

Client then:
1. Selects or creates a project folder (e.g. `couqley-cowork`).
2. Ensures `reports/` and `outputs/` exist.
3. Uploads Omega POS CSVs/Excel to `reports/`.
4. Asks Claude for analysis (sales, menu engineering, etc.).

---

## Migration Steps

1. Create `couqley-marketplace` structure (new repo or convert `couqley-cowork`).
2. Add `.claude-plugin/marketplace.json` at repo root.
3. Add `couqley-cowork/.claude-plugin/plugin.json`.
4. Copy skills from `~/.claude/skills/` into `couqley-cowork/skills/`, preserving each skill's `scripts/` and `templates/` inside its folder.
5. Apply inconsistency fixes (marketing, brand/cfo, naming).
6. Update README with installation and quick-start.
7. Test with: `claude --plugin-dir ./couqley-cowork` then `/plugin install` flow.

---

## Success Criteria

- [ ] Single plugin `couqley-cowork` installable via `/plugin install couqley-cowork@couqley-marketplace`.
- [ ] All 8 skills work: brand, sales, menu-engineer, breakeven, payroll, marketing, omega-extract, cfo.
- [ ] No broken script references in couqley-marketing.
- [ ] Single source of truth for brand (couqley-brand); cfo extends for financials only.
- [ ] Consistent `couqley-*` naming.
- [ ] Client can add marketplace and use skills without editing files.
