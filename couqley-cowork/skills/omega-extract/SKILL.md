---
name: couqley-omega-extract
description: Browser automation skill for extracting reports from Omega POS system
tags: [omega, pos, extraction, data, automation, browser]
---

# Couqley Omega Extract Skill

## When to Use This Skill

Use this skill whenever you need to:
- Extract fresh sales data from the Omega POS system
- Generate reports for marketing analysis
- Pull inventory or cost data
- Retrieve payroll information
- Update performance metrics
- Feed data into analysis pipelines

**Frequency**: Daily for sales reports, weekly for inventory, as-needed for special reports

## System Access

**Platform**: Omega CMS (Cloud-based)
**URL**: https://cms.omegasoftware.ca/
**System Type**: Browser-based POS reporting dashboard

## Critical Security Notice

**IMPORTANT**: This skill accesses sensitive business systems. Follow these security guidelines strictly:

- **Never store credentials** in any file, script, or configuration
- **Ask for credentials fresh** each time the skill runs
- **Do not log** username, password, or session tokens
- **Verify** the correct domain before entering credentials
- **Use HTTPS only** - confirm the connection is secure
- User is responsible for their Omega account security

## Step-by-Step Extraction Workflow

### Step 1: Navigate to Login Page
1. Open browser and navigate to: `https://cms.omegasoftware.ca/`
2. Verify the page shows "Omega CMS" branding
3. Confirm the URL matches exactly (no typos or similar domains)
4. Wait for page to load completely

### Step 2: Request User Credentials
**Before entering any credentials, ask the user**:

"I'm ready to log into Omega CMS. Please provide your username and password for this session. Your credentials will not be stored and will only be used during this current operation."

- Do not assume credentials
- Do not reuse credentials from previous sessions
- Do not attempt login without explicit user confirmation

### Step 3: Enter Credentials
1. Click on the username field
2. Enter the username provided by the user
3. Click on the password field
4. Enter the password provided by the user
5. Click the "Log In" or "Sign In" button
6. Wait for authentication to complete

### Step 4: Navigate to Reports Section
1. Look for "Reports" in the main navigation menu
2. Click to open Reports section
3. Verify you're in the correct module
4. Wait for reports list to load

### Step 5: Select Report Type
Choose from available report types. Common reports:

**Sales Reports:**
- Daily Sales Summary
- Item Sales Detail
- Category Sales Breakdown
- Hourly Sales Distribution
- Daily Revenue Report

**Payroll Reports:**
- Employee Hours & Pay
- Labor Cost Analysis
- Payroll Summary

**Inventory Reports:**
- Inventory Valuation
- Cost of Goods Sold (COGS)
- Inventory Movement
- Stock Levels

**Menu Engineering:**
- Menu Item Performance
- Sales Mix Analysis
- Price Performance

1. Click on desired report type
2. Wait for report configuration page to load

### Step 6: Set Date Range
1. Locate the "Date Range" or "From" and "To" fields
2. Enter the start date (format: MM/DD/YYYY or as specified by system)
3. Enter the end date
4. Most common: Last 7 days, last 30 days, or current month
5. Verify dates are correct before proceeding

### Step 7: Download as PDF
1. Look for "Download", "Export", or "Generate" button
2. Select format: Choose "PDF" if multiple options available
3. Click download button
4. File will download to browser's default download location
5. Wait for download to complete (watch for download notification)

### Step 8: Save to Reports Folder
Move or save the downloaded file to the `reports/` folder using this naming convention:

**Naming Convention**: `Couqley_[ReportType]_[DateRange].pdf`

**Examples**:
- `Couqley_DailySalesSummary_2024-01-15.pdf` (single day)
- `Couqley_ItemSalesDetail_2024-01-01-01-31.pdf` (date range)
- `Couqley_HourlySalesDistribution_2024-01-08-01-14.pdf` (week)
- `Couqley_InventoryValuation_2024-01-31.pdf` (month-end)
- `Couqley_CategorySalesBreakdown_2023-Q4.pdf` (quarter)

**Storage**: All files saved to `reports/` folder in project directory

## Available Report Types

