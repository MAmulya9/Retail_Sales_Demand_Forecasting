import streamlit as st

from utils.theme import apply_custom_theme
apply_custom_theme()

st.set_page_config(
    page_title="Rossmann Sales Forecasting",
    layout="wide"
)

st.title("📈 Rossmann Store Sales Forecasting System")

st.markdown("""
### Application Flow
1️⃣ Understand Rossmann store characteristics  
2️⃣ Explore historical sales patterns  
3️⃣ Forecast future sales using Time Series & ML models  

""")
