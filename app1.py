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
