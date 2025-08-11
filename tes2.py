import streamlit as st
import csv
import os
from datetime import datetime

# File names
filename_pemasangan = "pemasangan.csv"
filename_pelepasan = "pelepasan.csv"

# Save CSV row (append mode, no duplicate check)
def save_to_file(file_path, row, fieldnames):
    file_exists = os.path.exists(file_path)
    with open(file_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

# Load CSV for viewing
def load_csv(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', newline='') as f:
            return list(csv.DictReader(f))
    return []

# Menu selection
menu = st.sidebar.selectbox("Menu", ["Pemasangan", "Pelepasan", "Lihat CSV"])

# ----- PEMASANGAN -----
if menu == "Pemasangan":
    st.header("Input Pemasangan")
    tanggal = st.date_input("Tanggal", datetime.now().date())
    kode_filter = st.text_input("Kode filter")
    jam_pemasangan = st.text_input("Jam pemasangan (HH:MM)", value="08:00")
    flow_awal = st.number_input("Flow Awal")
    elapsed_awal = st.number_input("Elapsed Time Awal")
    nama_petugas = st.text_input("Nama Petugas Pemasangan")

    if st.button("Simpan Pemasangan"):
        save_to_file(filename_pemasangan, {
            'Tanggal': tanggal,
            'Kode filter': kode_filter,
            'Jam pemasangan': jam_pemasangan,
            'Flow Awal': flow_awal,
            'Elapsed Time Awal': elapsed_awal,
            'Nama Petugas Pemasangan': nama_petugas
        }, ['Tanggal','Kode filter','Jam pemasangan','Flow Awal','Elapsed Time Awal','Nama Petugas Pemasangan'])
        st.success("✅ Data pemasangan tersimpan.")

# ----- PELEPASAN -----
elif menu == "Pelepasan":
    st.header("Input Pelepasan")
    tanggal = st.date_input("Tanggal", datetime.now().date())
    kode_filter = st.text_input("Kode filter")
    jam_pelepasan = st.text_input("Jam pelepasan",value="08:00")
    flow_akhir = st.number_input("Flow Akhir")
    elapsed_akhir = st.number_input("Elapsed Time Akhir")
    nama_petugas = st.text_input("Nama Petugas Pelepasan")

    if st.button("Simpan Pelepasan"):
        save_to_file(filename_pelepasan, {
            'Tanggal': tanggal,
            'Kode filter': kode_filter,
            'Jam pelepasan': jam_pelepasan,
            'Flow Akhir': flow_akhir,
            'Elapsed Time Akhir': elapsed_akhir,
            'Nama Petugas Pelepasan': nama_petugas
        }, ['Tanggal','Kode filter','Jam pelepasan','Flow Akhir','Elapsed Time Akhir','Nama Petugas Pelepasan'])
        st.success("✅ Data pelepasan tersimpan.")

# ----- LIHAT CSV -----
elif menu == "Lihat CSV":
    st.header("📄 Lihat Data CSV")

    csv_choice = st.radio("Pilih file yang ingin dilihat:", ["Pemasangan", "Pelepasan"])
    
    if csv_choice == "Pemasangan":
        data = load_csv(filename_pemasangan)
        if data:
            st.write("### Data Pemasangan")
            st.dataframe(data)
        else:
            st.warning("Belum ada data pemasangan.")

    elif csv_choice == "Pelepasan":
        data = load_csv(filename_pelepasan)
        if data:
            st.write("### Data Pelepasan")
            st.dataframe(data)
        else:
            st.warning("Belum ada data pelepasan.")
