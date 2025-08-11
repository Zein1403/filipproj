import streamlit as st
import csv
import os
from datetime import datetime

# File names
filename_pemasangan = 'Pemasangan.csv'
filename_pelepasan = 'Pelepasan.csv'

# Create CSV with header if not exists
if not os.path.exists(filename_pemasangan):
    with open(filename_pemasangan, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Tanggal Pemasangan', 'Kode filter', 'Jam pemasangan', 'Flow Awal', 'Elapsed Time Awal', 'Nama Petugas Pemasangan'])

if not os.path.exists(filename_pelepasan):
    with open(filename_pelepasan, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Tanggal Pelepasan', 'Kode filter', 'Jam pelepasan', 'Flow Akhir', 'Elapsed Time Akhir', 'Nama Petugas Pelepasan'])

st.title("📦 Sampling Filipina")

# Sidebar menu
menu = st.sidebar.radio("Menu", ["Pemasangan", "Pelepasan", "Lihat CSV"])

# Load CSV data
def load_data(file_path):
    with open(file_path, 'r', newline='') as f:
        return list(csv.DictReader(f))

if menu == "Pemasangan":
    data = load_data(filename_pemasangan)
elif menu == "Pelepasan":
    data = load_data(filename_pelepasan)

# Save CSV data
def save_data(file_path, rows, fieldnames):
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

if menu == "Pemasangan":
    fieldnames = ['Tanggal Peamasangan','Kode filter', 'Jam pemasangan', 'Flow Awal', 'Elapsed Time Awal','Nama Petugas Pemasangan']
    save_data(filename_pemasangan, data, fieldnames)

elif menu == "Pelepasan":
    fieldnames = ['Tanggal Pelepasan','Kode filter', 'Jam pelepasan', 'Flow Akhir', 'Elapsed Time Akhir','Nama Petugas Pelepasan']
    save_data(filename_pelepasan, data, fieldnames)

if menu == "Pemasangan" :
    st.header("Pemasangan")
    kode = st.text_input
    flow = st.number_input
    elapsed = st.number_input
    petugas =st.text_input
    tanggal = datetime.now().strftime("%Y-%m-%d ")
    jam = datetime.now().strftime("%H:%M:%S")

    if st.button("Simpan"):
        save_data_append('Pemasangan.csv', {
            
            'Tanggal Peamasangan' : tanggal,
            'Kode filter' : kode,
            'Jam pemasangan' : jam,
            'Flow Awal' : flow,
            'Elapsed Time Awal' : elapsed,
            'Nama Petugas Pemasangan' : petugas
            
        })
        st.success("Data berhasil disimpan (tanpa cek duplikat)")


if menu == "Pelepasan" :
    st.header("Pelepasan")
    kode = st.text_input
    flow = st.number_input
    elapsed = st.number_input
    petugas =st.text_input
    tanggal = datetime.now().strftime("%Y-%m-%d ")
    jam = datetime.now().strftime("%H:%M:%S")

    if st.button("Simpan"):
        save_data_append('Pemasangan.csv', {
            
            'Tanggal Pelepasan' : tanggal,
            'Kode filter' : kode,
            'Jam pelepasan' : jam,
            'Flow Akhir' : flow,
            'Elapsed Time Akhir' : elapsed,
            'Nama Petugas pelepas' : petugas
            
        })
        st.success("Data berhasil disimpan (tanpa cek duplikat)")

elif menu == "Lihat CSV":
    st.header("📄 Data Inventory")
    rows = load_data()
    if rows:
        st.dataframe(rows)
    else:
        st.info("📂 Data masih kosong.")
