
from pathlib import Path

import pandas as pd


# Find the project root from this file's location.
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_DIR / "data"


def load_mandi_data():
    """Load and standardize all yearly mandi CSV files."""

    cleaned_frames = []

    files = sorted(DATA_FOLDER.glob("mandi_*.csv"))

    if not files:
        raise FileNotFoundError(
            f"No mandi_*.csv files found in {DATA_FOLDER}"
        )

    for file in files:
        df = pd.read_csv(file, header=1)

        price_col = next(
            col for col in df.columns if "Modal Price" in col
        )
        arrival_col = next(
            col for col in df.columns if "Arrival Quantity" in col
        )

        df = df.rename(columns={
            "State/UT": "state",
            "District": "district",
            "Market": "market",
            "Commodity Group": "commodity_group",
            "Commodity": "commodity",
            "Date": "date",
            arrival_col: "arrival_quantity",
            "Arrival Unit": "arrival_unit",
            price_col: "modal_price",
            "Price Unit": "price_unit",
        })

        columns = [
            "state", "district", "market", "commodity_group",
            "commodity", "date", "arrival_quantity",
            "arrival_unit", "modal_price", "price_unit",
        ]

        df = df[columns].copy()

        df["date"] = pd.to_datetime(
            df["date"], errors="coerce", dayfirst=True
        )
        df["arrival_quantity"] = pd.to_numeric(
            df["arrival_quantity"], errors="coerce"
        )
        df["modal_price"] = pd.to_numeric(
            df["modal_price"], errors="coerce"
        )

        cleaned_frames.append(df)

    mandi_all = pd.concat(cleaned_frames, ignore_index=True)

    batch_data = mandi_all.copy()
    batch_data = batch_data.dropna(how="all").copy()
    batch_data = batch_data.dropna(
        subset=["commodity", "market", "date"]
    ).copy()

    return mandi_all, batch_data
