---
name: couqley-marketing
description: Comprehensive marketing analysis for Couqley Bistro. Uses outputs from sales and menu-engineer skills to generate social content, calendars, and promo designs.
tags: [marketing, analysis, social-media, promotions, strategy]
---

# Couqley Marketing Analysis Skill

## When to Use This Skill

Use this skill for:
- Analyzing sales data and identifying trends
- Finding top-performing menu items and categories
- Generating social media content
- Designing promotions and marketing campaigns
- Menu marketing strategies and positioning
- Content calendar planning
- Email marketing campaigns
- Campaign performance analysis

## Data Flow (Orchestrator)

This skill **orchestrates** outputs from other Couqley skills. Data flow:

1. **Source**: CSV (REP_S_00001 sales, REP_S_00506 menu engineering) or Excel (accounting, payroll) in the project's `reports/` folder
2. **Parsing**: Run **couqley-sales** or **couqley-menu-engineer** first — they own the parse and analyze scripts
3. **Input to this skill**: Use their outputs (top items, group performance, slow movers, Challenge items, Boston Matrix)
4. **Output**: Social content, calendars, promo designs using this skill's templates

**Do NOT reference** pdf_parser.py, sales_analyzer.py, or menu_analyzer.py — those live in couqley-sales and couqley-menu-engineer.

## Analysis Workflow

### Step 1: Get Base Data

- For sales insights: Run couqley-sales (parses REP_S_00001 CSV) → get top items, group performance, slow movers
- For menu/Challenge items: Run couqley-menu-engineer (parses REP_S_00506 CSV) → get Boston Matrix, Challenge items, marketing plays
- Reports live in project `reports/`. Save dashboards to `outputs/`.

### Step 2: Generate Marketing Content

- Use findings from Step 1 to populate marketing templates
- Lead with business impact in all outputs
- Focus on actionable recommendations
- Connect data to specific marketing opportunities
- Maintain brand alignment (reference couqley-brand skill)

### Step 3: Output to Templates

- Use `templates/marketing_summary.html` for interactive dashboard
- Use `templates/social_calendar.html` for content calendar
- Use `templates/promo_design.html` for campaign mockups
- Save all outputs to project `outputs/` folder with clear naming

## Marketing Capabilities

### Top-Selling Items Analysis

- Identify best performers across categories (from couqley-sales)
- Generate social media feature posts
- Create "customer favorites" content
- Develop signature dish spotlights

### Slow-Movers & Challenge Items

- Flag underperforming items (from couqley-sales slow_movers)
- Use Challenge items from couqley-menu-engineer for targeted promotion
- Develop positioning and upsell strategies
- Consider bundling with popular items

### Category Performance Analysis

- Analyze performance by menu category (from couqley-sales group_performance)
- Identify trending food types
- Determine content themes for upcoming campaigns
- Spot cross-sell opportunities

### Cross-Sell Opportunities

- Map item pairings from sales data
- Create bundle promotion recommendations (couqley-menu-engineer marketing plays)
- Generate server upsell scripts
- Design combo meal suggestions

## Template References

Templates live in this skill folder: `skills/marketing/templates/`

- **Marketing Summary Dashboard**: `templates/marketing_summary.html`
- **Social Calendar**: `templates/social_calendar.html`
- **Promotion Design**: `templates/promo_design.html`

## Brand Compliance

All marketing outputs must follow Couqley brand guidelines:
- Reference the `couqley-brand` skill for visual standards
- Maintain warm, inviting, sensory tone
- Use approved color palette and typography
- Ensure French bistro aesthetic consistency

## Example Workflow

1. User uploads REP_S_00001_sales.csv to `reports/`
2. Run couqley-sales → get top items, slow movers, group breakdown
3. Run couqley-menu-engineer if REP_S_00506 is available → get Challenge items
4. This skill uses those insights to generate social calendar, promo designs, email copy
5. Output to `outputs/` with branded templates
6. All materials follow couqley-brand guidelines
