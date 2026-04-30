import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
import pandas as pd
import os
import time
from datetime import datetime

# 1. SETUP PAGE
st.set_page_config(page_title="Berchmans Spirit Center", page_icon="🕊️", layout="wide", initial_sidebar_state="expanded")

# 2. SETUP API & RADAR MODEL OTOMATIS
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    valid_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            valid_models.append(m.name)
    if valid_models:
        model_name = valid_models[0].replace("models/", "")
        model = genai.GenerativeModel(model_name)
    else:
        st.error("⚠️ Gak dapet akses model Gemini. Coba cek API Key lu.")
except Exception as e:
    st.error(f"⚠️ Masalah koneksi API: {e}")

# 3. SETUP DATABASE LOKAL
DB_MASTER = "master_siswa.csv"
DB_BATIN = "database_batin.csv"

if not os.path.exists(DB_MASTER):
    pd.DataFrame(columns=["Nama Siswa", "Kelas", "Unit"]).to_csv(DB_MASTER, index=False)
if not os.path.exists(DB_BATIN):
    pd.DataFrame(columns=["Tanggal", "Unit", "Kelas", "Nama Siswa", "Status Awal", "Refleksi", "Analisis AI"]).to_csv(DB_BATIN, index=False)

# 4. TEMA & WARNA 
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    h1, h2, h3 { color: #002244; } 
    .stButton>button { background-color: #002244; color: white; border-radius: 8px; border: none; }
    .stButton>button:hover { background-color: #d4af37; color: #002244; }
    [data-testid="stSidebar"] { background-color: #001f3f !important; }
    [data-testid="stSidebarNav"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# 5. SIDEBAR NAVIGASI
with st.sidebar:
    st.markdown('<p style="color:#8ba1b5; font-size:12px; font-weight:700; letter-spacing:1.5px; margin-bottom: 0px; margin-left: 15px;">MAIN MENU</p>', unsafe_allow_html=True)
    menu = option_menu(
        menu_title=None,
        options=["AI Dashboard", "Data Input Center", "Student Tracker", "Database Management"],
        icons=["grid", "server", "people", "hdd-stack"], 
        default_index=1, 
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#e0e0e0", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"5px", "color": "#e0e0e0", "--hover-color": "#003366"},
            "nav-link-selected": {"background-color": "#dca235", "color": "#001f3f", "font-weight": "bold", "border-radius": "8px"},
        }
    )

# ==========================================
# HALAMAN 1: AI DASHBOARD
# ==========================================
if menu == "AI Dashboard":
    st.title("AI Dashboard 🧠")
    try:
        df = pd.read_csv(DB_BATIN)
        if not df.empty:
            jumlah_konsolasi = len(df[df['Status Awal'] == 'Konsolasi'])
            jumlah_desolasi = len(df[df['Status Awal'] == 'Desolasi'])
            
            col1, col2 = st.columns(2)
            col1.metric("Total Konsolasi", jumlah_konsolasi)
            col2.metric("Total Desolasi", jumlah_desolasi)
        else:
            st.info("Belum ada data untuk ditampilkan grafiknya.")
    except:
        pass

# ==========================================
# HALAMAN 2: DATA INPUT CENTER
# ==========================================
elif menu == "Data Input Center":
    st.title("Data Input Center 📥")
    st.write("---")
    
    df_master = pd.read_csv(DB_MASTER)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 Bulk Excel Import & AI")
        st.info("Upload Template Refleksi yang udah diisi banyak orang. AI akan menganalisis semuanya sekaligus!")
        file_refleksi = st.file_uploader("Upload File Refleksi (CSV/Excel)", type=['csv', 'xlsx'], key="bulk")
        
        if file_refleksi:
            if st.button("🚀 Jalankan Analisis AI Massal"):
                if file_refleksi.name.endswith('.csv'):
                    df_bulk = pd.read_csv(file_refleksi)
                else:
                    df_bulk = pd.read_excel(file_refleksi)
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                df_batin = pd.read_csv(DB_BATIN)
                data_baru_list = []
                
                for i, row in df_bulk.iterrows():
                    nama = row.get('Nama Lengkap', row.get('Nama Siswa', 'Anonim'))
                    unit = row.get('Unit', '-')
                    kelas = row.get('Kelas', '-')
                    batin = row.get('Dominasi Batin', 'Tidak Diketahui')
                    refleksi = row.get('Teks Refleksi', '')
                    
                    status_text.text(f"Sedang menganalisis {nama}...")
                    
                    if str(refleksi).strip() and str(refleksi).lower() != 'nan':
                        prompt = f"Sebagai pendelor pastoral, analisis refleksi ini. Nama: {nama}. Refleksi: '{refleksi}'. Berikan 1 kata kunci masalah/kebahagiaan, dan 1 kalimat saran pendampingan."
                        try:
                            response = model.generate_content(prompt)
                            hasil_ai = response.text
                            time.sleep(2) 
                        except Exception as e:
                            hasil_ai = "Gagal dianalisis AI"
                    else:
                        hasil_ai = "Tidak ada teks refleksi."
                        
                    data_baru_list.append({
                        "Tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Unit": unit,
                        "Kelas": kelas,
                        "Nama Siswa": nama,
                        "Status Awal": batin,
                        "Refleksi": refleksi,
                        "Analisis AI": hasil_ai
                    })
                    progress_bar.progress((i + 1) / len(df_bulk))
                
                df_baru = pd.DataFrame(data_baru_list)
                df_batin = pd.concat([df_batin, df_baru], ignore_index=True)
                df_batin.to_csv(DB_BATIN, index=False)
                status_text.text("✅ Analisis massal selesai!")
                st.success(f"{len(df_bulk)} data refleksi berhasil dianalisis dan masuk database!")

    with col2:
        st.markdown("### ✍️ Manual Entry & AI Analysis")
        if df_master.empty:
            st.warning("⚠️ Upload Data Master dulu di menu 'Database Management' biar bisa pilih nama otomatis!")
        else:
            # 1. Pilih Unit Dulu
            list_unit = df_master['Unit'].dropna().unique().tolist()
            unit_terpilih = st.selectbox("Pilih Unit", sorted(list_unit))
            
            df_unit_itu = df_master[df_master['Unit'] == unit_terpilih]
            
            # 2. Cek apakah Unit ini punya Kelas (Kalau Guru/Staff biasanya kosong/NaN)
            list_kelas = [k for k in df_unit_itu['Kelas'].unique() if pd.notna(k) and str(k).strip() != '']
            
            if list_kelas:
                # Jika ada kelas (Siswa)
                kelas_terpilih = st.selectbox("Pilih Kelas", sorted(list_kelas))
                df_final = df_unit_itu[df_unit_itu['Kelas'] == kelas_terpilih]
            else:
                # Jika tidak ada kelas (Guru/Staff)
                kelas_terpilih = "-"
                df_final = df_unit_itu
                
            # 3. Pilih Nama sesuai filter di atas
            list_nama = df_final['Nama Siswa'].dropna().tolist()
            nama_terpilih = st.selectbox("Pilih Nama", sorted(list_nama))
            
            batin = st.radio("Dominasi Batin (Self-Reported)", ["Konsolasi", "Desolasi"], horizontal=True)
            refleksi = st.text_area("Teks Refleksi")
            
            if st.button("Simpan & Analisis"):
                if refleksi:
                    with st.spinner(f'Gemini sedang menganalisis batin {nama_terpilih}... 🧠'):
                        prompt = f"Sebagai pendelor pastoral, analisis refleksi ini. Nama: {nama_terpilih}. Refleksi: '{refleksi}'. Berikan 1 kata kunci masalah/kebahagiaan, dan 1 kalimat saran pendampingan."
                        try:
                            response = model.generate_content(prompt)
                            hasil_ai = response.text
                            
                            df = pd.read_csv(DB_BATIN)
                            data_baru = pd.DataFrame([{
                                "Tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "Unit": unit_terpilih,
                                "Kelas": kelas_terpilih,
                                "Nama Siswa": nama_terpilih,
                                "Status Awal": batin,
                                "Refleksi": refleksi,
                                "Analisis AI": hasil_ai
                            }])
                            df = pd.concat([df, data_baru], ignore_index=True)
                            df.to_csv(DB_BATIN, index=False)
                            
                            st.success(f"✅ Data {nama_terpilih} berhasil disimpan ke Database!")
                            st.info(hasil_ai)
                        except Exception as e:
                            st.error(f"Gagal memproses AI: {e}")
                else:
                    st.error("Teks Refleksi wajib diisi!")

# ==========================================
# HALAMAN 3: STUDENT TRACKER
# ==========================================
elif menu == "Student Tracker":
    st.title("Student Insights Directory 🔍")
    try:
        df = pd.read_csv(DB_BATIN)
        if df.empty:
            st.warning("Database refleksi masih kosong.")
        else:
            st.dataframe(df, use_container_width=True)
    except FileNotFoundError:
        st.error("Database belum terbentuk.")

# ==========================================
# HALAMAN 4: DATABASE MANAGEMENT
# ==========================================
elif menu == "Database Management":
    st.title("Manajemen Database Siswa & Staff 🗃️")
    st.write("Upload Excel/CSV berisi daftar nama se-sekolah di sini supaya otomatis masuk ke sistem.")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.info("Pastikan file lu punya kolom: **Nama Siswa**, **Unit**, dan **Kelas**. *(Kosongkan kolom Kelas untuk Guru/Staff)*")
        file_master = st.file_uploader("Upload Data (CSV/Excel)", type=['csv', 'xlsx'])
        
        if file_master:
            try:
                if file_master.name.endswith('.csv'):
                    df_upload = pd.read_csv(file_master)
                else:
                    df_upload = pd.read_excel(file_master)
                
                if st.button("Simpan ke Master Database"):
                    df_upload.to_csv(DB_MASTER, index=False)
                    st.success("✅ Master Data berhasil diperbarui!")
            except Exception as e:
                st.error(f"Gagal baca file: {e}")
                
    with col2:
        st.markdown("### Isi Master Data Saat Ini:")
        df_master = pd.read_csv(DB_MASTER)
        if not df_master.empty:
            st.dataframe(df_master, use_container_width=True)
        else:
            st.warning("Data Master masih kosong Bro!")
