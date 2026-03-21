"""
Parser for Omega POS Sales Report CSV (REP_S_00001). Self-contained — no imports from other couqley skills.

Provides functions to parse Sales Report CSV format from Omega POS,
including CSV exports from Omega reports.
"""

import pandas as pd
import re
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


def parse_sales_csv(csv_path: str) -> pd.DataFrame:
    """
    Parse Omega POS Sales Report CSV (REP_S_00001 format).

    Simpler format than Menu Engineering:
    - Summary of sales by items
    - Columns: Description, Qty (Mode 1-4), Total Amount, %
    - Includes group and division headers

    Args:
        csv_path: Path to the sales CSV file

    Returns:
        DataFrame with columns:
        - item_name: Item description
        - quantity: Total quantity sold
        - total_amount: Total revenue
        - percentage: Percentage of category
        - group: Item group (e.g., Apero, Beers)
        - division: Division (e.g., Alcoholic Beverages)
    """
    df = pd.read_csv(csv_path, header=None, skipinitialspace=True, on_bad_lines='skip')

    # Find the header row
    header_row_idx = None
    for idx, row in df.iterrows():
        row_str = ','.join([str(val) for val in row.values if pd.notna(val)])
        if 'Description' in row_str and 'Total Amount' in row_str:
            header_row_idx = idx
            break

    if header_row_idx is None:
        raise ValueError("Could not find header row in sales CSV")

    clean_data = []
    current_group = None
    current_division = None

    for idx, row in df.iterrows():
        if idx <= header_row_idx:
            continue

        row_str = ' '.join([str(val) for val in row.values if pd.notna(val)])

        # Skip page breaks and metadata
        if 'Page' in row_str and 'of' in row_str:
            continue
        if 'To Date:' in row_str or 'From Date:' in row_str:
            continue
        if 'Copyright' in row_str or 'Omega Software' in row_str:
            continue

        # Detect division
        if 'Division:' in row_str:
            match = re.search(r'Division:\s*(.+)', row_str)
            if match:
                current_division = match.group(1).strip()
            continue

        # Detect group
        if 'Group:' in row_str:
            match = re.search(r'Group:\s*(.+)', row_str)
            if match:
                current_group = match.group(1).strip()
            continue

        # Skip branch and other metadata
        if 'Branch:' in row_str or 'Summary' in row_str:
            continue

        # Check if this is a data row
        item_name = row.iloc[0] if len(row) > 0 else None

        if pd.isna(item_name) or str(item_name).strip() == '':
            continue

        item_name_str = str(item_name).strip()

        # Skip headers and metadata
        if any(kw in item_name_str.lower() for kw in ['description', 'mode', 'total', 'qty']):
            continue

        try:
            # Description (column 0)
            description = item_name_str

            # Qty (column 1)
            quantity = safe_float(row.iloc[1] if len(row) > 1 else None)

            # Total Amount (skip Mode columns, usually at column 12-13)
            total_amount = None
            if len(row) > 12:
                total_amount = safe_float(row.iloc[12])

            # Percentage (last column)
            percentage = safe_float(row.iloc[-1] if len(row) > 0 else None)

            # Only add rows with valid quantity
            if quantity > 0 and total_amount is not None:
                clean_data.append({
                    'item_name': description,
                    'quantity': quantity,
                    'total_amount': total_amount,
                    'percentage': percentage,
                    'group': current_group,
                    'division': current_division
                })
        except (ValueError, IndexError):
            continue

    return pd.DataFrame(clean_data)


if __name__ == "__main__":
    print("Omega POS Sales Report Parser (REP_S_00001)")
    print("=" * 60)
    print("\nAvailable functions:")
    print("  - parse_sales_csv(csv_path): Parse Sales Report CSV")
    print("  - safe_float(val, default=0.0): Safe float conversion")
