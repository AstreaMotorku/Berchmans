import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
import pandas as pd
import plotly.express as px
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
    pd.DataFrame(columns=["Tanggal", "Unit", "Kelas", "Nama Siswa", "Status Awal", "Refleksi"]).to_csv(DB_BATIN, index=False)

# 4. TEMA & WARNA 
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    h1, h2, h3 { color: #002244; } 
    .stButton>button { background-color: #002244; color: white; border-radius: 8px; border: none; }
    .stButton>button:hover { background-color: #d4af37; color: #002244; }
    [data-testid="stSidebar"] { background-color: #001f3f !important; }
    [data-testid="stSidebarNav"] {display: none;}
    [data-testid="stMetricValue"] { color: #d4af37; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 5. SIDEBAR NAVIGASI
with st.sidebar:
    st.markdown('<p style="color:#8ba1b5; font-size:12px; font-weight:700; letter-spacing:1.5px; margin-bottom: 0px; margin-left: 15px;">MAIN MENU</p>', unsafe_allow_html=True)
    menu = option_menu(
        menu_title=None,
        options=["AI Dashboard", "Data Input Center", "Student Insights (AI)", "Database Management"],
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
    st.markdown("Ringkasan pergerakan batin komunitas sekolah berdasarkan data refleksi.")
    st.write("---")
    
    try:
        df = pd.read_csv(DB_BATIN)
        if not df.empty:
            jumlah_konsolasi = len(df[df['Status Awal'] == 'Konsolasi'])
            jumlah_desolasi = len(df[df['Status Awal'] == 'Desolasi'])
            total_data = len(df)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Refleksi Masuk", total_data)
            col2.metric("Dominasi Konsolasi", f"{jumlah_konsolasi} Laporan")
            col3.metric("Dominasi Desolasi", f"{jumlah_desolasi} Laporan")
            
            st.write("---")
            
            col_chart1, col_chart2 = st.columns([1, 1.5])
            
            with col_chart1:
                st.markdown("#### Persentase Batin Global")
                fig_pie = px.pie(
                    df, names='Status Awal', color='Status Awal',
                    color_discrete_map={'Konsolasi':'#27ae60', 'Desolasi':'#c0392b'}, hole=0.4
                )
                fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig_pie, use_container_width=True)
                
            with col_chart2:
                st.markdown("#### Sebaran Batin per Unit")
                df_unit = df.groupby(['Unit', 'Status Awal']).size().reset_index(name='Jumlah')
                fig_bar = px.bar(
                    df_unit, x='Unit', y='Jumlah', color='Status Awal', barmode='group',
                    color_discrete_map={'Konsolasi':'#27ae60', 'Desolasi':'#c0392b'}
                )
                fig_bar.update_layout(margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Belum ada data refleksi yang masuk.")
    except Exception as e:
        st.error(f"Gagal memuat Dashboard: {e}")

# ==========================================
# HALAMAN 2: DATA INPUT CENTER (FAST ENTRY!)
# ==========================================
elif menu == "Data Input Center":
    st.title("Data Input Center 📥")
    st.write("Input harian sekarang super cepat. AI tidak akan langsung menganalisis agar sistem tidak berat. Analisis AI bisa dilakukan mingguan di menu Student Insights.")
    st.write("---")
    
    df_master = pd.read_csv(DB_MASTER)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 Bulk Excel Import (Fast Save)")
        file_refleksi = st.file_uploader("Upload File Refleksi (CSV/Excel)", type=['csv', 'xlsx'], key="bulk")
        
        if file_refleksi:
            if st.button("🚀 Simpan Massal ke Database"):
                if file_refleksi.name.endswith('.csv'):
                    df_bulk = pd.read_csv(file_refleksi)
                else:
                    df_bulk = pd.read_excel(file_refleksi)
                
                df_batin = pd.read_csv(DB_BATIN)
                data_baru_list = []
                
                for i, row in df_bulk.iterrows():
                    data_baru_list.append({
                        "Tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Unit": row.get('Unit', '-'),
                        "Kelas": row.get('Kelas', '-'),
                        "Nama Siswa": row.get('Nama Lengkap', row.get('Nama Siswa', 'Anonim')),
                        "Status Awal": row.get('Dominasi Batin', 'Tidak Diketahui'),
                        "Refleksi": row.get('Teks Refleksi', '')
                    })
                
                df_baru = pd.DataFrame(data_baru_list)
                df_batin = pd.concat([df_batin, df_baru], ignore_index=True)
                df_batin.to_csv(DB_BATIN, index=False)
                st.success(f"✅ {len(df_bulk)} data berhasil disimpan secara instan!")

    with col2:
        st.markdown("### ✍️ Manual Daily Entry")
        if df_master.empty:
            st.warning("⚠️ Upload Data Master dulu di menu 'Database Management'!")
        else:
            list_unit = df_master['Unit'].dropna().unique().tolist()
            unit_terpilih = st.selectbox("Pilih Unit", sorted(list_unit))
            df_unit_itu = df_master[df_master['Unit'] == unit_terpilih]
            
            list_kelas = [k for k in df_unit_itu['Kelas'].unique() if pd.notna(k) and str(k).strip() != '']
            if list_kelas:
                kelas_terpilih = st.selectbox("Pilih Kelas", sorted(list_kelas))
                df_final = df_unit_itu[df_unit_itu['Kelas'] == kelas_terpilih]
            else:
                kelas_terpilih = "-"
                df_final = df_unit_itu
                
            list_nama = df_final['Nama Siswa'].dropna().tolist()
            nama_terpilih = st.selectbox("Pilih Nama", sorted(list_nama))
            
            batin = st.radio("Dominasi Batin (Self-Reported)", ["Konsolasi", "Desolasi"], horizontal=True)
            refleksi = st.text_area("Teks Refleksi Harian")
            
            if st.button("Simpan Laporan Harian"):
                if refleksi:
                    df = pd.read_csv(DB_BATIN)
                    data_baru = pd.DataFrame([{
                        "Tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Unit": unit_terpilih,
                        "Kelas": kelas_terpilih,
                        "Nama Siswa": nama_terpilih,
                        "Status Awal": batin,
                        "Refleksi": refleksi
                    }])
                    df = pd.concat([df, data_baru], ignore_index=True)
                    df.to_csv(DB_BATIN, index=False)
                    st.success(f"✅ Refleksi harian {nama_terpilih} tersimpan!")
                else:
                    st.error("Teks Refleksi wajib diisi!")

# ==========================================
# HALAMAN 3: STUDENT INSIGHTS (REKAP AI MINGGUAN)
# ==========================================
elif menu == "Student Insights (AI)":
    st.title("Student Insights & Weekly AI 🔍")
    
    try:
        df_batin = pd.read_csv(DB_BATIN)
        if df_batin.empty:
            st.warning("Database refleksi masih kosong.")
        else:
            tab1, tab2 = st.tabs(["👤 Rekap Mingguan Individu (AI)", "📋 Database Lengkap"])
            
            # TAB 1: REKAP INDIVIDU DENGAN AI
            with tab1:
                st.markdown("### Analisis Batin Mendalam per Individu")
                st.write("Pilih nama siswa untuk melihat riwayat jurnalnya, lalu minta AI membuat ringkasan dan saran pendampingannya.")
                
                col_filter1, col_filter2, col_filter3 = st.columns(3)
                with col_filter1:
                    filter_unit = st.selectbox("Filter Unit", sorted(df_batin['Unit'].unique().tolist()))
                with col_filter2:
                    df_filtered_unit = df_batin[df_batin['Unit'] == filter_unit]
                    filter_kelas = st.selectbox("Filter Kelas", sorted(df_filtered_unit['Kelas'].unique().tolist()))
                with col_filter3:
                    df_filtered_kelas = df_filtered_unit[df_filtered_unit['Kelas'] == filter_kelas]
                    filter_nama = st.selectbox("Pilih Nama Siswa", sorted(df_filtered_kelas['Nama Siswa'].unique().tolist()))
                
                st.write("---")
                
                df_siswa = df_filtered_kelas[df_filtered_kelas['Nama Siswa'] == filter_nama].copy()
                
                if df_siswa.empty:
                    st.info(f"Belum ada data refleksi untuk {filter_nama}.")
                else:
                    df_siswa_terakhir = df_siswa.tail(5)
                    st.markdown(f"**Riwayat Refleksi Terakhir: {filter_nama} (Max 5 Hari)**")
                    st.dataframe(df_siswa_terakhir[['Tanggal', 'Status Awal', 'Refleksi']], use_container_width=True)
                    
                    if st.button(f"🧠 Buat Rekap AI untuk {filter_nama}"):
                        with st.spinner('Menganalisis pola batin...'):
                            kumpulan_teks = ""
                            for index, row in df_siswa_terakhir.iterrows():
                                kumpulan_teks += f"- [{row['Tanggal']}] ({row['Status Awal']}): {row['Refleksi']}\n"
                            
                            # Prompt Khusus AI (General & To The Point)
                            prompt = f"""
                            Sebagai seorang konselor pendidikan dan psikologi sekolah, tugasmu adalah menganalisis rekap jurnal harian siswa ini selama beberapa hari terakhir. 
                            PENTING: Jangan perkenalkan dirimu atau berbasa-basi. Langsung berikan analisisnya.

                            Nama: {filter_nama}
                            Riwayat Jurnal:
                            {kumpulan_teks}

                            Tolong berikan balasan profesional dengan format:
                            1. **Pola Emosi:** (Bagaimana tren emosinya? Apa pemicu utamanya?)
                            2. **Kesimpulan Ringkas:** (Kondisi psikologis siswa saat ini)
                            3. **Rekomendasi Pendampingan:** (Langkah nyata yang sangat spesifik untuk wali kelas / guru BK)
                            """
                            
                            try:
                                response = model.generate_content(prompt)
                                st.success("Analisis selesai!")
                                st.info(response.text)
                            except Exception as e:
                                st.error(f"Gagal memproses AI: {e}")
            
            # TAB 2: DATABASE LENGKAP
            with tab2:
                st.markdown("### Seluruh Data Mentah")
                st.dataframe(df_batin, use_container_width=True)
                
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
                
                st.warning("Pilih mode penyimpanan:")
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    if st.button("➕ Tambah ke Data Lama"):
                        df_lama = pd.read_csv(DB_MASTER)
                        df_gabung = pd.concat([df_lama, df_upload], ignore_index=True)
                        df_gabung.drop_duplicates(subset=['Nama Siswa', 'Unit', 'Kelas'], keep='last', inplace=True)
                        df_gabung.to_csv(DB_MASTER, index=False)
                        st.success("✅ Master Data berhasil ditambah!")
                
                with col_btn2:
                    if st.button("🔄 Timpa Semua (Reset)"):
                        df_upload.to_csv(DB_MASTER, index=False)
                        st.success("✅ Master Data lama dihapus, diganti yang baru!")
                        
            except Exception as e:
                st.error(f"Gagal baca file: {e}")
                
    with col2:
        st.markdown("### Isi Master Data Saat Ini:")
        try:
            df_master = pd.read_csv(DB_MASTER)
            if not df_master.empty:
                st.dataframe(df_master, use_container_width=True)
            else:
                st.warning("Data Master masih kosong Bro!")
        except Exception as e:
            st.warning("Data Master masih kosong Bro!")
