from pathlib import Path

import pandas as pd

def test_csv_file_exists():
    csv_path = Path("data/SaaS-Sales.csv")

    assert csv_path.is_file(), f"CSV file not found: {csv_path}"
    
def test_required_columns_exist():
    data = pd.read_csv("data/SaaS-Sales.csv")

    required_columns = {
        "Order ID",
        "Order Date",
        "Region",
        "Subregion",
        "Sales",
        "Profit",
    }

    missing_columns = required_columns - set(data.columns)

    assert not missing_columns, (
        f"Missing required columns: {missing_columns}"
    )