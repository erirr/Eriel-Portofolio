# =================================================================================
# Import library yang dibutuhkan
# =================================================================================
import streamlit as st
import pandas as pd

# =================================================================================
# Konfigurasi Halaman & Judul
# =================================================================================
st.set_page_config(
    page_title='Dashboard Analisis Penjualan Sepeda',
    page_icon='🚴',
    layout='wide'
)

st.title('🚴 Dashboard Analisis Penjualan Sepeda')
st.write('Ini adalah portofolio untuk tugas *Building Portfolio with Streamlit*.')
st.write('---')

# =================================================================================
# Fungsi untuk Memuat Data
# =================================================================================
# Menggunakan cache agar data hanya di-load sekali
@st.cache_data
def load_data():
    # Pastikan nama file CSV sesuai dengan yang kamu miliki
    df = pd.read_csv('dataset_bee_cycle (4).xlsx - Sheet1.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

# Memuat data
df_sales = load_data()

# =================================================================================
# Bagian Visualisasi Interaktif
# =================================================================================
st.header('Visualisasi Interaktif Penjualan Produk')

# --- Filter ---
st.write("Pilih kategori produk untuk melihat detail penjualan:")
category_options = df_sales['category'].unique()
selected_category = st.selectbox(
    label='Pilih Kategori Produk:',
    options=category_options
)

# --- Proses Filter Data ---
filtered_df = df_sales[df_sales['category'] == selected_category]

# --- Tampilkan Visualisasi ---
# Membuat agregasi data (total penjualan per sub-kategori)
sales_by_subcategory = filtered_df.groupby('sub_category')['totalprice_rupiah'].sum().sort_values(ascending=False)

st.write(f"#### Total Penjualan untuk Kategori: **{selected_category}**")

# Menggunakan kolom agar terlihat lebih rapi
col1, col2 = st.columns([0.6, 0.4]) # [lebar_grafik, lebar_tabel]

with col1:
    st.bar_chart(sales_by_subcategory)

with col2:
    st.write("Data Agregat:")
    st.dataframe(sales_by_subcategory)

st.write("---")

# =================================================================================
# Menampilkan Data Mentah
# =================================================================================
st.header('Cuplikan Data Penjualan')
st.write("Berikut adalah 5 baris pertama dari dataset yang digunakan.")
st.dataframe(df_sales.head())
