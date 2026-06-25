import streamlit as st
import pandas as pd

st.markdown("""
<style>

/* Main page */
.stApp{
    background: linear-gradient(180deg,#eef4ff,#f8fbff);
}

/* Hide Streamlit menu */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Welcome section */
.hero-card{
    background:white;
    padding:30px;
    border-radius:20px;
    box-shadow:0px 4px 20px rgba(0,0,0,0.08);
    margin-bottom:25px;
}

.hero-title{
    font-size:36px;
    font-weight:700;
    color:#1f2937;
}

.hero-blue{
    color:#4f46e5;
}

.hero-text{
    color:#6b7280;
    font-size:16px;
}

/* Section cards */
.section-card{
    background:white;
    padding:25px;
    border-radius:18px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.06);
    margin-bottom:20px;
}

/* Detail boxes */
.info-box{
    background:white;
    border:1px solid #e5e7eb;
    border-radius:15px;
    padding:15px;
    height:110px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.05);
}

.info-title{
    font-size:11px;
    color:#6b7280;
    text-transform:uppercase;
    font-weight:600;
}

.info-value{
    font-size:22px;
    font-weight:700;
    color:#111827;
}

/* Summary Cards */

.green-card{
    background:#f0fdf4;
    border:1px solid #bbf7d0;
    border-radius:18px;
    padding:20px;
}

.orange-card{
    background:#fff7ed;
    border:1px solid #fed7aa;
    border-radius:18px;
    padding:20px;
}

.blue-card{
    background:#eff6ff;
    border:1px solid #bfdbfe;
    border-radius:18px;
    padding:20px;
}

.green-value{
    color:#16a34a;
    font-size:34px;
    font-weight:700;
}

.orange-value{
    color:#ea580c;
    font-size:34px;
    font-weight:700;
}

.blue-value{
    color:#2563eb;
    font-size:34px;
    font-weight:700;
}

.section-title{
    font-size:24px;
    font-weight:700;
    margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>

.stApp{
    background:#f5f7fb;
}

.hero-box{
    background:Blue;
    border-radius:20px;
    padding:30px;
    box-shadow:0 4px 15px rgba(0,0,0,0.05);
    margin-bottom:25px;
}

.hero-title{
    font-size:40px;
    font-weight:700;
    text-align:center;
}

.hero-title span{
    color:#3b82f6;
}

.hero-sub{
    text-align:center;
    color:#666;
    margin-top:10px;
    font-size:18px;
}

.card{
    background:white;
    border-radius:16px;
    padding:20px;
    box-shadow:0 4px 10px rgba(0,0,0,0.05);
    border:1px solid #eef2f7;
}

.small-title{
    font-size:12px;
    color:#666;
    text-transform:uppercase;
}

.big-value{
    font-size:20px;
    font-weight:700;
    color:#111827;
}

.metric-card{
    background:white;
    border-radius:16px;
    padding:20px;
    text-align:center;
    box-shadow:0 4px 10px rgba(0,0,0,0.05);
}

.green{
    color:#10b981;
}

.orange{
    color:#f97316;
}

.blue{
    color:#2563eb;
}

.metric-value{
    font-size:28px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-box">

<div class="hero-title">
Welcome to <span>Site Imprest</span> Validation Tool
</div>

<div class="hero-sub">
Upload the site imprest workbook to automatically validate category-wise totals,
expenses and supporting sheets.
</div>

</div>
""", unsafe_allow_html=True)


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

        st.subheader("👤 Employee & Site Details")
        
        c1,c2,c3,c4 = st.columns(4)
        
        with c1:
            st.markdown(f"""
            <div class="card">
            <div class="small-title">PROJECT NAME</div>
            <div class="big-value">{project_name}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with c2:
            st.markdown(f"""
            <div class="card">
            <div class="small-title">EMPLOYEE NAME</div>
            <div class="big-value">{employee_name}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with c3:
            st.markdown(f"""
            <div class="card">
            <div class="small-title">EMPLOYEE ID</div>
            <div class="big-value">{employee_id}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with c4:
            st.markdown(f"""
            <div class="card">
            <div class="small-title">SITE NAME</div>
            <div class="big-value">{site_name}</div>
            </div>
            """, unsafe_allow_html=True)
        
        c1,c2,c3,c4 = st.columns(4)
        
        with c1:
            st.markdown(f"""
            <div class="card">
            <div class="small-title">ACCOUNT NUMBER</div>
            <div class="big-value">{account_number}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with c2:
            st.markdown(f"""
            <div class="card">
            <div class="small-title">IFSC CODE</div>
            <div class="big-value">{ifsc}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with c3:
            st.markdown(f"""
            <div class="card">
            <div class="small-title">EMAIL ID</div>
            <div class="big-value">{email}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with c4:
            st.markdown(f"""
            <div class="card">
            <div class="small-title">PHONE NUMBER</div>
            <div class="big-value">{phone}</div>
            </div>
            """, unsafe_allow_html=True)
    
        # ==================================================
        # FINANCIAL SUMMARY
        # ==================================================

        st.subheader("💰 Financial Summary")
        
        c1,c2,c3 = st.columns(3)
        
        with c1:
            st.markdown(f"""
            <div class="metric-card">
            <div>ADVANCE TOTAL</div>
            <div class="metric-value green">
            ₹ {advance_total:,.2f}
            </div>
            </div>
            """, unsafe_allow_html=True)
        
        with c2:
            st.markdown(f"""
            <div class="metric-card">
            <div>EXPENSES TOTAL</div>
            <div class="metric-value orange">
            ₹ {expenses_total:,.2f}
            </div>
            </div>
            """, unsafe_allow_html=True)
        
        with c3:
            st.markdown(f"""
            <div class="metric-card">
            <div>BALANCE ON HAND</div>
            <div class="metric-value blue">
            ₹ {balance_on_hand:,.2f}
            </div>
            </div>
            """, unsafe_allow_html=True)
            

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
        
        CATEGORY_MAP = {
            1: "Air Ticket",
            2: "Train Tickets",
            3: "Hotel",
            4: "Food",
            5: "Car Rental",
            6: "Daily Rental Vehicle",
            7: "Stationery Expenses",
            8: "Printing Charges",
            9: "Subscription Charges",
            10: "Cleaning Charges",
            11: "Telephone Charges",
            12: "Courier Charges",
            13: "Repairs & Maintenance",
            14: "Loading & Unloading / Transport charges",
            15: "Diesel Oil",
            16: "Consumables",
            17: "Rent",
            18: "Electricity charges",
            19: "Other Expense"
        }
        
        validation_rows = []
        
        total_pass = 0
        total_fail = 0
        
        sub_sheet_grand_total = 0.0
        
        expense_df = expense_df.reset_index(drop=True)
        
        for idx, row in expense_df.iterrows():
        
            sl_no = idx + 1
        
            category = CATEGORY_MAP.get(
                sl_no,
                f"Category {sl_no}"
            )
        
            template_amount = safe_float(
                row["Total Expenses"]
            )
        
            sheet_name = str(sl_no)
        
            sheet_total = 0.0
        
            # =====================================
            # SHEET EXISTS
            # =====================================
        
            if sheet_name in excel_file.sheet_names:
        
                sub_df = pd.read_excel(
                    uploaded_file,
                    sheet_name=sheet_name,
                    header=None
                )
        
                rows_sub, cols_sub = sub_df.shape
        
                found_total = False
        
                for r in range(rows_sub):
        
                    for c in range(cols_sub):
        
                        cell = sub_df.iloc[r, c]
        
                        if pd.notna(cell):
        
                            text = str(cell).strip().lower()
        
                            if (
                                text == "total"
                                or "total expenses" in text
                            ):
        
                                numeric_values = []
        
                                for cc in range(cols_sub):
        
                                    val = sub_df.iloc[r, cc]
        
                                    try:
        
                                        num = safe_float(val)
        
                                        if num > 0:
                                            numeric_values.append(num)
        
                                    except:
                                        pass
        
                                if numeric_values:
        
                                    sheet_total = max(
                                        numeric_values
                                    )
        
                                found_total = True
                                break
        
                    if found_total:
                        break
        
            # =====================================
            # MISSING SHEET LOGIC
            # =====================================
        
            else:
        
                if template_amount == 0:
        
                    sheet_total = 0
        
                else:
        
                    sheet_total = 0
        
            sub_sheet_grand_total += sheet_total
        
            difference = abs(
                template_amount - sheet_total
            )
        
            if difference < 0.01:
        
                status = "✅ PASS"
                total_pass += 1
        
            else:
        
                status = "❌ FAIL"
                total_fail += 1
        
            validation_rows.append({
        
                "Sl No": sl_no,
        
                "Category": category,
        
                "Template Amount":
                    round(template_amount, 2),
        
                "Sheet Total":
                    round(sheet_total, 2),
        
                "Difference":
                    round(difference, 2),
        
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
