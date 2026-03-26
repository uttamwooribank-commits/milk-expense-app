import streamlit as st
import pandas as pd
import calendar
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="Milk Expense App", layout="centered")

st.title("🧾 Milk Expense Generator")

# --- INPUTS ---
year = st.number_input("Enter Year", min_value=2020, max_value=2100, value=2026)
month = st.number_input("Enter Month (1-12)", min_value=1, max_value=12, value=3)

price_cd = st.number_input("Country Delight Price (₹)", value=50)
price_amul = st.number_input("Amul Price (₹)", value=30)

num_days = calendar.monthrange(year, month)[1]

# --- HOLIDAYS ---
holiday_dates = st.multiselect(
    f"Select Holidays (1-{num_days})",
    options=list(range(1, num_days + 1))
)

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

    df = pd.DataFrame(data, columns=[
        "Date", "Day Names", "Type", "Qty",
        "Country Delight Price", "Country Delight",
        "Amul Price", "Amul"
    ])

    # --- TOTAL ROW ---
    total_row = pd.DataFrame([[
        "", "", "TOTAL", "",
        "", df["Country Delight"].sum(),
        "", df["Amul"].sum()
    ]], columns=df.columns)

    df_final = pd.concat([df, total_row], ignore_index=True)

    st.subheader(f"📅 Milk Expense - {month_name} {year}")
    st.dataframe(df_final)

    # --- DOWNLOAD ---
    file_name = f"Milk_Expense_{month_name}_{year}.xlsx"
    
buffer = BytesIO()
df_final.to_excel(buffer, index=False)
buffer.seek(0)

    st.download_button(
        "📥 Download Excel",
        data=excel,
        file_name=file_name
    )
