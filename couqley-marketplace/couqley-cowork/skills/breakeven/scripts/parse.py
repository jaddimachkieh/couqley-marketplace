"""
Parser for Omega POS Accounting Excel files.

Handles both raw Excel and pre-formatted accounting data.
Supports account mapping via the Mapping Sheet for proper IS Family classification.
Self-contained — no imports from other couqley skills.
"""

import pandas as pd
import openpyxl
import re
import logging
from pathlib import Path
from typing import Optional, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mapping sheet lives in plugin reference/ (resolved from script location)
# parse.py is at skills/breakeven/scripts/ -> 4 levels up to couqley-cowork/
_PLUGIN_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_MAPPING_PATH = _PLUGIN_ROOT / 'reference' / 'Mapping Sheet.xlsx'


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


def _clean_account_number(val) -> str:
    """Clean account number: remove _x000D_\\n artifacts, whitespace, convert to string."""
    if pd.isna(val):
        return ''
    s = str(val).strip()
    # Remove Excel XML artifacts
    s = re.sub(r'_x000D_\\n|_x000D_|\r|\n', '', s)
    # Remove trailing/leading whitespace again
    s = s.strip()
    return s


def load_account_mapping(mapping_path: Optional[str] = None) -> pd.DataFrame:
    """
    Load the account mapping sheet (Chart of Accounts).

    The mapping sheet classifies each account into:
    - Report type: BS (Balance Sheet) or IS (Income Statement)
    - IS Family: e.g., Food Sales, Beverage Cost, Staff Cost, etc.
    - BS Cat: Balance sheet category

    Args:
        mapping_path: Path to the Mapping Sheet Excel file.
                     Defaults to plugin's bundled reference/Mapping Sheet.xlsx

    Returns:
        DataFrame with columns: account_number, account_name, currency,
        report_type, is_family, bs_cat
    """
    if mapping_path is None:
        mapping_path = DEFAULT_MAPPING_PATH

    try:
        df = pd.read_excel(mapping_path, sheet_name='Chart')

        # Clean account numbers (remove _x000D_\n artifacts)
        df['account_number'] = df['Account #'].apply(_clean_account_number)

        # Clean account names
        df['account_name'] = df['Account Name'].apply(
            lambda x: re.sub(r'_x000D_\\n|_x000D_|\r|\n', '', str(x)).strip() if pd.notna(x) else ''
        )

        # Standardize output columns
        result = pd.DataFrame({
            'account_number': df['account_number'],
            'account_name': df['account_name'],
            'currency': df['CUR'].fillna(''),
            'report_type': df['Report'].fillna(''),
            'is_family': df['IS Family'].fillna(''),
            'bs_cat': df['BS Cat'].fillna('')
        })

        # Remove rows with empty account numbers
        result = result[result['account_number'] != '']

        logger.info(f"Loaded account mapping: {len(result)} accounts "
                    f"({len(result[result['report_type'] == 'IS'])} IS, "
                    f"{len(result[result['report_type'] == 'BS'])} BS)")

        return result

    except FileNotFoundError:
        logger.warning(f"Mapping sheet not found at: {mapping_path}")
        return pd.DataFrame(columns=[
            'account_number', 'account_name', 'currency',
            'report_type', 'is_family', 'bs_cat'
        ])
    except Exception as e:
        logger.warning(f"Error loading mapping sheet: {e}")
        return pd.DataFrame(columns=[
            'account_number', 'account_name', 'currency',
            'report_type', 'is_family', 'bs_cat'
        ])


def parse_excel_accounting(xlsx_path: str, mapping_path: Optional[str] = None) -> pd.DataFrame:
    """
    Parse Accounting Data Excel file with optional account mapping.

    Expected accounting format:
    - Headers already in row 0
    - Key columns: DATE, HISAB_NUMBER (account #), HISAB_NAME, M DOLLAR, D DOLLAR

    If a mapping sheet is provided (or found at default location), each transaction
    is enriched with report_type, is_family, and bs_cat from the Chart of Accounts.

    Args:
        xlsx_path: Path to the Accounting Excel file
        mapping_path: Optional path to Mapping Sheet. If None, tries default location.

    Returns:
        DataFrame with accounting data, cleaned, normalized, and optionally
        enriched with mapping classifications
    """
    try:
        df = pd.read_excel(xlsx_path, sheet_name=0)

        # Clean column names
        df.columns = [col.strip().upper() if isinstance(col, str) else f'col_{i}'
                      for i, col in enumerate(df.columns)]

        # Normalize currency columns
        currency_cols = [col for col in df.columns if 'DOLLAR' in col or 'AMOUNT' in col or 'PRICE' in col]
        for col in currency_cols:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: normalize_currency(str(x)) if isinstance(x, str) else x)

        # Clean date columns
        date_cols = [col for col in df.columns if 'DATE' in col]
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        # --- Account Mapping Integration ---
        # Find the account number column (HISAB_NUMBER or SAB_NUMBER or similar)
        acct_col = None
        for candidate in ['HISAB_NUMBER', 'SAB_NUMBER', 'SAB NUMBER', 'HISAB NUMBER']:
            if candidate in df.columns:
                acct_col = candidate
                break

        # Try to load mapping
        mapping_df = load_account_mapping(mapping_path)

        if acct_col and len(mapping_df) > 0:
            # Clean the account number column in the accounting data
            df['_acct_clean'] = df[acct_col].apply(_clean_account_number)

            # Merge with mapping
            df = df.merge(
                mapping_df[['account_number', 'report_type', 'is_family', 'bs_cat']],
                left_on='_acct_clean',
                right_on='account_number',
                how='left'
            )

            # Drop helper columns
            df = df.drop(columns=['_acct_clean', 'account_number'], errors='ignore')

            matched = df['is_family'].notna().sum()
            unmatched = df['is_family'].isna().sum()
            logger.info(f"Account mapping: {matched} matched, {unmatched} unmatched")

            # Fill unmatched with empty strings
            df['report_type'] = df['report_type'].fillna('')
            df['is_family'] = df['is_family'].fillna('')
            df['bs_cat'] = df['bs_cat'].fillna('')
        else:
            if len(mapping_df) == 0:
                logger.info("No mapping sheet available — transactions will use keyword classification")
            if acct_col is None:
                logger.info("No account number column found — cannot join mapping")

            df['report_type'] = ''
            df['is_family'] = ''
            df['bs_cat'] = ''

        logger.info(f"Parsed accounting data: {df.shape[0]} rows, {df.shape[1]} columns")
        return df

    except Exception as e:
        logger.error(f"Error parsing accounting Excel: {str(e)}")
        raise


