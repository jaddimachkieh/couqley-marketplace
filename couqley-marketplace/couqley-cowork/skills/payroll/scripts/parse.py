"""
Parser for Omega POS Payroll Excel files.

Handles the specific Payroll Excel structure (headers at row 4).
Self-contained — no imports from other couqley skills.
"""

import pandas as pd
import openpyxl
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_excel_payroll(xlsx_path: str) -> pd.DataFrame:
    """
    Parse Payroll Data Excel file.

    Expected format:
    - Headers at row 4 (skipped)
    - Actual column names at row 6 (after row 4, index 1)
    - Data rows follow
    - Requires cleanup per create_formatted_files.py logic

    Args:
        xlsx_path: Path to the Payroll Excel file

    Returns:
        DataFrame with payroll data, properly formatted with headers in row 0
    """
    try:
        # Read with header at row 4
        df_raw = pd.read_excel(xlsx_path, header=4)

        # Extract actual column names from row 1 (index 1 of the raw dataframe)
        if len(df_raw) > 1 and df_raw.iloc[1, 2] == 'Name':
            column_names = df_raw.iloc[1].values
            df = df_raw.iloc[2:].copy()
            df.columns = column_names
            df = df.reset_index(drop=True)
        else:
            # Fallback: try first row
            first_row_vals = [str(v) for v in df_raw.iloc[0].values[:5]]
            if 'Name' in first_row_vals or 'SQ' in first_row_vals:
                column_names = df_raw.iloc[0].values
                df = df_raw.iloc[1:].copy()
                df.columns = column_names
                df = df.reset_index(drop=True)
            else:
                raise ValueError("Could not find proper header row in Payroll file")

        # Clean up: remove rows where Name or Department is missing
        if 'Name' in df.columns and 'Dep' in df.columns:
            df = df[df['Name'].notna() & df['Dep'].notna()]

        # Clean column names
        df.columns = [col.strip() if isinstance(col, str) else f'col_{i}'
                      for i, col in enumerate(df.columns)]

        logger.info(f"Parsed payroll data: {df.shape[0]} rows, {df.shape[1]} columns")
        return df

    except Exception as e:
        logger.error(f"Error parsing payroll Excel: {str(e)}")
        raise


def format_payroll_excel(xlsx_path: str) -> pd.DataFrame:
    """
    Read and clean Payroll Excel file.

    The Payroll Excel file has a specific structure with headers at row 4.
    This function:
    1. Reads the file starting at row 4
    2. Finds the actual column names by looking for 'Name' marker
    3. Skips to data rows after headers
    4. Cleans data by removing rows with missing Name or Dep

    Args:
        xlsx_path: Path to the Payroll Excel file

    Returns:
        Cleaned DataFrame with proper column headers
    """
    try:
        # Read Excel file with header at row 4 (index 4)
        df = pd.read_excel(xlsx_path, header=4)

        logger.info(f"Loaded Payroll Excel file: {xlsx_path}")
        logger.info(f"Initial shape: {df.shape}, Columns: {df.columns.tolist()}")

        # Clean: remove rows where Name or Dep is NaN
        initial_rows = len(df)

        if 'Name' in df.columns:
            df = df.dropna(subset=['Name'])
        if 'Dep' in df.columns:
            df = df.dropna(subset=['Dep'])

        removed_rows = initial_rows - len(df)
        if removed_rows > 0:
            logger.info(f"Removed {removed_rows} rows with missing Name or Dep")

        # Strip whitespace from column names
        df.columns = df.columns.str.strip()

        # Remove completely empty rows
        df = df.dropna(how='all')

        logger.info(f"Final shape: {df.shape}")

        return df

    except FileNotFoundError:
        logger.error(f"File not found: {xlsx_path}")
        raise
    except Exception as e:
        logger.error(f"Error reading Payroll Excel file: {e}")
        raise
