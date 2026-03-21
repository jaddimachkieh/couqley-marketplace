"""
Parser for Omega POS Menu Engineering CSV reports (REP_S_00506).
Self-contained — no imports from other couqley skills.

Designed to handle CSV files exported from PDF reports, which often contain:
- Repeated headers on each page
- Page break markers (e.g., "Page 1 of 12")
- Footer information (copyright, URLs)
- HTML export artifacts
- Group headers and menu categories
"""

import pandas as pd
import re
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def safe_float(val, default=0.0) -> float:
    """
    Safely convert a value to float, handling commas, quotes, and other formatting.

    Args:
        val: Value to convert (can be float, string, None, etc.)
        default: Default value if conversion fails

    Returns:
        float: Converted value or default
    """
    if pd.isna(val):
        return default
    try:
        val_str = str(val).replace(',', '').replace('"', '').replace('%', '').strip()
        if not val_str or val_str == '':
            return default
        return float(val_str)
    except (ValueError, AttributeError):
        return default


def normalize_currency(value: str) -> float:
    """
    Clean currency values: remove $, commas, handle parentheses for negatives.

    Args:
        value: Currency value as string (e.g., "$1,234.56", "($100.00)")

    Returns:
        float: Numeric value
    """
    try:
        # Remove whitespace
        value = value.strip()

        # Handle empty or None values
        if not value or value.lower() == 'none':
            return 0.0

        # Check for parentheses indicating negative
        is_negative = value.startswith('(') and value.endswith(')')

        # Remove currency symbols and commas
        value = value.replace('$', '').replace(',', '').replace('(', '').replace(')', '')

        # Convert to float
        result = float(value)

        # Apply negative if indicated
        if is_negative:
            result = -result

        return result
    except (ValueError, AttributeError):
        logger.warning(f"Could not normalize currency value: {value}")
        return 0.0