def format_accounting_excel(xlsx_path: str, mapping_path: Optional[str] = None) -> pd.DataFrame:
    """
    Read and clean Accounting Excel file with optional mapping enrichment.

    This function:
    1. Reads the file normally
    2. Verifies expected columns (DATE, M DOLLAR)
    3. Standardizes column names to lowercase with underscores
    4. Parses DATE column to datetime
    5. Joins with account mapping if available
    6. Removes invalid rows

    Args:
        xlsx_path: Path to the Accounting Excel file
        mapping_path: Optional path to Mapping Sheet

    Returns:
        Cleaned DataFrame with standardized column names and mapping fields
    """
    try:
        # Read Excel file with default headers
        df = pd.read_excel(xlsx_path)

        logger.info(f"Loaded Accounting Excel file: {xlsx_path}")
        logger.info(f"Initial shape: {df.shape}, Columns: {df.columns.tolist()}")

        # Strip whitespace from column names
        df.columns = df.columns.str.strip()

        # Find account number column before renaming
        acct_col = None
        for candidate in ['HISAB_NUMBER', 'SAB_NUMBER', 'SAB NUMBER', 'HISAB NUMBER']:
            if candidate in df.columns:
                acct_col = candidate
                break

        # Verify expected columns
        expected_cols = ['DATE', 'M DOLLAR']
        found_cols = [col for col in expected_cols if col in df.columns]

        if len(found_cols) == 0:
            logger.warning(
                f"Expected columns {expected_cols} not found. Available: {df.columns.tolist()}"
            )

        # Standardize column names: UPPERCASE with SPACE -> lowercase with underscores
        new_columns = {}
        for col in df.columns:
            new_col = col.lower().replace(' ', '_')
            new_columns[col] = new_col

        # Track the renamed account column
        acct_col_lower = new_columns.get(acct_col, '') if acct_col else ''

        df = df.rename(columns=new_columns)

        logger.info(f"Standardized columns: {df.columns.tolist()}")

        # Parse DATE column to datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            invalid_dates = df['date'].isna().sum()
            if invalid_dates > 0:
                logger.warning(f"Found {invalid_dates} invalid dates")
                df = df.dropna(subset=['date'])

        # Ensure numeric columns are numeric
        numeric_cols = ['m_dollar', 'd_dollar', 'm_ll', 'd_ll', 'm_aj', 'd_aj']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # --- Account Mapping Integration ---
        mapping_df = load_account_mapping(mapping_path)

        if acct_col_lower and acct_col_lower in df.columns and len(mapping_df) > 0:
            df['_acct_clean'] = df[acct_col_lower].apply(_clean_account_number)

            df = df.merge(
                mapping_df[['account_number', 'report_type', 'is_family', 'bs_cat']],
                left_on='_acct_clean',
                right_on='account_number',
                how='left'
            )

            df = df.drop(columns=['_acct_clean', 'account_number'], errors='ignore')

            matched = df['is_family'].notna().sum()
            logger.info(f"Account mapping: {matched} transactions matched")

            df['report_type'] = df['report_type'].fillna('')
            df['is_family'] = df['is_family'].fillna('')
            df['bs_cat'] = df['bs_cat'].fillna('')
        else:
            df['report_type'] = ''
            df['is_family'] = ''
            df['bs_cat'] = ''

        # Remove completely empty rows
        df = df.dropna(how='all')

        logger.info(f"Final shape: {df.shape}")

        return df

    except FileNotFoundError:
        logger.error(f"File not found: {xlsx_path}")
        raise
    except Exception as e:
        logger.error(f"Error reading Accounting Excel file: {e}")
        raise
