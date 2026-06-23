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

        # ==================================================
        # READ TEMPLATE SHEET
        # ==================================================
        df = pd.read_excel(
            uploaded_file,
            sheet_name="Template",
            header=None
        )

        excel_file = pd.ExcelFile(uploaded_file)

        # ==================================================
        # HELPER FUNCTIONS
        # ==================================================

        def safe_float(value):

            try:

                if pd.isna(value):
                    return 0.0

                value = str(value).replace(",", "").strip()

                if value == "":
                    return 0.0

                return float(value)

            except:
                return 0.0

        def get_value_after_label(label):

            rows, cols = df.shape

            for r in range(rows):
                for c in range(cols):

                    cell = df.iloc[r, c]

                    if pd.notna(cell):

                        text = str(cell).strip()

                        if text.lower().startswith(label.lower()):

                            if ":" in text:

                                parts = text.split(":", 1)

                                if len(parts) > 1:
                                    return parts[1].strip()

                            for nc in range(c + 1, min(c + 4, cols)):

                                val = df.iloc[r, nc]

                                if pd.notna(val):
                                    return str(val).strip()

            return ""

        # ==================================================
        # EMPLOYEE DETAILS
        # ==================================================

        project_name = get_value_after_label("Project Name:")
        employee_name = get_value_after_label("NAME:")
        employee_id = get_value_after_label("Emp ID:")
        site_name = get_value_after_label("Site Name:")

        account_number = get_value_after_label("Account")
        ifsc = get_value_after_label("IFSC")
        email = get_value_after_label("Email")
        phone = get_value_after_label("Phone")

        advance_total = safe_float(
            get_value_after_label("Advance Total")
        )

        expenses_total = safe_float(
            get_value_after_label("Expenses total")
        )

        balance_on_hand = safe_float(
            get_value_after_label("Balance on hand")
        )

        st.success("✅ Template Sheet Extracted Successfully")

        # ==================================================
        # EMPLOYEE DETAILS DISPLAY
        # ==================================================

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

        # ==================================================
        # FINANCIAL SUMMARY
        # ==================================================

        st.subheader("💰 Financial Summary")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Advance Total",
                f"₹ {advance_total:,.2f}"
            )

        with c2:
            st.metric(
                "Expenses Total",
                f"₹ {expenses_total:,.2f}"
            )

        with c3:
            st.metric(
                "Balance On Hand",
                f"₹ {balance_on_hand:,.2f}"
            )

        # ==================================================
        # EXPENSE TABLE EXTRACTION
        # ==================================================

        st.subheader("📊 Expense Details")

        rows, cols = df.shape

        header_row = None

        for r in range(rows):

            for c in range(cols):

                value = df.iloc[r, c]

                if pd.notna(value):

                    if str(value).strip().lower() == "description of expenses":

                        header_row = r

                        desc_col = c
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

                if description.lower().startswith("opening balance"):
                    break

                total_expense = 0.0

                if expense_col < cols:

                    total_expense = safe_float(
                        df.iloc[r, expense_col]
                    )

                special_approval = ""

                if approval_col < cols:

                    val = df.iloc[r, approval_col]

                    if pd.notna(val):
                        special_approval = str(val)

                expense_data.append({
                    "Description of Expenses": description,
                    "Total Expenses": total_expense,
                    "Special Approval": special_approval
                })

        expense_df = pd.DataFrame(expense_data)

        st.dataframe(
            expense_df,
            use_container_width=True,
            hide_index=True
        )

        # ==================================================
        # CATEGORY VALIDATION
        # ==================================================

        st.subheader("🔍 Category Validation")

        validation_rows = []

        total_pass = 0
        total_fail = 0

        sub_sheet_grand_total = 0.0

        sheet_names = [
            sheet.strip().lower()
            for sheet in excel_file.sheet_names
        ]

        for _, row in expense_df.iterrows():

            category = str(
                row["Description of Expenses"]
            ).strip()

            template_amount = safe_float(
                row["Total Expenses"]
            )

            matching_sheet = None

            for sheet in excel_file.sheet_names:

                if sheet.strip().lower() == category.lower():

                    matching_sheet = sheet
                    break

            # ==========================
            # SHEET NOT FOUND
            # ==========================

            if matching_sheet is None:

                if template_amount == 0:

                    sheet_total = 0.0
                    difference = 0.0
                    status = "✅ PASS"
                    total_pass += 1

                else:

                    sheet_total = 0.0
                    difference = template_amount
                    status = "❌ FAIL"
                    total_fail += 1

            else:

                sub_df = pd.read_excel(
                    uploaded_file,
                    sheet_name=matching_sheet,
                    header=None
                )

                sheet_total = 0.0

                found_total = False

                s_rows, s_cols = sub_df.shape

                for r in range(s_rows):

                    for c in range(s_cols):

                        cell = sub_df.iloc[r, c]

                        if pd.notna(cell):

                            text = str(cell).strip().lower()

                            if "total" in text:

                                if c + 1 < s_cols:

                                    sheet_total = safe_float(
                                        sub_df.iloc[r, c + 1]
                                    )

                                    found_total = True
                                    break

                    if found_total:
                        break

                difference = abs(
                    template_amount - sheet_total
                )

                sub_sheet_grand_total += sheet_total

                if difference < 0.01:

                    status = "✅ PASS"
                    total_pass += 1

                else:

                    status = "❌ FAIL"
                    total_fail += 1

            validation_rows.append({

                "Category": category,
                "Template Amount": round(
                    template_amount, 2
                ),
                "Sheet Total": round(
                    sheet_total, 2
                ),
                "Difference": round(
                    difference, 2
                ),
                "Status": status
            })

        validation_df = pd.DataFrame(
            validation_rows
        )

        st.dataframe(
            validation_df,
            use_container_width=True,
            hide_index=True
        )

        # ==================================================
        # VALIDATION SUMMARY
        # ==================================================

        st.subheader("📋 Validation Summary")

        s1, s2, s3 = st.columns(3)

        with s1:
            st.metric(
                "Total Categories Checked",
                len(validation_df)
            )

        with s2:
            st.metric(
                "Passed",
                total_pass
            )

        with s3:
            st.metric(
                "Failed",
                total_fail
            )

        # ==================================================
        # GRAND TOTAL VALIDATION
        # ==================================================

        st.subheader("💯 Grand Total Validation")

        g1, g2 = st.columns(2)

        with g1:

            st.metric(
                "Template Expenses Total",
                f"₹ {expenses_total:,.2f}"
            )

        with g2:

            st.metric(
                "Sub-sheet Grand Total",
                f"₹ {sub_sheet_grand_total:,.2f}"
            )

        grand_difference = abs(
            expenses_total - sub_sheet_grand_total
        )

        if grand_difference < 0.01:

            st.success(
                "✅ GRAND TOTAL MATCHED"
            )

        else:

            st.error(
                f"❌ GRAND TOTAL MISMATCH | Difference = ₹ {grand_difference:,.2f}"
            )

    except Exception as e:

        st.error(f"❌ Error: {e}")
