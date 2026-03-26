#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import calendar
from datetime import datetime
import io

st.set_page_config(page_title="Milk Report Generator", layout="centered")

st.title("🧾 Milk Expense "month" ")

# Inputs
month = st.selectbox("Select Month", list(range(1, 13)))
year = st.number_input("Enter Year", min_value=2020, max_value=2100, value=2026)

price_cd = st.number_input("Country Delight Price", value=30.6)
price_amul = st.number_input("Amul Price", value=35.0)

holiday_input = st.text_input("Enter Holidays (e.g. 5,12,25)")

# Convert holidays
holidays = []
if holiday_input:
    holidays = [int(x.strip()) for x in holiday_input.split(",") if x.strip().isdigit()]

# Button
if st.button("Generate Report"):

    days = calendar.monthrange(year, month)[1]
    data = []

    for day in range(1, days + 1):
        date = datetime(year, month, day)
        day_name = date.strftime("%A")

        if day_name in ["Saturday", "Sunday"] or day in holidays:
            qty = 0
        else:
            qty = 8

        total_cd = qty * price_cd
        total_amul = qty * price_amul

        data.append([
            day,
            date.strftime("%d-%m-%Y"),
            day_name,
            "Milk",
            qty,
            price_cd,
            total_cd,
            price_amul,
            total_amul
        ])

    df = pd.DataFrame(data, columns=[
        "S.NO", "DATE", "Day", "ITEM", "QTY",
        "PRICE / PKT (CD)", "TOTAL CD",
        "PRICE / PKT (AMUL)", "TOTAL AMUL"
    ])

    st.success("✅ Report Generated")
    st.dataframe(df, use_container_width=True)

    # Download Excel
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False, engine="xlswriter")

    st.download_button(
        label="⬇️ Download Excel Report",
        data=buffer.getvalue(),
        file_name=f"Milk_Expense_{calendar.month_name[month]}_{year}.xlsx",
        mime="application/vnd.ms-excel"
    )

