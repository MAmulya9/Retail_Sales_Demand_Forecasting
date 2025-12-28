import streamlit as st

def apply_custom_theme():

    # -------------------------------
    # Load clean readable font
    # -------------------------------
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        """,
        unsafe_allow_html=True
    )

    # -------------------------------
    # Dark Theme CSS
    # -------------------------------
    st.markdown(
        """
        <style>

        /* ===============================
           GLOBAL BACKGROUND
        =============================== */
        .stApp {
            background-color: #0E1117;
            color: #E5E7EB;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #E5E7EB;
        }

        /* ===============================
           SIDEBAR
        =============================== */
        section[data-testid="stSidebar"] {
            background-color: #161B22;
            border-right: 1px solid #30363D;
        }

        section[data-testid="stSidebar"] * {
            color: #F9FAFB !important;
        }

        /* ===============================
           HEADINGS & TEXT
        =============================== */
        h1 {
            color: #F9FAFB;
            font-weight: 700;
        }

        h2, h3 {
            color: #E5E7EB;
            font-weight: 600;
        }

        p, label, span {
            color: #D1D5DB;
        }

        /* ===============================
           METRIC CARDS (HIGH CONTRAST)
        =============================== */
        div[data-testid="metric-container"] {
            background-color: #161B22;
            border: 1px solid #30363D;
            border-radius: 14px;
            padding: 18px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.6);
        }

        /* Metric label */
        div[data-testid="metric-container"] label {
            color: #9CA3AF !important;
            font-size: 0.85rem;
        }

        /* Metric value */
        div[data-testid="metric-container"] div {
            color: #F9FAFB !important;
            font-size: 1.9rem;
            font-weight: 700;
        }

        /* ===============================
           INPUTS / SELECTBOXES
        =============================== */
        input, textarea, select {
            background-color: #0E1117 !important;
            color: #F9FAFB !important;
            border: 1px solid #30363D !important;
            border-radius: 8px;
        }

        /* ===============================
           BUTTONS
        =============================== */
        button[kind="primary"] {
            background: linear-gradient(135deg, #3B82F6, #6366F1);
            color: #FFFFFF;
            font-weight: 600;
            border-radius: 10px;
            border: none;
        }

        button[data-testid="baseButton-secondary"] {
            background-color: #161B22;
            color: #E5E7EB;
            border-radius: 10px;
            border: 1px solid #30363D;
        }

        /* ===============================
           DATAFRAMES
        =============================== */
        .stDataFrame {
            background-color: #161B22;
            border-radius: 12px;
            border: 1px solid #30363D;
        }

        .stDataFrame * {
            color: #E5E7EB !important;
        }

        thead tr th {
            background-color: #0E1117 !important;
            color: #F9FAFB !important;
        }

        tbody tr td {
            background-color: #161B22 !important;
            color: #E5E7EB !important;
        }

        /* ===============================
           PLOTLY CHART CONTAINER (FIXED)
        =============================== */
        div[data-testid="stPlotlyChart"] {
            background-color: #161B22;
            border-radius: 16px;
            border: 1px solid #30363D;
            box-shadow: 0 8px 22px rgba(0,0,0,0.7);
            overflow: hidden;   /* 🔥 prevents clipping */
        }

        </style>
        """,
        unsafe_allow_html=True
    )
