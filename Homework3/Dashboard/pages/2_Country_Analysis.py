import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from utils.data_loader import load_data, load_country_list

# st.set_page_config must be the FIRST Streamlit call of the page.
st.set_page_config(page_title="Country Analysis", page_icon="🌍", layout="wide")

st.title("Country Analysis")

data = load_data()


def barh_chart(series, title, xlabel):
    """Horizontal bar chart with the largest value on top."""
    fig, ax = plt.subplots(figsize=(8, 3))
    series = series.sort_values(ascending=True)
    ax.barh(series.index, series.values)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    st.pyplot(fig)


# ------------------------------------------------------------
# Filter: country of the company associated with the traded stock.
# The list comes from the symbols master data (all 42 countries),
# so countries without any transaction can also be selected.
# ------------------------------------------------------------
countries = load_country_list()
country = st.selectbox("Country", countries)

# BUY + SELL transactions of the selected country
selected = data[
    (data["Country"] == country)
    & data["TransactionType"].isin(["BUY", "SELL"])
]

# The assignment asks for an explicit message when there is nothing to show.
if selected.empty:
    st.info(f"No transactions found for {country}.")
    st.stop()

# ------------------------------------------------------------
# Line chart: trend of total transactions (BUY + SELL) during 2024
# ------------------------------------------------------------
st.subheader(f"BUY + SELL transactions trend for {country} in 2024")

# Aggregated by month: for a single country the daily counts are sparse,
# so the monthly trend is much easier to read.
per_month = selected.groupby(selected["Date"].dt.to_period("M")).size()

# Reindex over ALL the months of 2024, filling the missing ones with 0:
# the line always covers the whole year, even for countries with very
# few transactions, and stays comparable across countries.
all_months = pd.period_range("2024-01", "2024-12", freq="M")
per_month = per_month.reindex(all_months, fill_value=0).rename("Transactions")
per_month.index = per_month.index.to_timestamp()

st.line_chart(per_month)

# ------------------------------------------------------------
# Bar charts: top industries by BUY and by SELL transactions
# ------------------------------------------------------------
st.subheader("Top industries")

left, right = st.columns(2)

with left:
    barh_chart(
        selected.loc[selected["TransactionType"] == "BUY", "Industry"]
        .value_counts().head(5),
        "Top industries by BUY transactions",
        "BUY transactions",
    )

with right:
    barh_chart(
        selected.loc[selected["TransactionType"] == "SELL", "Industry"]
        .value_counts().head(5),
        "Top industries by SELL transactions",
        "SELL transactions",
    )
