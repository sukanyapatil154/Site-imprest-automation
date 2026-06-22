import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Site Imprest Validator",
    layout="wide"
)

st.title("📋 Site Imprest Validation Tool")

uploaded_file = st.file_uploader(
    "Upload Site Imprest Excel File",
    type=["xlsx", "xlsm"]
)

if uploaded_file:

    try:
        # =========================
        # Read Template Sheet
        # =========================
        df = pd.read_excel(
            uploaded_file,
            sheet_name="Template",
            header=None
        )

        # =========================
        # Helper Functions
        # =========================

        def find_text_value(keyword):

            for row in df.values:
                for cell in row:

                    if pd.notna(cell):

                        text = str(cell).strip()

                        if keyword.lower() in text.lower():

                            if ":" in text:
                                return text.split(":", 1)[1].strip()

            return ""

        def find_value_near_label(keyword):

            rows, cols = df.shape

            for r in range(rows):
                for c in range(cols):

                    cell = df.iloc[r, c]

                    if pd.notna(cell):

                        text = str(cell).strip().lower()

                        if keyword.lower() in text:

                            # Check right side
                            for nc in range(c + 1, min(c + 5, cols)):

                                value = df.iloc[r, nc]

                                if pd.notna(value):
                                    return value

                            # Check below
                            for nr in range(r + 1, min(r + 5, rows)):

                                value = df.iloc[nr, c]

                                if pd.notna(value):
                                    return value

            return ""

        # =========================
        # Basic Details
        # =========================

        project_name = find_text_value("Project Name")
        employee_name = find_text_value("Name")
        employee_id = find_text_value("Emp ID")
        site_name = find_text_value("Site Name")

        account_number = find_value_near_label("Account")
        ifsc = find_value_near_label("IFSC")
        email = find_value_near_label("Email")
        phone = find_value_near_label("Phone")

        advance_total = find_value_near_label("Advance Total")
        expenses_total = find_value_near_label("Expenses Total")
        balance_on_hand = find_value_near_label("Balance On Hand")

        st.success("✅ Template Sheet Extracted Successfully")

        # =========================
        # Employee Details
        # =========================

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
            st.write("**IFSC Code:**", ifsc)
            st.write("**Account Number:**", account_number)

        # =========================
        # Financial Summary
        # =========================

        st.subheader("💰 Financial Summary")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Advance Total", advance_total)

        with c2:
            st.metric("Expenses Total", expenses_total)

        with c3:
            st.metric("Balance On Hand", balance_on_hand)

        # =========================
        # Expense Table Extraction
        # =========================

        st.subheader("📊 Expense Details")

        expense_table = None

        rows, cols = df.shape

        header_row = None
        desc_col = None

        for r in range(rows):
            for c in range(cols):

                value = df.iloc[r, c]

                if pd.notna(value):

                    text = str(value).strip().lower()

                    if "description of expenses" in text:

                        header_row = r
                        desc_col = c
                        break

            if header_row is not None:
                break

        if header_row is not None:

            extracted_rows = []

            for r in range(header_row + 1, rows):

                description = df.iloc[r, desc_col]

                if pd.isna(description):
                    continue

                description = str(description).strip()

                if description == "":
                    continue

                row_values = []

                for c in range(desc_col, min(desc_col + 4, cols)):
                    row_values.append(df.iloc[r, c])

                extracted_rows.append(row_values)

            if extracted_rows:

                max_cols = max(len(row) for row in extracted_rows)

                column_names = [
                    "Description of Expenses",
                    "Total Expenses",
                    "Special Approval",
                    "Remarks"
                ][:max_cols]

                expense_table = pd.DataFrame(
                    extracted_rows,
                    columns=column_names
                )

                st.dataframe(
                    expense_table,
                    use_container_width=True
                )

            else:
                st.warning("Expense table found but no data extracted.")

        else:
            st.warning(
                "Could not automatically locate the 'Description of Expenses' table."
            )

    except Exception as e:
        st.error(f"❌ Error: {e}")
