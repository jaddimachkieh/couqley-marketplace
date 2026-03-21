# Couqley Marketplace Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Restructure Couqley skills as a Claude Code plugin marketplace inside couqley-cowork, fix inconsistencies, enable distribution via `/plugin marketplace add` + `/plugin install`.

**Architecture:** Single plugin `couqley-cowork` at repo root. Skills live in `couqley-cowork/skills/{skill}/` with self-contained scripts and templates. Marketplace manifest at `.claude-plugin/marketplace.json`. Reports/outputs stay at workspace root.

**Tech Stack:** Claude Code plugins (plugin.json, marketplace.json), Python (pandas), HTML/CSS/Chart.js.

**Design reference:** `docs/plans/2026-03-21-couqley-marketplace-design.md`

---

## Task 1: Create marketplace directory structure

**Files:** Create directories

**Steps:**
1. Create `.claude-plugin/` at repo root
2. Create `couqley-cowork/.claude-plugin/`
3. Create `couqley-cowork/skills/` and subdirs: `brand/`, `sales/`, `menu-engineer/`, `breakeven/`, `payroll/`, `marketing/`, `omega-extract/`, `cfo/`

**Commands:**
```bash
mkdir -p .claude-plugin
mkdir -p couqley-cowork/.claude-plugin
mkdir -p couqley-cowork/skills/{brand,sales,menu-engineer,breakeven,payroll,marketing,omega-extract,cfo}
```

**Verify:** `ls couqley-cowork/skills/` shows all 8 skill dirs.

---

## Task 2: Create marketplace.json

**File:** Create ` .claude-plugin/marketplace.json`

**Content:**
```json
{
  "name": "couqley-marketplace",
  "owner": { "name": "Couqley" },
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
      "author": { "name": "Couqley" }
    }
  ]
}
```

**Verify:** `cat .claude-plugin/marketplace.json | python3 -m json.tool` succeeds.

---

## Task 3: Create plugin.json

**File:** Create `couqley-cowork/.claude-plugin/plugin.json`

**Content:**
```json
{
  "name": "couqley-cowork",
  "description": "Restaurant analytics for Couqley French Bistro. Sales analysis, menu engineering, break-even, payroll, marketing. Upload Omega POS reports (CSV/Excel) to reports/ folder.",
  "version": "1.0.0",
  "author": { "name": "Couqley" },
  "keywords": ["restaurant", "omega", "pos", "sales", "menu-engineering", "breakeven", "payroll", "marketing", "couqley"]
}
```

**Verify:** `cat couqley-cowork/.claude-plugin/plugin.json | python3 -m json.tool` succeeds.

---

## Task 4: Copy couqley-brand skill

**Source:** `~/.claude/skills/couqley-brand/SKILL.md`  
**Target:** `couqley-cowork/skills/brand/SKILL.md`

**Steps:**
1. Copy `~/.claude/skills/couqley-brand/SKILL.md` → `couqley-cowork/skills/brand/SKILL.md`
2. Update frontmatter `name` to `couqley-brand` (keep for discovery)

**Command:**
```bash
cp ~/.claude/skills/couqley-brand/SKILL.md couqley-cowork/skills/brand/SKILL.md
```

**Verify:** `head -5 couqley-cowork/skills/brand/SKILL.md` shows YAML frontmatter.

---

## Task 5: Copy couqley-sales skill (with scripts and templates)

**Source:** `~/.claude/skills/couqley-sales/`  
**Target:** `couqley-cowork/skills/sales/`

**Steps:**
1. Copy `SKILL.md` → `couqley-cowork/skills/sales/SKILL.md`
2. Copy `scripts/` → `couqley-cowork/skills/sales/scripts/`
3. Copy `templates/` → `couqley-cowork/skills/sales/templates/`
4. In SKILL.md, add path note: "Reports live in project `reports/`. Dashboards go to `outputs/`."

**Commands:**
```bash
cp ~/.claude/skills/couqley-sales/SKILL.md couqley-cowork/skills/sales/
cp -r ~/.claude/skills/couqley-sales/scripts couqley-cowork/skills/sales/
cp -r ~/.claude/skills/couqley-sales/templates couqley-cowork/skills/sales/
```

**Verify:** `ls couqley-cowork/skills/sales/` shows SKILL.md, scripts/, templates/.

---

## Task 6: Copy couqley-menu-engineer skill

**Source:** `~/.claude/skills/couqley-menu-engineer/`  
**Target:** `couqley-cowork/skills/menu-engineer/`

