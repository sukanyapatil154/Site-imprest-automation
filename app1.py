import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Site Imprest Validator", layout="wide")

st.title("📋 Site Imprest Validation Tool")

uploaded_file = st.file_uploader(
    "Upload Site Imprest Excel File",
    type=["xlsx", "xlsm"]
)

if uploaded_file:

    try:
        # Read Template sheet
        df = pd.read_excel(
            uploaded_file,
            sheet_name="Template",
            header=None
        )

        def extract_value(pattern):
            """
            Search entire sheet and return value after ':'
            """
            for row in df.values:
                for cell in row:
                    if pd.notna(cell):
                        text = str(cell)

                        if pattern.lower() in text.lower():
                            if ":" in text:
                                return text.split(":", 1)[1].strip()

            return ""

        # Basic Information
        project_name = extract_value("Project Name")
        employee_name = extract_value("NAME")
        employee_id = extract_value("Emp ID")
        site_name = extract_value("Site Name")

        # Right side information
        account_number = str(df.iloc[3, 7]) if pd.notna(df.iloc[3, 7]) else ""
        ifsc = str(df.iloc[4, 7]) if pd.notna(df.iloc[4, 7]) else ""
        email = str(df.iloc[5, 7]) if pd.notna(df.iloc[5, 7]) else ""
        phone = str(df.iloc[6, 7]) if pd.notna(df.iloc[6, 7]) else ""

        # Financial Details
        advance_total = df.iloc[31, 4] if pd.notna(df.iloc[31, 4]) else 0
        expenses_total = df.iloc[32, 5] if pd.notna(df.iloc[32, 5]) else 0
        balance_on_hand = df.iloc[33, 5] if pd.notna(df.iloc[33, 5]) else 0

        st.success("Template Sheet Extracted Successfully")

        st.subheader("📌 Employee & Site Details")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Project Name:**", project_name)
            st.write("**Employee Name:**", employee_name)
            st.write("**Employee ID:**", employee_id)
            st.write("**Site Name:**", site_name)

        with col2:
            st.write("**Email:**", email)
            st.write("**Phone Number:**", phone)
            st.write("**IFSC:**", ifsc)
            st.write("**Account Number:**", account_number)

        st.subheader("💰 Financial Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Advance Total", f"₹ {advance_total:,.2f}")

        with col2:
            st.metric("Expenses Total", f"₹ {expenses_total:,.2f}")

        with col3:
            st.metric("Balance On Hand", f"₹ {balance_on_hand:,.2f}")

    except Exception as e:
        st.error(f"Error reading file: {e}")
