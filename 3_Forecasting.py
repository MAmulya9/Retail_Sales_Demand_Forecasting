import streamlit as st
import plotly.express as px
import pandas as pd
import io


from utils.model_loader import load_lgbm_models, load_exp_models
from utils.predictors import predict_lgbm, predict_exp
from utils.theme import apply_custom_theme
apply_custom_theme()

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(layout="wide")

st.markdown("## 🔮 Sales Forecasting")

st.caption(
    "Select a store and forecast sales using statistical and machine learning models."
)

# -------------------------------------------------
# Load data
# -------------------------------------------------
train = pd.read_csv("data/Train-Store.csv")
train["Date"] = pd.to_datetime(train["Date"])

test = pd.read_csv("data/Test-Store.csv")
test["Date"] = pd.to_datetime(test["Date"])

# -------------------------------------------------
# Load models (cached)
# -------------------------------------------------
@st.cache_resource
def load_models():
    return load_lgbm_models(), load_exp_models()

lgbm_models, exp_models = load_models()

# -------------------------------------------------
# Sidebar / Controls
# -------------------------------------------------
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        store = st.selectbox(
            "🏬 Select Store",
            sorted(test["Store"].unique())
        )

    with col2:
        mode = st.radio(
            "📅 Prediction Type",
            ["Single Date", "Date Range"],
            horizontal=True
        )

store_dates = sorted(
    test[test["Store"] == store]["Date"].unique()
)

if mode == "Single Date":
    selected_dates = [
        st.selectbox(
            "📆 Select Date",
            store_dates
        )
    ]
else:
    start, end = st.select_slider(
        "📆 Select Date Range",
        options=store_dates,
        value=(store_dates[0], store_dates[-1])
    )
    selected_dates = pd.date_range(start, end)

steps = len(selected_dates)

# -------------------------------------------------
# AUTO PREDICTION (NO BUTTON)
# -------------------------------------------------
with st.spinner("Generating forecasts..."):
    # Exponential Smoothing
    exp_preds = predict_exp(exp_models, store, steps)

    # LightGBM
    X_future = test[
        (test["Store"] == store) &
        (test["Date"].isin(selected_dates))
    ]
    lgbm_preds = predict_lgbm(lgbm_models, store, X_future)

# -------------------------------------------------
# Model switch buttons (tabs-style)
# -------------------------------------------------
model_tab = st.radio(
    "🔀 Select Model",
    ["Exponential Smoothing", "LightGBM"],
    horizontal=True
)

# -------------------------------------------------
# Display results
# -------------------------------------------------
if model_tab == "Exponential Smoothing":
    st.subheader("📈 Exponential Smoothing Forecast")

    result = pd.DataFrame({
        "Date": selected_dates,
        "Predicted Sales": exp_preds
    })

else:
    st.subheader("🌳 LightGBM Forecast")

    result = pd.DataFrame({
        "Date": selected_dates,
        "Predicted Sales": lgbm_preds
    })

# -------------------------------------------------
# Output
# -------------------------------------------------
st.dataframe(result, use_container_width=True)

if steps > 1:
    fig = px.line(
        result,
        x="Date",
        y="Predicted Sales",
        title=f"{model_tab} Forecast")

    st.plotly_chart(fig, use_container_width=True)
    
else:
    st.metric(
        "Predicted Sales",
        f"{result['Predicted Sales'].iloc[0]:,.0f}"
    )

# -----------------------------
# Download Forecast CSV
# -----------------------------
csv_buffer = io.StringIO()
result.to_csv(csv_buffer, index=False)

file_name = (
    f"forecast_store_{store}_"
    f"{model_tab.replace(' ', '_').lower()}_"
    f"{selected_dates[0].date()}_to_{selected_dates[-1].date()}.csv"
)

st.download_button(
    label="⬇️ Download Forecast CSV",
    data=csv_buffer.getvalue(),
    file_name=file_name,
    mime="text/csv"
)