**Commands:**
```bash
cp ~/.claude/skills/couqley-menu-engineer/SKILL.md couqley-cowork/skills/menu-engineer/
cp -r ~/.claude/skills/couqley-menu-engineer/scripts couqley-cowork/skills/menu-engineer/
cp -r ~/.claude/skills/couqley-menu-engineer/templates couqley-cowork/skills/menu-engineer/
```

**Verify:** `ls couqley-cowork/skills/menu-engineer/` shows SKILL.md, scripts/, templates/.

---

## Task 7: Copy couqley-breakeven skill

**Source:** `~/.claude/skills/couqley-breakeven/`  
**Target:** `couqley-cowork/skills/breakeven/`

**Commands:**
```bash
cp ~/.claude/skills/couqley-breakeven/SKILL.md couqley-cowork/skills/breakeven/
cp -r ~/.claude/skills/couqley-breakeven/scripts couqley-cowork/skills/breakeven/
cp -r ~/.claude/skills/couqley-breakeven/templates couqley-cowork/skills/breakeven/
```

**Verify:** `ls couqley-cowork/skills/breakeven/` shows SKILL.md, scripts/, templates/.

---

## Task 8: Copy couqley-payroll skill

**Source:** `~/.claude/skills/couqley-payroll/`  
**Target:** `couqley-cowork/skills/payroll/`

**Commands:**
```bash
cp ~/.claude/skills/couqley-payroll/SKILL.md couqley-cowork/skills/payroll/
cp -r ~/.claude/skills/couqley-payroll/scripts couqley-cowork/skills/payroll/
cp -r ~/.claude/skills/couqley-payroll/templates couqley-cowork/skills/payroll/
```

**Verify:** `ls couqley-cowork/skills/payroll/` shows SKILL.md, scripts/, templates/.

---

## Task 9: Copy couqley-marketing skill (templates only; SKILL.md will be rewritten)

**Source:** `~/.claude/skills/couqley-marketing/`  
**Target:** `couqley-cowork/skills/marketing/`

**Commands:**
```bash
cp -r ~/.claude/skills/couqley-marketing/templates couqley-cowork/skills/marketing/
```

**Verify:** `ls couqley-cowork/skills/marketing/templates/` shows marketing_summary.html, social_calendar.html, promo_design.html.

---

## Task 10: Rewrite couqley-marketing SKILL.md (fix broken script references)

**File:** Create `couqley-cowork/skills/marketing/SKILL.md`

**Content:** New orchestrator-focused skill. Remove all references to `pdf_parser.py`, `sales_analyzer.py`, `menu_analyzer.py`. Describe data flow: couqley-sales and couqley-menu-engineer parse CSVs → marketing consumes their findings.

**Key sections:**
- When to Use: marketing content, social calendar, promo design, email campaigns
- Data flow: "Uses outputs from couqley-sales (top items, group performance, slow movers) and couqley-menu-engineer (Challenge items, Boston Matrix). Run those skills first, or provide their analysis. Data lives in project `reports/` as CSV (REP_S_00001, REP_S_00506)."
- Templates: `templates/marketing_summary.html`, `social_calendar.html`, `promo_design.html` in this skill folder
- Brand: reference couqley-brand

**Verify:** Grep for "pdf_parser|sales_analyzer|menu_analyzer" in SKILL.md — no matches.

---

## Task 11: Copy couqley-omega-extract skill

**Source:** `~/.claude/skills/couqley-omega-extract/`  
**Target:** `couqley-cowork/skills/omega-extract/`

**Commands:**
```bash
cp ~/.claude/skills/couqley-omega-extract/SKILL.md couqley-cowork/skills/omega-extract/
```

**Verify:** `cat couqley-cowork/skills/omega-extract/SKILL.md` shows Omega extraction workflow.

---

## Task 12: Copy and refactor cfo-skills → couqley-cfo

**Source:** `~/.claude/skills/cfo-skills/`  
**Target:** `couqley-cowork/skills/cfo/`

**Steps:**
1. Copy SKILL.md to `couqley-cowork/skills/cfo/SKILL.md`
2. Copy `templates/` to `couqley-cowork/skills/cfo/templates/`
3. Update SKILL.md frontmatter: `name: couqley-cfo`
4. Add at top of content (after frontmatter): "For visual identity (colors, typography, logo), follow the couqley-brand skill. This skill extends with financial reporting standards only."
5. Remove duplicated brand sections (colors, typography, logo) — keep only financial scenario tables, EBITDA format, chart colors Bear/Base/Target, number formatting. Reference couqley-brand for visuals.

