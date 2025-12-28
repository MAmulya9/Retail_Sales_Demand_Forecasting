import streamlit as st
import pandas as pd
import io
import plotly.express as px
from utils.theme import apply_custom_theme
apply_custom_theme()

st.title("📊 Store-wise Sales Explorer")

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("data/Train-Store.csv")
df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------
# Store selection
# -----------------------------
store = st.selectbox(
    "Select Store",
    sorted(df["Store"].unique())
)

# -----------------------------
# Date range selection
# -----------------------------
start, end = st.date_input(
    "Select Date Range",
    [df["Date"].min(), df["Date"].max()]
)

# -----------------------------
# Filter data
# -----------------------------
filt = df[
    (df["Store"] == store) &
    (df["Date"] >= pd.to_datetime(start)) &
    (df["Date"] <= pd.to_datetime(end))
]

# -----------------------------
# Plot: Year-wise colored sales trend
# -----------------------------
fig = px.line(
    filt,
    x="Date",
    y="Sales",
    color="Year",
    title=f"Actual Sales – Store {store}",
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig.update_layout(
    title_x=0.5,
    xaxis_title="Date",
    yaxis_title="Sales",
    plot_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Download CSV button
# -----------------------------
csv_buffer = io.StringIO()
filt.to_csv(csv_buffer, index=False)

st.download_button(
    label="⬇️ Download Store Data (CSV)",
    data=csv_buffer.getvalue(),
    file_name=f"store_{store}_sales_data.csv",
    mime="text/csv"
)

# -----------------------------
# Show recent records (optional)
# -----------------------------
st.dataframe(filt.tail(10), use_container_width=True)
