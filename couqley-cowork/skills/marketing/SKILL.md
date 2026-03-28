---
name: couqley-marketing
description: Comprehensive marketing analysis for Couqley Bistro. Uses sales and menu engineering data to generate social content calendars, promo designs, and marketing dashboards.
tags: [marketing, analysis, social-media, promotions, strategy]
---

# Couqley Marketing Analysis

## Trigger
User asks for marketing content, social media calendar, promotional campaigns, or marketing strategy — with or without data files.

## Input Options
- **With data:** Sales CSV (REP_S_00001) and/or Menu Engineering CSV (REP_S_00506) uploaded or in working folder
- **Without data:** Ask the user for key items/insights to base content on, or use outputs from couqley-sales / couqley-menu-engineer if already run

If files are available, read them directly to extract insights. Do not run external scripts.

## Workflow

### Step 1: Gather Insights
**If data files are available:**
- Read Sales CSV → identify top 5 items by revenue, top group, slow movers
- Read Menu CSV → identify Challenge items (low popularity, high margin), Stars

**If no data files:**
- Ask: "What are your top-selling items and any items you'd like to promote more?"

### Step 2: Generate Marketing Content
Based on the data insights, produce:

1. **4-Week Social Media Calendar** — 3–4 posts/week covering:
   - Star item features (celebrate customer favorites)
   - Challenge item spotlights (story-driven, sensory language)
   - Behind-the-scenes / chef/kitchen content
   - Seasonal or event-based posts
   - Each post: platform (Instagram/Facebook), caption draft, hashtag suggestions, best posting time

2. **Promotional Campaign Plays** — For top Challenge items:
   - Campaign name and angle
   - Email subject line
   - Social caption (sensory-focused, warm bistro tone)
   - Server upsell script (1–2 sentences)
   - Bundle offer suggestion

3. **Marketing Summary Dashboard** — HTML file with:
   - Brand colors: Cream `#F7F3E9`, Red `#CC3333`, Gold `#BF9966`
   - Top items to feature this month
   - Social calendar grid (4 weeks)
   - Campaign cards for each promo
   - Key marketing insights
   - Save as `Couqley_Marketing_[YYYY-MM].html`

## Tone & Voice
- Warm, inviting, authentic — sophisticated but approachable
- Sensory language: taste, aroma, texture, ambiance
- French terminology used sparingly (Coq au Vin, Crème Brûlée — not every post)
- Never: "AMAZING!!!", exclamation spam, generic promotional language

## Example Post (Challenge item — Sole Meunière)
"Delicate, buttery, and finished tableside — our Sole Meunière is a quiet masterpiece that deserves more time in the spotlight. Ask your server about tonight's preparation. 🐟🍋 #CouqleyFrenchBistro #SoleMeuniere #FrenchBistro"

## Brand Compliance
- All content follows Couqley brand guidelines (see couqley-brand skill)
- Cream backgrounds, Red accents, Gold borders in all HTML output
- File naming: `Couqley_Marketing_[Description]_[YYYY-MM].html`
