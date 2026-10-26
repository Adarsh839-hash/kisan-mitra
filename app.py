
import streamlit as st
import pandas as pd

from src.data_loader import load_mandi_data
from src.forecasting import predict_kisan_mitra

def navigate_to(page_name):
    st.session_state["navigation_page"] = page_name

st.set_page_config(
    page_title="Kisan Mitra",
    page_icon="🌾",
    layout="wide"
)



st.markdown("""
<style>
    /* Main page: warm cream */
    [data-testid="stAppViewContainer"] {
        background-color: #F7F5EA;
    }

    /* Sidebar: soft sage green */
    [data-testid="stSidebar"] {
        background-color: #E5EEDF;
    }

    /* Headings */
    h1, h2, h3 {
        color: #245A35 !important;
    }

    /* Statistic cards */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #D5E2D0;
        padding: 18px;
        border-radius: 14px;
    }

    /* Primary and ordinary buttons */
    .stApp button[kind="primary"],
    .stApp button[kind="secondary"],
    .stApp div.stButton > button {
        background-color: #28643B !important;
        color: #FFFFFF !important;
        border: 1px solid #28643B !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    /* Button hover */
    .stApp button[kind="primary"]:hover,
    .stApp button[kind="secondary"]:hover,
    .stApp div.stButton > button:hover {
        background-color: #1E4D2D !important;
        color: #FFFFFF !important;
        border-color: #1E4D2D !important;
    }

    /* Dropdown text */
    [data-testid="stSelectbox"] {
        background-color: transparent;
    }

    /* Page spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
</style>
""", unsafe_allow_html=True)


language = st.sidebar.selectbox(
    "🌐 Choose Language / भाषा चुनें",
    ["English", "हिंदी"]
)
st.title("🌾 Kisan Mitra")
st.subheader(
    "Agricultural Mandi Price Intelligence"
    if language == "English"
    else "कृषि मंडी भाव की जानकारी"
)

st.write(
    "Explore mandi prices and forecast crop prices."
    if language == "English"
    else "मंडी के भाव देखें और फसलों के भाव का अनुमान जानें।"
)

# Load the dataset.
@st.cache_data
def get_mandi_data():
    return load_mandi_data()

try:
    mandi_all, batch_data = get_mandi_data()
except Exception as error:
    st.error(f"Unable to load mandi data: {error}")
    st.stop()

st.sidebar.header("🌾 Kisan Mitra")


st.sidebar.divider()
st.sidebar.header("Navigation" if language == "English" else "नेविगेशन")

if language == "English":
    page_options = [
        "Home",
        "Price Forecast",
        "Historical Prices",
        "Compare Mandis",
        "Calculate Sale Value",
        "About",
    ]
else:
    page_options =[
        "होम",
        "फसल के भाव का अनुमान",
        "पुराने मंडी भाव",
        "मंडियों की तुलना",
        "फसल की बिक्री का मूल्य",
        "हमारे बारे में",
    ]

page = st.sidebar.selectbox(
    "Choose a page" if language == "English" else "पेज चुनें",
    page_options,
    key="navigation_page"
)

