"""
Sales Analyzer for Couqley. Top items, group performance, slow movers, promotion candidates, insights. Self-contained — no imports from other couqley skills.

Works directly with DataFrames produced by parse.py:
  - Sales CSV: item_name, quantity, total_amount, percentage, group, division
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Column helpers — work with Sales CSV columns
# ---------------------------------------------------------------------------

def _name_col(df: pd.DataFrame) -> Optional[str]:
    """Return the item name column present in df."""
    for c in ['item_name']:
        if c in df.columns:
            return c
    return None


def _revenue_col(df: pd.DataFrame) -> Optional[str]:
    """Return the revenue column present in df."""
    for c in ['total_amount']:
        if c in df.columns:
            return c
    return None


def _qty_col(df: pd.DataFrame) -> Optional[str]:
    for c in ['quantity']:
        if c in df.columns:
            return c
    return None


def _group_col(df: pd.DataFrame) -> Optional[str]:
    for c in ['group']:
        if c in df.columns:
            return c
    return None


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def top_items(df: pd.DataFrame, n: int = 10, by: str = 'revenue') -> pd.DataFrame:
    """
    Return top N items by revenue or quantity.

    Args:
        df: Parsed Omega DataFrame (sales).
        n:  Number of top items.
        by: 'revenue' or 'quantity'.

    Returns:
        DataFrame sorted descending with rank and pct_of_total columns added.
    """
    if df.empty:
        return pd.DataFrame()

    if by == 'revenue':
        col = _revenue_col(df)
    else:
        col = _qty_col(df)

    if col is None:
        logger.error(f"Column for '{by}' not found")
        return pd.DataFrame()

    top = df.nlargest(n, col).copy()
    top['rank'] = range(1, len(top) + 1)
    top['pct_of_total'] = (top[col] / df[col].sum() * 100).round(2)
    return top


def slow_movers(df: pd.DataFrame, percentile: int = 25) -> pd.DataFrame:
    """Items below a given quantity-sold percentile — promotion candidates."""
    if df.empty:
        return pd.DataFrame()

    col = _qty_col(df)
    if col is None:
        return pd.DataFrame()

    threshold = df[col].quantile(percentile / 100)
    slow = df[df[col] <= threshold].copy()
    slow['performance_score'] = (slow[col] / df[col].max() * 100).round(2)
    return slow.sort_values(col)


def group_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Breakdown by Omega group (e.g., Apero, Beers, Boeuf, Cocktails…).

    Returns DataFrame with: total_revenue, total_quantity, item_count, avg_revenue_per_item,
    pct_of_total_revenue — sorted descending by revenue.
    """
    if df.empty:
        return pd.DataFrame()

    grp = _group_col(df)
    rev = _revenue_col(df)
    qty = _qty_col(df)
    name = _name_col(df)

    if not grp or not rev:
        logger.warning("Group or revenue column missing")
        return pd.DataFrame()

    agg = {}
    agg[rev] = 'sum'
    if qty:
        agg[qty] = 'sum'
    if name:
        agg[name] = 'count'

    result = df.groupby(grp).agg(agg).round(2)
    rename_map = {rev: 'total_revenue'}
    if qty:
        rename_map[qty] = 'total_quantity'
    if name:
        rename_map[name] = 'item_count'
    result.rename(columns=rename_map, inplace=True)

    if 'item_count' in result.columns and result['total_revenue'].sum() > 0:
        result['avg_revenue_per_item'] = (result['total_revenue'] / result['item_count']).round(2)

    result['pct_of_total_revenue'] = (result['total_revenue'] / result['total_revenue'].sum() * 100).round(2)
    return result.sort_values('total_revenue', ascending=False)


def revenue_metrics(df: pd.DataFrame) -> Dict:
    """
    Calculate key metrics: total_revenue, avg_item_revenue, total_items_sold,
    total_items_count, top_group.
    """
    metrics: Dict = {
        'total_revenue': 0.0,
        'avg_item_revenue': 0.0,
        'total_items_sold': 0,
        'unique_items': 0,
        'top_group': None,
    }
    if df.empty:
        return metrics

    rev = _revenue_col(df)
    qty = _qty_col(df)
    grp = _group_col(df)

    if rev:
        metrics['total_revenue'] = round(df[rev].sum(), 2)
    if qty:
        metrics['total_items_sold'] = int(df[qty].sum())

    metrics['unique_items'] = len(df)

    if rev and metrics['unique_items'] > 0:
        metrics['avg_item_revenue'] = round(metrics['total_revenue'] / metrics['unique_items'], 2)

    if grp and rev:
        group_rev = df.groupby(grp)[rev].sum()
        if not group_rev.empty:
            metrics['top_group'] = group_rev.idxmax()

    return metrics


