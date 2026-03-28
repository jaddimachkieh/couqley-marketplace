---
name: couqley-omega-extract
description: Step-by-step guide to manually download reports from the Omega POS system and prepare them for analysis.
tags: [omega, pos, extraction, data, reports]
---

# Omega POS Report Extraction Guide

## Trigger
User needs to download fresh reports from Omega POS before running analysis skills.

## Overview
This skill guides you through downloading reports from Omega CMS so they are ready for the couqley-sales, couqley-menu-engineer, couqley-payroll, and couqley-breakeven skills.

## Step-by-Step

### Step 1: Log into Omega CMS
1. Open your browser and go to: **https://cms.omegasoftware.ca/**
2. Enter your username and password
3. Click **Log In**

> **Security:** Never share your credentials. This skill does not store or transmit your login information.

### Step 2: Navigate to Reports
1. In the main navigation, click **Reports**
2. Select the report type you need (see table below)

### Step 3: Set the Date Range
- Set **From** and **To** dates for the period you want to analyze
- Recommended: current month or last 30 days for regular analysis

### Step 4: Export the Report

| Report | Format | Use with skill |
|--------|--------|----------------|
| Item Sales Detail (REP_S_00001) | CSV | couqley-sales |
| Menu Engineering Summary (REP_S_00506) | CSV | couqley-menu-engineer |
| Payroll / Employee Hours | Excel (.xlsx) | couqley-payroll |
| Accounting / GL Export | Excel (.xlsx) | couqley-breakeven |

1. Click **Export** or **Download**
2. Choose **CSV** or **Excel** format as shown above
3. Wait for the download to complete

### Step 5: Upload to Cowork
1. In your Cowork conversation, click the **+** button
2. Select **Add files or photos**
3. Upload the downloaded report file
4. Then invoke the appropriate analysis skill (e.g., `/sales`)

## File Naming (recommended)
- `Couqley_Sales_2026-03.csv`
- `Couqley_MenuEngineering_2026-03.csv`
- `Couqley_Payroll_2026-03.xlsx`
- `Couqley_Accounting_2026-03.xlsx`

## Troubleshooting

| Issue | Solution |
|-------|---------|
| Can't find the report | Try Reports → Report List, search by name |
| CSV option not available | Export as Excel, the skills handle both |
| Login not working | Verify credentials, check caps lock, contact Omega support |
| Download takes too long | Try a shorter date range, then re-export |

## Next Steps
Once your file is uploaded, use:
- `/sales` — for sales analysis
- `/menu-engineer` — for Boston Matrix analysis
- `/payroll` — for payroll breakdown
- `/breakeven` — for financial forecast
