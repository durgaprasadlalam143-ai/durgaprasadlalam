# expense_tracker.py

import streamlit as st
import pandas as pd
from datetime import date

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="Expense Tracker", layout="wide")

# -----------------------------
# Session State for Transactions
# -----------------------------
if "transactions" not in st.session_state:
    st.session_state.transactions = []

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Add Transaction", "View Transactions", "Summary"]
)

# -----------------------------
# Home Page
# -----------------------------
if page == "Home":

    st.title("💰 Personal Expense Tracker")

    st.write("""
    Welcome to the Personal Expense Tracker Application.

    This application helps users:
    - Add income details
    - Add expense details
    - View transaction history
    - Calculate total income
    - Calculate total expenses
    - Display remaining balance
    - View category-wise expense summary

    Built using Python and Streamlit.
    """)

# -----------------------------
# Add Transaction Page
# -----------------------------
elif page == "Add Transaction":

    st.title("➕ Add Transaction")

    transaction_type = st.selectbox(
        "Select Transaction Type",
        ["Income", "Expense"]
    )

    # -----------------------------
    # Income Form
    # -----------------------------
    if transaction_type == "Income":

        source = st.text_input("Income Source")
        amount = st.number_input("Amount", min_value=0.0)
        trans_date = st.date_input("Date", value=date.today())
        description = st.text_area("Description")

        if st.button("Add Income"):

            transaction = {
                "type": "Income",
                "category": source,
                "amount": amount,
                "date": str(trans_date),
                "description": description
            }

            st.session_state.transactions.append(transaction)

            st.success("Income added successfully!")

    # -----------------------------
    # Expense Form
    # -----------------------------
    else:

        category = st.selectbox(
            "Expense Category",
            [
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Education",
                "Medical",
                "Others"
            ]
        )

        amount = st.number_input("Amount", min_value=0.0)
        trans_date = st.date_input("Date", value=date.today())
        description = st.text_area("Description")

        if st.button("Add Expense"):

            transaction = {
                "type": "Expense",
                "category": category,
                "amount": amount,
                "date": str(trans_date),
                "description": description
            }

            st.session_state.transactions.append(transaction)

            st.success("Expense added successfully!")

# -----------------------------
# View Transactions Page
# -----------------------------
elif page == "View Transactions":

    st.title("📋 Transaction History")

    if st.session_state.transactions:

        df = pd.DataFrame(st.session_state.transactions)

        st.dataframe(df, use_container_width=True)

    else:
        st.warning("No transactions available.")

# -----------------------------
# Summary Page
# -----------------------------
elif page == "Summary":

    st.title("📊 Financial Summary")

    if st.session_state.transactions:

        df = pd.DataFrame(st.session_state.transactions)

        # Total Income
        total_income = df[df["type"] == "Income"]["amount"].sum()

        # Total Expense
        total_expense = df[df["type"] == "Expense"]["amount"].sum()

        # Balance
        balance = total_income - total_expense

        # Display Metrics
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Income", f"₹ {total_income}")
        col2.metric("Total Expenses", f"₹ {total_expense}")
        col3.metric("Balance", f"₹ {balance}")

        st.subheader("Category-wise Expense Summary")

        expense_df = df[df["type"] == "Expense"]

        if not expense_df.empty:

            category_summary = (
                expense_df.groupby("category")["amount"]
                .sum()
                .reset_index()
            )

            category_summary.columns = [
                "Category",
                "Total Spent (₹)"
            ]

            st.table(category_summary)

            # Bar Chart
            st.bar_chart(
                category_summary.set_index("Category")
            )

        else:
            st.info("No expenses added yet.")

    else:
        st.warning("No transaction data available.")