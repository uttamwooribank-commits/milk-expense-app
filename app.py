import streamlit as st
import pandas as pd
import calendar
from datetime import datetime

st.set_page_config(page_title="Milk Expense App", layout="centered")

st.title("🧾 Milk Expense Generator")

# --- INPUTS ---
year = st.number_input("Enter Year", min_value=2020, max_value=2100, value=2026)
month = st.number_input("Enter Month (1-12)", min_value=1, max_value=12, value=5)

price_cd = st.number_input(
    "Country Delight Price (₹)",
    min_value=0.0,
    value=30.06,
    step=0.1,
    format="%.2f"
)

price_amul = st.number_input(
    "Amul Price (₹)",
    min_value=0.0,
    value=35.0,
    step=0.1,
    format="%.2f"
)

# --- NEW INPUTS ---
membership = st.number_input(
    "Membership (₹)",
    min_value=0.0,
    value=0.0,
    step=0.1,
    format="%.2f"
)

cashback = st.number_input(
    "Cashback (₹)",
    min_value=0.0,
    value=0.0,
    step=0.1,
    format="%.2f"
)

num_days = calendar.monthrange(year, month)[1]

# --- HOLIDAYS ---
holiday_dates = st.multiselect(
    f"Select Holidays (1-{num_days})",
    options=list(range(1, num_days + 1))
)

# --- GENERATE ---
if st.button("Generate Report"):

    month_name = calendar.month_name[month]
    data = []

    for day in range(1, num_days + 1):
        date = datetime(year, month, day)
        weekday = date.weekday()

        if weekday in [5, 6] or day in holiday_dates:
            qty = 0
            day_type = "Holiday" if day in holiday_dates else "Weekend"
        else:
            qty = 8
            day_type = "Working Day"

        total_cd = qty * price_cd
        total_amul = qty * price_amul

        data.append([
            date.strftime("%d-%m-%Y"),
            date.strftime("%A"),
            day_type,
            qty,
            price_cd,
            total_cd,
            price_amul,
            total_amul
        ])

    # --- DATAFRAME ---
    df = pd.DataFrame(data, columns=[
        "Date",
        "Day Names",
        "Type",
        "Qty",
        "Country Delight Price",
        "Country Delight",
        "Amul Price",
        "Amul"
    ])

    # --- MEMBERSHIP ROW ---
    membership_row = pd.DataFrame([[
        "", "", "Membership", "",
        "", membership,
        "", ""
    ]], columns=df.columns)

    # --- CASHBACK ROW (NEGATIVE) ---
    cashback_value = -abs(cashback)

    cashback_row = pd.DataFrame([[
        "", "", "Cashback", "",
        "", cashback_value,
        "", ""
    ]], columns=df.columns)

    # --- TOTAL CALCULATION ---
    final_cd_total = round(df["Country Delight"].sum() + membership + cashback_value)
    final_amul_total = round(df["Amul"].sum())

    total_row = pd.DataFrame([[
        "", "", "TOTAL", "",
        "",
        final_cd_total,
        "",
        final_amul_total
    ]], columns=df.columns)

    # --- FINAL DATA ---
    df_final = pd.concat(
        [df, membership_row, cashback_row, total_row],
        ignore_index=True
    )

    st.subheader(f"📅 Milk Expense - {month_name} {year}")
    st.dataframe(df_final)

    # --- DOWNLOAD CSV (SAFE) ---
    file_name = f"Milk_Expense_{month_name}_{year}.csv"

    csv = df_final.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Download Report",
        data=csv,
        file_name=file_name,
        mime="text/csv"
    )
