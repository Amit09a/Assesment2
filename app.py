# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Title
st.title("📊 Stock Portfolio Analysis Dashboard")

# Load data
xirr_df = pd.read_csv("xirr_summary (1).csv")
portfolio_df = pd.read_csv("portfolio_value.csv")

# Format date
portfolio_df['Date'] = pd.to_datetime(portfolio_df['Date'])

# Show Portfolio Value Line Chart
st.subheader("📈 Daily Portfolio Value")
fig = px.line(portfolio_df, x='Date', y='Total', title="Portfolio Value Over Time")
st.plotly_chart(fig)

# Show XIRR per Symbol
st.subheader("📊 Per-Stock XIRR (%)")
xirr_df['XIRR (%)'] = (xirr_df['XIRR'] * 100).round(2)
fig2 = px.bar(xirr_df, x='Symbol', y='XIRR (%)', title="XIRR by Stock")
st.plotly_chart(fig2)

# Optional: View Raw Tables
with st.expander("🧾 View Raw Data"):
    st.write("Portfolio Value Table", portfolio_df.head(213))
    st.write("XIRR Summary", xirr_df.head(16))

# --- 📰 NewsAPI Integration ---
st.subheader("📰 Latest News on Your Stocks")

# Map symbols to company names
symbol_to_name = {
    "AAPL": "Apple",
    "GOOGL": "Google",
    "GOOG": "Alphabet",
    "MSFT": "Microsoft",
    "TSLA": "Tesla",
    "AMZN": "Amazon",
    "META": "Meta",
    "NFLX": "Netflix",
    "NVDA": "Nvidia",
    "ORCL": "Oracle",
    "SE": "Sea Limited",
    "AXP": "American Express",
    "IBIT": "Bitcoin ETF",
    "MARA": "Marathon Digital",
    "NU": "Nu Holdings",
    "SPY": "S&P 500 ETF",
    "NET": "Cloudflare",
    "C6L": "China Mobile"
}

# Your NewsAPI Key
NEWSAPI_KEY = "65a9d0c3d6c247d4844b903626753794"

# Function to fetch news
def get_news(company_name, api_key):
    url = f"https://newsapi.org/v2/everything?q={company_name}&sortBy=publishedAt&language=en&pageSize=5&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("articles", [])
    return []

# Get available symbols in xirr_df that have name mappings
available_symbols = list(set(xirr_df["Symbol"]).intersection(symbol_to_name.keys()))

if available_symbols:
    selected_symbol = st.selectbox("Select a stock to view recent news", sorted(available_symbols))

    if selected_symbol:
        company_name = symbol_to_name[selected_symbol]
        news_articles = get_news(company_name, NEWSAPI_KEY)

        if news_articles:
            for article in news_articles:
                st.markdown(f"**[{article['title']}]({article['url']})**")
                st.caption(f"🗞️ {article['source']['name']} | {article['publishedAt']}")
                st.write(article['description'])
                st.markdown("---")
        else:
            st.info("No recent news articles found.")
else:
    st.warning("No company name mappings found for the current stock symbols.")
