import pandas as pd

data = {
    "Region": ["North", "South", "East", "West", "North", "South", "East", "West"],
    "Sales": [2500, 1800, 2200, 2100, 2700, 2300, 1900, 2400],
    "Month": ["Jan", "Jan", "Jan", "Jan", "Feb", "Feb", "Feb", "Feb"],
}

df = pd.DataFrame(data)
print("Initial DataFrame:")
print(df, "\n")

summary = df.groupby("Region")["Sales"].agg(["sum", "mean"]).reset_index()
summary.rename(columns={"sum": "Total Sales", "mean": "Average Sales"}, inplace=True)
print("Sales Summary by Region:")
print(summary, "\n")

top_region = summary.loc[summary["Total Sales"].idxmax(), "Region"]
print(f"🏆 Top Region: {top_region}\n")

pivot = df.pivot_table(values="Sales", index="Region", columns="Month", aggfunc="sum")
print("Pivot Table (Sales by Region and Month):")
print(pivot, "\n")

pivot["Growth %"] = ((pivot["Feb"] - pivot["Jan"]) / pivot["Jan"] * 100).round(2)
print("With Growth Percentage:")
print(pivot)
