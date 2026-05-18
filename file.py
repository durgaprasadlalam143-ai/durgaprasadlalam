import streamlit as st
import pandas as pd
from datetime import date

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# -----------------------------------
# Session State
# -----------------------------------
if "transactions" not in st.session_state:
    st.session_state.transactions = []

# -----------------------------------
# Sidebar Navigation
# -----------------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    ["Home", "Add Transaction", "View Transactions", "Summary"]
)

# -----------------------------------
# Home Page
# -----------------------------------
if page == "Home":

    st.title("💰 Personal Expense Tracker")

    st.markdown("""
    ### Features
    - Add Income
    - Add Expenses
    - View Transactions
    - Financial Summary
    - Category-wise Expense Analysis
    """)

# -----------------------------------
# Add Transaction Page
# -----------------------------------
elif page == "Add Transaction":

    st.title("➕ Add Transaction")

    transaction_type = st.selectbox(
        "Transaction Type",
        ["Income", "Expense"]
    )

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        format="%.2f"
    )

    trans_date = st.date_input(
        "Date",
        value=date.today()
    )

    description = st.text_area("Description")

    # -----------------------------------
    # Income
    # -----------------------------------
    if transaction_type == "Income":

        source = st.text_input("Income Source")

        if st.button("Add Income"):

            if source and amount > 0:

                transaction = {
                    "type": "Income",
                    "category": source,
                    "amount": amount,
                    "date": str(trans_date),
                    "description": description
                }

                st.session_state.transactions.append(transaction)

                st.success("Income added successfully!")

            else:
                st.error("Please enter valid details.")

    # -----------------------------------
    # Expense
    # -----------------------------------
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

        if st.button("Add Expense"):

            if amount > 0:

                transaction = {
                    "type": "Expense",
                    "category": category,
                    "amount": amount,
                    "date": str(trans_date),
                    "description": description
                }

                st.session_state.transactions.append(transaction)

                st.success("Expense added successfully!")

            else:
                st.error("Amount must be greater than 0.")

# -----------------------------------
# View Transactions
# -----------------------------------
elif page == "View Transactions":

    st.title("📋 Transaction History")

    if st.session_state.transactions:

        df = pd.DataFrame(st.session_state.transactions)

        st.dataframe(
            df,
            use_container_width=True
        )

    else:
        st.warning("No transactions available.")

# -----------------------------------
# Summary Page
# -----------------------------------
elif page == "Summary":

    st.title("📊 Financial Summary")

    if st.session_state.transactions:

        df = pd.DataFrame(st.session_state.transactions)

        total_income = df[df["type"] == "Income"]["amount"].sum()

        total_expense = df[df["type"] == "Expense"]["amount"].sum()

        balance = total_income - total_expense

        # Metrics
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Income",
            f"₹ {total_income:.2f}"
        )

        col2.metric(
            "Total Expenses",
            f"₹ {total_expense:.2f}"
        )

        col3.metric(
            "Balance",
            f"₹ {balance:.2f}"
        )

        # Expense Summary
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
                "Total Spent"
            ]

            st.table(category_summary)

            st.bar_chart(
                category_summary.set_index("Category")
            )

        else:
            st.info("No expenses added yet.")

    else:
        st.warning("No transaction data available.")