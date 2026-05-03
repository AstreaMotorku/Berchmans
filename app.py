import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import os
import time
from datetime import datetime
from docx import Document
import io

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
        st.error("⚠️ Gagal mengakses model analitik. Periksa konfigurasi sistem.")
except Exception as e:
    st.error(f"⚠️ Masalah koneksi: {e}")

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
        options=["Dashboard", "Data Input Center", "Student Insights", "Database Management"],
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
# HALAMAN 1: DASHBOARD (UI/UX UPGRADE)
# ==========================================
if menu == "Dashboard":
    st.markdown("""
<style>
.dash-title { color: #002244; font-size: 24px; font-weight: 800; margin-bottom: 0px; padding-bottom: 0px; }
.dash-subtitle { color: #8ba1b5; font-size: 14px; margin-top: 0px; padding-top: 0px; margin-bottom: 20px;}

.kpi-card { background-color: #ffffff; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); height: 160px; display: flex; flex-direction: column; justify-content: center; margin-bottom: 5px;}
.kpi-card-blue { border: 2px solid #002244; }
.kpi-card-yellow { border: 2px solid #f39c12; }
.kpi-card-cyan { border: 2px solid #00a8ff; }

.kpi-label { font-size: 12px; font-weight: 700; color: #8ba1b5; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 10px; }
.kpi-val { font-size: 24px; font-weight: 800; color: #002244; margin-bottom: 5px; line-height: 1.2;}
.kpi-val-yellow { color: #d35400; }
.kpi-val-cyan { color: #0097e6; }
.kpi-desc { font-size: 13px; color: #8ba1b5; }

.section-container { background-color: #ffffff; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }
.section-title { color: #002244; font-size: 18px; font-weight: 800; margin-bottom: 5px; }
.section-subtitle { color: #8ba1b5; font-size: 13px; margin-bottom: 20px; }

.priority-item { border-bottom: 1px solid #f0f2f6; padding-bottom: 10px; margin-bottom: 10px; }
.priority-item:last-child { border-bottom: none; }
.p-name { font-weight: 700; color: #002244; font-size: 15px; margin-bottom: 2px; }
.p-class { font-size: 12px; color: #8ba1b5; }
.badge-red { background-color: #ff767533; color: #d63031; padding: 3px 8px; border-radius: 12px; font-size: 10px; font-weight: 800; float: right; }
.p-status { font-size: 12px; color: #d63031; font-weight: 600; margin-top: 5px;}
.p-time { font-size: 11px; color: #b2bec3; float: right; font-style: italic; margin-top: 5px;}
.view-all-btn { display: block; width: 100%; text-align: center; padding: 10px; border: 1px solid #e0e0e0; border-radius: 8px; color: #002244; font-weight: 600; font-size: 13px; text-decoration: none; margin-top: 15px; }
.view-all-btn:hover { background-color: #f4f6f9; }
</style>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    col_header1, col_header2 = st.columns([2.5, 1])
    with col_header1:
        st.markdown('<p class="dash-title" style="color:#dca235; font-size:28px;">Berchmans Spirit Center</p>', unsafe_allow_html=True)
        st.markdown('<p class="dash-subtitle">Analitik Pergerakan Batin & Evaluasi Pastoral</p>', unsafe_allow_html=True)
    with col_header2:
        st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
        st.text_input("Search", placeholder="🔍 Cari siswa...", label_visibility="collapsed")

    try:
        df = pd.read_csv(DB_BATIN)
        if not df.empty:
            total_data = len(df)
            jumlah_konsolasi = len(df[df['Status Awal'] == 'Konsolasi'])
            persen_konsolasi = int((jumlah_konsolasi / total_data) * 100) if total_data > 0 else 0
            
            df_desolasi = df[df['Status Awal'] == 'Desolasi']

            # --- LOGIKA UNIT ALERT (THRESHOLD) ---
            unit_alert = "Semua Unit Stabil"
            pesan_alert = "Tidak ada tren negatif signifikan"
            
            df_mood_unit = df.groupby('Unit')['Status Awal'].value_counts().unstack(fill_value=0)
            if 'Desolasi' not in df_mood_unit.columns:
                df_mood_unit['Desolasi'] = 0
            if 'Konsolasi' not in df_mood_unit.columns:
                df_mood_unit['Konsolasi'] = 0
                
            df_mood_unit['Total'] = df_mood_unit['Konsolasi'] + df_mood_unit['Desolasi']
            df_mood_unit['Persen_Desolasi'] = (df_mood_unit['Desolasi'] / df_mood_unit['Total']) * 100
            
            df_kritis = df_mood_unit[(df_mood_unit['Desolasi'] >= 3) & (df_mood_unit['Persen_Desolasi'] >= 30)]
            
            if not df_kritis.empty:
                unit_terparah = df_kritis['Persen_Desolasi'].idxmax()
                persen_parah = int(df_kritis.loc[unit_terparah, 'Persen_Desolasi'])
                jumlah_parah = df_kritis.loc[unit_terparah, 'Desolasi']
                
                unit_alert = f"{unit_terparah}: Perlu Atensi!"
                pesan_alert = f"⚠️ {persen_parah}% ({jumlah_parah} laporan) mengalami Desolasi"
            # ----------------------------------------

            # --- ROW 1: KPI CARDS DENGAN EXPANDER ---
            col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
            
            with col_kpi1:
                st.markdown(f"""
<div class="kpi-card kpi-card-blue">
    <div class="kpi-label">SCHOOL-WIDE MOOD 📈</div>
    <div class="kpi-val">{persen_konsolasi}% Konsolasi</div>
    <div class="kpi-desc">Berdasarkan {total_data} total laporan batin</div>
</div>
                """, unsafe_allow_html=True)
                with st.expander("📊 Lihat Detail per Unit"):
                    df_mood = df.groupby(['Unit', 'Status Awal']).size().unstack(fill_value=0).reset_index()
                    if 'Konsolasi' not in df_mood.columns: df_mood['Konsolasi'] = 0
                    if 'Desolasi' not in df_mood.columns: df_mood['Desolasi'] = 0
                    df_mood['Total'] = df_mood['Konsolasi'] + df_mood['Desolasi']
                    df_mood['% Konsolasi'] = (df_mood['Konsolasi'] / df_mood['Total'] * 100).round(1)
                    st.dataframe(df_mood[['Unit', '% Konsolasi', 'Total']], hide_index=True, use_container_width=True)
                
            with col_kpi2:
                st.markdown(f"""
<div class="kpi-card kpi-card-yellow">
    <div class="kpi-label">UNIT ALERT ⚠️</div>
    <div class="kpi-val kpi-val-yellow">{unit_alert}</div>
    <div class="kpi-desc">{pesan_alert}</div>
</div>
                """, unsafe_allow_html=True)
                with st.expander("⚠️ Pantau Unit Lainnya"):
                    if not df_desolasi.empty:
                        df_desolasi_counts = df_desolasi['Unit'].value_counts().reset_index()
                        df_desolasi_counts.columns = ['Unit', 'Jumlah Desolasi']
                        st.dataframe(df_desolasi_counts, hide_index=True, use_container_width=True)
                    else:
                        st.success("Tidak ada data desolasi saat ini.")
                
            with col_kpi3:
                st.markdown("""
<div class="kpi-card kpi-card-cyan">
    <div class="kpi-label">PATTERN DETECTED 🧠</div>
    <div class="kpi-val kpi-val-cyan">Perlu Pemindaian</div>
    <div class="kpi-desc">Klik dropdown di bawah untuk memindai pola batin.</div>
</div>
                """, unsafe_allow_html=True)
                with st.expander("🔍 Pindai Pola Batin"):
                    opsi_pola = ["Seluruh Sekolah"] + sorted(df['Unit'].unique().tolist())
                    target_pola = st.selectbox("Pilih Target Pindaian:", opsi_pola, label_visibility="collapsed")
                    
                    if st.button("Jalankan Pemindaian Pola"):
                        with st.spinner("Memproses data teks..."):
                            df_target = df if target_pola == "Seluruh Sekolah" else df[df['Unit'] == target_pola]
                            teks_refleksi = " ".join(df_target.tail(30)['Refleksi'].dropna().astype(str).tolist())
                            
                            if teks_refleksi.strip():
                                prompt_pola = f"Sebutkan 1 frasa singkat (maksimal 4 kata) yang menjadi tema utama atau masalah paling sering muncul dari kumpulan curhatan ini: '{teks_refleksi}'. Lalu berikan 2 kalimat penjelasan singkat."
                                try:
                                    response = model.generate_content(prompt_pola)
                                    st.success("Pemindaian Selesai!")
                                    st.info(response.text)
                                except Exception as e:
                                    st.error("Gagal terhubung ke AI.")
                            else:
                                st.warning("Data refleksi tidak cukup untuk dipindai.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- ROW 2: CHART & PRIORITY LIST ---
            col_mid1, col_mid2 = st.columns([2.5, 1.2])
            
            with col_mid1:
                st.markdown("""
<div style="background-color: #ffffff; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 10px;">
    <div style="color: #002244; font-size: 18px; font-weight: 800; margin-bottom: 5px;">Trend Batin Per Unit</div>
    <div style="color: #8ba1b5; font-size: 13px;">Perbandingan Tingkat Konsolasi vs Desolasi (Data Real-Time)</div>
</div>
                """, unsafe_allow_html=True)
                
                df_unit = df.groupby(['Unit', 'Status Awal']).size().reset_index(name='Jumlah')
                fig_bar = px.bar(
                    df_unit, 
                    y='Unit', 
                    x='Jumlah', 
                    color='Status Awal', 
                    orientation='h', 
                    barmode='group',
                    color_discrete_map={'Konsolasi':'#002244', 'Desolasi':'#e2e8f0'} 
                )
                fig_bar.update_layout(
                    margin=dict(t=10, b=0, l=0, r=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    yaxis_title=None,
                    xaxis_title=None,
                    legend_title=None,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            with col_mid2:
                st.markdown("""
<div class="section-container" style="padding-bottom: 5px;">
    <div class="section-title">Priority Cura Personalis</div>
    <div class="section-subtitle">High Risk Intervention List</div>
</div>
                """, unsafe_allow_html=True)
                
                df_desolasi_terakhir = df[df['Status Awal'] == 'Desolasi'].tail(3).iloc[::-1]
                
                if not df_desolasi_terakhir.empty:
                    for idx, row in df_desolasi_terakhir.iterrows():
                        st.markdown(f"""
                        <div class="priority-item">
                            <span class="badge-red">PERLU ATENSI</span>
                            <div class="p-name">{row['Nama Siswa']}</div>
                            <div class="p-class">{row['Unit']} - {row['Kelas']}</div>
                            <div><span class="p-status">Desolasi</span> <span class="p-time">{row['Tanggal']}</span></div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Tidak ada siswa dalam radar risiko tinggi saat ini.")
                    
                st.markdown('<a href="#" class="view-all-btn">Lihat Semua di Menu Insight ></a>', unsafe_allow_html=True)

        else:
            st.info("Belum ada data refleksi yang masuk dalam sistem.")
            
    except Exception as e:
        st.error(f"Gagal memuat Dashboard: {e}")

# ==========================================
# HALAMAN 2: DATA INPUT CENTER 
# ==========================================
elif menu == "Data Input Center":
    st.title("Data Input Center 📥")
    st.write("Pusat pencatatan data refleksi harian. Sistem dirancang untuk entri data cepat. Analisis komprehensif dapat diakses melalui menu Student Insights.")
    st.write("---")
    
    df_master = pd.read_csv(DB_MASTER)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 Bulk Excel Import")
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
                    tgl_input = row.get('Tanggal', datetime.now().strftime("%Y-%m-%d"))
                    data_baru_list.append({
                        "Tanggal": tgl_input,
                        "Unit": row.get('Unit', '-'),
                        "Kelas": row.get('Kelas', '-'),
                        "Nama Siswa": row.get('Nama Lengkap', row.get('Nama Siswa', 'Anonim')),
                        "Status Awal": row.get('Dominasi Batin', 'Tidak Diketahui'),
                        "Refleksi": row.get('Teks Refleksi', '')
                    })
                
                df_baru = pd.DataFrame(data_baru_list)
                df_batin = pd.concat([df_batin, df_baru], ignore_index=True)
                df_batin.to_csv(DB_BATIN, index=False)
                st.success(f"✅ {len(df_bulk)} data berhasil disimpan!")

    with col2:
        st.markdown("### ✍️ Manual Entry")
        if df_master.empty:
            st.warning("⚠️ Silakan lengkapi Master Data di menu 'Database Management' terlebih dahulu.")
        else:
            tanggal_refleksi = st.date_input("Tanggal Refleksi", datetime.now().date())
            
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
            refleksi = st.text_area("Teks Refleksi Siswa")
            
            if st.button("Simpan Laporan"):
                if refleksi:
                    df = pd.read_csv(DB_BATIN)
                    data_baru = pd.DataFrame([{
                        "Tanggal": tanggal_refleksi.strftime("%Y-%m-%d"),
                        "Unit": unit_terpilih,
                        "Kelas": kelas_terpilih,
                        "Nama Siswa": nama_terpilih,
                        "Status Awal": batin,
                        "Refleksi": refleksi
                    }])
                    df = pd.concat([df, data_baru], ignore_index=True)
                    df.to_csv(DB_BATIN, index=False)
                    st.success(f"✅ Data refleksi {nama_terpilih} tanggal {tanggal_refleksi.strftime('%d-%m-%Y')} tersimpan!")
                else:
                    st.error("Teks Refleksi wajib diisi!")

# ==========================================
# HALAMAN 3: STUDENT INSIGHTS 
# ==========================================
elif menu == "Student Insights":
    st.title("Student Insights & Weekly Report 🔍")
    st.write("Laporan analitik mendalam untuk memantau perkembangan psikologis dan spiritualitas siswa, baik secara individu maupun komunitas.")
    st.write("---")
    
    try:
        df_batin = pd.read_csv(DB_BATIN)
        if df_batin.empty:
            st.warning("Database refleksi masih kosong.")
        else:
            tab1, tab2 = st.tabs(["👤 Rekap Analisis", "📋 Database Lengkap"])
            
            # TAB 1: REKAP ANALISIS
            with tab1:
                col_filter1, col_filter2, col_filter3 = st.columns(3)
                
                with col_filter1:
                    opsi_unit = ["Semua Unit"] + sorted(df_batin['Unit'].unique().tolist())
                    filter_unit = st.selectbox("Filter Unit", opsi_unit)
                    
                with col_filter2:
                    if filter_unit == "Semua Unit":
                        df_filtered_unit = df_batin
                        opsi_kelas = ["Semua Kelas"]
                    else:
                        df_filtered_unit = df_batin[df_batin['Unit'] == filter_unit]
                        opsi_kelas = ["Semua Kelas"] + sorted(df_filtered_unit['Kelas'].unique().tolist())
                    
                    filter_kelas = st.selectbox("Filter Kelas", opsi_kelas)
                    
                with col_filter3:
                    if filter_kelas == "Semua Kelas":
                        df_filtered_kelas = df_filtered_unit
                        opsi_nama = ["Semua Siswa"]
                    else:
                        df_filtered_kelas = df_filtered_unit[df_filtered_unit['Kelas'] == filter_kelas]
                        opsi_nama = ["Semua Siswa"] + sorted(df_filtered_kelas['Nama Siswa'].unique().tolist())
                        
                    filter_nama = st.selectbox("Pilih Nama Siswa", opsi_nama)
                
                st.write("---")
                
                if filter_nama == "Semua Siswa":
                    df_target = df_filtered_kelas.copy()
                    target_analisis = f"Komunitas ({filter_unit} - {filter_kelas})"
                else:
                    df_target = df_filtered_kelas[df_filtered_kelas['Nama Siswa'] == filter_nama].copy()
                    target_analisis = filter_nama
                
                if df_target.empty:
                    st.info(f"Belum ada data refleksi untuk {target_analisis}.")
                else:
                    df_target_terakhir = df_target.tail(50)
                    st.markdown(f"**Riwayat Refleksi: {target_analisis}**")
                    st.dataframe(df_target_terakhir[['Tanggal', 'Kelas', 'Nama Siswa', 'Status Awal', 'Refleksi']], use_container_width=True)
                    
                    if st.button(f"🧠 Buat Rekap Analisis untuk {target_analisis}"):
                        with st.spinner('Memproses pola analitik data...'):
                            kumpulan_teks = ""
                            for index, row in df_target_terakhir.iterrows():
                                kumpulan_teks += f"- [{row['Tanggal']}] {row['Nama Siswa']} ({row['Kelas']}) - {row['Status Awal']}: {row['Refleksi']}\n"
                            
                            prompt = f"""
                            Sebagai seorang konselor pendidikan dan psikologi sekolah, tugasmu adalah menganalisis rekap jurnal refleksi dari {target_analisis} berdasarkan data berikut. 
                            PENTING: Jangan perkenalkan dirimu atau berbasa-basi. Langsung berikan analisisnya secara profesional.

                            Data Refleksi:
                            {kumpulan_teks}

                            Tolong berikan laporan dengan format:
                            1. **Pola Emosi Dominan:** (Bagaimana tren emosi mayoritas? Apa tema atau pemicu utamanya?)
                            2. **Kesimpulan Ringkas:** (Kondisi psikologis dan dinamika batin saat ini)
                            3. **Rekomendasi Pendampingan:** (Langkah nyata yang sangat spesifik untuk pimpinan unit / wali kelas / guru BK)
                            """
                            
                            try:
                                response = model.generate_content(prompt)
                                st.success("Laporan analitik selesai dibuat.")
                                st.info(response.text)

                                # --- KODE BARU UNTUK DOWNLOAD WORD ---
                                doc = Document()
                                doc.add_heading('LAPORAN ANALITIK BINA IMAN & PSIKOLOGIS', level=1)
                                doc.add_paragraph(f"Target Analisis: {target_analisis}")
                                doc.add_paragraph(f"Tanggal Cetak: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
                                
                                teks_bersih = response.text.replace('**', '')
                                doc.add_paragraph(teks_bersih)
                                
                                bio = io.BytesIO()
                                doc.save(bio)
                                bio.seek(0)
                                
                                st.download_button(
                                    label="📥 Download Laporan (Word)",
                                    data=bio,
                                    file_name=f"Laporan_Analitik_{target_analisis.replace(' ', '_')}.docx",
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                )
                                # --------------------------------

                            except Exception as e:
                                st.error(f"Gagal memproses sistem: {e}")
            
            # TAB 2: DATABASE LENGKAP
            with tab2:
                st.markdown("### Seluruh Data Refleksi (Disortir per Unit)")
                df_batin_sorted = df_batin.sort_values(by=['Unit', 'Kelas', 'Tanggal'], ascending=[True, True, False]).reset_index(drop=True)
                st.dataframe(df_batin_sorted, use_container_width=True)
                
    except FileNotFoundError:
        st.error("Database belum terbentuk.")

# ==========================================
# HALAMAN 4: DATABASE MANAGEMENT 
# ==========================================
elif menu == "Database Management":
    st.title("Manajemen Data Induk 🗃️")
    st.write("Pusat pengelolaan direktori civitas akademika. Data yang diunggah akan terintegrasi secara otomatis dengan seluruh modul.")
    
    # --- BAGIAN 1: UPLOAD DENGAN KOLOM ---
    col_up1, col_up2 = st.columns([1, 1])
    with col_up1:
        st.info("Pastikan format kolom Excel/CSV memuat: **Nama Siswa**, **Unit**, dan **Kelas**. *(Kosongkan kolom Kelas untuk Guru/Staff)*")
        file_master = st.file_uploader("Unggah Dokumen (CSV/Excel)", type=['csv', 'xlsx'])
        
    with col_up2:
        if file_master:
            try:
                if file_master.name.endswith('.csv'):
                    df_upload = pd.read_csv(file_master)
                else:
                    df_upload = pd.read_excel(file_master)
                
                st.warning("Pilih mode penyimpanan:")
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    if st.button("➕ Tambah ke Data Lama", use_container_width=True):
                        df_lama = pd.read_csv(DB_MASTER)
                        df_gabung = pd.concat([df_lama, df_upload], ignore_index=True)
                        df_gabung.drop_duplicates(subset=['Nama Siswa', 'Unit', 'Kelas'], keep='last', inplace=True)
                        df_gabung = df_gabung.sort_values(by=['Unit', 'Kelas', 'Nama Siswa']).reset_index(drop=True)
                        df_gabung.to_csv(DB_MASTER, index=False)
                        st.success("✅ Data induk berhasil diperbarui!")
                
                with col_btn2:
                    if st.button("🔄 Timpa Semua (Reset)", use_container_width=True):
                        df_upload = df_upload.sort_values(by=['Unit', 'Kelas', 'Nama Siswa']).reset_index(drop=True)
                        df_upload.to_csv(DB_MASTER, index=False)
                        st.success("✅ Seluruh data diganti dokumen baru!")
                        
            except Exception as e:
                st.error(f"Gagal membaca dokumen: {e}")

    st.write("---")
    
    # --- BAGIAN 2: UI DIREKTORI FILTER DINAMIS ---
    st.markdown("### 🗂️ Direktori Master Data")
    try:
        df_master = pd.read_csv(DB_MASTER)
        if not df_master.empty:
            
            # BARIS 1: MENU UNIT & SEARCH BAR
            col_nav, col_search = st.columns([2.5, 1])
            with col_nav:
                list_unit = ["SEMUA UNIT"] + sorted([str(u).upper() for u in df_master['Unit'].dropna().unique().tolist()])
                pilih_unit = option_menu(
                    menu_title=None,
                    options=list_unit,
                    orientation="horizontal",
                    styles={
                        "container": {"padding": "5px", "background-color": "#ffffff", "border": "1px solid #e0e0e0", "border-radius": "10px", "margin":"0px"},
                        "nav-link": {"font-size": "13px", "font-weight": "bold", "color": "#8ba1b5", "margin":"0px", "padding": "10px"},
                        "nav-link-selected": {"background-color": "#002244", "color": "#ffffff", "border-radius": "8px"},
                    },
                    key="menu_unit_db"
                )
                
            with col_search:
                st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True) 
                search_query = st.text_input("Pencarian", label_visibility="collapsed", placeholder="🔍 Search student name...")

            # Logika Filter Unit
            if pilih_unit == "SEMUA UNIT":
                df_tampil = df_master
            else:
                df_tampil = df_master[df_master['Unit'].str.upper() == pilih_unit]
                
            # BARIS 2: MENU KELAS (Otomatis sembunyi jika Guru/Staff)
            list_kelas = [k for k in df_tampil['Kelas'].unique() if pd.notna(k) and str(k).strip() != '']
            if list_kelas and pilih_unit != "SEMUA UNIT":
                col_teks, col_pills = st.columns([1, 6])
                with col_teks:
                    st.markdown("<p style='font-size:13px; font-weight:800; color:#8ba1b5; margin-top:20px; text-align:right; letter-spacing: 1px;'>FILTER KELAS:</p>", unsafe_allow_html=True)
                with col_pills:
                    opsi_kelas = ["Semua Kelas"] + sorted(list_kelas)
                    pilih_kelas = option_menu(
                        menu_title=None,
                        options=opsi_kelas,
                        orientation="horizontal",
                        styles={
                            "container": {"padding": "0!important", "background-color": "transparent", "margin-top":"10px"},
                            "nav-link": {"font-size": "13px", "color": "#002244", "background-color": "#ffffff", "border": "1px solid #e0e0e0", "border-radius": "20px", "margin": "0 5px", "padding": "5px 15px"},
                            "nav-link-selected": {"background-color": "#dca235", "color": "#002244", "font-weight": "bold", "border": "none"},
                        },
                        key="menu_kelas_db"
                    )
                    if pilih_kelas != "Semua Kelas":
                        df_tampil = df_tampil[df_tampil['Kelas'] == pilih_kelas]

            # Logika Search
            if search_query:
                df_tampil = df_tampil[df_tampil['Nama Siswa'].str.contains(search_query, case=False, na=False)]

            # TAMPILKAN TABEL
            st.markdown("<br>", unsafe_allow_html=True)
            df_tampil = df_tampil.sort_values(by=['Unit', 'Kelas', 'Nama Siswa']).reset_index(drop=True)
            st.dataframe(df_tampil, use_container_width=True)
            
            # TOMBOL DELETE
            st.write("---")
            col_del1, col_del2, col_del3 = st.columns([1,2,1])
            with col_del2:
                if st.button("🗑️ Kosongkan Seluruh Direktori Master", use_container_width=True):
                    pd.DataFrame(columns=["Nama Siswa", "Kelas", "Unit"]).to_csv(DB_MASTER, index=False)
                    st.success("Direktori berhasil dikosongkan. Muat ulang (refresh) halaman.")
        else:
            st.warning("Direktori data masih kosong.")
    except Exception as e:
         st.warning("Direktori data masih kosong.")
