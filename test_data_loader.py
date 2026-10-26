
from src.data_loader import load_mandi_data

mandi_all, batch_data = load_mandi_data()

print("All rows:", len(mandi_all))
print("Forecasting rows:", len(batch_data))
print("Date range:", batch_data["date"].min(), "to", batch_data["date"].max())
print("Commodities:", batch_data["commodity"].nunique())
print("Markets:", batch_data["market"].nunique())
print("Missing modal prices:", batch_data["modal_price"].isna().sum())