if page in ["Home", "होम"]:
    st.header(
        "Welcome to Kisan Mitra"
        if language == "English"
        else "किसान मित्र में आपका स्वागत है"
    )
    
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #E5EEDF, #F7F5EA);
            padding: 24px;
            border-radius: 16px;
            border-left: 6px solid #28643B;
            margin-bottom: 24px;
        ">
            <h3 style="margin-top: 0; color: #245A35;">
                Your crop, your market, your decision.
            </h3>
            <p style="font-size: 17px; color: #344A38; margin-bottom: 0;">
                Check recorded mandi prices, compare markets, and explore
                price estimates to help plan your crop sale.
            </p>
        </div>
        """
        if language == "English"
        else
        """
        <div style="
            background: linear-gradient(135deg, #E5EEDF, #F7F5EA);
            padding: 24px;
            border-radius: 16px;
            border-left: 6px solid #28643B;
            margin-bottom: 24px;
        ">
            <h3 style="margin-top: 0; color: #245A35;">
                आपकी फसल, आपकी मंडी, आपका फैसला।
            </h3>
            <p style="font-size: 17px; color: #344A38; margin-bottom: 0;">
                मंडी के दर्ज भाव देखें, मंडियों की तुलना करें और फसल बेचने
                की योजना बनाने के लिए अनुमानित भाव जानें।
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Records" if language == "English" else "कुल रिकॉर्ड",
        f"{len(mandi_all):,}"
    )

    col2.metric(
        "Commodities" if language == "English" else "फसलें",
        batch_data["commodity"].nunique()
    )

    col3.metric(
        "Markets" if language == "English" else "मंडियाँ",
        batch_data["market"].nunique()
    )

    st.info(
        
        "Select Price Forecast from the sidebar to explore a commodity and mandi."
        if language == "English"
        else "फसल और मंडी का भाव जानने के लिए साइडबार में 'फसल के भाव का अनुमान' चुनें।"
    )
    
    st.subheader(
        "What can you do here?"
        if language == "English"
        else "आप यहाँ क्या कर सकते हैं?"
    )

    card1, card2, card3 = st.columns(3)

    with card1:
        st.markdown(
            """
            <div style="background:white; padding:20px;
            border-radius:14px; border:1px solid #D5E2D0;
            min-height:170px;">
                <div style="font-size:30px;">🌾</div>
                <h3 style="color:#245A35;">Check Crop Prices</h3>
                <p style="color:#4D5D50;">
                    View recorded prices for your selected crop and mandi.
                </p>
            </div>
            """
            if language == "English"
            else
            """
            <div style="background:white; padding:20px;
            border-radius:14px; border:1px solid #D5E2D0;
            min-height:170px;">
                <div style="font-size:30px;">🌾</div>
                <h3 style="color:#245A35;">फसल के भाव देखें</h3>
                <p style="color:#4D5D50;">
                    अपनी चुनी हुई फसल और मंडी के दर्ज भाव देखें।
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with card2:
        st.markdown(
            """
            <div style="background:white; padding:20px;
            border-radius:14px; border:1px solid #D5E2D0;
            min-height:170px;">
                <div style="font-size:30px;">📍</div>
                <h3 style="color:#245A35;">Compare Mandis</h3>
                <p style="color:#4D5D50;">
                    Compare recorded prices for the same crop across markets.
                </p>
            </div>
            """
            if language == "English"
            else
            """
            <div style="background:white; padding:20px;
            border-radius:14px; border:1px solid #D5E2D0;
            min-height:170px;">
                <div style="font-size:30px;">📍</div>
                <h3 style="color:#245A35;">मंडियों की तुलना करें</h3>
                <p style="color:#4D5D50;">
                    एक ही फसल के अलग-अलग मंडियों में दर्ज भाव की तुलना करें।
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with card3:
        st.markdown(
            """
            <div style="background:white; padding:20px;
            border-radius:14px; border:1px solid #D5E2D0;
            min-height:170px;">
                <div style="font-size:30px;">🧮</div>
                <h3 style="color:#245A35;">Calculate Sale Value</h3>
                <p style="color:#4D5D50;">
                    Estimate gross sale value from your crop quantity and price.
                </p>
            </div>
            """
            if language == "English"
            else
            """
            <div style="background:white; padding:20px;
            border-radius:14px; border:1px solid #D5E2D0;
            min-height:170px;">
                <div style="font-size:30px;">🧮</div>
                <h3 style="color:#245A35;">फसल की कीमत का हिसाब</h3>
                <p style="color:#4D5D50;">
                    फसल की मात्रा और भाव से कुल बिक्री मूल्य का अनुमान लगाएँ।
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    

  
elif page in ["Price Forecast", "फसल के भाव का अनुमान"]:
    st.header(
        "Crop Price Forecast"
        if language == "English"
        else "फसल के भाव का अनुमान"
    )

    st.write(
        "Explore recorded prices and estimate the next price."
        if language == "English"
        else "दर्ज मंडी भाव देखें और अगले भाव का अनुमान जानें।"
    )

    # Select crop
    commodities = sorted(batch_data["commodity"].dropna().unique())

    commodity = st.selectbox(
        "Select commodity" if language == "English" else "फसल चुनें",
        commodities,
        key="forecast_commodity"
    )

    # Get districts where the selected crop is recorded
    crop_data = batch_data[
        batch_data["commodity"] == commodity
    ]

    available_districts = sorted(
        crop_data["district"].dropna().unique()
    )

    district = st.selectbox(
        "Select district" if language == "English" else "जिला चुनें",
        available_districts,
        key="forecast_district"
    )

    # Show only mandis in the selected district for that crop
    available_markets = sorted(
        crop_data.loc[
            crop_data["district"] == district, "market"
        ].dropna().unique()
    )

    market = st.selectbox(
        "Select mandi" if language == "English" else "मंडी चुनें",
        available_markets,
        key="forecast_market"
    )

    st.info(
    "Select a crop, district, and mandi, then generate the forecast below."
    if language == "English"
    else "फसल, जिला और मंडी चुनें, फिर नीचे भाव का अनुमान प्राप्त करें।"
)

    if st.button("Generate Forecast", type="primary"):
        result = predict_kisan_mitra(
            commodity=commodity,
            market=market,
            data=batch_data
        )

        if result["status"] == "success":
            st.success(f"Data freshness: {result['freshness']}")

            predicted_price = result["predicted_modal_price"]
            last_price = result["last_recorded_price"]

            price_change = predicted_price - last_price
            price_change_percent = (
                (price_change / last_price) * 100
                if last_price != 0
                else 0
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Predicted Modal Price" if language == "English" else "अनुमानित मॉडल भाव",
                f"₹{predicted_price:,.2f}/quintal"
                if language == "English"
                else f"₹{predicted_price:,.2f}/क्विंटल"
            )

            col2.metric(
                "Last Recorded Price" if language == "English" else "अंतिम दर्ज भाव",
                f"₹{last_price:,.2f}/quintal"
                if language == "English"
                else f"₹{last_price:,.2f}/क्विंटल"
            )

            col3.metric(
                "Expected Price Change" if language == "English" else "भाव में अनुमानित बदलाव",
                f"₹{price_change:+,.2f}",
                delta=f"{price_change_percent:+.2f}%"
            )
            date_col1, date_col2 = st.columns(2)

            date_col1.metric(
                "Last Price Recorded"
                if language == "English"
                else "अंतिम भाव दर्ज होने की तारीख",
                result["last_record_date"].strftime("%d %b %Y")
            )

            date_col2.metric(
                "Forecast Date"
                if language == "English"
                else "अनुमान की तारीख",
                result["target_date"].strftime("%d %b %Y")
            )
            # Explain how old the latest recorded data is
            data_age_days = result["data_age_days"]

            if language == "English":
                if data_age_days == 0:
                    st.info(
                        "Data notice: The latest recorded price is from today."
                    )
                elif data_age_days == 1:
                    st.info(
                        "Data notice: The latest recorded price is 1 day old. "
                        "The forecast targets the next day after the last recorded observation."
                    )
                else:
                    st.info(
                        f"Data notice: The latest recorded price is "
                        f"{data_age_days} days old. The forecast targets the next "
                        "day after the last recorded observation, not necessarily tomorrow."
                    )
            else:
                if data_age_days == 0:
                    st.info(
                        "डेटा सूचना: नवीनतम दर्ज भाव आज का है।"
                    )
                elif data_age_days == 1:
                    st.info(
                        "डेटा सूचना: नवीनतम दर्ज भाव 1 दिन पुराना है। "
                        "अनुमान अंतिम दर्ज रिकॉर्ड के अगले दिन के लिए है।"
                    )
                else:
                    st.info(
                        f"डेटा सूचना: नवीनतम दर्ज भाव {data_age_days} दिन पुराना है। "
                        "अनुमान अंतिम दर्ज रिकॉर्ड के अगले दिन के लिए है, "
                        "ज़रूरी नहीं कि वह कल का भाव हो।"
                    )

        else:
            st.warning(result["message"])
    st.subheader(
        "Historical Price Trend"
        if language == "English"
        else "पुराने भावों का रुझान"
    )

    chart_data = batch_data[
        (batch_data["commodity"] == commodity)
        & (batch_data["market"] == market)
    ].copy()

    chart_data["date"] = pd.to_datetime(
        chart_data["date"], errors="coerce"
    )
    chart_data["modal_price"] = pd.to_numeric(
        chart_data["modal_price"], errors="coerce"
    )

    chart_data = (
        chart_data.dropna(subset=["date", "modal_price"])
        .groupby("date", as_index=False)["modal_price"].mean()
        .sort_values("date")
        .tail(60)
    )

    if not chart_data.empty:
        st.line_chart(
            chart_data.set_index("date")["modal_price"],
            y_label=(
                "Modal Price (₹/quintal)"
                if language == "English"
                else "मॉडल भाव (₹/क्विंटल)"
            )
        )
        st.caption(
            "Showing up to the 60 most recent recorded dates for this selection."
            if language == "English"
            else "चुने गए विकल्पों के लिए अधिकतम 60 नवीनतम दर्ज तारीखें दिखाई गई हैं।"
        )
    else:
        st.info(
            "No historical prices are available for this selection."
            if language == "English"
            else "इस विकल्प के लिए पुराने भाव उपलब्ध नहीं हैं।"
        )


elif page in ["Historical Prices", "पुराने मंडी भाव"]:
    st.header("Historical Mandi Prices")

    commodities = sorted(
        batch_data["commodity"].dropna().unique()
    )

    commodity = st.selectbox(
        "Select commodity",
        commodities,
        key="history_commodity"
    )

    available_markets = sorted(
        batch_data.loc[
            batch_data["commodity"] == commodity, "market"
        ].dropna().unique()
    )

    market = st.selectbox(
        "Select mandi",
        available_markets,
        key="history_market"
    )

    history = batch_data.loc[
        (batch_data["commodity"] == commodity)
        & (batch_data["market"] == market),
        ["date", "modal_price"]
    ].dropna().sort_values("date")

    if history.empty:
        st.warning("No historical price records are available.")
    else:
        st.line_chart(
            history.set_index("date")["modal_price"],
            y_label="Modal price (₹ per quintal)",
            x_label="Date"
        )

        st.caption(
            f"Showing {len(history):,} recorded price observations."
        )
        st.subheader("Historical Price Records")

        st.dataframe(
            history.sort_values("date", ascending=False),
            use_container_width=True,
            hide_index=True
        )


elif page in ["Compare Mandis", "मंडियों की तुलना"]:
    st.header(
        "Compare Mandis"
        if language == "English"
        else "मंडियों की तुलना"
    )

    st.write(
        "Compare recorded crop prices across markets for a selected period."
        if language == "English"
        else "चुनी गई अवधि में अलग-अलग मंडियों के दर्ज फसल भावों की तुलना करें।"
    )

    # Prepare data
    compare_data = batch_data.copy()
    compare_data["date"] = pd.to_datetime(
        compare_data["date"], errors="coerce"
    )
    compare_data["modal_price"] = pd.to_numeric(
        compare_data["modal_price"], errors="coerce"
    )

    compare_data = compare_data.dropna(
        subset=["state", "district", "market", "commodity",
                "date", "modal_price"]
    )

    # State filter
    states = sorted(compare_data["state"].astype(str).unique())

    selected_state = st.selectbox(
        "Select state" if language == "English" else "राज्य चुनें",
        states,
        key="compare_state"
    )

    state_data = compare_data[
        compare_data["state"].astype(str) == selected_state
    ]

    # District filter
    districts = sorted(state_data["district"].astype(str).unique())

    selected_district = st.selectbox(
        "Select district" if language == "English" else "जिला चुनें",
        districts,
        key="compare_district"
    )

    district_data = state_data[
        state_data["district"].astype(str) == selected_district
    ]

    # Crop filter
    commodities = sorted(
        district_data["commodity"].astype(str).unique()
    )

    selected_commodity = st.selectbox(
        "Select crop" if language == "English" else "फसल चुनें",
        commodities,
        key="compare_commodity"
    )

    crop_data = district_data[
        district_data["commodity"].astype(str) == selected_commodity
    ]

    # Date filters
    min_date = crop_data["date"].min().date()
    max_date = crop_data["date"].max().date()

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "From date" if language == "English" else "शुरुआती तारीख",
            value=min_date,
            min_value=min_date,
            max_value=max_date,
            key="compare_start_date"
        )

    with col2:
        end_date = st.date_input(
            "To date" if language == "English" else "अंतिम तारीख",
            value=max_date,
            min_value=min_date,
            max_value=max_date,
            key="compare_end_date"
        )

    if start_date > end_date:
        st.error(
            "Start date must be on or before the end date."
            if language == "English"
            else "शुरुआती तारीख अंतिम तारीख से पहले या उसके बराबर होनी चाहिए।"
        )
    else:
        filtered_data = crop_data[
            (crop_data["date"].dt.date >= start_date)
            & (crop_data["date"].dt.date <= end_date)
        ].copy()

        if filtered_data.empty:
            st.warning(
                "No recorded prices were found for this selection."
                if language == "English"
                else "चुने गए विकल्पों और तारीखों के लिए कोई दर्ज भाव नहीं मिला।"
            )
        else:
            # Summarize recorded prices for each market
            market_summary = (
                filtered_data.groupby("market", as_index=False)
                .agg(
                    Average_Price=("modal_price", "mean"),
                    Highest_Price=("modal_price", "max"),
                    Lowest_Price=("modal_price", "min"),
                    Records=("modal_price", "count")
                )
                .sort_values("Average_Price", ascending=False)
            )
                        # Highlight the market with the highest average recorded price
            best_market = market_summary.iloc[0]

            st.subheader(
                "Best Recorded Average Price"
                if language == "English"
                else "सबसे अधिक औसत दर्ज भाव"
            )

            col1, col2 = st.columns(2)

            col1.metric(
                "Highest Average Price" if language == "English" else "सबसे अधिक औसत भाव",
                f"₹{best_market['Average_Price']:,.2f}/quintal"
                if language == "English"
                else f"₹{best_market['Average_Price']:,.2f}/क्विंटल"
            )

            col2.metric(
                "Market" if language == "English" else "मंडी",
                str(best_market["market"])
            )

            st.caption(
                "This market has the highest average recorded modal price among the markets in your current selection. It is not a guarantee of today's price."
                if language == "English"
                else "आपके चुने गए विकल्पों में इस मंडी का औसत दर्ज मॉडल भाव सबसे अधिक है। यह आज के भाव की गारंटी नहीं है।"
            )
            st.subheader(
                "Market price comparison"
                if language == "English"
                else "मंडी के भावों की तुलना"
            )

            st.caption(
                "Prices are based on recorded modal prices in the selected date range, not live prices."
                if language == "English"
                else "भाव चुनी गई तारीखों के दर्ज मॉडल भावों पर आधारित हैं, लाइव भाव नहीं हैं।"
            )

            market_summary = market_summary.rename(
                columns={
                    "market": "Market" if language == "English" else "मंडी",
                    "Average_Price": (
                        "Average Price (₹/quintal)"
                        if language == "English"
                        else "औसत भाव (₹/क्विंटल)"
                    ),
                    "Highest_Price": (
                        "Highest Price (₹/quintal)"
                        if language == "English"
                        else "सबसे अधिक भाव (₹/क्विंटल)"
                    ),
                    "Lowest_Price": (
                        "Lowest Price (₹/quintal)"
                        if language == "English"
                        else "सबसे कम भाव (₹/क्विंटल)"
                    ),
                    "Records": (
                        "Number of Records"
                        if language == "English"
                        else "रिकॉर्ड की संख्या"
                    )
                }
            )

            st.dataframe(
                market_summary.round(2),
                use_container_width=True,
                hide_index=True
            )

            st.subheader(
                "Average price by market"
                if language == "English"
                else "मंडी के अनुसार औसत भाव"
            )

            chart_data = market_summary.set_index(
                "Market" if language == "English" else "मंडी"
            )

            average_column = (
                "Average Price (₹/quintal)"
                if language == "English"
                else "औसत भाव (₹/क्विंटल)"
            )

            st.bar_chart(chart_data[average_column])


elif page == "Calculate Sale Value" or page == "फसल की बिक्री का मूल्य":
    st.title(
        "Calculate Sale Value"
        if language == "English"
        else "फसल की बिक्री का मूल्य"
    )

    st.write(
        "Estimate your crop's gross sale value."
        if language == "English"
        else "अपनी फसल की कुल बिक्री का अनुमान लगाएँ।"
    )

    price_method = st.radio(
        "Price Source" if language == "English" else "भाव का स्रोत",
        [
            "Recorded Mandi Price",
            "Manual Price",
        ]
        if language == "English"
        else [
            "मंडी में दर्ज भाव",
            "खुद भाव दर्ज करें",
        ],
    )

    quantity = st.number_input(
        "Quantity (quintals)" if language == "English" else "मात्रा (क्विंटल)",
        min_value=0.0,
        value=1.0,
        step=1.0,
    )

    selected_price = None

    if price_method in ["Recorded Mandi Price", "मंडी में दर्ज भाव"]:
        sale_crop = st.selectbox(
            "Select Crop" if language == "English" else "फसल चुनें",
            sorted(batch_data["commodity"].dropna().unique()),
            key="sale_crop",
        )

        crop_data = batch_data[
            batch_data["commodity"] == sale_crop
        ].copy()

        sale_district = st.selectbox(
            "Select District" if language == "English" else "जिला चुनें",
            sorted(crop_data["district"].dropna().unique()),
            key="sale_district",
        )

        district_data = crop_data[
            crop_data["district"] == sale_district
        ].copy()

        sale_market = st.selectbox(
            "Select Mandi" if language == "English" else "मंडी चुनें",
            sorted(district_data["market"].dropna().unique()),
            key="sale_market",
        )

        market_data = district_data[
            district_data["market"] == sale_market
        ].copy()

        market_data["date"] = pd.to_datetime(
            market_data["date"], errors="coerce"
        )
        market_data["modal_price"] = pd.to_numeric(
            market_data["modal_price"], errors="coerce"
        )

        market_data = market_data.dropna(
            subset=["date", "modal_price"]
        )

        if not market_data.empty:
            latest_row = market_data.loc[
                market_data["date"].idxmax()
            ]

            selected_price = float(latest_row["modal_price"])
            recorded_date = latest_row["date"]

            st.metric(
                "Latest Recorded Price" if language == "English"
                else "नवीनतम दर्ज भाव",
                f"₹{selected_price:,.2f}/quintal"
                if language == "English"
                else f"₹{selected_price:,.2f}/क्विंटल",
            )

            st.caption(
                f"Recorded on: {recorded_date:%d %b %Y}"
                if language == "English"
                else f"दर्ज तारीख: {recorded_date:%d %b %Y}"
            )
        else:
            st.warning(
                "No recorded price is available for this selection."
                if language == "English"
                else "इस चयन के लिए कोई दर्ज भाव उपलब्ध नहीं है।"
            )

    else:
        selected_price = st.number_input(
            "Price per quintal (₹)" if language == "English"
            else "प्रति क्विंटल भाव (₹)",
            min_value=0.0,
            value=2500.0,
            step=50.0,
            key="manual_sale_price",
        )

    if selected_price is not None:
        sale_value = quantity * selected_price

        st.divider()

        st.subheader(
            "Estimated Gross Sale Value"
            if language == "English"
            else "अनुमानित कुल बिक्री मूल्य"
        )

        st.metric(
            "Total Sale Value" if language == "English"
            else "कुल बिक्री मूल्य",
            f"₹{sale_value:,.2f}",
        )

        st.caption(
            "This is the gross value before transport, fees, commission, and other deductions."
            if language == "English"
            else "यह परिवहन, शुल्क, कमीशन और अन्य कटौतियों से पहले का कुल मूल्य है।"
        )

elif page in ["About", "हमारे बारे में"]:
    st.header("About Kisan Mitra")
    st.write(
        "Kisan Mitra is a student project focused on agricultural "
        "data analysis and price forecasting."
    )
