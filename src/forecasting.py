
import numpy as np
import pandas as pd


def forecast_series(history, forecast_date):
    forecast_date = pd.to_datetime(forecast_date)

    known = (
        history.loc[
            history["date"] <= forecast_date,
            ["date", "modal_price"]
        ]
        .dropna(subset=["modal_price"])
        .sort_values("date")
    )

    if known.empty:
        return {
            "predicted_modal_price": np.nan,
            "history_count": 0,
            "last_record_date": pd.NaT,
            "days_since_last_record": np.nan,
            "base_alpha": np.nan
        }

    known = known.drop_duplicates("date", keep="last")
    prices = known["modal_price"].astype(float)

    recent_prices = prices.tail(3)
    volatility = (
        recent_prices.pct_change().abs().mean()
        if len(recent_prices) >= 2
        else 0.0
    )

    alpha = 0.15 + min(float(volatility) / 0.50, 1.0) * 0.15
    alpha = float(np.clip(alpha, 0.15, 0.30))

    level = float(prices.iloc[0])
    previous_date = known["date"].iloc[0]

    for i in range(1, len(known)):
        current_date = known["date"].iloc[i]
        current_price = float(prices.iloc[i])

        gap_days = max((current_date - previous_date).days, 1)
        effective_alpha = min(1 - (1 - alpha) ** gap_days, 0.64)

        level = (
            effective_alpha * current_price
            + (1 - effective_alpha) * level
        )

        previous_date = current_date

    last_record_date = known["date"].iloc[-1]

    return {
        "predicted_modal_price": round(level, 2),
        "history_count": len(known),
        "last_record_date": last_record_date,
        "days_since_last_record": (
            forecast_date - last_record_date
        ).days,
        "base_alpha": round(alpha, 4)
    }


def predict_kisan_mitra(commodity, market, data):
    # Select the requested commodity and mandi.
    history = data.loc[
        (data["commodity"] == commodity)
        & (data["market"] == market),
        ["date", "modal_price"]
    ].dropna(subset=["date", "modal_price"])

    history = (
        history.sort_values("date")
        .drop_duplicates("date", keep="last")
        .reset_index(drop=True)
    )

    if len(history) < 60:
        return {
            "status": "insufficient_data",
            "message": "At least 60 recorded prices are required."
        }

    last_date = history["date"].max()

    last_price = float(
        history.loc[
            history["date"] == last_date, "modal_price"
        ].iloc[-1]
    )

    forecast = forecast_series(
        history=history,
        forecast_date=last_date
    )

    reference_date = data["date"].max()
    today = pd.Timestamp.now().normalize()
    last_date_normalized = pd.Timestamp(last_date).normalize()

    data_age_days = max(
        0,
        (today - last_date_normalized).days
    )
    print("DEBUG today:", today)
    print("DEBUG last_date:", last_date)
    print("DEBUG data_age_days:", data_age_days)

    if data_age_days > 30:
        return {
            "status": "stale_data",
            "commodity": commodity,
            "market": market,
            "last_record_date": last_date,
            "data_age_days": data_age_days,
            "message": (
                "Latest mandi data is over 30 days old. "
                "A current prediction cannot be shown reliably."
            )
        }

    if data_age_days <= 3:
        freshness = "Fresh"
    elif data_age_days <= 14:
        freshness = "Moderately stale"
    else:
        freshness = "Stale"

    return {
        "status": "success",
        "commodity": commodity,
        "market": market,
        "last_record_date": last_date,
        "target_date": last_date + pd.Timedelta(days=1),
        "last_recorded_price": round(last_price, 2),
        "predicted_modal_price": forecast["predicted_modal_price"],
        "history_count": len(history),
        "data_age_days": data_age_days,
        "freshness": freshness
    }
