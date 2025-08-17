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

sheet_pemasangan = client.open_by_key(SPREADSHEET_ID).worksheet("Pemasangan")
sheet_pelepasan = client.open_by_key(SPREADSHEET_ID).worksheet("Pelepasan")


st.title("📦 Sampling Filipina")

menu = st.sidebar.radio("Menu", ["Pemasangan", "Pelepasan", "Lihat Data"])

if menu == "Pemasangan":
    st.header("Form Pemasangan")
    tanggal = st.date_input("Tanggal", datetime.now().date())
    kode_filter = st.text_input("Kode filter")
    jam_pemasangan = st.time_input("Jam pemasangan")
    flow_awal = st.number_input("Flow Awal", min_value=0.0)
    elapsed_awal = st.number_input("Elapsed Time Awal", min_value=0.0)
    petugas = st.text_input("Nama Petugas Pemasangan")

    if st.button("Simpan Pemasangan"):
        sheet_pemasangan.append_row([
            str(tanggal), kode_filter, str(jam_pemasangan),
            flow_awal, elapsed_awal, petugas
        ])
        st.success("Data pemasangan disimpan ke Google Sheets ✅")

elif menu == "Pelepasan":
    st.header("Form Pelepasan")
    tanggal = st.date_input("Tanggal", datetime.now().date())
    kode_filter = st.text_input("Kode filter")
    jam_pelepasan = st.time_input("Jam pelepasan")
    flow_akhir = st.number_input("Flow Akhir", min_value=0.0)
    elapsed_akhir = st.number_input("Elapsed Time Akhir", min_value=0.0)
    petugas = st.text_input("Nama Petugas Pelepasan")

    if st.button("Simpan Pelepasan"):
        sheet_pelepasan.append_row([
            str(tanggal), kode_filter, str(jam_pelepasan),
            flow_akhir, elapsed_akhir, petugas
        ])
        st.success("Data pelepasan disimpan ke Google Sheets ✅")

elif menu == "Lihat Data":
    st.subheader("Data Pemasangan")
    pemasangan_data = sheet_pemasangan.get_all_values()
    st.dataframe(pemasangan_data)

    st.subheader("Data Pelepasan")
    pelepasan_data = sheet_pelepasan.get_all_values()
    st.dataframe(pelepasan_data)
    st.title("📦 Sampling Filipina")
