# Import library yang dibutuhkan
import streamlit as st
import pandas as pd

# 1. Judul Aplikasi (st.title)
st.title('Portofolio Analisis Data Sederhana')

# 2. Header (st.header)
st.header('Proyek Analisis Data Penjualan 📈')

# 3. Teks biasa (st.write atau st.text)
st.write(
    """
    Halo! Selamat datang di portofolio interaktifku. 
    Di bawah ini adalah contoh proyek analisis data yang pernah aku kerjakan.
    """
)

# 4. Menampilkan Gambar (st.image)
# Pastikan kamu punya file gambar (misal: 'profile.jpg') di dalam folder yang sama
try:
    st.image('profile.jpg', caption='Ini foto profilku!', width=200)
except FileNotFoundError:
    st.warning("Gambar tidak ditemukan! Pastikan ada file 'profile.jpg' di folder proyek.")


# 5. Menampilkan DataFrame (st.dataframe)
# Kita buat data bohongan dulu pakai Pandas
data = {
    'Produk': ['Buku', 'Pensil', 'Penghapus', 'Penggaris'],
    'Jumlah Terjual': [120, 350, 80, 210],
    'Harga Satuan': [25000, 2000, 1500, 5000]
}
df = pd.DataFrame(data)

st.write("Berikut adalah contoh data penjualan dalam bentuk tabel:")
st.dataframe(df)
