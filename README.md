# Kisan Mitra 🌾

Kisan Mitra is a machine learning project focused on agricultural mandi data analysis and crop price forecasting, with the goal of helping farmers make more informed market decisions.

## Objectives

- Analyze historical mandi prices across commodities and markets.
- Explore price trends, data quality, and missing values.
- Forecast crop modal prices using historical observations.
- Investigate potential selling-time and mandi-selection decision support.

## Current Progress

- Collected and explored historical mandi price data from 2021–2026.
- Performed data cleaning and exploratory data analysis using Pandas and NumPy.
- Developed an adaptive, gap-aware Simple Exponential Smoothing forecasting method.
- Evaluated the model against a last-observed-price baseline using chronological backtesting.
- Preparing a simple user interface to display forecasts and data freshness.

## Model Evaluation

For the Wheat series at Bhikangaon APMC, a chronological backtest of 340 recorded observations produced:

| Metric | Result |
|---|---:|
| Model MAE | ₹54.28 per quintal |
| Baseline MAE | ₹62.01 per quintal |
| MAE reduction | 12.46% |
| Test observations with lower model error | 53.82% |

These results apply to the tested series only. Performance may vary by commodity, mandi, and date. The backtest predicts the next recorded observation, which is not always the next calendar day.

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Jupyter Notebook
- Git and GitHub
- Streamlit (planned for the interface)

## Future Scope

- Weather and market-arrival analysis.
- Transport-adjusted mandi comparisons.
- More comprehensive evaluation across commodities and mandis.
- Farmer-focused decision support.

## Disclaimer

Forecasts are estimates based on historical data. They are not guarantees of future prices, profits, or the best time to sell. Users should consider current market conditions before making decisions.
