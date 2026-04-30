import streamlit as st
import google.generativeai as genai
import pandas as pd
import os
from datetime import datetime

# 1. SETUP API & DATABASE
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash') 
except Exception as e:
    st.error("⚠️ API Key Gemini belum terpasang!")

DB_FILE = "database_batin.csv"
if not os.path.exists(DB_FILE):
    df_awal = pd.DataFrame(columns=["Tanggal", "Kelas", "Nama Siswa", "Status Awal", "Refleksi", "Analisis AI"])
    df_awal.to_csv(DB_FILE, index=False)

# 2. PENGATURAN HALAMAN
st.set_page_config(page_title="Berchmans Spirit Center", page_icon="🕊️", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    h1, h2, h3 { color: #003366; } 
    .stButton>button { background-color: #003366; color: white; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 3. NAVIGASI
st.sidebar.title("🕊️ Berchmans Lite")
st.sidebar.write("Head of Campus Ministry Portal")
menu = st.sidebar.radio("Navigasi:", ["Data Input Center", "Student Tracker", "AI Dashboard"])

# 4. HALAMAN INPUT & ANALISIS
if menu == "Data Input Center":
    st.title("Data Input Center 📥")
    st.write("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 Bulk Excel Import (Coming Soon)")
        st.info("Upload file template CSV lu di sini. (Sedang dibangun)")
            
    with col2:
        st.markdown("### ✍️ Manual Entry & AI Analysis")
        kelas = st.selectbox("Pilih Kelas", ["Kelas 7A", "Kelas 8B", "Kelas 9A", "Kelas 10C", "Kelas 12A"])
        nama = st.text_input("Nama Siswa")
        batin = st.radio("Dominasi Batin (Self-Reported)", ["Konsolasi", "Desolasi"], horizontal=True)
        refleksi = st.text_area("Teks Refleksi Siswa")
        
        if st.button("Simpan & Analisis"):
            if nama and refleksi:
                with st.spinner('Gemini sedang menganalisis batin siswa... 🧠'):
                    prompt = f"Sebagai pendelor pastoral, analisis refleksi ini. Nama: {nama}. Refleksi: '{refleksi}'. Berikan 1 kata kunci masalah/kebahagiaan, dan 1 kalimat saran pendampingan."
                    try:
                        response = model.generate_content(prompt)
                        hasil_ai = response.text
                        
                        # Simpan ke Database CSV
                        df = pd.read_csv(DB_FILE)
                        data_baru = pd.DataFrame([{
                            "Tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "Kelas": kelas,
                            "Nama Siswa": nama,
                            "Status Awal": batin,
                            "Refleksi": refleksi,
                            "Analisis AI": hasil_ai
                        }])
                        df = pd.concat([df, data_baru], ignore_index=True)
                        df.to_csv(DB_FILE, index=False)
                        
                        st.success(f"✅ Data {nama} berhasil disimpan ke Database!")
                        st.info(hasil_ai)
                    except Exception as e:
                        st.error(f"Gagal memproses AI: {e}")
            else:
                st.error("Nama dan Refleksi wajib diisi!")

# 5. HALAMAN DATABASE TRACKER
elif menu == "Student Tracker":
    st.title("Student Insights Directory 🔍")
    st.write("Ini adalah database mentah hasil input lu. Lu bisa download ini nanti untuk laporan unit atau bahan penelitian.")
    
    try:
        df = pd.read_csv(DB_FILE)
        if df.empty:
            st.warning("Database masih kosong. Silakan input data di menu 'Data Input Center' dulu.")
        else:
            # Menampilkan tabel database
            st.dataframe(df, use_container_width=True)
    except FileNotFoundError:
        st.error("Database belum terbentuk.")

# 6. HALAMAN DASHBOARD (Draft)
elif menu == "AI Dashboard":
    st.title("AI Dashboard 🧠")
    st.info("Di sini nanti akan muncul grafik tren batin sekolah berdasarkan database.")
    try:
        df = pd.read_csv(DB_FILE)
        if not df.empty:
            jumlah_konsolasi = len(df[df['Status Awal'] == 'Konsolasi'])
            jumlah_desolasi = len(df[df['Status Awal'] == 'Desolasi'])
            
            col1, col2 = st.columns(2)
            col1.metric("Total Konsolasi", jumlah_konsolasi)
            col2.metric("Total Desolasi", jumlah_desolasi)
    except:
        pass
