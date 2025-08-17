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

# --- Pemasangan ---
if menu == "Pemasangan":
    st.subheader("Form Pemasangan")
    kode_filter = st.text_input("Kode Filter")
    flow_awal = st.text_input("Flow Awal")
    elapsed_awal = st.text_input("Elapsed Time Awal")

    if st.button("Simpan Pemasangan"):
        # Find existing row for the kode_filter
        records = sheet.get_all_values()
        row_index = None
        for i, row in enumerate(records):
            if len(row) > 1 and row[1] == kode_filter:  # Column B = Kode Filter
                row_index = i + 1  # gspread rows start at 1
                break

        if row_index is None:  
            # If kode_filter not found, add a new row at the end
            row_index = len(records) + 1

        # Prepare data for A–F columns
        pemasangan_data = [
             kode_filter, flow_awal, elapsed_awal
        ]

        # Update A–F in the row
        sheet.update(f"E{row_index}:G{row_index}", [pemasangan_data])
        st.success(f"Data pemasangan untuk {kode_filter} berhasil disimpan di baris {row_index}!")

# --- Pelepasan ---
elif menu == "Pelepasan":
    st.subheader("Form Pelepasan")
    kode_filter = st.text_input("Kode Filter")  # match pemasangan
    flow_akhir = st.text_input("Flow Akhir")
    elapsed_akhir = st.text_input("Elapsed Time Akhir")
    nama_petugas = st.text_input("Nama Petugas Pengganti(jika ada)")

    if st.button("Simpan Pelepasan"):
        # Find row for kode_filter
        records = sheet.get_all_values()
        row_index = None
        for i, row in enumerate(records):
            if len(row) > 1 and row[1] == kode_filter:  # compare with kode_filter
                row_index = i + 1
                break

        if row_index is None:
            st.error(f"Kode filter {kode_filter} belum ada di data pemasangan!")
        else:
            # Prepare data for H–J columns
            pelepasan_data = [flow_akhir, elapsed_akhir, nama_petugas]
            sheet.update(f"H{row_index}:J{row_index}", [pelepasan_data])
            st.success(f"Data pelepasan untuk {kode_filter} berhasil disimpan di baris {row_index}!")

# --- Lihat Data ---
elif menu == "Lihat Data":
    data = sheet.get_all_records()
    st.dataframe(data)
elif menu == "Pelepasan":
    st.subheader("Form Pelepasan")
    kode_filter = st.text_input("Kode Filter")  # match pemasangan
    flow_akhir = st.text_input("Flow Akhir")
    elapsed_akhir = st.text_input("Elapsed Time Akhir")
    nama_petugas = st.text_input("Nama Petugas Pengganti(jika ada)")

    if st.button("Simpan Pelepasan"):
        # Find row for kode_filter
        records = sheet.get_all_values()
        row_index = None
        for i, row in enumerate(records):
            if len(row) > 1 and row[1] == kode_filter:  # compare with kode_filter
                row_index = i + 1
                break

        if row_index is None:
            st.error(f"Kode filter {kode_filter} belum ada di data pemasangan!")
        else:
            # Prepare data for H–J columns
            pelepasan_data = [flow_akhir, elapsed_akhir, nama_petugas]
            sheet.update(f"H{row_index}:J{row_index}", [pelepasan_data])
            st.success(f"Data pelepasan untuk {kode_filter} berhasil disimpan di baris {row_index}!")

# --- Lihat Data ---
elif menu == "Lihat Data":
    data = sheet.get_all_records()
    st.dataframe(data)