### Daily Sales Summary
- **Contains**: Total revenue, transactions, average ticket size
- **Use for**: Daily performance tracking, trend identification
- **Frequency**: Daily download recommended
- **Date range**: Single day or range

### Item Sales Detail
- **Contains**: Each menu item's units sold, revenue, percentage of mix
- **Use for**: Marketing analysis, top/bottom performer identification
- **Frequency**: Weekly or bi-weekly
- **Date range**: Minimum 7 days for trend reliability

### Category Sales Breakdown
- **Contains**: Revenue by menu category, category trends
- **Use for**: Content theme planning, inventory focus
- **Frequency**: Monthly
- **Date range**: Monthly or quarterly

### Hourly Sales Distribution
- **Contains**: Sales by hour of operation
- **Use for**: Social media posting optimization, staffing analysis
- **Frequency**: Weekly
- **Date range**: 1-2 weeks

### Employee/Payroll Reports
- **Contains**: Hours worked, wages, labor costs
- **Use for**: Labor cost analysis, staffing efficiency
- **Frequency**: As needed for payroll
- **Date range**: Pay period or monthly

### Inventory/COGS Reports
- **Contains**: Inventory valuation, cost of goods sold, food costs
- **Use for**: Pricing analysis, margin calculation, menu engineering
- **Frequency**: Monthly or bi-weekly
- **Date range**: Monthly or period-to-date

## Post-Download Workflow

After successfully downloading a report:

1. **Verify file saved** to `reports/` folder with correct naming
2. **Confirm file integrity** - check file size is reasonable
3. **Suggest next steps** to user:
   - "Report saved as [filename]. Ready to run marketing analysis?"
   - "Run couqley-marketing skill to analyze this data"
   - "Use menu_analyzer.py to identify Challenge items"

4. **Do not automatically** run analysis - ask user for confirmation

## Error Handling

### Login Failed
**If credentials don't work:**
1. Ask user to verify username and password
2. Confirm they have current access to Omega CMS
3. Check if caps lock is on (password fields are case-sensitive)
4. Suggest resetting password if needed (must be done by user in Omega)
5. Do not retry more than 2 times per session

### Report Not Found
**If report type is unavailable:**
1. List available reports in the system
2. Ask user which report they prefer
3. Explain the alternative report options
4. Navigate to available report instead

### Download Failed
**If download doesn't complete:**
1. Check browser download folder
2. Verify internet connection is stable
3. Try downloading again (reload report, re-download)
4. If persistent, may need to check with Omega support

### Session Timeout
**If session expires during process:**
1. Return to login page (Step 1)
2. Ask user for credentials again (Step 2)
3. Do not reuse previous session - start fresh

## Security Checklist

Before running this skill, verify:

- [ ] URL is exactly `https://cms.omegasoftware.ca/` (HTTPS, not HTTP)
- [ ] Browser shows secure connection indicator (lock icon)
- [ ] No unusual security warnings or certificate errors
- [ ] User has confirmed they are ready to provide credentials
- [ ] No credentials are visible in any chat history
- [ ] Credentials will not be stored after this session

## Post-Extraction Best Practices

1. **Clear sensitive data** - Don't keep credentials in clipboard
2. **Verify downloads** - Confirm PDF files are in reports folder
3. **Update timestamps** - Note when report was extracted
4. **Secure storage** - Reports folder should have restricted access
5. **Regular cleanup** - Archive old reports periodically (monthly)

## Troubleshooting Guide

| Issue | Solution |
|-------|----------|
| Can't navigate to reports section | Try menu structure: Main Nav → Reports → Report Type |
| Date picker not working | Try manual entry in MM/DD/YYYY format |
| PDF won't download | Check browser download settings, try again |
| File saved to wrong location | Manually move file to `reports/` folder with correct name |
| Need different date format | Check Omega system requirements, adjust as needed |

## Integration with Analysis Pipeline

Once extraction is complete:

1. **pdf_parser.py** reads the PDF from `reports/` folder
2. **sales_analyzer.py** or **menu_analyzer.py** processes the data
3. **couqley-marketing** skill generates actionable insights
4. **Output** is sent to `outputs/` folder for use

This skill is the first step in the data-driven marketing pipeline for Couqley Bistro.
