from datetime import date

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from utils.data_loader import load_data

# st.set_page_config must be the FIRST Streamlit call of the page.
st.set_page_config(page_title="Time Analysis", page_icon="📈", layout="wide")

st.title("Time Analysis")

data = load_data()


def barh_chart(series, title, xlabel):
    """Horizontal bar chart with the largest value on top."""
    fig, ax = plt.subplots(figsize=(8, 3))
    # sort ascending so that, after drawing, the longest bar ends up on top
    series = series.sort_values(ascending=True)
    ax.barh(series.index, series.values)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    st.pyplot(fig)


# ------------------------------------------------------------
# Filter: date range with the default values required
# by the assignment (01/01/2024 - 31/12/2024)
# ------------------------------------------------------------
picked = st.date_input(
    "Date range",
    value=(date(2024, 1, 1), date(2024, 12, 31)),
    min_value=date(2024, 1, 1),
    max_value=date(2024, 12, 31),
)

# While the user is still picking, date_input returns a single date:
# wait until the range is complete.
if not (isinstance(picked, tuple) and len(picked) == 2):
    st.stop()
start, end = picked

# All the charts of this page count BUY + SELL transactions,
# restricted to the selected date range.
mask = (
    data["TransactionType"].isin(["BUY", "SELL"])
    & (data["Date"] >= pd.Timestamp(start))
    & (data["Date"] <= pd.Timestamp(end))
)
selected = data[mask]

if selected.empty:
    st.info("No transactions in the selected date range.")
    st.stop()

# ------------------------------------------------------------
# Line chart: total transactions (BUY + SELL) over time
# ------------------------------------------------------------
st.subheader("BUY + SELL transactions over time")

# one point per day: how many BUY + SELL transactions happened that day
per_day = selected.groupby("Date").size().rename("Transactions")
st.line_chart(per_day)

# ------------------------------------------------------------
# Bar charts: top 3 symbols, top 5 sectors, top 5 industries
# ------------------------------------------------------------
st.subheader("Top rankings in the selected period")

barh_chart(
    selected["Symbol"].value_counts().head(3),
    "Top 3 traded symbols by transaction count",
    "Transactions",
)

barh_chart(
    selected["Sector"].value_counts().head(5),
    "Top 5 sectors by transaction count",
    "Transactions",
)

barh_chart(
    selected["Industry"].value_counts().head(5),
    "Top 5 industries by transaction count",
    "Transactions",
)
