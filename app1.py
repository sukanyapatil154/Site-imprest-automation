import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Site Imprest Validation Tool",
    layout="wide"
)
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
<div class='hero-card'>
    <div class='hero-title'>
        Welcome to <span class='hero-blue'>Site Imprest</span> Validation Tool
    </div>
    <br>
    <div class='hero-text'>
        Upload the site imprest Excel workbook to automatically extract employee details,
        expense information and validate category-wise totals.
    </div>
</div>
""", unsafe_allow_html=True)




# For uploading file
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

        st.markdown("""
        <h3 style="
        font-size:28px;
        font-weight:700;
        color:#1f2937;
        margin-bottom:18px;">
        👤 Employee & Site Details
        </h3>
        """, unsafe_allow_html=True)
        
        cards = [
        ("🏢","Project Name",project_name,"#6366f1","#eef2ff"),
        ("👤","Name",employee_name,"#22c55e","#ecfdf5"),
        ("🆔","EMP ID",employee_id,"#38bdf8","#eff6ff"),
        ("📍","Site Name",site_name,"#a855f7","#faf5ff"),
        ("🏦","Account Number",account_number,"#f59e0b","#fff7ed"),
        ("🏛️","IFSC Code",ifsc,"#ef4444","#fef2f2"),
        ("📧","Email ID",email,"#3b82f6","#eff6ff"),
        ("📞","Phone Number",phone,"#22c55e","#ecfdf5")
        ]
        
        cols = st.columns(4)
        
        for i, card in enumerate(cards):
        
            icon, title, value, color, bg = card
        
            with cols[i % 4]:
        
                # Slightly reduce font size for long values
                value_size = "17px"
                if len(str(value)) > 25:
                    value_size = "15px"
        
                st.markdown(f"""
                <div style="
                    background:white;
                    border:1px solid #edf2f7;
                    border-radius:14px;
                    padding:14px;
                    height:108px;
                    box-shadow:0 2px 10px rgba(0,0,0,.05);
                ">
        
                    <div style="
                        width:38px;
                        height:38px;
                        border-radius:10px;
                        background:{bg};
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        font-size:20px;
                        margin-bottom:10px;
                    ">
                        {icon}
                    </div>
        
                    <div style="
                        font-size:9px;
                        font-weight:600;
                        color:#9ca3af;
                        text-transform:uppercase;
                        letter-spacing:.5px;
                        margin-bottom:4px;
                    ">
                        {title}
                    </div>
        
                    <div style="
                        font-size:{value_size};
                        font-weight:600;
                        color:#1f2937;
                        line-height:1.25;
                        word-break:break-word;
                    ">
                        {value}
                    </div>
        
                </div>
                """, unsafe_allow_html=True)
        
            if i == 3:
                st.markdown("<div style='margin-bottom:12px'></div>", unsafe_allow_html=True)
                cols = st.columns(4)
        
    
        # ==================================================
        # FINANCIAL SUMMARY
        # ==================================================

        st.markdown("## 💰 Financial Summary")
        
        c1,c2,c3=st.columns(3)
        
        with c1:
        
            st.markdown(f"""
        <div style="
        background:#f0fdf4;
        padding:20px;
        border-radius:18px;
        border:1px solid #bbf7d0;
        ">
        
        <div style="display:flex;justify-content:space-between;align-items:center;">
        
        <div>
        
        <div style="font-size:12px;color:#777;">ADVANCE TOTAL</div>
        
        <div style="font-size:32px;
        font-weight:700;
        color:#16a34a;">
        ₹ {advance_total:,.2f}
        </div>
        
        </div>
        
        <div style="font-size:34px;">💵</div>
        
        </div>
        
        </div>
        """,unsafe_allow_html=True)
        
        with c2:
        
            st.markdown(f"""
        <div style="
        background:#fff7ed;
        padding:20px;
        border-radius:18px;
        border:1px solid #fed7aa;
        ">
        
        <div style="display:flex;justify-content:space-between;align-items:center;">
        
        <div>
        
        <div style="font-size:12px;color:#777;">EXPENSES TOTAL</div>
        
        <div style="font-size:32px;
        font-weight:700;
        color:#ea580c;">
        ₹ {expenses_total:,.2f}
        </div>
        
        </div>
        
        <div style="font-size:34px;">📊</div>
        
        </div>
        
        </div>
        """,unsafe_allow_html=True)
        
        with c3:
        
            st.markdown(f"""
        <div style="
        background:#eff6ff;
        padding:20px;
        border-radius:18px;
        border:1px solid #bfdbfe;
        ">
        
        <div style="display:flex;justify-content:space-between;align-items:center;">
        
        <div>
        
        <div style="font-size:12px;color:#777;">BALANCE ON HAND</div>
        
        <div style="font-size:32px;
        font-weight:700;
        color:#2563eb;">
        ₹ {balance_on_hand:,.2f}
        </div>
        
        </div>
        
        <div style="font-size:34px;">💳</div>
        
        </div>
        
        </div>
        """,unsafe_allow_html=True)
            

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

        st.markdown("## 📋 Validation Summary")
        
        c1,c2,c3=st.columns(3)
        
        with c1:
        
            st.markdown(f"""
        <div style="
        background:#eef2ff;
        padding:22px;
        border-radius:18px;
        ">
        
        <div style="font-size:12px;color:#777;">
        TOTAL CATEGORIES
        </div>
        
        <div style="
        font-size:38px;
        font-weight:bold;
        color:#4f46e5;">
        {len(validation_df)}
        </div>
        
        <div style="font-size:30px;">
        📄
        </div>
        
        </div>
        """,unsafe_allow_html=True)
        
        with c2:
        
            st.markdown(f"""
        <div style="
        background:#f0fdf4;
        padding:22px;
        border-radius:18px;
        ">
        
        <div style="font-size:12px;color:#777;">
        PASSED
        </div>
        
        <div style="
        font-size:38px;
        font-weight:bold;
        color:#16a34a;">
        {total_pass}
        </div>
        
        <div style="font-size:30px;">
        ✅
        </div>
        
        </div>
        """,unsafe_allow_html=True)
        
        with c3:
        
            st.markdown(f"""
        <div style="
        background:#fef2f2;
        padding:22px;
        border-radius:18px;
        ">
        
        <div style="font-size:12px;color:#777;">
        FAILED
        </div>
        
        <div style="
        font-size:38px;
        font-weight:bold;
        color:#ef4444;">
        {total_fail}
        </div>
        
        <div style="font-size:30px;">
        ❌
        </div>
        
        </div>
        """,unsafe_allow_html=True)

    
        # ==================================================
        # GRAND TOTAL VALIDATION
        # ==================================================

        st.markdown("## ✅ Grand Total Validation")
        
        match = abs(expenses_total - sub_sheet_grand_total) < 0.01
        
        color = "#16a34a" if match else "#dc2626"
        bg = "#ecfdf5" if match else "#fef2f2"
        
        status = (
            "✅ GRAND TOTAL MATCHED"
            if match
            else "❌ GRAND TOTAL MISMATCH"
        )
        
        st.markdown(f"""
<div style="
background:{bg};
padding:28px;
border-radius:18px;
text-align:center;
">

<div style="font-size:17px;color:#777;">
Template Total :
₹ {expenses_total:,.2f}
</div>

<br>

<div style="font-size:17px;color:#777;">
Sub Sheet Total :
₹ {sub_sheet_grand_total:,.2f}
</div>

<br>

<div style="
font-size:28px;
font-weight:bold;
color:{color};">
{status}
</div>

</div>
""", unsafe_allow_html=True)
    except Exception as e:
         st.error(f"❌ Error: {e}")
