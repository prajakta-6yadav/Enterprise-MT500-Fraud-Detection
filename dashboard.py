import streamlit as st
import pandas as pd
import plotly.express as px
import glob
import plotly.graph_objects as go
import sqlite3
from datetime import datetime

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Enterprise MT500 Fraud Detection",
    page_icon="🛡️",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #020617;
    color: white;
}

.stMetric {
    background-color: #111827;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

div[data-testid="stSidebar"] {
    background-color: #111827;
}

h1, h2, h3 {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

csv_files = glob.glob(
    "Data/processed/*.csv"
)

df_list = []

for file in csv_files:

    temp_df = pd.read_csv(file)

    df_list.append(temp_df)

df = pd.concat(
    df_list,
    ignore_index=True
)

# --------------------------------------------------
# DATE CONVERSION
# --------------------------------------------------

df["trade_date"] = pd.to_datetime(
    df["trade_date"]
)

st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] {
        width: 260px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🔐 User Login")

role = st.sidebar.selectbox(

    "Select Role",

    [
        "ADMIN",
        "ANALYST",
        "AUDITOR"
    ]
)

st.sidebar.success(
    f"Logged in as: {role}"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title(
    "🛡️ Enterprise MT500 Fraud Detection Dashboard"
)

st.markdown("---")

# --------------------------------------------------
# KPI METRICS
# --------------------------------------------------

total_transactions = len(df)

fraud_transactions = int(
    df["fraud_flag"].sum()
)

high_risk_cases = len(

    df[df["risk_level"] == "HIGH"]
)

fraud_percentage = round(

    (fraud_transactions / total_transactions) * 100,

    2
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Transactions",
    total_transactions
)

col2.metric(
    "Fraud Transactions",
    fraud_transactions
)

col3.metric(
    "High Risk Cases",
    high_risk_cases
)

col4.metric(
    "Fraud %",
    f"{fraud_percentage}%"
)

# --------------------------------------------------
# LIVE ALERT
# --------------------------------------------------

if high_risk_cases > 0:

    st.error(
        f"🚨 {high_risk_cases} HIGH RISK transactions detected"
    )

# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.markdown("---")

st.subheader("🔎 Search & Filters")

fcol1, fcol2 = st.columns(2)

search_value = fcol1.text_input(
    "Search Transaction Reference"
)

risk_filter = fcol2.selectbox(

    "Risk Level",

    ["ALL"] +
    list(df["risk_level"].unique())
)

filtered_df = df.copy()

if search_value:

    filtered_df = filtered_df[

        filtered_df[
            "transaction_reference"
        ].astype(str).str.contains(

            search_value,
            case=False
        )
    ]

if risk_filter != "ALL":

    filtered_df = filtered_df[
        filtered_df["risk_level"]
        == risk_filter
    ]

st.markdown("---")

st.subheader("📊 Live Fraud Analytics")

# Risk Level Count
risk_chart = (
    filtered_df["risk_level"]
    .value_counts()
    .reset_index()
)

risk_chart.columns = [
    "Risk Level",
    "Count"
]

fig1 = px.bar(
    risk_chart,
    x="Risk Level",
    y="Count",
    color="Risk Level",
    title="Risk Level Distribution"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# Fraud Type Distribution
fraud_chart = (
    filtered_df["fraud_type"]
    .value_counts()
    .reset_index()
)

fraud_chart.columns = [
    "Fraud Type",
    "Count"
]

fig2 = px.pie(
    fraud_chart,
    names="Fraud Type",
    values="Count",
    title="Fraud Type Distribution"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)    

# --------------------------------------------------
# DATASET
# --------------------------------------------------

st.markdown("---")

st.subheader("📄 Transaction Dataset")

st.dataframe(

    filtered_df.head(100),

    use_container_width=True
)

# --------------------------------------------------
# FRAUD PIE CHART
# --------------------------------------------------

st.markdown("---")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:

    fraud_counts = (
        df["fraud_flag"]
        .value_counts()
    )

    pie_chart = px.pie(

        values=fraud_counts.values,

        names=["Safe", "Fraud"],

        hole=0.5,

        title="Fraud Distribution"
    )

    st.plotly_chart(
        pie_chart,
        use_container_width=True
    )

# --------------------------------------------------
# RISK LEVEL CHART
# --------------------------------------------------

with chart_col2:

    risk_chart = px.histogram(

        df,

        x="risk_level",

        color="risk_level",

        title="Risk Level Distribution"
    )

    st.plotly_chart(
        risk_chart,
        use_container_width=True
    )

# --------------------------------------------------
# FRAUD TYPE CHART
# --------------------------------------------------

st.markdown("---")

fraud_type_chart = px.histogram(

    df,

    x="fraud_type",

    color="fraud_type",

    title="Fraud Type Analysis"
)

st.plotly_chart(
    fraud_type_chart,
    use_container_width=True
)

# --------------------------------------------------
# BANK ANALYSIS
# --------------------------------------------------

st.markdown("---")

st.subheader("🏦 Bank-wise Fraud Analysis")

fraud_df = df[
    df["fraud_flag"] == 1
]

bank_chart = px.histogram(

    fraud_df,

    x="sender_bic",

    color="risk_level",

    title="Fraud Transactions by Bank"
)

st.plotly_chart(
    bank_chart,
    use_container_width=True
)

# --------------------------------------------------
# LIVE TRANSACTION MONITOR
# --------------------------------------------------

st.markdown("---")

st.subheader("📡 Live Transaction Monitor")

live_df = df.sort_values(
    by="trade_date",
    ascending=False
)

st.dataframe(

    live_df[[
        "transaction_reference",
        "sender_bic",
        "receiver_bic",
        "currency",
        "amount",
        "risk_level",
        "fraud_type"
    ]].head(25),

    use_container_width=True
)

# --------------------------------------------------
# TOP FRAUD CASES
# --------------------------------------------------

st.markdown("---")

st.subheader("🚨 Top Fraud Transactions")

st.dataframe(

    fraud_df.head(50),

    use_container_width=True
)

# --------------------------------------------------
# SAVE CASE
# --------------------------------------------------

st.markdown("---")

st.subheader("💾 Save Fraud Investigation")

fraud_refs = list(
    fraud_df["transaction_reference"]
)

selected_case = st.selectbox(

    "Select Fraud Case",

    fraud_refs
)

analyst_notes = st.text_area(
    "Analyst Notes"
)

if st.button("Save Investigation"):

    conn = sqlite3.connect(
        "fraud_cases.db"
    )

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS fraud_cases (

        transaction_reference TEXT,

        notes TEXT,

        timestamp TEXT

    )

    """)

    cursor.execute("""

    INSERT INTO fraud_cases VALUES (
        ?, ?, ?
    )

    """, (

        selected_case,

        analyst_notes,

        str(datetime.now())

    ))

    conn.commit()

    conn.close()

    st.success(
        "Case Saved Successfully"
    )

# --------------------------------------------------
# CASE HISTORY VIEWER
# --------------------------------------------------

st.markdown("---")

st.subheader("📁 Saved Investigation History")

try:

    conn = sqlite3.connect(
        "fraud_cases.db"
    )

    history_df = pd.read_sql_query(

        "SELECT * FROM fraud_cases",

        conn
    )

    conn.close()

    if len(history_df) > 0:

        st.dataframe(

            history_df,

            use_container_width=True
        )

    else:

        st.info(
            "No saved investigations found"
        )

except Exception as error:

    st.warning(
        f"History loading error: {error}"
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Enterprise MT500 Fraud Detection Platform"
)