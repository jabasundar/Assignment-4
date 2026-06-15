import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Telangana PDS Analytics",
    layout="wide"
)

st.title("📊 Telangana PDS Analytics Dashboard")
st.markdown("Cluster Analysis & FPS Shop Performance Monitoring")

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/clustered_pds_data.csv")
    return df

df = load_data()

# =====================================================
# SIDEBAR FILTERS
# =====================================================
st.sidebar.header("Filters")

cluster_filter = st.sidebar.multiselect(
    "Select Cluster",
    options=sorted(df["cluster"].unique()),
    default=sorted(df["cluster"].unique())
)

df_filtered = df[df["cluster"].isin(cluster_filter)]

# =====================================================
# KPI SECTION
# =====================================================
total_shops = df_filtered["shopno"].nunique()
avg_trans = int(df_filtered["nooftrans"].mean())
avg_rcs = int(df_filtered["noofrcs"].mean())
avg_util = round(df_filtered["utilization_ratio"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Shops", total_shops)
col2.metric("Avg Transactions", avg_trans)
col3.metric("Avg Ration Cards", avg_rcs)
col4.metric("Avg Utilization Ratio", avg_util)

st.divider()

# =====================================================
# PCA CLUSTER VISUALIZATION
# =====================================================
st.subheader("📌 PCA Cluster Visualization")

fig = px.scatter(
    df_filtered,
    x="pca1",
    y="pca2",
    color="cluster",
    hover_data=["shopno", "nooftrans", "noofrcs"],
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# =====================================================
# CLUSTER DISTRIBUTION
# =====================================================
st.subheader("📌 Cluster Distribution")

cluster_count = (
    df_filtered["cluster"]
    .value_counts()
    .reset_index()
)

cluster_count.columns = ["Cluster", "Count"]

fig2 = px.bar(
    cluster_count,
    x="Cluster",
    y="Count",
    text_auto=True,
    height=500
)

st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# UTILIZATION RATIO DISTRIBUTION
# =====================================================
st.subheader("📌 Utilization Ratio Distribution")

fig3 = px.histogram(
    df_filtered,
    x="utilization_ratio",
    nbins=50,
    height=500
)

st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# SHOP SEARCH TOOL
# =====================================================
st.subheader("🔍 Search Shop Performance")

shop_search = st.text_input("Enter Shop Number")

if shop_search:
    result = df_filtered[
        df_filtered["shopno"].astype(str) == shop_search
    ]

    if not result.empty:
        st.success("Shop Found")
        st.dataframe(result)
    else:
        st.error("Shop Not Found")

# =====================================================
# RAW DATA
# =====================================================
st.subheader("📄 Clustered Dataset Preview")

st.dataframe(df_filtered.head(100))

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.markdown("Developed using Streamlit | Telangana PDS Analytics Project")