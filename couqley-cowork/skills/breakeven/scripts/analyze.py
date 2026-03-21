"""
Break-even forecast analysis for Couqley.

Monthly P&L, break-even calculation, 12-month forecast with growth modeling.
Uses IS Family from the account mapping sheet for accurate classification.
Falls back to keyword matching if no mapping is available.
Self-contained — no imports from other couqley skills.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional


# ── IS Family → P&L Category Mapping ──────────────────────────────────
# These sets are derived from the Chart of Accounts mapping sheet.
# Each IS Family is classified into Revenue, COGS, or OpEx.

REVENUE_FAMILIES = {
    'Food Sales',
    'Beverage Sales',
    'Kiosk Sales',
    'Other Revenues',
}

COGS_FAMILIES = {
    'Food Cost',
    'Beverage Cost',
    'COGS Branches Adjustment',
    'Kiosk COS',
    'F&B Transfers',
}

# Everything else on the IS report is treated as Operating Expense.
# Listed here explicitly for documentation and dashboard breakdown:
OPEX_FAMILIES = {
    'Staff Cost',
    'Rent & Related Charges',
    'DOE',
    'Other Operational Expenses',
    'Professional Services',
    'Marketing & Promotion Activities',
    'Shop Supplies',
    'Gas',
    'Electricity & Generator',
    'Maintenance & Repairs',
    'Delivery Cost',
    'Packaging Material',
    'Printing',
    'Financial Charges',
    'Depreciation',
    'Governmental Fees',
    'Management Fees',
    'Royalty Fees',
    'Royalty Fees Kiosk',
    'Kiosk OPEX',
    'Sponsorship',
    'Income Tax',
}


def categorize_from_is_family(is_family: str) -> str:
    """
    Categorize a transaction using its IS Family from the mapping sheet.

    Args:
        is_family: The IS Family value (e.g., 'Food Sales', 'Staff Cost')

    Returns:
        One of: 'Revenue', 'COGS', 'Operating Expense', or 'Other'
    """
    if not is_family or pd.isna(is_family) or str(is_family).strip() == '':
        return 'Other'

    family = str(is_family).strip()

    if family in REVENUE_FAMILIES:
        return 'Revenue'
    if family in COGS_FAMILIES:
        return 'COGS'
    if family in OPEX_FAMILIES:
        return 'Operating Expense'

    # Fallback: try partial matching for families we haven't seen yet
    family_lower = family.lower()
    if any(kw in family_lower for kw in ['sales', 'revenue', 'income']):
        return 'Revenue'
    if any(kw in family_lower for kw in ['cost', 'cos', 'cogs']):
        return 'COGS'

    return 'Operating Expense'  # Default for unknown IS families


def categorize_account(account_name: str) -> str:
    """
    Fallback: categorize an account based on its name (keyword matching).

    Used only when the mapping sheet is not available or a transaction
    doesn't match any mapped account.

    Args:
        account_name: The name of the account to categorize

    Returns:
        One of: 'Revenue', 'COGS', 'Operating Expense', or 'Other'
    """
    if not account_name:
        return 'Other'

    name_lower = str(account_name).lower()

    # Revenue keywords
    revenue_keywords = [
        'revenue', 'income', 'sales', 'subscription', 'service income',
        'product sales', 'interest income', 'other income'
    ]

    # COGS keywords
    cogs_keywords = [
        'cogs', 'cost of goods', 'cost of sales', 'direct cost',
        'production cost', 'material', 'inventory', 'purchase', 'wholesale',
        'food cost', 'beverage cost', 'food purchase', 'beverage purchase'
    ]

    # Operating Expense keywords
    operating_keywords = [
        'marketing', 'advertising', 'general', 'administrative',
        'g&a', 'operating', 'rent', 'utilities', 'salary', 'payroll',
        'software', 'it', 'consulting', 'professional', 'legal', 'insurance',
        'depreciation', 'amortization', 'cleaning', 'transport', 'telephone',
        'staff', 'uniform', 'maintenance', 'repair', 'electric', 'generator',
        'gas', 'delivery', 'packaging', 'printing', 'subscription',
        'government', 'royalty', 'management fee', 'sponsorship'
    ]

    for keyword in revenue_keywords:
        if keyword in name_lower:
            return 'Revenue'

    for keyword in cogs_keywords:
        if keyword in name_lower:
            return 'COGS'

    for keyword in operating_keywords:
        if keyword in name_lower:
            return 'Operating Expense'

    return 'Other'


def _categorize_row(row) -> str:
    """
    Categorize a single transaction row.
    Uses IS Family mapping if available, falls back to keyword matching.
    """
    # First: try IS Family from mapping
    is_family = row.get('is_family', '') if hasattr(row, 'get') else ''
    if not is_family:
        is_family = row.get('IS_FAMILY', '')

    if is_family and str(is_family).strip():
        return categorize_from_is_family(is_family)

    # Fallback: keyword matching on account name
    for col in ['HISAB_NAME', 'hisab_name', 'account_name']:
        name = row.get(col, '') if hasattr(row, 'get') else ''
        if name and str(name).strip():
            return categorize_account(str(name))

    return 'Other'


def break_even_forecast(
    accounting_df: pd.DataFrame,
    forecast_months: int = 12,
    start_date: Optional[str] = None,
    revenue_growth_rate: float = 0.0,
    expense_growth_rate: float = 0.0
) -> Dict[str, Any]:
    """
    Perform break-even analysis and forecast for accounting data.

    Uses IS Family classifications from the mapping sheet when available.
    Falls back to keyword-based classification otherwise.

    Args:
        accounting_df: DataFrame with accounting transactions. Expected columns:
                      DATE, M DOLLAR (or m_dollar), D DOLLAR (or d_dollar),
                      HISAB_NAME (or hisab_name).
                      Optional: is_family, report_type (from mapping join)
        forecast_months: Number of months to forecast (default: 12)
        start_date: Start date for analysis (default: earliest date in data)
        revenue_growth_rate: Monthly revenue growth rate (0.0 to 1.0)
        expense_growth_rate: Monthly expense growth rate (0.0 to 1.0)

    Returns:
        Dictionary with keys:
        - historical_monthly: DataFrame of historical monthly data
        - forecast_monthly: DataFrame of forecasted monthly data
        - break_even_months: Number of months to break-even
        - chart_data: Dict for Chart.js visualization
        - summary: Dict with key metrics
        - summary_text: Human-readable summary
        - expense_breakdown: Dict with IS Family level detail
    """

    # Make a copy to avoid modifying original
    df = accounting_df.copy()

    # Normalize column names (handle both uppercase and lowercase)
    df.columns = df.columns.str.strip()
    col_map = {}
    for col in df.columns:
        col_lower = col.lower()
        if col_lower == 'date':
            col_map[col] = 'DATE'
        elif col_lower == 'm dollar' or col_lower == 'm_dollar':
            col_map[col] = 'M_DOLLAR'
        elif col_lower == 'd dollar' or col_lower == 'd_dollar':
            col_map[col] = 'D_DOLLAR'
        elif col_lower == 'hisab_name':
            col_map[col] = 'HISAB_NAME'
        elif col_lower == 'is_family':
            col_map[col] = 'is_family'
        elif col_lower == 'report_type':
            col_map[col] = 'report_type'

    df = df.rename(columns=col_map)

    # Ensure DATE is datetime
    if 'DATE' in df.columns:
        df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    else:
        raise ValueError("DATE column not found in accounting_df")

    # Remove rows with invalid dates
    df = df.dropna(subset=['DATE'])

    # Ensure M_DOLLAR and D_DOLLAR are numeric
    if 'M_DOLLAR' in df.columns:
        df['M_DOLLAR'] = pd.to_numeric(df['M_DOLLAR'], errors='coerce').fillna(0)
    else:
        df['M_DOLLAR'] = 0

    if 'D_DOLLAR' in df.columns:
        df['D_DOLLAR'] = pd.to_numeric(df['D_DOLLAR'], errors='coerce').fillna(0)
    else:
        df['D_DOLLAR'] = 0

    # ── Categorize transactions ──
    # Check if mapping data is available
    has_mapping = 'is_family' in df.columns and df['is_family'].notna().any() and (df['is_family'] != '').any()

    if has_mapping:
        # Filter to IS (Income Statement) accounts only for P&L
        if 'report_type' in df.columns:
            is_mask = df['report_type'] == 'IS'
            bs_count = (~is_mask & (df['report_type'] == 'BS')).sum()
            df = df[is_mask | (df['report_type'] == '')].copy()

        # Use IS Family mapping for classification
        df['Category'] = df['is_family'].apply(categorize_from_is_family)
    else:
        # Fallback: keyword matching on HISAB_NAME
        if 'HISAB_NAME' not in df.columns:
            raise ValueError("HISAB_NAME column not found and no mapping available")
        df['Category'] = df['HISAB_NAME'].apply(categorize_account)

    # Determine start date
    if start_date:
        start_date = pd.to_datetime(start_date)
    else:
        start_date = df['DATE'].min()

    df = df[df['DATE'] >= start_date].copy()

    # Extract year-month for grouping
    df['YearMonth'] = df['DATE'].dt.to_period('M')

    # ── Build expense breakdown by IS Family ──
    expense_breakdown = {}
    if has_mapping and 'is_family' in df.columns:
        for family in df['is_family'].unique():
            if not family or str(family).strip() == '':
                continue
            family_df = df[df['is_family'] == family]
            category = categorize_from_is_family(family)
            total_debit = family_df['M_DOLLAR'].sum()
            total_credit = family_df['D_DOLLAR'].sum()
            expense_breakdown[family] = {
                'category': category,
                'total_debit': float(total_debit),
                'total_credit': float(total_credit),
                'net': float(total_credit - total_debit) if category == 'Revenue' else float(total_debit - total_credit),
                'transaction_count': len(family_df)
            }

    # ── Calculate monthly revenue and expenses ──
    monthly_data = []

    for period in sorted(df['YearMonth'].unique()):
        period_df = df[df['YearMonth'] == period]

        # Revenue: D_DOLLAR (credits) on Revenue accounts
        revenue = period_df[period_df['Category'] == 'Revenue']['D_DOLLAR'].sum()
        # COGS: M_DOLLAR (debits) on COGS accounts
        cogs = period_df[period_df['Category'] == 'COGS']['M_DOLLAR'].sum()
        # OpEx: M_DOLLAR (debits) on Operating Expense accounts
        opex = period_df[period_df['Category'] == 'Operating Expense']['M_DOLLAR'].sum()

        revenue = max(0, revenue)
        cogs = max(0, cogs)
        opex = max(0, opex)

        total_expenses = cogs + opex
        gross_profit = revenue - cogs
        operating_profit = revenue - total_expenses

        monthly_data.append({
            'YearMonth': period,
            'Date': period.to_timestamp(),
            'Revenue': revenue,
            'COGS': cogs,
            'Operating_Expense': opex,
            'Total_Expenses': total_expenses,
            'Gross_Profit': gross_profit,
            'Operating_Profit': operating_profit
        })

    historical_monthly = pd.DataFrame(monthly_data)

    # Calculate average metrics for forecasting
    if len(historical_monthly) > 0:
        avg_revenue = historical_monthly['Revenue'].mean()
        avg_expenses = historical_monthly['Total_Expenses'].mean()

        # Use last 3 months trend if available
        if len(historical_monthly) >= 3:
            recent_revenue = historical_monthly['Revenue'].tail(3).mean()
            recent_expenses = historical_monthly['Total_Expenses'].tail(3).mean()
        else:
            recent_revenue = avg_revenue
            recent_expenses = avg_expenses
    else:
        avg_revenue = 0
        avg_expenses = 0
        recent_revenue = 0
        recent_expenses = 0

    # Use provided growth rates or calculate from last 3 months
    if revenue_growth_rate == 0.0 and len(historical_monthly) >= 3:
        revenues = historical_monthly['Revenue'].tail(3).values
        if revenues[0] > 0:
            revenue_growth_rate = (revenues[-1] - revenues[0]) / (revenues[0] * 2)
            revenue_growth_rate = max(-0.2, min(0.2, revenue_growth_rate))
        else:
            revenue_growth_rate = 0.02

    if expense_growth_rate == 0.0 and len(historical_monthly) >= 3:
        expenses = historical_monthly['Total_Expenses'].tail(3).values
        if expenses[0] > 0:
            expense_growth_rate = (expenses[-1] - expenses[0]) / (expenses[0] * 2)
            expense_growth_rate = max(-0.2, min(0.2, expense_growth_rate))
        else:
            expense_growth_rate = 0.01

    # ── Generate forecast ──
    forecast_data = []
    last_date = historical_monthly['Date'].max() if len(historical_monthly) > 0 else start_date

    current_revenue = recent_revenue if recent_revenue > 0 else avg_revenue
    current_expenses = recent_expenses if recent_expenses > 0 else avg_expenses

    cumulative_profit = 0
    if len(historical_monthly) > 0:
        cumulative_profit = historical_monthly['Operating_Profit'].sum()

    # Use actual COGS/OpEx ratio from historical data for forecast split
    if len(historical_monthly) > 0:
        total_hist_cogs = historical_monthly['COGS'].sum()
        total_hist_expenses = historical_monthly['Total_Expenses'].sum()
        cogs_ratio = total_hist_cogs / total_hist_expenses if total_hist_expenses > 0 else 0.4
    else:
        cogs_ratio = 0.4

    break_even_months = None

    for month_offset in range(forecast_months):
        forecast_date = last_date + timedelta(days=30 * (month_offset + 1))

        forecast_revenue = current_revenue * ((1 + revenue_growth_rate) ** (month_offset + 1))
        forecast_expenses = current_expenses * ((1 + expense_growth_rate) ** (month_offset + 1))

        forecast_profit = forecast_revenue - forecast_expenses
        cumulative_profit += forecast_profit

        if break_even_months is None and cumulative_profit >= 0:
            break_even_months = len(historical_monthly) + month_offset + 1

        forecast_data.append({
            'YearMonth': f"Forecast {month_offset + 1}",
            'Date': forecast_date,
            'Revenue': forecast_revenue,
            'COGS': forecast_expenses * cogs_ratio,
            'Operating_Expense': forecast_expenses * (1 - cogs_ratio),
            'Total_Expenses': forecast_expenses,
            'Gross_Profit': forecast_revenue - (forecast_expenses * cogs_ratio),
            'Operating_Profit': forecast_profit,
            'Is_Forecast': True
        })

    forecast_monthly = pd.DataFrame(forecast_data)

    if break_even_months is None:
        monthly_improvement = cumulative_profit / forecast_months if forecast_months > 0 else 0
        if monthly_improvement != 0:
            current_deficit = -cumulative_profit
            months_to_breakeven = current_deficit / monthly_improvement
            break_even_months = len(historical_monthly) + int(months_to_breakeven)
        else:
            break_even_months = None

    # ── Prepare chart data for Chart.js ──
    all_data = pd.concat(
        [
            historical_monthly.assign(Is_Forecast=False),
            forecast_monthly
        ],
        ignore_index=True
    )

    chart_data = {
        'labels': [str(d) for d in all_data['YearMonth']],
        'datasets': [
            {
                'label': 'Revenue',
                'data': all_data['Revenue'].tolist(),
                'borderColor': '#CC3333',
                'backgroundColor': 'rgba(204, 51, 51, 0.1)',
                'tension': 0.4
            },
            {
                'label': 'Total Expenses',
                'data': all_data['Total_Expenses'].tolist(),
                'borderColor': '#BF9966',
                'backgroundColor': 'rgba(191, 153, 102, 0.1)',
                'tension': 0.4
            },
            {
                'label': 'Operating Profit',
                'data': all_data['Operating_Profit'].tolist(),
                'borderColor': '#2ECC71',
                'backgroundColor': 'rgba(46, 204, 113, 0.1)',
                'tension': 0.4
            }
        ]
    }

    # ── Summary statistics ──
    total_historical_revenue = historical_monthly['Revenue'].sum() if len(historical_monthly) > 0 else 0
    total_historical_expenses = historical_monthly['Total_Expenses'].sum() if len(historical_monthly) > 0 else 0
    total_historical_profit = historical_monthly['Operating_Profit'].sum() if len(historical_monthly) > 0 else 0
    avg_monthly_revenue = historical_monthly['Revenue'].mean() if len(historical_monthly) > 0 else 0
    avg_monthly_expenses = historical_monthly['Total_Expenses'].mean() if len(historical_monthly) > 0 else 0
    total_historical_cogs = historical_monthly['COGS'].sum() if len(historical_monthly) > 0 else 0
    total_historical_opex = historical_monthly['Operating_Expense'].sum() if len(historical_monthly) > 0 else 0

    summary = {
        'total_historical_months': len(historical_monthly),
        'total_historical_revenue': float(total_historical_revenue),
        'total_historical_expenses': float(total_historical_expenses),
        'total_historical_cogs': float(total_historical_cogs),
        'total_historical_opex': float(total_historical_opex),
        'total_historical_profit': float(total_historical_profit),
        'avg_monthly_revenue': float(avg_monthly_revenue),
        'avg_monthly_expenses': float(avg_monthly_expenses),
        'break_even_months': break_even_months,
        'revenue_growth_rate': float(revenue_growth_rate),
        'expense_growth_rate': float(expense_growth_rate),
        'cumulative_profit_at_end': float(cumulative_profit),
        'classification_method': 'mapping' if has_mapping else 'keyword',
        'cogs_ratio': float(cogs_ratio)
    }

    # ── Generate summary text ──
    method_note = "using account mapping" if has_mapping else "using keyword classification"

    if break_even_months:
        summary_text = (
            f"Based on {len(historical_monthly)} months of data ({method_note}), "
            f"the business reaches break-even in approximately {break_even_months} months. "
            f"Avg monthly revenue: ${avg_monthly_revenue:,.0f}. "
            f"Avg monthly expenses: ${avg_monthly_expenses:,.0f} "
            f"(COGS: ${total_historical_cogs/max(len(historical_monthly),1):,.0f}, "
            f"OpEx: ${total_historical_opex/max(len(historical_monthly),1):,.0f})."
        )
    else:
        if cumulative_profit < 0:
            summary_text = (
                f"Based on {len(historical_monthly)} months of data ({method_note}), "
                f"the business is not projected to reach break-even within the forecast period. "
                f"Avg monthly revenue: ${avg_monthly_revenue:,.0f}. "
                f"Avg monthly expenses: ${avg_monthly_expenses:,.0f}."
            )
        else:
            summary_text = (
                f"Based on {len(historical_monthly)} months of data ({method_note}), "
                f"the business is profitable. "
                f"Avg monthly revenue: ${avg_monthly_revenue:,.0f}. "
                f"Avg monthly expenses: ${avg_monthly_expenses:,.0f} "
                f"(COGS: ${total_historical_cogs/max(len(historical_monthly),1):,.0f}, "
                f"OpEx: ${total_historical_opex/max(len(historical_monthly),1):,.0f})."
            )

    return {
        'historical_monthly': historical_monthly,
        'forecast_monthly': forecast_monthly,
        'break_even_months': break_even_months,
        'chart_data': chart_data,
        'summary': summary,
        'summary_text': summary_text,
        'expense_breakdown': expense_breakdown
    }
