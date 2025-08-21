import pandas as pd
from config import EXCEL_FILE, REQUIRED_COLUMNS

def load_inventory_data():
    """Load and concatenate data from all sheets in the Excel file."""
    xls = pd.ExcelFile(EXCEL_FILE, engine='openpyxl')
    all_data = []
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        df.columns = [col.lower().strip() for col in df.columns]
        filtered = df[[col for col in df.columns if col in REQUIRED_COLUMNS]]
        all_data.append(filtered)
    return pd.concat(all_data, ignore_index=True).fillna('')

def apply_filters(data, factory_filter, location_filter, needle_filter):
    """Apply filtering based on factory, location, and needle ID."""
    filtered_data = data.copy()
    if factory_filter:
        filtered_data = filtered_data[filtered_data['factory'] == factory_filter]
    if location_filter:
        filtered_data = filtered_data[filtered_data['stock location'] == location_filter]
    if needle_filter:
        filtered_data = filtered_data[filtered_data['needle id'] == needle_filter]
    return filtered_data
