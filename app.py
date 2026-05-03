import streamlit as st
import pandas as pd

# ======================
# SAFE IMPORT (ANTI BLANK)
# ======================
try:
    from sistem_jadwalkuliah import rekomendasi_jadwal, dosen_mk
except Exception as e:
    st.error("Error saat import sistem_jadwalkuliah.py")
    st.exception(e)
    st.stop()

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Sistem Rekomendasi Jadwal Kuliah Sistem Informasi Semester 4",
    layout="centered"
)

# ======================
# CSS (ADAPTIF)
# ======================
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    opacity: 0.7;
    margin-bottom: 25px;
}

.card {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,0.2);
    margin-bottom: 20px;
}

.stButton>button {
    border-radius: 8px;
    height: 45px;
    width: 100%;
    font-weight: 600;
}

.stTextInput>div>div>input {
    border-radius: 8px;
}

.stSelectbox>div>div {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================
st.markdown('<div class="title">Sistem Rekomendasi Jadwal Kuliah</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Rekomendasi jadwal berdasarkan preferensi dosen dan constraint penjadwalan</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Kelompok 2 - Sistem Cerdas</div>', unsafe_allow_html=True)

# ======================
# SESSION STATE
# ======================
if "hasil" not in st.session_state:
    st.session_state.hasil = None

# ======================
# INPUT
# ======================
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("Input Data")

nama_dosen = st.selectbox("Dosen", list(dosen_mk.keys()))
mk = st.selectbox("Mata Kuliah", dosen_mk[nama_dosen])
preferensi_jam = st.text_input("Preferensi Jam (contoh: 09.00)")

if st.button("Generate Rekomendasi"):
    if preferensi_jam.strip() == "":
        st.warning("Masukkan jam terlebih dahulu")
    else:
        try:
            hasil = rekomendasi_jadwal(nama_dosen, preferensi_jam)
            st.session_state.hasil = hasil
        except Exception as e:
            st.error("Terjadi error saat generate rekomendasi")
            st.exception(e)

st.markdown('</div>', unsafe_allow_html=True)

# ======================
# OUTPUT
# ======================
if st.session_state.hasil:

    df = pd.DataFrame(st.session_state.hasil)

    if not df.empty:
        df["Score"] = df["Score"].round(2)

        # TOP
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Rekomendasi Utama")
        st.dataframe(df.head(5), use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ALT
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Alternatif Jadwal")
        st.dataframe(df.iloc[5:], use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # DOWNLOAD
        csv = df.to_csv(index=False)

        st.download_button(
            "Download Hasil",
            csv,
            "rekomendasi_jadwal.csv",
            "text/csv"
        )
    else:
        st.warning("Tidak ada rekomendasi ditemukan.")
