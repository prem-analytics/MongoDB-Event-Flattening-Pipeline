import streamlit as st
import duckdb
import pandas as pd

# Import our processing modules to run them dynamically if needed
import ingest_nosql
import transform_nosql

st.set_page_config(page_title="NoSQL Event Flattening Engine", layout="wide")

st.title("🛰️ NoSQL Data Pipeline: MongoDB Event Flattening Engine")
st.markdown("Decompressing and transformation-modeling nested JSON application tracking streams into structured relational marts.")

db_filename = "unstructured_analytics.db"

# --- PRODUCTION DATA QUALITY & INITIALIZATION CHECK ---
db_conn = duckdb.connect(db_filename)

# Check what tables currently exist in the database instance
try:
    tables = [row[0] for row in db_conn.execute("SHOW TABLES").fetchall()]
except Exception:
    tables = []

if "fct_flattened_order_items" not in tables:
    with st.spinner("⏳ First-time setup: Initializing NoSQL mock layers and executing SQL UNNEST engines..."):
        # 1. Force run ingestion to land raw logs into staging
        ingest_nosql.generate_mock_mongodb_data()
        # 2. Force run transformation to flatten everything completely
        transform_nosql.flatten_unstructured_events()
    st.success("✅ Analytical marts successfully modeled on the cloud!")

# Read the modeled warehouse dataset safely
df_flat = db_conn.execute("SELECT * FROM fct_flattened_order_items").df()
db_conn.close()

# --- METRICS COMPILATION ---
total_orders = df_flat['event_id'].nunique()
total_gross_revenue = df_flat['total_item_revenue'].sum()
total_items_moved = df_flat['item_quantity'].sum()

st.subheader("📋 Executive Mart Overview")
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.metric(label="Total Unique Conversions", value=total_orders)
with m_col2:
    st.metric(label="Total Processed Gross Revenue", value=f"${total_gross_revenue:,.2f}")
with m_col3:
    st.metric(label="Total Individual Units Dispatched", value=total_items_moved)

st.markdown("---")

# --- VISUALIZATION BLOCK ---
v_col1, v_col2 = st.columns(2)

with v_col1:
    st.markdown("**Revenue Breakdown by Product Category**")
    category_chart = df_flat.groupby('item_category')['total_item_revenue'].sum().reset_index()
    st.bar_chart(data=category_chart, x='item_category', y='total_item_revenue', color='#FF4B4B')

with v_col2:
    st.markdown("**Device Type Distribution Matrix**")
    device_chart = df_flat.groupby('user_device')['event_id'].nunique().reset_index()
    st.area_chart(data=device_chart, x='user_device', y='event_id')

st.subheader("🗄️ Downstream Production Mart Preview (`fct_flattened_order_items`)")
st.dataframe(df_flat, use_container_width=True)