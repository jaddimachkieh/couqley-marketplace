"""
Payroll Analyzer for Couqley.
Department breakdown, cost analysis, employee rankings, monthly trends.
Self-contained — no imports from other couqley skills.
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def payroll_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Comprehensive payroll analysis from parsed payroll DataFrame.

    Args:
        df: Parsed payroll DataFrame with columns including:
            Name, Dep (department), and numeric salary/cost columns

    Returns:
        Dict with: department_breakdown, top_employees, metrics, insights, summary_text
    """
    if df.empty:
        return {
            'department_breakdown': [],
            'top_employees': [],
            'metrics': {},
            'insights': [],
            'summary_text': 'No payroll data available.'
        }

    # Identify numeric columns (salary/cost data)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Try to find the total cost column
    total_col = None
    for col in numeric_cols:
        col_lower = str(col).lower()
        if 'total' in col_lower or 'net' in col_lower or 'gross' in col_lower:
            total_col = col
            break

    # If no total column, sum all numeric columns per row
    if total_col is None and numeric_cols:
        df = df.copy()
        df['_total_cost'] = df[numeric_cols].sum(axis=1)
        total_col = '_total_cost'

    if total_col is None:
        return {
            'department_breakdown': [],
            'top_employees': [],
            'metrics': {},
            'insights': [],
            'summary_text': 'Could not identify payroll cost columns.'
        }

    # Department breakdown
    dept_col = None
    for col in df.columns:
        if str(col).lower() in ['dep', 'department', 'dept']:
            dept_col = col
            break

    department_breakdown = []
    if dept_col:
        dept_agg = df.groupby(dept_col).agg(
            total_cost=(total_col, 'sum'),
            employee_count=('Name', 'count'),
            avg_cost=(total_col, 'mean')
        ).round(2)
        dept_agg = dept_agg.sort_values('total_cost', ascending=False)
        total_payroll = dept_agg['total_cost'].sum()

        for dept_name, row in dept_agg.iterrows():
            department_breakdown.append({
                'department': str(dept_name),
                'total_cost': round(float(row['total_cost']), 2),
                'employee_count': int(row['employee_count']),
                'avg_cost': round(float(row['avg_cost']), 2),
                'pct_of_total': round(float(row['total_cost'] / total_payroll * 100), 1) if total_payroll > 0 else 0
            })
    else:
        total_payroll = df[total_col].sum()

    # Top employees by cost
    top_employees = []
    if 'Name' in df.columns:
        top_n = df.nlargest(10, total_col)
        for _, emp in top_n.iterrows():
            entry = {
                'name': str(emp['Name']),
                'total_cost': round(float(emp[total_col]), 2)
            }
            if dept_col and dept_col in emp.index:
                entry['department'] = str(emp[dept_col])
            top_employees.append(entry)

    # Metrics
    metrics = {
        'total_employees': len(df),
        'total_payroll': round(float(total_payroll), 2),
        'avg_per_employee': round(float(total_payroll / len(df)), 2) if len(df) > 0 else 0,
        'departments': len(department_breakdown)
    }

    # Insights
    insights = []
    if department_breakdown:
        top_dept = department_breakdown[0]
        insights.append({
            'title': f'{top_dept["department"]} Leads Payroll',
            'insight': f'{top_dept["department"]} accounts for {top_dept["pct_of_total"]}% of total payroll (${top_dept["total_cost"]:,.0f}) with {top_dept["employee_count"]} employees.',
            'type': 'positive'
        })

        if len(department_breakdown) >= 2:
            second_dept = department_breakdown[1]
            insights.append({
                'title': f'{second_dept["department"]} is Second',
                'insight': f'{second_dept["department"]} represents {second_dept["pct_of_total"]}% of payroll (${second_dept["total_cost"]:,.0f}) with {second_dept["employee_count"]} employees.',
                'type': 'positive'
            })

    if top_employees:
        top_emp = top_employees[0]
        dept_info = f' ({top_emp.get("department", "")})' if 'department' in top_emp else ''
        insights.append({
            'title': 'Top Earner',
            'insight': f'{top_emp["name"]}{dept_info} is the highest-paid employee at ${top_emp["total_cost"]:,.0f}.',
            'type': 'positive'
        })

    if len(department_breakdown) >= 2:
        top_2_pct = department_breakdown[0]['pct_of_total'] + department_breakdown[1]['pct_of_total']
        if top_2_pct > 75:
            insights.append({
                'title': 'Cost Concentration',
                'insight': f'Top 2 departments account for {top_2_pct:.0f}% of payroll. Monitor for efficiency opportunities.',
                'type': 'warning'
            })
        else:
            insights.append({
                'title': 'Balanced Distribution',
                'insight': f'Top 2 departments account for {top_2_pct:.0f}% of payroll — a healthy distribution across teams.',
                'type': 'positive'
            })

    summary_text = (
        f"{metrics['total_employees']} employees across {metrics['departments']} departments. "
        f"Total payroll: ${metrics['total_payroll']:,.0f}. "
        f"Average cost per employee: ${metrics['avg_per_employee']:,.0f}."
    )

    return {
        'department_breakdown': department_breakdown,
        'top_employees': top_employees,
        'metrics': metrics,
        'insights': insights,
        'summary_text': summary_text
    }
