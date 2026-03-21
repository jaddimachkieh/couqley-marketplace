# Omega POS Browser Navigation Guide

**Status:** Guide framework prepared. Will be refined after first live session with Omega POS interface.

**Current Instructions:** Based on typical POS web portal patterns and best practices. Actual UI/navigation will be confirmed and updated once we interact with the live system.

---

## Important Security Note

⚠️ **Credentials are personal and must never be stored or cached.**

When Claude Cowork needs to access Omega POS:
1. Request credentials from the user directly in the chat
2. Use credentials only for that session
3. Do NOT save, store, or reference credentials in any code or logs
4. After session ends, credentials are discarded

---

## Pre-Session Checklist

Before attempting to extract reports:

- [ ] User has valid Omega POS account credentials
- [ ] User can manually log in to https://cms.omegasoftware.ca/ successfully
- [ ] Required report types are available in Omega account
- [ ] Date range for report is known (e.g., "last 30 days", "January 2024")
- [ ] Local `reports/` folder exists for saving PDFs/CSVs

---

## Step-by-Step Navigation

### Step 1: Navigate to Omega POS Login
**URL:** `https://cms.omegasoftware.ca/`

**What to expect:**
- Clean login interface with username and password fields
- Possible "Remember me" or "Stay signed in" checkbox (uncheck for security)
- Login button
- Optional: "Forgot password" link

**Expected page elements:**
- Omega Software logo or branding
- Username/Email input field
- Password input field
- Submit/Login button

---

### Step 2: Request User Credentials

**Claude's action:** Ask the user directly in chat:

```
I need to access your Omega POS account to download sales reports.

Please provide:
1. Username or Email
2. Password

(These will be used only for this session and will not be saved.)
```

**Do NOT:**
- Assume or guess credentials
- Store credentials in variables or files
- Log credentials in console output
- Include credentials in generated content

---

### Step 3: Enter Credentials

**Fill in the login form:**

1. Click the username/email field
2. Type the username or email provided by user
3. Click the password field
4. Type the password provided by user
5. Click the "Login" or "Sign In" button

**Expected outcome:**
- Page redirects to dashboard or main menu
- Authentication successful, OR
- Error message if credentials are incorrect

**If login fails:**
- Check that username/password are entered correctly
- Verify with user that credentials are accurate
- If repeatedly failing, suggest user verify their credentials via password reset link
- Do NOT retry repeatedly (may trigger account lockout)

---

### Step 4: Navigate to Reports Section

**Expected menu structure** (typical for POS portals):

Main menu options may include:
- Dashboard / Home
- **Reports** ← This is what we need
- Sales / Transactions
- Inventory
- Staff / Payroll
- Settings / Admin

**Navigation action:**
1. Look for "Reports" in main navigation menu
2. This may be in top menu bar, left sidebar, or dropdown menu
3. Click "Reports" to access report generator

**Expected outcome:**
- Reports dashboard or report selection page
- List of available report types
- Date range picker
- Download/Export buttons

---

### Step 5: Select Report Type

**Expected report types available:**

Common report names in Omega or similar POS systems:
- Daily Sales Summary
- Sales by Item / Item Sales Detail
- Sales by Category
- Hourly Sales Distribution
- Payroll Report
- Labor Report
- Inventory Report
- COGS (Cost of Goods Sold)
- Customer Report
- Transaction Detail

**Navigation action:**
1. Look for report list or dropdown menu
2. Identify desired report type
3. Click to select report

**Example workflow:**
- User requests: "Download January sales by item"
- Navigate to Reports → Select "Item Sales Detail" or "Sales by Item"

---

### Step 6: Set Date Range

**Expected date picker interface:**

Most POS systems have:
- "Start Date" field (calendar picker or text input)
- "End Date" field (calendar picker or text input)
- Preset options (This Month, Last 30 Days, Year-to-Date, Custom Range)

**Navigation action:**
1. Click the "Start Date" field
2. Select or type the start date (e.g., 01/01/2024)
3. Click the "End Date" field
4. Select or type the end date (e.g., 01/31/2024)
5. Verify date range displays correctly

**Date format note:**
- Different systems accept different formats: MM/DD/YYYY, YYYY-MM-DD, or calendar picker
- If calendar picker available, use it (reduces format errors)
- If text input required, try MM/DD/YYYY first

**Expected outcome:**
- Date range is populated and valid
- System indicates date range is selectable (e.g., "30 days" or "Jan 1 - Jan 31")

---

### Step 7: Apply Filters (Optional)

**Possible filter options** (may vary):

- Location / Restaurant (if multi-location)
- Register / Terminal
- Employee / Staff member
- Payment Method (Cash, Card, etc.)
- Department (Kitchen, Bar, etc.)
- Category (if report supports it)

**Navigation action:**
1. Look for "Filters" section (often near date pickers)
2. If multi-location, ensure correct location is selected
3. Leave other filters default unless specifically requested
4. Common safest approach: Use defaults unless user specifies filters

**Expected outcome:**
- Filters are applied
- Report preview may update to show filtered data

---

### Step 8: Generate or Download Report

**Expected buttons/actions:**

Look for button labeled:
- "Generate Report"
- "Download"
- "Export"
- "View Report"
- "Get Report"
- "Run Report"

