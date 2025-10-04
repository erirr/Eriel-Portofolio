import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="My Digital Portfolio",
    page_icon="👨‍💻",
    layout="wide",
)

# --- FUNGSI UNTUK LOTTIE ANIMATION ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- FUNGSI UNTUK MEMUAT DATA PENGUIN ---
@st.cache_data
def load_penguin_data():
    url = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv"
    df = pd.read_csv(url)
    df.dropna(inplace=True)
    return df

# --- NAVIGASI SIDEBAR ---
with st.sidebar:
    st.header("Navigasi")
    page = st.radio("Pilih Halaman:", ["Homepage", "Project: Palmer Penguins"])

# --- =================== HOMEPAGE =================== ---
if page == "Homepage":
    lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
    
    # --- HEADER SECTION ---
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader("Halo, saya [Nama Kamu] 👋")
            st.title("Seorang Mahasiswa Teknologi Informasi")
            st.write(
                "Saya bersemangat dalam bidang Data Analytics dan Machine Learning. "
                "Saat ini sedang mendalami berbagai teknologi untuk membangun solusi berbasis data yang inovatif."
            )
            st.write("[Lihat LinkedIn Saya >](https://www.linkedin.com/in/username-anda/)")
        with right_column:
            st_lottie(lottie_coding, height=300, key="coding")

    st.markdown("---")

    # --- KEAHLIAN SAYA ---
    with st.container():
        st.header("Keahlian Saya 🛠️")
        st.write("##")
        skill_col1, skill_col2, skill_col3 = st.columns(3)
        with skill_col1:
            st.subheader("Data Analysis")
            st.write("- Python (Pandas, NumPy)\n- SQL\n- Matplotlib, Seaborn")
        with skill_col2:
            st.subheader("Data Science")
            st.write("- Machine Learning (Scikit-learn)\n- Hypothesis Testing\n- Jupyter Notebook")
        with skill_col3:
            st.subheader("Tools")
            st.write("- Git & GitHub\n- Streamlit Cloud\n- VSCode")
    
    st.markdown("---")

    # --- HUBUNGI SAYA ---
    with st.container():
        st.header("Hubungi Saya 📬")
        contact_form = """
        <form action="https://formsubmit.co/your-email@email.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Nama Anda" required>
            <input type="email" name="email" placeholder="Email Anda" required>
            <textarea name="message" placeholder="Pesan Anda" required></textarea>
            <button type="submit">Kirim</button>
        </form>
        """
        st.markdown(contact_form, unsafe_allow_html=True)

# --- =================== PROJECT: PALMER PENGUINS =================== ---
elif page == "Project: Palmer Penguins":
    st.title("🐧 Project: Palmer Penguins Data Analysis")
    st.markdown("""
    Dashboard ini melakukan analisis eksplorasi data (EDA) sederhana pada dataset Palmer Penguins.
    Gunakan filter di sidebar untuk menjelajahi hubungan antar variabel.
    """)

    df = load_penguin_data()
    
    # --- SIDEBAR KHUSUS UNTUK FILTER PENGUIN ---
    st.sidebar.header("Filter Your Penguins")
    species = st.sidebar.multiselect("Select Species", options=df["species"].unique())
    island = st.sidebar.multiselect("Select Island", options=df["island"].unique())
    sex = st.sidebar.multiselect("Select Sex", options=df["sex"].unique())
    min_mass, max_mass = int(df["body_mass_g"].min()), int(df["body_mass_g"].max())
    body_mass_slider = st.sidebar.slider("Select Body Mass (g)", min_value=min_mass, max_value=max_mass, value=(min_mass, max_mass))

    # --- FILTERING DATAFRAME ---
    df_selection = df.copy()
    if species: df_selection = df_selection[df_selection["species"].isin(species)]
    if island: df_selection = df_selection[df_selection["island"].isin(island)]
    if sex: df_selection = df_selection[df_selection["sex"].isin(sex)]
    df_selection = df_selection[(df_selection["body_mass_g"] >= body_mass_slider[0]) & (df_selection["body_mass_g"] <= body_mass_slider[1])]

    if df_selection.empty:
        st.warning("No data available for the selected filters.")
        st.stop()

    # --- KONTEN UTAMA HALAMAN PENGUIN ---
    st.subheader("📊 Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Penguins", value=df_selection.shape[0])
    col2.metric(label="Avg. Bill Length (mm)", value=round(df_selection["bill_length_mm"].mean(), 1))
    col3.metric(label="Avg. Body Mass (g)", value=f"{round(df_selection['body_mass_g'].mean() / 1000, 2)} kg")

    st.markdown("---")

    # --- VISUALISASI ---
    st.subheader("📈 Visualizations")
    viz_col1, viz_col2 = st.columns(2)
    with viz_col1:
        st.subheader("Bill Length vs. Bill Depth")
        st.scatter_chart(data=df_selection, x="bill_length_mm", y="bill_depth_mm", color="species")
    with viz_col2:
        st.subheader("Average Body Mass by Species")
        avg_mass_by_species = df_selection.groupby('species')['body_mass_g'].mean()
        st.bar_chart(avg_mass_by_species)

    # --- DATA MENTAH ---
    with st.expander("View Raw Data"):
        st.dataframe(df_selection)

st.markdown("---")
