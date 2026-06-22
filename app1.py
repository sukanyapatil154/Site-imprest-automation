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
        df = pd.read_excel(
            uploaded_file,
            sheet_name="Template",
            header=None
        )

        def find_text_value(keyword):
            """
            Finds values written like:
            Project Name: FPEL Kudligi
            Name: Abhishek G
            """
            for row in df.values:
                for cell in row:
                    if pd.notna(cell):

                        text = str(cell).strip()

                        if keyword.lower() in text.lower():

                            if ":" in text:
                                return text.split(":", 1)[1].strip()

            return ""

        def find_value_below_or_right(keyword):
            """
            Finds labels like:
            Account Number | 42091673874

            IFSC CODE      | SBIN0040092
            """

            rows, cols = df.shape

            for r in range(rows):
                for c in range(cols):

                    cell = df.iloc[r, c]

                    if pd.notna(cell):

                        text = str(cell).strip().lower()

                        if keyword.lower() in text:

                            # Check right side first
                            for next_col in range(c + 1, min(c + 4, cols)):
                                value = df.iloc[r, next_col]

                                if pd.notna(value):
                                    return value

                            # Check below
                            for next_row in range(r + 1, min(r + 4, rows)):
                                value = df.iloc[next_row, c]

                                if pd.notna(value):
                                    return value

            return ""

        # ==========================
        # Employee Details
        # ==========================

        project_name = find_text_value("Project Name")
        employee_name = find_text_value("NAME")
        employee_id = find_text_value("Emp ID")
        site_name = find_text_value("Site Name")

        # ==========================
        # Bank Details
        # ==========================

        account_number = find_value_below_or_right("Account number")
        ifsc = find_value_below_or_right("IFSC")
        email = find_value_below_or_right("Email")
        phone = find_value_below_or_right("Phone")
        # =====================================
# Expense Summary Table
# =====================================

st.subheader("📊 Expense Summary")

expense_table = None

rows, cols = df.shape

for r in range(rows):
    for c in range(cols):

        cell = str(df.iloc[r, c]).strip().lower() if pd.notna(df.iloc[r, c]) else ""

        if "description of expenses" in cell:

            # Table starts from this row
            header_row = r

            table_data = []

            for i in range(header_row + 1, rows):

                desc = df.iloc[i, c]

                amount = df.iloc[i, c + 1] if c + 1 < cols else ""
                approval = df.iloc[i, c + 2] if c + 2 < cols else ""

                # Stop when blank rows start appearing
                if pd.isna(desc):
                    continue

                desc_text = str(desc).strip()

                if desc_text == "":
                    continue

                table_data.append([
                    desc,
                    amount,
                    approval
                ])

            expense_table = pd.DataFrame(
                table_data,
                columns=[
                    "Description of Expenses",
                    "Total Expenses",
                    "Any Special Approval"
                ]
            )

            break

    if expense_table is not None:
        break

if expense_table is not None:
    st.dataframe(
        expense_table,
        use_container_width=True
    )
else:
    st.warning("Expense table not found.")

        # ==========================
        # Financial Details
        # ==========================

        advance_total = find_value_below_or_right("Advance Total")
        expenses_total = find_value_below_or_right("Expenses total")
        balance_on_hand = find_value_below_or_right("Balance on hand")

        st.success("✅ Template Sheet Extracted Successfully")

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

        st.subheader("💰 Financial Summary")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Advance Total",
                f"₹ {float(advance_total):,.2f}"
            )

        with c2:
            st.metric(
                "Expenses Total",
                f"₹ {float(expenses_total):,.2f}"
            )

        with c3:
            st.metric(
                "Balance On Hand",
                f"₹ {float(balance_on_hand):,.2f}"
            )

        # ==========================
        # Show Available Sheets
        # ==========================

        excel_file = pd.ExcelFile(uploaded_file)

        st.subheader("📄 Available Sheets")

        for sheet in excel_file.sheet_names:
            st.write("•", sheet)

    except Exception as e:
        st.error(f"❌ Error: {e}")
