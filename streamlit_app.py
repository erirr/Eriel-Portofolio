import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie
from PIL import Image

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Eriel's Digital Portfolio",
    page_icon="👨‍💻",
    layout="wide",
)

# --- FUNGSI-FUNGSI ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

@st.cache_data
def load_penguin_data():
    url = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv"
    df = pd.read_csv(url)
    df.dropna(inplace=True)
    return df

# --- NAVIGASI SIDEBAR ---
with st.sidebar:
    st.header("Navigasi")
    page = st.radio("Pilih Halaman:", ["Homepage", "Project: Palmer Penguins", "Project: Power BI Sales Dashboard"])

# --- =================== HOMEPAGE =================== ---
if page == "Homepage":
    lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
    
    with st.container():
        left_column, right_column = st.columns((2, 1))
        with left_column:
            st.subheader("Halo, saya Eriel Setiawan Dewantoro 👋")
            st.title("Mahasiswa Teknologi Informasi di Bina Sarana Informatika")
            st.write(
                """
                Saya sangat tertarik dengan cara data dapat digunakan untuk menemukan pola dan cerita. 
                Saat ini, saya fokus mendalami Data Analysis, Data Science, machine learning dan 
                visualisasi data untuk mengubah data kompleks menjadi insight yang mudah dipahami.
                """
            )
            st.write("[Lihat Profil LinkedIn Saya >](https://www.linkedin.com/in/eriel-setiawan-dewantoro/)")
        with right_column:
            st_lottie(lottie_coding, height=300, key="coding")

# --- =================== PROJECT: PALMER PENGUINS (INTERAKTIF) =================== ---
elif page == "Project: Palmer Penguins":
    st.title("🐧 Project Interaktif: Analisis Data Palmer Penguins")
    st.markdown("Dashboard ini memenuhi syarat **visualisasi interaktif**. Gunakan filter di sidebar untuk mengubah grafik.")

    df = load_penguin_data()
    
    st.sidebar.header("Filter Penguins")
    species = st.sidebar.multiselect("Pilih Spesies:", options=df["species"].unique(), default=df["species"].unique())
    island = st.sidebar.multiselect("Pilih Pulau:", options=df["island"].unique(), default=df["island"].unique())
    sex = st.sidebar.multiselect("Pilih Jenis Kelamin:", options=df["sex"].unique(), default=df["sex"].unique())
    
    df_selection = df.query("species == @species & island == @island & sex == @sex")

    if df_selection.empty:
        st.warning("Tidak ada data yang tersedia untuk filter yang dipilih.")
        st.stop()

    st.subheader("📊 Metrik Utama")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Penguins", value=df_selection.shape[0])
    col2.metric(label="Avg. Bill Length (mm)", value=f"{df_selection['bill_length_mm'].mean():.1f}")
    col3.metric(label="Avg. Body Mass (g)", value=f"{df_selection['body_mass_g'].mean() / 1000:.2f} kg")

    st.markdown("---")
    viz_col1, viz_col2 = st.columns(2)
    with viz_col1:
        st.subheader("Panjang vs Kedalaman Paruh")
        st.scatter_chart(data=df_selection, x="bill_length_mm", y="bill_depth_mm", color="species")
    with viz_col2:
        st.subheader("Rata-rata Massa Tubuh per Spesies")
        avg_mass_by_species = df_selection.groupby('species')['body_mass_g'].mean()
        st.bar_chart(avg_mass_by_species)

# --- =================== PROJECT: POWER BI (STUDI KASUS) =================== ---
elif page == "Project: Power BI Sales Dashboard":
    st.title("🚀 Studi Kasus: Beecycle Sales Performance Dashboard")
    st.write("##")

    # Pastikan nama file gambar sama dengan yang kamu simpan
    try:
        image = Image.open(''Screenshot 2025-10-04 230637.png') 
        st.image(image, caption='Dashboard Performa Penjualan Beecycle (2016-2021)', use_column_width=True)
    except FileNotFoundError:
        st.error("File gambar 'dashboard_beecycle.png' tidak ditemukan. Pastikan file tersebut berada di folder yang sama dengan file Python-mu.")
    
    st.markdown("---")
    
    st.subheader("📝 Tentang Proyek Ini")
    st.write(
        """
        Proyek ini adalah studi kasus pembuatan dashboard Business Intelligence untuk menganalisis performa penjualan "Beecycle" selama periode 6 tahun (2016-2021). Dashboard ini merangkum metrik-metrik kunci seperti total pendapatan, profit, dan jumlah pesanan untuk membantu pengambilan keputusan strategis. Analisis mencakup performa produk, segmen pelanggan, dan wilayah geografis.
        """
    )

    st.subheader("🎯 Insight & Temuan Utama")
    st.markdown(
        """
        - **Total Pendapatan:** Mencapai **Rp 77.18 Miliar** dengan profit **Rp 30.47 Miliar**.
        - **Tahun Puncak:** Performa penjualan tertinggi terjadi pada tahun **2019**.
        - **Produk Terlaris:** *Mountain-200 Red, 62* menjadi produk penyumbang pendapatan terbesar.
        - **Wilayah Teratas:** **Australia** merupakan wilayah dengan kontribusi pendapatan tertinggi.
        """
    )
    
    st.subheader("🛠️ Tools yang Digunakan")
    st.info("Microsoft Power BI")