def parse_menu_engineering_csv(csv_path: str) -> pd.DataFrame:
    """
    Parse Omega POS Menu Engineering CSV file into a clean DataFrame.

    Designed to handle CSV files exported from PDF reports, which often contain:
    - Repeated headers on each page
    - Page break markers (e.g., "Page 1 of 12")
    - Footer information (copyright, URLs)
    - HTML export artifacts
    - Group headers and menu categories

    Args:
        csv_path: Path to the CSV file (can be exported from PDF)

    Returns:
        DataFrame with columns:
        - menu_item: Menu item name
        - quantity: Quantity sold
        - popularity: Popularity percentage
        - item_cost: Cost per item
        - item_sell_price: Selling price per item
        - item_profit: Profit per item
        - total_cost: Total cost
        - total_revenue: Total revenue
        - total_profit: Total profit
        - profit_margin: Profit margin (High/Low)
        - popularity_level: Popularity level (High/Low)
        - category: Menu engineering category (Star/Challenge/Workhorse/Dog)
        - menu: Menu type (e.g., Tables)
        - group: Item group (e.g., Apero, Beers, Boeuf)
    """
    # Read the CSV file
    df = pd.read_csv(csv_path, header=None, skipinitialspace=True)

    # Find the header row (usually row 3, index 3)
    header_row_idx = None
    for idx, row in df.iterrows():
        row_str = ','.join([str(val) for val in row.values if pd.notna(val)])
        if 'Menu Item' in row_str and 'Qty' in row_str and 'Popularity' in row_str:
            header_row_idx = idx
            break

    if header_row_idx is None:
        raise ValueError("Could not find header row in CSV")

    # Read CSV again with proper header
    df = pd.read_csv(csv_path, skiprows=header_row_idx, header=0, skipinitialspace=True)

    # Clean column names - remove extra spaces and handle empty columns
    df.columns = [col.strip() if isinstance(col, str) else f'col_{i}' for i, col in enumerate(df.columns)]

    # Create a clean dataframe
    clean_data = []
    current_group = None

    for idx, row in df.iterrows():
        # Skip header rows, group rows, menu rows, and page breaks
        row_str = ' '.join([str(val) for val in row.values if pd.notna(val)])

        # Skip PDF export artifacts: page breaks, headers, footers
        if 'Page' in row_str and 'of' in row_str:
            continue

        if 'Year:' in row_str or 'Month:' in row_str:
            continue

        if 'Copyright' in row_str or 'Omega Software' in row_str:
            continue

        if 'www.omegapos.com' in row_str:
            continue

        # Skip HTML/PDF export errors
        if 'Error' in row_str or 'Cannot modify' in row_str or '<div' in row_str or '<footer' in row_str:
            continue

        # Skip empty rows or rows with only commas
        if not row_str.strip() or row_str.strip() == ',' * len(row_str.strip()):
            continue

        # Skip header repetition (PDF exports often repeat headers on each page)
        if 'Menu Item' in row_str and 'Qty' in row_str and 'Popularity' in row_str and idx > header_row_idx:
            continue

        if 'Group:' in row_str:
            # Extract group name
            match = re.search(r'Group:\s*(.+)', row_str)
            if match:
                current_group = match.group(1).strip()
            continue

        if 'Menu :' in row_str or 'Menu:' in row_str:
            continue

        if 'Category :' in row_str or 'Category:' in row_str:
            continue

        # Check if this is a data row (has a menu item name and numeric quantity)
        menu_item_val = row.iloc[0] if len(row) > 0 else None

        if pd.isna(menu_item_val) or str(menu_item_val).strip() == '':
            continue

        # Skip if menu item looks like a header or PDF artifact
        menu_item_lower = str(menu_item_val).lower()
        if any(keyword in menu_item_lower for keyword in [
            'menu item', 'category', 'restaurant menu', 'worksheet',
            'couqley gemayzeh', 'rep_s_', 'copyright', 'error occured'
        ]):
            continue

        # Skip rows that are just report metadata (like "REP_S_00506")
        if re.match(r'^REP_S_\d+$', str(menu_item_val).strip(), re.IGNORECASE):
            continue

        try:
            # Extract data using fixed positions
            menu_item = str(row.iloc[0]).strip() if len(row) > 0 else ''

            # Parse quantity (handle comma-separated numbers like "1,058.00")
            quantity = safe_float(row.iloc[1] if len(row) > 1 else None)

            # Parse popularity
            popularity = safe_float(row.iloc[2] if len(row) > 2 else None)

            # Item cost (column 4)
            item_cost = safe_float(row.iloc[4] if len(row) > 4 else None)

            # Item sell price (column 5)
            item_sell_price = safe_float(row.iloc[5] if len(row) > 5 else None)

            # Item profit (column 7)
            item_profit = safe_float(row.iloc[7] if len(row) > 7 else None)

            # Total cost (column 8)
            total_cost = safe_float(row.iloc[8] if len(row) > 8 else None)

            # Total revenue (column 9)
            total_revenue = safe_float(row.iloc[9] if len(row) > 9 else None)

            # Total profit (column 10)
            total_profit = safe_float(row.iloc[10] if len(row) > 10 else None)

            # Profit margin (column 12) - High/Low
            profit_margin = str(row.iloc[12]).strip() if len(row) > 12 else ''

            # Popularity level (column 13) - High/Low
            popularity_level = str(row.iloc[13]).strip() if len(row) > 13 else ''

            # Category (column 15) - Challenge/Star/Dog/Workhorse (skipping empty column 14)
            category = str(row.iloc[15]).strip() if len(row) > 15 else ''

            # Menu (column 17)
            menu = str(row.iloc[17]).strip() if len(row) > 17 else ''

            # Only add rows with valid category and non-empty menu item
            if (category in ['Challenge', 'Star', 'Dog', 'Workhorse'] and
                menu_item.strip() and
                not menu_item.strip().isdigit() and
                len(menu_item.strip()) > 1):
                clean_data.append({
                    'menu_item': menu_item,
                    'quantity': quantity,
                    'popularity': popularity,
                    'item_cost': item_cost,
                    'item_sell_price': item_sell_price,
                    'item_profit': item_profit,
                    'total_cost': total_cost,
                    'total_revenue': total_revenue,
                    'total_profit': total_profit,
                    'profit_margin': profit_margin,
                    'popularity_level': popularity_level,
                    'category': category,
                    'menu': menu,
                    'group': current_group
                })
        except (ValueError, IndexError):
            # Skip rows that can't be parsed
            continue

    result_df = pd.DataFrame(clean_data)

    # Calculate profit margin percentage if not already present and DataFrame is not empty
    if not result_df.empty and 'profit_margin_pct' not in result_df.columns:
        result_df['profit_margin_pct'] = (
            (result_df['item_profit'] / result_df['item_sell_price'] * 100)
            .where(result_df['item_sell_price'] > 0, 0)
            .round(2)
        )

    return result_df


if __name__ == "__main__":
    print("Omega POS Menu Engineering CSV Parser - Example Usage")
    print("=" * 60)
    print("\nAvailable functions:")
    print("  - parse_menu_engineering_csv(csv_path): Parse Menu Engineering CSV")
    print("\nUtility functions:")
    print("  - safe_float(val, default=0.0): Safe float conversion")
    print("  - normalize_currency(value): Clean currency values")
