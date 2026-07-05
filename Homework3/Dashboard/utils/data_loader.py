import pandas as pd
import streamlit as st


@st.cache_data  # load and clean once, then reuse on every re-run
def load_data():
    """Load the two sources and return one clean, joined dataframe.

    The cleaning repeats the steps of section 2.1 of the notebook,
    keeping only what the dashboard needs: for every valid transaction,
    its date, type, symbol, sector, industry and company country.
    """

    # The account statement and the symbols file use ";" as separator and
    # start with an invisible character, so they are read with sep=";" and
    # encoding="utf-8-sig" (same options as in the notebook).
    transactions = pd.read_csv(
        "data/account-statement-1-1-2024-12-31-2024.csv",
        sep=";", encoding="utf-8-sig",
    )
    symbols = pd.read_csv("data/symbols.csv", sep=";", encoding="utf-8-sig")

    # Remove the fully empty rows and the empty trailing column.
    transactions = transactions.dropna(how="all")
    transactions = transactions[["Date", "TransactionType", "Symbol"]]

    # Fix the DIVIDENT typo (the charts use BUY/SELL only, but the label
    # is kept consistent with the notebook anyway).
    transactions["TransactionType"] = transactions["TransactionType"].replace(
        "DIVIDENT", "DIVIDEND"
    )

    # Keep only the transactions whose ticker exists in the master data
    # ("process valid data only", as in check 3 of the notebook).
    transactions = transactions[transactions["Symbol"].isin(symbols["symbol"])]

    # Parse the timestamps and keep the calendar day only.
    transactions["Date"] = pd.to_datetime(
        transactions["Date"], format="%d/%m/%Y %H:%M:%S"
    ).dt.normalize()

    # Join the transactions with the symbols master data to bring in
    # sector, industry and the company country.
    data = transactions.merge(
        symbols[["symbol", "sector", "industry", "country"]],
        left_on="Symbol", right_on="symbol",
    )

    # Keep only the columns used by the dashboard, with readable names.
    data = data[["Date", "TransactionType", "Symbol",
                 "sector", "industry", "country"]]
    data = data.rename(columns={"sector": "Sector",
                                "industry": "Industry",
                                "country": "Country"})
    return data


@st.cache_data
def load_country_list():
    """All the countries of the symbols master data.

    The selector of the Country page uses this full list (not only the
    countries that appear in the transactions): this way the "no
    transactions" message required by the assignment can actually show up.
    """
    symbols = pd.read_csv("data/symbols.csv", sep=";", encoding="utf-8-sig")
    return sorted(symbols["country"].unique())