**Commands:**
```bash
cp ~/.claude/skills/cfo-skills/SKILL.md couqley-cowork/skills/cfo/
cp -r ~/.claude/skills/cfo-skills/templates couqley-cowork/skills/cfo/
```

**Verify:** `couqley-cowork/skills/cfo/SKILL.md` contains "couqley-brand" reference and no full color palette definition.

---

## Task 13: Copy shared reference docs to plugin

**Source:** `reference/` (workspace)  
**Target:** `couqley-cowork/reference/`

**Commands:**
```bash
mkdir -p couqley-cowork/reference
cp reference/OMEGA_REPORTS_REFERENCE.md couqley-cowork/reference/ 2>/dev/null || true
cp reference/OMEGA_LOGIN_GUIDE.md couqley-cowork/reference/ 2>/dev/null || true
cp reference/MARKETING_TEMPLATES.md couqley-cowork/reference/ 2>/dev/null || true
```

**Verify:** `ls couqley-cowork/reference/` shows at least one file.

---

## Task 14: Update script paths in analysis skills

**Files:** `couqley-cowork/skills/sales/SKILL.md`, `menu-engineer/SKILL.md`, `breakeven/SKILL.md`, `payroll/SKILL.md`

**Change:** In each SKILL.md, document that:
- Reports path: project `reports/` folder (user uploads CSVs/Excel there)
- Outputs path: project `outputs/` folder
- Scripts path: `skills/{skill}/scripts/` (relative to plugin root when running from project)
- Templates path: `skills/{skill}/templates/`

Add one-line note in Workflow sections: "Look for reports in the project's `reports/` folder. Save dashboards to `outputs/`."

---

## Task 15: Create couqley-cowork README.md

**File:** Create `couqley-cowork/README.md`

**Content:** Installation and quick-start per design doc. Include:
- What this plugin does
- Prerequisites (Omega POS, reports in CSV/Excel)
- Installation: `/plugin marketplace add github:...` and `/plugin install couqley-cowork@couqley-marketplace`
- Quick start: create reports/ and outputs/, upload files, ask Claude
- Skills list with one-line descriptions

---

## Task 16: Update root README.md

**File:** Modify `README.md`

**Changes:**
- Add section "Claude Code Plugin Installation" with marketplace commands
- Update "What's Inside" to reflect new structure (couqley-cowork plugin, skills inside)
- Fix data flow: CSV/Excel (not PDF) as primary format
- Add `.claude-plugin/` and `couqley-cowork/` to structure description

---

## Task 17: Update .claude/CLAUDE.md (optional)

**File:** ` .claude/CLAUDE.md`

**Changes:** Ensure skills table matches new skill names (couqley-cfo not cfo-skills). Paths reference project reports/ and outputs/. No changes if CLAUDE.md is already generic.

---

## Task 18: Add .gitignore entries (if needed)

**File:** `.gitignore`

**Add if not present:**
```
outputs/*.html
reports/*.csv
reports/*.xlsx
```

Keep outputs/ and reports/ dirs with .gitkeep if you want them tracked. User data (CSV, Excel) should not be committed.

---

## Task 19: Verify plugin structure

**Command:**
```bash
find couqley-cowork -type f | head -50
```

**Expected:** plugin.json, 8× SKILL.md, scripts in sales/menu-engineer/breakeven/payroll, templates in each.

---

## Task 20: Test plugin load (manual)

**Command:**
```bash
claude --plugin-dir ./couqley-cowork
```

**Verify:** Claude Code starts. Run `/help` or `/couqley-cowork:brand` (or equivalent) to confirm skills load. If Claude Code not installed, note: "Manual test: run `claude --plugin-dir ./couqley-cowork` when Claude Code is available."

---

## Commit Strategy

- Commit after Task 3: "Add marketplace and plugin manifests"
- Commit after Task 12: "Add all skills to couqley-cowork plugin"
- Commit after Task 16: "Update README and docs for marketplace install"

---

## Execution Handoff

Plan complete and saved to `docs/plans/2026-03-21-couqley-marketplace-implementation.md`.

**Two execution options:**

1. **Subagent-Driven (this session)** — I execute tasks in sequence, you review between major milestones.
2. **Parallel Session (separate)** — Open a new session with executing-plans skill for batch execution with checkpoints.

Which approach?
