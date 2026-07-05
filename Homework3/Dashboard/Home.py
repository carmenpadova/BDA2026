import streamlit as st

# st.set_page_config must be the FIRST Streamlit call of the page.
st.set_page_config(
    page_title="Financial Transactions Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("Financial Transactions Dashboard")

st.write(
    """
This dashboard explores the 2024 transactions of a brokerage account,
built on the star schema designed in the Homework 3 notebook.

Use the sidebar to open the two pages:

- **Time Analysis** — transactions over time, with a date range filter;
- **Country Analysis** — transactions of a single country, chosen with a selector.
"""
)
