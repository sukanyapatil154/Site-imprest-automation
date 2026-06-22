import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Site Imprest Validation Tool",
    layout="wide"
)

st.title("📋 Site Imprest Validation Tool")

uploaded_file = st.file_uploader(
    "Upload Site Imprest Excel File",
    type=["xlsx", "xlsm"]
)

if uploaded_file:

    try:

        # ==========================
        # Read Template Sheet
        # ==========================
        df = pd.read_excel(
            uploaded_file,
            sheet_name="Template",
            header=None
        )

        # ==========================
        # Helper Functions
        # ==========================

        def get_value_after_label(label):

            rows, cols = df.shape

            for r in range(rows):
                for c in range(cols):

                    value = df.iloc[r, c]

                    if pd.notna(value):

                        text = str(value).strip()

                        if text.lower().startswith(label.lower()):

                            # Handle labels written as:
                            # NAME: Abhishek G

                            if ":" in text:
                                parts = text.split(":", 1)

                                if len(parts) > 1:
                                    return parts[1].strip()

                            # Handle labels with value in next column
                            for nc in range(c + 1, min(c + 4, cols)):

                                next_value = df.iloc[r, nc]

                                if pd.notna(next_value):
                                    return str(next_value).strip()

            return ""

        # ==========================
        # Employee Details
        # ==========================

        project_name = get_value_after_label("Project Name:")
        employee_name = get_value_after_label("NAME:")
        employee_id = get_value_after_label("Emp ID:")
        site_name = get_value_after_label("Site Name:")

        account_number = get_value_after_label("Account number")
        ifsc = get_value_after_label("IFSC")
        email = get_value_after_label("Email")
        phone = get_value_after_label("Phone")

        advance_total = get_value_after_label("Advance Total")
        expenses_total = get_value_after_label("Expenses total")
        balance_on_hand = get_value_after_label("Balance on hand")

        st.success("✅ Template Sheet Extracted Successfully")

        # ==========================
        # Employee Details Display
        # ==========================

        st.subheader("📌 Employee & Site Details")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Project Name:** {project_name}")
            st.write(f"**Employee Name:** {employee_name}")
            st.write(f"**Employee ID:** {employee_id}")
            st.write(f"**Site Name:** {site_name}")

        with col2:
            st.write(f"**Email:** {email}")
            st.write(f"**Phone Number:** {phone}")
            st.write(f"**IFSC Code:** {ifsc}")
            st.write(f"**Account Number:** {account_number}")

        # ==========================
        # Financial Summary
        # ==========================

        st.subheader("💰 Financial Summary")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Advance Total", advance_total)

        with c2:
            st.metric("Expenses Total", expenses_total)

        with c3:
            st.metric("Balance On Hand", balance_on_hand)

        # ==========================
        # Expense Table Extraction
        # ==========================

        st.subheader("📊 Expense Details")

        rows, cols = df.shape

        header_row = None

        for r in range(rows):
            for c in range(cols):

                cell = df.iloc[r, c]

                if pd.notna(cell):

                    if str(cell).strip().lower() == "description of expenses":

                        header_row = r

                        desc_col = c
                        gl_col = c + 1
                        advance_col = c + 2
                        expense_col = c + 3
                        approval_col = c + 4

                        break

            if header_row is not None:
                break

        expense_data = []

        if header_row is not None:

            for r in range(header_row + 1, rows):

                description = df.iloc[r, desc_col]

                if pd.isna(description):
                    continue

                description = str(description).strip()

                # Stop reading when summary section starts
                if description.lower().startswith("opening balance"):
                    break

                total_expense = ""

                if expense_col < cols:
                    value = df.iloc[r, expense_col]

                    if pd.notna(value):
                        total_expense = value

                special_approval = ""

                if approval_col < cols:
                    value = df.iloc[r, approval_col]

                    if pd.notna(value):
                        special_approval = value

                expense_data.append(
                    {
                        "Description of Expenses": description,
                        "Total Expenses": total_expense,
                        "Special Approval": special_approval
                    }
                )

        expense_df = pd.DataFrame(expense_data)

        st.dataframe(
            expense_df,
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")