def promotion_candidates(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """
    Identify items ideal for promotion: items with volume gaps and decent revenue.

    Adds a promotion_score column (0-100) combining revenue strength and volume gap.
    """
    if df.empty:
        return pd.DataFrame()

    qty = _qty_col(df)
    rev = _revenue_col(df)

    if not qty or not rev:
        return pd.DataFrame()

    candidates = df.copy()

    # Score components
    qty_max = candidates[qty].max() or 1
    rev_max = candidates[rev].max() or 1

    # Lower volume → higher score (room to grow)
    volume_gap = (1 - (candidates[qty] / qty_max)) * 50

    # Higher revenue per item → higher score (worth promoting)
    revenue_strength = (candidates[rev] / rev_max) * 50

    candidates['promotion_score'] = (volume_gap + revenue_strength).round(2)
    candidates = candidates.sort_values('promotion_score', ascending=False)

    return candidates.head(top_n)


def generate_insights(df: pd.DataFrame) -> List[Dict]:
    """
    Generate natural-language insights from parsed data.

    Returns list of dicts: {'title': str, 'insight': str, 'type': 'positive'|'warning'|'opportunity'}
    """
    insights: List[Dict] = []
    if df.empty:
        return insights

    rev = _revenue_col(df)
    qty = _qty_col(df)
    name = _name_col(df)

    # 1. Top performer
    if rev and name:
        top = df.nlargest(1, rev).iloc[0]
        insights.append({
            'title': 'Star Performer',
            'insight': f"{top[name]} leads revenue at ${top[rev]:,.0f}.",
            'type': 'positive',
        })

    # 2. Group concentration
    grp = _group_col(df)
    if grp and rev:
        group_rev = df.groupby(grp)[rev].sum().sort_values(ascending=False)
        if len(group_rev) >= 2:
            top_grp = group_rev.index[0]
            top_pct = (group_rev.iloc[0] / group_rev.sum() * 100)
            insights.append({
                'title': 'Revenue Concentration',
                'insight': f"{top_grp} accounts for {top_pct:.1f}% of total revenue.",
                'type': 'warning' if top_pct > 40 else 'positive',
            })

    # 3. Slow movers
    if qty:
        bottom_25 = df[df[qty] <= df[qty].quantile(0.25)]
        if len(bottom_25) > 0:
            insights.append({
                'title': 'Slow Movers',
                'insight': f"{len(bottom_25)} items in the bottom quartile by volume — consider promotions or removal.",
                'type': 'warning',
            })

    # 4. Menu diversity
    if name:
        insights.append({
            'title': 'Menu Diversity',
            'insight': f"{len(df)} unique items analyzed. More variety = better customer choice.",
            'type': 'positive',
        })

    return insights


# ---------------------------------------------------------------------------
# Utility: quick summary for chat responses
# ---------------------------------------------------------------------------

def quick_summary(df: pd.DataFrame) -> str:
    """
    Return a short natural-language summary suitable for dropping straight
    into a chat conversation.
    """
    if df.empty:
        return "No data to summarize."

    rev = _revenue_col(df)
    qty = _qty_col(df)
    name = _name_col(df)

    parts = []
    parts.append(f"**{len(df)} items** analyzed.")

    if rev:
        total = df[rev].sum()
        parts.append(f"Total revenue: **${total:,.0f}**.")

    if qty:
        total_qty = int(df[qty].sum())
        parts.append(f"Total units sold: **{total_qty:,}**.")

    if name and rev:
        top = df.nlargest(1, rev).iloc[0]
        parts.append(f"Top item: **{top[name]}** (${top[rev]:,.0f}).")

    return " ".join(parts)


if __name__ == "__main__":
    print("Couqley Sales Analyzer")
    print("=" * 50)
    print("\nCore functions:")
    print("  top_items(df, n=10, by='revenue')")
    print("  slow_movers(df, percentile=25)")
    print("  group_performance(df)")
    print("  revenue_metrics(df)")
    print("\nMarketing functions:")
    print("  promotion_candidates(df, 15)  — scored promo list")
    print("  generate_insights(df)         — natural-language insights")
    print("  quick_summary(df)             — one-liner for chat")
