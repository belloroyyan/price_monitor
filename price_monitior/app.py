# app.py
import streamlit as st
import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join("data", "tracker.db")

def load_data():
    """Connects to SQLite and loads all history into a Pandas DataFrame."""
    if not os.path.exists(DB_PATH):
        return pd.DataFrame() # Return empty DataFrame if DB doesn't exist yet
        
    with sqlite3.connect(DB_PATH) as conn:
        # Read SQL query straight into a clean Pandas DataFrame
        query = "SELECT product_name, price, is_in_stock, timestamp FROM price_history"
        df = pd.read_sql_query(query, conn)
        
        # Convert timestamp strings to actual datetime objects for accurate graphing
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df

# --- 1. Streamlit Web Page Configuration ---
st.set_page_config(page_title="Competitor Price Intelligence Dashboard", layout="wide")

st.title("📊 Competitor Price Intelligence Dashboard")
st.markdown("Real-time pricing data and inventory tracking extracted from competitor storefronts.")

# --- 2. Load Data ---
df = load_data()

if df.empty:
    st.warning("⚠️ No historical data found. Please run 'python main.py' first to collect data.")
else:
    # --- 3. Sidebar Filter ---
    st.sidebar.header("Filter Options")
    all_products = df['product_name'].unique()
    selected_product = st.sidebar.selectbox("Choose a product to analyze:", all_products)
    
    # Filter the DataFrame based on user selection
    filtered_df = df[df['product_name'] == selected_product].sort_values(by='timestamp')

    # --- 4. High-Level Metrics KPIs ---
    st.subheader(f"Current Metrics for: {selected_product}")
    
    # Get the latest entry for metrics
    latest_entry = filtered_df.iloc[-1]
    current_price = latest_entry['price']
    in_stock_status = "✅ In Stock" if latest_entry['is_in_stock'] == 1 else "❌ Out of Stock"
    
    # Calculate price change if there's history
    if len(filtered_df) > 1:
        previous_price = filtered_df.iloc[-2]['price']
        price_delta = round(current_price - previous_price, 2)
    else:
        price_delta = 0.0

    # Display clean visual cards
    col1, col2 = st.columns(2)
    col1.metric(label="Latest Monitored Price", value=f"£{current_price}", delta=f"{price_delta} £" if price_delta != 0 else None, delta_color="inverse")
    col2.metric(label="Stock Status", value=in_stock_status)

    # --- 5. Interactive Time-Series Chart ---
    st.subheader("📈 Historical Price Trend Over Time")
    
    # Streamlit natively renders highly interactive line charts
    st.line_chart(
        data=filtered_df, 
        x="timestamp", 
        y="price", 
        use_container_width=True
    )

    # --- 6. Raw Data Inspection ---
    st.subheader("📋 Raw Historical Log")
    st.dataframe(filtered_df, use_container_width=True)
