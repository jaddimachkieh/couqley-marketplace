# Couqley Cowork Marketing Package

Self-contained package for Couqley French Bistro marketing analytics, menu engineering, and sales intelligence. No external APIs, databases, or MCPs required.

---

## Installation

1. Open **Claude Desktop** and launch **Claude Cowork**
2. Go to the **Plugins** panel (click the "+" icon)
3. Add the Couqley Cowork plugin — install from the [plugin directory](https://claude.com/plugins-for/cowork) (if available) or add from GitHub: `github:jaddimachkieh/couqley-marketplace`
4. Select a project folder with `reports/` and `outputs/` (see setup below)

## Project Setup (Required)

The plugin reads data from `reports/` and saves dashboards to `outputs/`. You must create these folders in your working directory:

1. **Create a project folder** (e.g. `Couqley-Analytics` or `My-Restaurant-Data`)
2. **Create the two subdirectories** inside it:

   ```bash
   mkdir reports outputs
   ```

3. **Open that folder** in Claude Cowork
4. **Upload Omega POS reports** (CSV/Excel) to `reports/`
5. Ask Claude to analyze — dashboards will be saved to `outputs/`

## Prerequisites

- Omega POS reports exported as CSV or Excel  
- Report types: REP_S_00001 (sales), REP_S_00506 (menu engineering), accounting Excel, payroll Excel  
- Mapping Sheet (Chart of Accounts) is bundled in the plugin — no setup needed

## Skills at a Glance

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

**Data flow:** `reports/` (CSV, Excel) → skills parse & analyze → `outputs/` (HTML dashboards)

---

## Overview

This package transforms raw Omega POS data into actionable marketing insights and branded content. From sales analysis to social media calendars, everything is designed to help Couqley understand customer behavior and optimize revenue.

**Key Philosophy:** Fast, elegant, standalone. No setup required beyond downloading the folder.

---

## Quick Start

### 1. Set Up

Open **Claude Cowork**, select your project folder, upload reports to `reports/`, and ask questions (see Installation above if you haven't installed the plugin yet).

### 2. Common Requests

Ask Claude any of these:

**Sales Analysis:**
- "Download the latest sales report from Omega"
- "Analyze this month's sales and suggest marketing ideas"
- "What are our top 10 items by revenue?"
- "Which categories are underperforming?"

**Menu Engineering:**
- "Run a Boston Matrix analysis on our menu"
- "What menu items should we promote?"
- "Find cross-sell opportunities"
- "Calculate food cost impact of removing [item]"

**Marketing Content:**
- "Create a social media calendar for next week"
- "Design a promotion for [holiday/season]"
- "Generate email campaign copy for happy hour"
- "Write Instagram captions for these menu items"

**Reporting:**
- "Build a marketing summary dashboard"
- "Create a campaign mockup for [promo]"
- "Generate a weekly report of sales trends"

---

## What's Inside

### Plugin Structure

```
couqley-cowork/
├── .claude-plugin/plugin.json
├── skills/           # brand, sales, menu-engineer, breakeven, payroll, marketing, omega-extract, cfo
│   └── {skill}/
│       ├── SKILL.md
│       ├── scripts/   # parse.py, analyze.py
│       └── templates/ # dashboard.html
├── reference/
└── README.md
```

**Data:** Upload CSV (REP_S_00001, REP_S_00506) or Excel (accounting, payroll) to `reports/`. Dashboards save to `outputs/`.

#### **couqley-brand**
Brand identity and guidelines.

**What it does:**
- Centralized brand definitions
- Used by all other skills to maintain consistency

**Key Colors:**
```
Cream:  #F7F3E9 (backgrounds)
Red:    #CC3333 (headers, CTAs)
Gold:   #BF9966 (borders, accents)
Dark:   #333333 (text, footers)
```

---

#### **couqley-marketing**
Marketing analysis, content generation, and promotional design.

**Skills:**
- Analyze sales data and identify marketing opportunities
- Generate social media captions and content calendars
- Create promotional campaign mockups
- Build email marketing copy
- Suggest hashtags and content themes

**Templates:**
- `marketing_summary.html` - Interactive dashboard with charts
- `social_calendar.html` - 4-week content calendar
- `promo_design.html` - Campaign mockup with email and social previews

**Example Use:**
```
User: "Analyze January sales and suggest marketing ideas"
→ Claude parses Omega reports, identifies top items and trends
→ Generates marketing_summary.html dashboard
→ Suggests targeted promotions and content angles
→ Provides social media calendar template filled with ideas
```

---

#### **couqley-menu-engineer**
Menu optimization using Boston Matrix and profitability analysis.

**Skills:**
- Identify stars (high margin, high volume - promote)
- Identify plowhorses (low margin, high volume - reprice)
- Identify puzzles (high margin, low volume - feature)
- Identify dogs (low margin, low volume - consider removing)
- Calculate menu mix and profitability
- Suggest pricing adjustments

**Example Use:**
```
User: "Run a Boston Matrix analysis"
→ Claude analyzes item sales and cost data
→ Plots items on profitability vs. popularity grid
→ Provides recommendations for each category
→ Suggests menu adjustments and upsell strategies
```

---

#### **couqley-omega-extract**
Browser automation for extracting data from Omega POS.

**Skills:**
- Navigate to Omega POS login (https://cms.omegasoftware.ca/)
- Request user credentials securely
- Download reports (PDF or CSV)
- Save reports to local folder with proper naming
- Handle common authentication issues

**Security:**
- Credentials requested directly from user, never stored
- Session logged out after report download
- No credential logging or caching

**Example Use:**
```
User: "Download the latest sales report from Omega"
→ Claude requests username and password in chat
→ Navigates to Omega POS and logs in
→ Downloads available reports
→ Saves to reports/ folder with timestamped filenames
→ Confirms completion and ready for analysis
```

---

### `scripts/` Directory

Python scripts for data parsing and analysis.

**scripts/pdf_parser.py**
- Extracts tables from Omega PDF reports using `pdfplumber`
- Parses CSV exports using `pandas`
- Normalizes currency values and dates
- Filters subtotal/total rows
- Returns structured DataFrames

**scripts/sales_analyzer.py**
- Calculates top items by revenue and quantity
- Identifies peak hours and day-of-week patterns
- Computes average ticket value and customer metrics
- Detects sales trends and anomalies
- Suggests marketing insights based on data

**scripts/menu_analyzer.py**
- Implements Boston Matrix categorization
- Calculates item profitability
- Identifies cross-sell pairs
- Suggests pricing adjustments
- Recommends promotion strategies

**scripts/marketing_helpers.py**
- Generates social media captions from templates
- Creates hashtag combinations
- Builds content calendars
- Formats email copy with brand voice
- Renders HTML dashboards from templates

**scripts/pdf_generator.py** (Optional)
- Converts HTML dashboards to PDF for print/email
- Requires `weasyprint` or similar

---

### `reference/` Directory

Reference documents and content templates.

**OMEGA_REPORTS_REFERENCE.md**
- Expected structure for each Omega report type
- Column mappings and data types
- Parsing guidelines for PDF and CSV
- Date and currency format handling
- Troubleshooting guide

**MARKETING_TEMPLATES.md**
- Reusable social media captions (Instagram, Facebook)
- Email marketing templates (newsletters, promotions, reminders)
- Promotional copy templates (happy hour, seasonal, bundle deals)
- Hashtag sets by content type
- CTA phrases for different channels
- Brand voice guidelines

**OMEGA_LOGIN_GUIDE.md**
- Step-by-step browser navigation for Omega POS
- Security best practices for credential handling
- Troubleshooting login and download issues
- Expected menu structure and report types
- Will be refined after first live session

**FILE_STRUCTURE.md** (This file)
- Overview of all folders and files
- How to use each skill and script
- Common workflows and examples

---

### `reports/` Directory

Store your Omega POS reports here. File naming convention:

```
Couqley_[ReportType]_[StartDate]_to_[EndDate].[pdf/csv]
```

**Examples:**
- `Couqley_DailySalesSummary_2024-01-01_to_2024-01-31.pdf`
- `Couqley_ItemSalesDetail_2024-01-15_to_2024-01-22.csv`
- `Couqley_HourlyDistribution_2024-01-20_to_2024-01-20.pdf`

**Organization:**
- Keep raw reports organized by month
- Archive old reports to avoid cluttering
- Use consistent naming for easy programmatic access

---

### `outputs/` Directory

Your generated dashboards and reports are saved here.

**Subdirectories:**
```
outputs/
├── dashboards/
│   ├── marketing_summary_2024-01.html
│   ├── sales_analysis_jan.html
│   └── campaign_mockup_vday_promo.html
├── content/
│   ├── social_calendar_2024-w1-4.html
│   ├── email_newsletter_jan.html
│   └── instagram_captions.txt
├── analysis/
│   ├── boston_matrix_analysis.json
│   ├── sales_trends.json
│   └── menu_recommendations.txt
└── exports/
    ├── couqley_dashboards.pdf (batch export)
    └── couqley_reports_jan.zip (archive)
```

---

## Workflows

### Workflow 1: Weekly Sales Analysis → Marketing Insights

**Time:** ~10 minutes (if report already downloaded)

```
1. Ask: "Analyze last week's sales"
   → couqley-omega-extract downloads latest report
   → sales_analyzer.py processes data

2. Claude generates:
   → marketing_summary.html dashboard
   → Identifies top 3 actionable insights
   → Suggests targeted promotions

3. Use insights to:
   → Create social media calendar (couqley-marketing)
   → Design email campaign (marketing_helpers.py)
   → Update menu positioning (couqley-menu-engineer)
```

---

### Workflow 2: Menu Optimization

**Time:** ~15 minutes

```
1. Ask: "Run a Boston Matrix analysis on our current menu"
   → menu_analyzer.py processes item sales and COGS data

2. Claude categorizes each item:
   → STARS (promote & feature)
   → PLOWHORSES (reprice or remove)
   → PUZZLES (test promotions)
   → DOGS (consider removing)

3. Generate recommendations:
   → Which items to feature in marketing
   → Which items to offer at happy hour
   → Which items need pricing review
   → Which items could be bundled
```

---

### Workflow 3: Campaign Launch

**Time:** ~30 minutes

```
1. Ask: "Create a Valentine's Day promotion campaign"
   → couqley-marketing designs full campaign

2. Generated outputs:
   → promo_design.html mockup (email + social preview)
   → email_newsletter.html ready to send
   → social_calendar.html with Valentine's content
   → campaign_metrics.json (expected reach, budget, ROI)

3. Customize and launch:
   → Review generated mockups
   → Adjust copy or dates as needed
   → Send email campaign
   → Schedule social media posts
   → Brief staff on upsell talking points
```

---

### Workflow 4: Content Creation

**Time:** ~20 minutes

```
1. Ask: "Generate a 4-week social media calendar for February"
   → couqley-marketing.py creates social_calendar.html

2. Calendar includes:
   → Daily content themes (Feature Dish, Behind Kitchen, etc.)
   → Caption ideas for each post
   → Hashtag suggestions
   → Platform-specific guidance (Instagram, Facebook, Email)

3. Use as:
   → Content planning guide
   → Caption templates (refine before posting)
   → Hashtag reference
   → Timing/frequency standard
```

---

## Adding Your Data

### Manually Add a Report

1. Download the report from Omega POS (or ask Claude to do it)
2. Rename the file: `Couqley_[Type]_[Date]_to_[Date].[pdf/csv]`
3. Save to your `reports/` folder
4. Ask Claude to analyze: "Analyze the [Month] sales report"

---

## Technology Stack

**No complex dependencies—everything uses common libraries:**

- **Python:** `pandas`, `pdfplumber`, `json`, `csv`
- **HTML/CSS:** Pure HTML5 and CSS3 (no frameworks)
- **JavaScript:** Chart.js (via CDN) for dashboards
- **Browser Automation:** Claude Cowork native browser tools

**Why minimal dependencies?**
- Faster to install and maintain
- Works offline (except Omega POS login)
- Easier to debug and customize
- No security risks from external packages

---

## Brand Guidelines at a Glance

**Colors:**
- Cream: `#F7F3E9` - Primary background
- Red: `#CC3333` - Headers, CTAs, emphasis
- Gold: `#BF9966` - Borders, secondary accents
- Dark: `#333333` - Text, footers

**Typography:**
- Body: Georgia serif (elegant, French bistro feel)
- Headlines: Bold Georgia or sans-serif (clear hierarchy)
- Accent: Uppercase, small caps for labels

**Tone:**
- Warm, inviting, elegant
- Community-focused (not pretentious)
- Quality and technique matter
- Stories and tradition important

**Visual Style:**
- Cream/white backgrounds
- Red and gold accents
- Serif fonts for sophistication
- High-quality food photography
- Clean, spacious layouts

---

## Troubleshooting

### "Module not found" error

**Solution:** Ensure Python dependencies are installed
```bash
pip install pandas pdfplumber
```

### Reports folder doesn't exist

**Solution:** Create it manually
```bash
mkdir reports
```

### HTML dashboards don't display correctly

**Solution:** Open in modern browser (Chrome, Firefox, Safari, Edge)
- Dashboards use CSS Grid and modern JavaScript
- Older browsers may not render properly

### Chart.js not loading

**Solution:** Check internet connection
- Chart.js loads from CDN (`cdn.jsdelivr.net`)
- Some networks block CDN access
- If blocked, download Chart.js locally and reference locally

### Data missing from dashboards

**Solution:** Check placeholder comments in HTML
- Dashboards have `<!-- REPLACE: field_name -->` comments
- The script must inject actual data before rendering
- If placeholders remain, verify parser output matches expected field names

---

## Storage & Backups

**Recommended practice:**

1. **reports/** - Keep raw Omega exports; archive monthly
2. **outputs/** - Keep recent dashboards; archive older versions
3. **Git:** Commit README, scripts, templates (not generated outputs)
4. **Backups:** Monthly archive of outputs/dashboards

**Directory size estimates:**
- Single Omega report: 500 KB - 5 MB
- Single dashboard: 100 KB - 500 KB
- Full month of content: 20-50 MB

---

## Quick Reference: Common Tasks

| Task | Ask Claude | Time |
|------|-----------|------|
| Download latest report | "Download the latest sales report from Omega" | 2-3 min |
| Analyze sales data | "Analyze [month] sales and suggest marketing ideas" | 5-10 min |
| Boston Matrix | "Run a Boston Matrix analysis on our menu" | 5-7 min |
| Social calendar | "Create a 4-week social media calendar for [month]" | 10-15 min |
| Email campaign | "Design a promotional email for [offer]" | 10-15 min |
| Marketing dashboard | "Build a marketing summary dashboard for [period]" | 5-10 min |
| Sales trends | "What are our sales trends for [period]?" | 5 min |
| Top items | "What are our top 10 menu items by revenue?" | 2-3 min |

---

## Support

**Questions about data?**
- Check `reference/OMEGA_REPORTS_REFERENCE.md` in the plugin
- Verify your data format matches the expected structure

**Issues with marketing templates?**
- Reference `reference/MARKETING_TEMPLATES.md` in the plugin

**Need help?** Ask Claude directly—it knows this package and can help with any task.

---

## Roadmap

**Planned Enhancements:**

- [ ] Automated weekly report generation (email digest)
- [ ] Customer loyalty program analysis
- [ ] Reservation optimization recommendations
- [ ] Supplier performance dashboard
- [ ] Staff performance metrics
- [ ] Integration with review platforms (Google, Yelp)
- [ ] Dynamic pricing recommendations
- [ ] Seasonal forecasting

---

**Last Updated:** February 2026
