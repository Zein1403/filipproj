import streamlit as st
import csv
import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from gspread_formatting import *

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Baca secret dari environment
service_account_info = json.loads(os.environ["GOOGLE_SERVICE_KEY"])

# Buat credential object
creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)

# Authorize gspread
client = gspread.authorize(creds)


sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Sampling filipina")

cell_range = 'E7:J100'  # misalnya data ada di tabel baris 7–100

fmt = CellFormat(
    textFormat=TextFormat(fontFamily='Arial',fontSize=12),
    horizontalAlignment='CENTER',
    verticalAlignment='MIDDLE'
)

# Terapkan format
format_cell_range(sheet, cell_range, fmt)
import streamlit as st

st.title("📦 Sampling Filipina")

#menu = st.sidebar.radio("Menu", ["Pemasangan", "Pelepasan", "Lihat Data"], key="main_menu")
menu = st.selectbox("Pilih Mode", ["Pemasangan", "Pelepasan", "Lihat Data"])

# --- Konfigurasi tabel ---
TABLE_START_ROW = 7  
COLS = {
    "kode_filter": "E",
    "pemasangan": ["F", "G"],   # Flow Awal, Elapsed Awal
    "pelepasan": ["H", "I", "J"]  # Flow Akhir, Elapsed Akhir, Nama Petugas
}

def col_letter_to_index(letter):
    """Convert kolom huruf ke index (E -> 4)"""
    return ord(letter.upper()) - ord("A")

def find_row_by_kode(sheet, kode_filter):
    """Cari baris berdasarkan kode_filter mulai row 7"""
    records = sheet.get_all_values()
    kode_index = col_letter_to_index(COLS["kode_filter"])
    for i in range(TABLE_START_ROW-1, len(records)):
        if len(records[i]) > kode_index and records[i][kode_index] == kode_filter:
            return i + 1
    return None

def find_next_empty_row(sheet):
    """Cari baris kosong baru kalau kode_filter belum ada"""
    col_values = sheet.col_values(col_letter_to_index(COLS["kode_filter"]) + 1)
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
        row_index = find_row_by_kode(sheet, kode_filter)
        if row_index is None:
            row_index = find_next_empty_row(sheet)
            sheet.update(f"{COLS['kode_filter']}{row_index}", [[kode_filter]])

        pemasangan_data = [flow_awal, elapsed_awal]
        sheet.update(f"{COLS['pemasangan'][0]}{row_index}:{COLS['pemasangan'][-1]}{row_index}",
                     [pemasangan_data])
        st.success(f"✅ Data pemasangan untuk {kode_filter} tersimpan di baris {row_index}")

# --- Pelepasan ---
elif menu == "Pelepasan":
    st.subheader("Form Pelepasan")
    kode_filter = st.text_input("Kode Filter")
    flow_akhir = st.text_input("Flow Akhir")
    elapsed_akhir = st.text_input("Elapsed Time Akhir")
    nama_petugas = st.text_input("Nama Petugas Pengganti (jika ada)")

    if st.button("Simpan Pelepasan"):
        row_index = find_row_by_kode(sheet, kode_filter)
        if row_index is None:
            row_index = find_next_empty_row(sheet)
            sheet.update(f"{COLS['kode_filter']}{row_index}", [[kode_filter]])

        pelepasan_data = [flow_akhir, elapsed_akhir, nama_petugas]
        sheet.update(f"{COLS['pelepasan'][0]}{row_index}:{COLS['pelepasan'][-1]}{row_index}",
                     [pelepasan_data])
        st.success(f"✅ Data pelepasan untuk {kode_filter} tersimpan di baris {row_index}")

# --- Lihat Data ---
elif menu == "Lihat Data":
    data = sheet.get_all_values()
    table_data = data[TABLE_START_ROW-4:]  # ambil mulai baris tabel
    st.dataframe(table_data)
