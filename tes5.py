import streamlit as st
import csv
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("test-data-filipin-3cd188664241.json", scope)
client = gspread.authorize(creds)
SPREADSHEET_ID = "1D9R_x2rt8hyBaEOj8ytbj9YvwxFz7X60vUvn-8vQbvk"
sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Sheet3")


st.title("📦 Sampling Filipina")

menu = st.sidebar.radio("Menu", ["Pemasangan", "Pelepasan", "Lihat Data"], key="main_menu")

# define where table starts
TABLE_START_ROW = 7  

def find_next_empty_row(sheet, col="E"):
    """Find the first empty row in column E after TABLE_START_ROW"""
    col_values = sheet.col_values(5)  # column E is index 5
    for i in range(TABLE_START_ROW, len(col_values) + 2):  
        if i > len(col_values) or col_values[i-1] == "":
            return i
    return len(col_values) + 1

# --- Pemasangan ---
if menu == "Pemasangan":
    st.subheader("Form Pemasangan")
    kode_filter = st.text_input("Kode Filter")
    flow_awal = st.text_input("Flow Awal")
    elapsed_awal = st.text_input("Elapsed Time Awal")

    if st.button("Simpan Pemasangan"):
        row_index = find_next_empty_row(sheet)

        pemasangan_data = [kode_filter, flow_awal, elapsed_awal]
        sheet.update(f"E{row_index}:G{row_index}", [pemasangan_data])
        st.success(f"✅ Data pemasangan berhasil disimpan di baris {row_index}")

# --- Pelepasan ---
elif menu == "Pelepasan":
    st.subheader("Form Pelepasan")
    kode_filter = st.text_input("Kode Filter")
    flow_akhir = st.text_input("Flow Akhir")
    elapsed_akhir = st.text_input("Elapsed Time Akhir")
    nama_petugas = st.text_input("Nama Petugas Pengganti (jika ada)")

    if st.button("Simpan Pelepasan"):
        row_index = find_next_empty_row(sheet)

        pelepasan_data = [kode_filter, flow_akhir, elapsed_akhir, nama_petugas]
        sheet.update(f"E{row_index}:H{row_index}", [pelepasan_data])
        st.success(f"✅ Data pelepasan berhasil disimpan di baris {row_index}")

# --- Lihat Data ---
elif menu == "Lihat Data":
    all_data = sheet.get_all_values()
    table_data = all_data[TABLE_START_ROW-1:]  # cut rows before table
    st.dataframe(table_data)
