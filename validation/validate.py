# python -m venv .venv
# .venv/Scripts/activate
# pip install pandas
# python validation/validate.py

import logging
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(
            "output/validation_.result.log",
            mode="w",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

data = pd.read_csv('data/SaaS-Sales.csv')
# print(data.describe())

# Dataset validation checks
checks = {
    "No missing order IDs": data["Order ID"].notna().all(),
    "No invalid dates": data["Order Date"].notna().all(),
    "Sales is numeric": pd.api.types.is_numeric_dtype(data["Sales"]),
    "Quantity is positive": (data["Quantity"] > 0).all(),
    "No duplicate rows": not data.duplicated().any(),
    "Regions are valid": data["Region"].isin(
        ["AMER", "APJ", "EMEA"]
    ).all(),
}

logging.info("SALES DATA VALIDATION REPORT")
logging.info("=" * 40)

for check_name, passed in checks.items():
    result = "PASS" if passed else "FAIL"
    logging.info("%s: %s", result, check_name)

logging.info("=" * 40)


# check for missing values
# if data.isna().any().any():
#     print("Dataset check : Missing values found")
#     print(data.isna().sum())
# else:
#     print("Dataset check : No missing values found. \n")

print("Number of rows:", len(data))
logging.info("No. of Rows: %s", len(data))
print("Distinct orders:", data["Order ID"].nunique())
logging.info("Distinct orders: %s", data["Order ID"].nunique())

print("Total Sales : ", data['Sales'].sum().round(2))
logging.info("Total sales: %.2f", data["Sales"].sum())

print("Total Profit : ", data['Profit'].sum().round(2))
logging.info("Total profit: %.2f", data["Profit"].sum())

# Convert string to date
data["Order Date Parsed"] = pd.to_datetime(
    data["Order Date"],
    format="%m/%d/%Y",
    errors="coerce"
)

# Sales(sum) by month
monthly_sales = (
    data.groupby(data["Order Date Parsed"].dt.to_period("M"))["Sales"]
        .sum()
        .round(2)
)

print("Monthly Sales : ")
print(monthly_sales)
print("Minimum Monthly Sales : ", monthly_sales.idxmin(), f"$ {monthly_sales.min().round(2)}")
print("Maximum Monthly Sales : ", monthly_sales.idxmax(), f"$ {monthly_sales.max().round(2)}")
logging.info("Minimum monthly sales: %s, $%.2f", monthly_sales.idxmin(), monthly_sales.min())
logging.info("Maximum monthly sales: %s, $%.2f", monthly_sales.idxmax(), monthly_sales.max())
last_month = monthly_sales.index[-1]
last_month_sales = monthly_sales.iloc[-1]
print("Last month sales:", last_month, last_month_sales)
logging.info("Last month sales: %s, $%.2f", last_month, last_month_sales)

# Create a new column for quarter
# data["Quarter"] = data["Order Date Parsed"].dt.to_period("Q")

# Calculate total sales by quarter
quarterly_sales = (
    data.groupby(data["Order Date Parsed"].dt.to_period("Q"))["Sales"]
        .sum()
        .round(2)
        .reset_index()
)
print("\nQuarterly Sales : ")
print(quarterly_sales)
print("\nLast Quarter Sales : ", quarterly_sales.iloc[-1]["Sales"])
print("Second Last Quarter Sales : ", quarterly_sales.iloc[-2]["Sales"])
print(quarterly_sales.tail(2))
print("QoQ Growth : ", ((quarterly_sales.iloc[-1]["Sales"] - quarterly_sales.iloc[-2]["Sales"])))

# print(quarterly_sales)
this_quarter = quarterly_sales.iloc[-1]["Order Date Parsed"]
last_quarter = quarterly_sales.iloc[-2]["Order Date Parsed"]
print(last_quarter, f"$ {quarterly_sales.iloc[-2]['Sales'].round(2)}")
print(this_quarter, f"$ {quarterly_sales.iloc[-1]['Sales'].round(2)}")
logging.info("Last quarter sales: %s, $%.2f", last_quarter, quarterly_sales.iloc[-2]["Sales"])
logging.info("This quarter sales: %s, $%.2f", this_quarter, quarterly_sales.iloc[-1]["Sales"])
print("QoQ Growth : ", f"{this_quarter} vs {last_quarter} : ", ((quarterly_sales.iloc[-1]["Sales"] - quarterly_sales.iloc[-2]["Sales"])))
logging.info("QoQ Growth: %s vs %s: $%.2f", this_quarter, last_quarter, (quarterly_sales.iloc[-1]["Sales"] - quarterly_sales.iloc[-2]["Sales"]))

# print("Quarterly Sales : ")
# print(quarterly_sales.head())

# sales and profit by region 
region_results = (
    data.groupby("Region")
        .agg(
            Records=("Row ID", "count"),
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .round(2)
)

print(region_results)

data["Order Date Parsed"] = pd.to_datetime(
    data["Order Date"],
    format="%m/%d/%Y"
)

# sales and profit by region pivot table
data["Year"] = data["Order Date Parsed"].dt.year

regional_details = (
    pd.pivot_table(
        data,
        index=["Region", "Subregion"],
        columns="Year",
        values="Sales",
        aggfunc="sum",
        margins=False,
    )
.sort_index(axis=1, ascending=False)
.round(2)
)

print(regional_details)
logging.info("Regional details:\n%s", regional_details)

# regional_details = (
#     data.pivot_table(
#         index=["Region", "Subregion"],
#         columns="Year",
#         values="Sales",
#         aggfunc="sum"
#     )
#     .sort_index(axis=1, ascending=False)
#     .round(2)
# )

# print(regional_details)