**Navigation action:**
1. Click the "Generate" or "Download" button
2. Select desired format if prompted:
   - PDF (recommended for visual review)
   - CSV (recommended for data processing)
   - Excel (.xlsx)
3. Wait for report to process (may take 5-30 seconds depending on date range)

**Expected outcome:**
- Report begins generating
- Progress indicator may appear
- Once complete, download dialog appears or file auto-downloads

---

### Step 9: Save Report to Local Folder

**Expected behavior:**

Browser download dialog appears (varies by browser):
- Chrome/Edge: Download icon → filename shown
- Firefox: Download popup with save options
- Safari: Downloads sidebar

**Navigation action:**
1. When download dialog appears, select save location
2. Save to: `/sessions/vigilant-serene-curie/mnt/outputs/couqley-cowork/reports/`
3. Filename should follow convention: `Couqley_[ReportType]_[StartDate]_to_[EndDate].[pdf/csv]`
4. Click "Save" or "Download"

**Example filenames:**
- `Couqley_DailySalesSummary_2024-01-01_to_2024-01-31.pdf`
- `Couqley_ItemSalesDetail_2024-01-15_to_2024-01-22.csv`
- `Couqley_HourlyDistribution_2024-01-20_to_2024-01-20.pdf`

**Expected outcome:**
- File downloads and saves to reports/ folder
- File appears in reports/ directory
- Claude can now reference file for parsing

---

### Step 10: Logout (Security Best Practice)

**Navigation action:**
1. Look for user menu (top-right corner, typically)
2. Click account icon or username
3. Select "Logout" or "Sign Out"
4. Page redirects to login screen

**Important:** Always logout after downloading to ensure session is closed.

---

## Troubleshooting Guide

### Issue: Login Fails

**Possible causes:**
- Incorrect username or password
- CAPS LOCK is on
- Spaces in password not entered correctly
- Account temporarily locked (too many failed attempts)
- Browser cookies need clearing

**Solutions:**
1. Verify credentials with user (ask them to type slowly)
2. Clear browser cookies: Settings → Cookies and cache data → Clear
3. Try in incognito/private window to avoid cached credentials
4. If still failing, ask user to reset password via "Forgot Password" link
5. Do NOT retry more than 3 times (account lockout risk)

---

### Issue: Report Generation Times Out

**Possible causes:**
- Date range is too large (e.g., 2 years of data)
- Server is slow or experiencing load
- Connection was interrupted
- Report type requires intensive calculation

**Solutions:**
1. Reduce date range (try 30 days instead of 365)
2. Wait 30 seconds and try again
3. Try exporting as CSV instead of PDF (often faster)
4. If still timing out, ask user to manually download from Omega and provide file

---

### Issue: Report Format Unexpected

**Possible causes:**
- Report template in Omega has changed
- Multi-page PDF (multiple tables scattered across pages)
- Currency format different than expected (£, €, etc.)
- Date format unfamiliar

**Solutions:**
1. Open downloaded file to inspect structure
2. If PDF, use `pdfplumber` to extract and inspect tables
3. If CSV, load with `pd.read_csv()` and inspect columns
4. Adjust parser code to handle new format
5. Document changes in OMEGA_REPORTS_REFERENCE.md for future reference

---

### Issue: "Access Denied" or Permission Error

**Possible causes:**
- User account doesn't have report access
- Report type restricted to managers/admins only
- User hasn't granted permission to access location data

**Solutions:**
1. Ask user to verify they have report permissions in their Omega account
2. User may need to contact their Omega account manager
3. Suggest trying a different, simpler report type first (e.g., Daily Sales Summary)
4. If persistent, contact Omega support

---

### Issue: Downloaded File is Corrupted

**Possible causes:**
- Download interrupted
- Browser download settings interfering
- File format mismatch (file claimed to be PDF but is HTML)

**Solutions:**
1. Try downloading again
2. Use incognito/private window to avoid cache issues
3. Try exporting as CSV instead
4. Check file size: should be >100KB for typical report
5. If very small, file may be error message instead of report

---

## Navigation Reference (Will Update After First Session)

**Currently estimated menu structure:**

```
Omega POS Dashboard
├── Reports
│   ├── Daily Sales Summary
│   ├── Item Sales Detail
│   ├── Category Sales
│   ├── Hourly Distribution
│   ├── Payroll
│   └── Inventory/COGS
├── [Other menu items]
└── Logout
```

This structure is typical for POS systems. After first live session, we'll map the exact Omega interface and update this guide with actual menu names, button locations, and any quirks.

---

## Next Steps After Download

1. Report file saved to `reports/` folder ✓
2. Run `pdf_parser.py` to extract structured data
3. Data validated against OMEGA_REPORTS_REFERENCE.md
4. Data loaded into analysis scripts
5. Generated branded dashboards from templates
6. Insights shared with team

---

## Security Checklist

- [ ] Credentials requested from user, not assumed
- [ ] Credentials not stored in code or files
- [ ] Credentials not included in logs or console output
- [ ] Session logged out after report download
- [ ] Downloaded file saved to correct folder
- [ ] File naming follows convention
- [ ] No screenshots containing credentials taken

---

## Support & Contact

If you encounter issues not covered here:

1. Check Omega support documentation: https://cms.omegasoftware.ca/support
2. Contact Omega support team directly
3. Document the issue and next steps for future reference

Last Updated: [SYSTEM DATE]
Next Review: After first live Omega POS session
