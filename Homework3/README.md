# Homework 3 - Financial Transactions

This repository contains a star schema model and an interactive dashboard for the analysis of financial transactions from a securities account in 2024.

## Repository Contents

- `Homework3_FinancialTransactions.ipynb` - Jupyter notebook containing the ETL process, star schema construction, and analytical queries for Parts 1 and 2.
- `Datasets/` - Original CSV input files used in the notebook.
- `images/` - Star schema and fact schema diagrams.
- `Dashboard/` - Streamlit application for the interactive dashboard in Part 3.
- `Dashboard.zip` - Zipped version of the Streamlit dashboard.
- `Report.pdf` - Short report describing modeling choices, data quality considerations, and main results.

## How to Run the Dashboard

Open the terminal and move into the `Dashboard/` folder:

```bash
cd /path/to/Dashboard
python3 -m pip install -r requirements.txt
streamlit run Home.py
```

On macOS, you can type `cd ` and then drag the `Dashboard` folder into the terminal. This automatically inserts the correct full path.

Example:

```bash
cd /Users/your-name/Desktop/Dashboard
python3 -m pip install -r requirements.txt
streamlit run Home.py
```

The dashboard will open in the browser and provides interactive views for:

- portfolio and transaction overview;
- time-based analysis;
- country-based analysis.

## Data

The project uses three CSV files:

- `account-statement-1-1-2024-12-31-2024.csv` - transaction data for 2024;
- `symbols.csv` - financial instrument information;
- `country.csv` - country reference data.

The dashboard includes its own `data/` folder so that it can be run independently from the notebook.

## Notes

The notebook should be executed first if you want to inspect the full ETL and analytical workflow. The Streamlit dashboard can be launched separately using the instructions above.
