---
name: couqley-menu-engineer
description: Menu engineering analysis using Boston Matrix methodology. Upload a Menu Engineering CSV (REP_S_00506) and get Challenge item marketing plays, profit optimization, and branded dashboard.
---

# Menu Engineering Analysis

## Trigger
User uploads a Menu Engineering CSV file (REP_S_00506 from Omega POS) and asks for menu analysis, optimization, or marketing plays.

## Input
- **File:** Menu Engineering CSV (REP_S_00506_SMRY.csv or similar)
- **Format:** CSV exported from Omega POS PDF report

## Workflow

**Paths:** Look for reports in the project's `reports/` folder. Save dashboards to `outputs/`.

1. Save uploaded file to `reports/` folder
2. Run `scripts/parse.py` → `parse_menu_engineering_csv(csv_path)` → returns DataFrame
3. Run `scripts/analyze.py` → `menu_marketing_engine(df, top_n=20)` → returns analysis dict
4. Populate `templates/dashboard.html` with analysis data
5. Save output to `outputs/` folder
6. Present business impact summary first, then offer dashboard

## Output
- Branded HTML dashboard with Boston Matrix, Challenge item plays, profit scenarios
- Executive summary: "[X] Challenge items identified with $[Y] profit potential"

## Scripts (local to this skill)
- `scripts/parse.py` — Parses REP_S_00506 CSV format
- `scripts/analyze.py` — Boston Matrix, marketing plays, profit optimization

## Key Functions
- `parse_menu_engineering_csv(csv_path)` → DataFrame
- `menu_marketing_engine(df, top_n=20)` → dict with challenge_items, marketing_plays, matrix, optimization, summary
- `boston_matrix(df)` → dict with quadrant analysis
- `calculate_profit_optimization(df, volume_increase_pct=30.0)` → what-if scenarios

---

## Boston Matrix Methodology

This skill uses the Boston Matrix framework to classify menu items into four strategic categories. Each classification drives specific business actions.

### Boston Matrix Categories

#### Stars: High Popularity + High Margin
**Definition**: Items that sell well AND generate strong profit margins

**Characteristics**:
- Consistent high sales volume
- Good profit margin
- Customer favorites
- Strong brand alignment

**Strategic Actions**:
- Protect these items - never remove them
- Promote actively in marketing
- Feature prominently on menus
- Use as flagship items
- Consider slight price increases (carefully)
- Ensure consistent quality and availability
- Highlight in social media content

**Marketing Focus**: Celebration, signature positioning, brand confidence

**Examples**: Classic signature dishes, popular appetizers, signature drinks

---

#### Workhorses: High Popularity + Low Margin
**Definition**: Items that sell well but generate low or thin profit margins

**Characteristics**:
- High sales volume
- Consistent demand
- Low profit percentage
- Often commodity-heavy dishes

**Strategic Actions**:
- Increase price gradually (test 5-10% increases)
- Reduce cost without quality loss (supplier review, portion optimization)
- Bundle with higher-margin items
- Add premium variations (larger, specialty ingredients)
- Review cost structure and recipe efficiency
- Consider special pricing for slow periods only

**Marketing Focus**: Premium positioning, ingredient elevation, value communication

**Examples**: Popular pasta dishes, french fries, simple soups

---

#### Challenge Items: Low Popularity + High Margin
**Definition**: Items with strong profit potential but low sales volume

**Characteristics**:
- Low sales volume
- High profit margin
- Untapped potential
- Customer awareness issue

**Strategic Actions** (MARKETING OPPORTUNITY):
- These are primary marketing focus - maximize ROI opportunity
- Educate customers about the item (story, preparation)
- Create server upsell scripts for consistent recommending
- Feature in email campaigns and social media
- Bundle with popular items (Workhorses or Stars)
- Test positioning changes on menu
- Develop sensory-focused marketing language
- Create content around the item's story

**Why Challenge?**: High profit items with low awareness represent maximum ROI opportunity

**Marketing Plays Include**:
- Social media feature posts (story angles, photography)
- Server recommendations and upsell scripts
- Email spotlight campaigns
- Bundled promotions with popular items
- Menu placement optimization
- Limited-time feature positioning
- Ingredient or chef story emphasis

**Examples**: Premium cuts, specialty preparations, unique appetizers, signature cocktails

---

#### Dogs: Low Popularity + Low Margin
**Definition**: Items with low sales and low profit margins

**Characteristics**:
- Poor sales performance
- Thin margins
- Menu space wasted
- No clear strategic advantage

**Strategic Actions**:
- Consider removing from menu
- Only keep if part of required variety (salads, vegetarian options)
- If keeping: reduce portion size to lower cost
- Reposition on menu to less prominent locations
- Don't promote - focus marketing elsewhere
- Review if there's a cost-reduction opportunity
- Consider bundling to move inventory
- Reevaluate quarterly for removal

**Marketing Focus**: If kept, only promote in bundle deals with Stars/Challenges

**Examples**: Slow-moving desserts, niche dishes, items with high waste

---

## Analysis Output

### Dashboard Components

The skill generates an HTML dashboard with:

1. **Key Metrics Grid**
   - Total Items
   - Challenge Items count
   - Stars count
   - Average Profit Margin %

2. **Boston Matrix Scatter Chart**
   - X-axis: Popularity (%)
   - Y-axis: Profit Margin (%)
   - Color-coded by quadrant
   - Interactive tooltips

3. **Challenge Items Table**
   - Item name, group, quantity sold
   - Price, profit margin %, total profit
   - Sorted by profit potential

4. **Marketing Plays Section**
   - Top N items by profit potential
   - Action plans, bundle suggestions
   - Pricing strategies, social media hooks
   - Server recommendation scripts

5. **Profit Optimization Chart**
   - Current vs. projected profit (30% volume increase)
   - Top opportunities ranked by impact

6. **Key Insights Cards**
   - Summary of findings
   - Strategic recommendations
   - ROI potential calculations

---

## Implementation Timeline

### Immediate (This Week)
1. Upload Menu Engineering CSV
2. Generate Boston Matrix analysis
3. Identify top 5 Challenge items
4. Review dashboard and findings

### Short-term (2-4 Weeks)
1. Implement Challenge item marketing plays
2. Train servers on recommendations
3. Create social media content calendar
4. Test bundle pricing

### Mid-term (1-3 Months)
1. Measure Challenge item sales impact
2. Optimize Workhorse margins
3. Review bundle attachment rates
4. Adjust pricing based on results

### Quarterly
1. Re-run full Boston Matrix analysis
2. Identify new Challenge items
3. Evaluate removal candidates (Dogs)
4. Update menu positioning

---

## Success Metrics

You'll know menu engineering is working when:
- Challenge item sales increase by 20-30%
- Bundle sales reach 10-15% of total orders
- Margin on Workhorses improves 5-10%
- Dogs inventory reduces significantly
- Server feedback indicates ease of upselling
- Customer engagement with featured items grows

---

## Brand Compliance

All menu engineering outputs must:
- Use Couqley brand colors: Cream (#F7F3E9), Red (#CC3333), Gold (#BF9966)
- Maintain warm, inviting language
- Present data in a visually elegant format
- Include French bistro aesthetic

---

## Support

For questions about:
- **Menu item classification:** See Boston Matrix categories above
- **Marketing play implementation:** Check templates in dashboard output
- **Data parsing issues:** Review CSV format requirements in script documentation
- **Dashboard customization:** Edit templates/dashboard.html with analysis data
