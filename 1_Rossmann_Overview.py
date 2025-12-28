import streamlit as st
import pandas as pd
import plotly.express as px
from utils.theme import apply_custom_theme

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(layout="wide")
apply_custom_theme()
st.markdown("# 🏬 Rossmann Store Overview")
st.caption(
    "High-level exploration of sales patterns across Store Types, Assortments, Time, Promotions, Customers, and Clusters."
)

# -------------------------------------------------
# Load data
# -------------------------------------------------
df = pd.read_csv("data/Train-Store.csv")
df["Date"] = pd.to_datetime(df["Date"])

# -------------------------------------------------
# KPI METRICS
# -------------------------------------------------
c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric("Total Stores", df["Store"].nunique())
c2.metric("Store Types", df["StoreType"].nunique())
c3.metric("Assortment Types", df["Assortment"].nunique())
c4.metric("Avg Daily Sales", f"{df['Sales'].mean():,.0f}")
c5.metric("Total Sales", f"{df['Sales'].sum()/1e9:.2f} B")
c6.metric("Clusters", df["Cluster_Name"].nunique())


st.divider()

# =================================================
# SECTION 1: STORE & ASSORTMENT ANALYSIS
# =================================================
st.subheader("📦 Store & Assortment Analysis")

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        df.groupby("StoreType")["Sales"].mean().reset_index(),
        x="StoreType",
        y="Sales",
        color="StoreType",
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="Average Sales by Store Type"
    )
    fig.update_layout(title_x=0.5, yaxis_title="Average Sales")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        df.groupby("Assortment")["Sales"].mean().reset_index(),
        x="Assortment",
        y="Sales",
        color="Assortment",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="Average Sales by Assortment Type"
    )
    fig.update_layout(title_x=0.5, yaxis_title="Average Sales")
    st.plotly_chart(fig, use_container_width=True)

# =================================================
# SECTION 2: TIME-BASED SALES PATTERNS
# =================================================
st.subheader("📅 Time-Based Sales Patterns")

col1, col2 = st.columns(2)

with col1:
    df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)

    monthly_total = (
        df.groupby("YearMonth")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly_total,
        x="YearMonth",
        y="Sales",
        title="Monthly Total Sales Trend"
    )

    fig.update_layout(
        xaxis_title="Year-Month",
        yaxis_title="Total Sales",
        title_x=0.5
    )

    st.plotly_chart(fig, use_container_width=True)


with col2:
    monthly_sales = df.groupby("Month")["Sales"].mean().reset_index()
    fig = px.bar(
        monthly_sales,
        x="Month",
        y="Sales",
        color="Month",
        title="Average Monthly Sales"
    )
    fig.update_layout(title_x=0.5, yaxis_title="Average Sales")
    st.plotly_chart(fig, use_container_width=True)

# =================================================
# SECTION 3: PROMOTION & CUSTOMER INSIGHTS
# =================================================
st.subheader("🎯 Promotion & Customer Insights")

col1, col2 = st.columns(2)

with col1:
    promo_sales = df.groupby("Promo")["Sales"].mean().reset_index()
    promo_sales["Promo"] = promo_sales["Promo"].map({0: "No Promo", 1: "Promo"})

    fig = px.bar(
        promo_sales,
        x="Promo",
        y="Sales",
        color="Promo",
        title="Impact of Promotion on Sales"
    )
    fig.update_layout(title_x=0.5, yaxis_title="Average Sales")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.scatter(
        df.sample(20000, random_state=42),
        x="Customers",
        y="Sales",
        color="Cluster_Name",
        title="Customers vs Sales (Cluster-wise)",
        opacity=0.6
    )
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

# =================================================
# SECTION 4: CLUSTER-BASED ANALYSIS
# =================================================
st.subheader("🧩 Cluster-Based Store Analysis")

col1, col2 = st.columns(2)

with col1:
    cluster_sales = (
    df.groupby("Cluster_Name")["Sales"]
    .sum()
    .reset_index()
)

    fig = px.pie(
        cluster_sales,
        values="Sales",
        names="Cluster_Name",
        hole=0.4,
        title="Sales Contribution by Cluster"
    )

    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)


with col2:
    cluster_sales = df.groupby("Cluster_Name")["Sales"].mean().reset_index()
    fig = px.bar(
        cluster_sales,
        x="Cluster_Name",
        y="Sales",
        color="Cluster_Name",
        title="Average Sales by Cluster"
    )
    fig.update_layout(title_x=0.5, yaxis_title="Average Sales")
    st.plotly_chart(fig, use_container_width=True)

# =================================================
# SECTION 5: TOP PERFORMING STORES
# =================================================

st.subheader("🏆 Top 10 Stores by Average Sales")

# ----------------------------------------
# Compute store-wise average sales
# ----------------------------------------
top_10_stores = (
    df.groupby("Store")["Sales"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# Convert Store to string so X-axis is categorical
top_10_stores["Store"] = top_10_stores["Store"].astype(str)




fig = px.bar(
    top_10_stores,
    x="Store",
    y="Sales",
    color="Store",
    color_discrete_sequence=px.colors.qualitative.Set3,
    title="Top 10 Stores by Average Sales"
)

fig.update_layout(
    xaxis_title="Store ID",
    yaxis_title="Average Sales",
    title_x=0.5,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)


