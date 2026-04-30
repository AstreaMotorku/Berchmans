import streamlit as st

# 1. PENGATURAN HALAMAN DASAR
st.set_page_config(page_title="Berchmans Spirit Center", page_icon="🕊️", layout="wide")

# 2. WARNA & TEMA (Sesuai panduan lu: Academic Blue)
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    h1, h2, h3 { color: #003366; } 
    .stButton>button { background-color: #003366; color: white; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR NAVIGASI
st.sidebar.title("🕊️ Berchmans Lite")
st.sidebar.write("Head of Campus Ministry Portal")
menu = st.sidebar.radio("Navigasi:", ["AI Dashboard", "Data Input Center", "Student Tracker"])

# 4. LOGIKA HALAMAN: DATA INPUT CENTER
if menu == "Data Input Center":
    st.title("Data Input Center 📥")
    st.subheader("Upload Excel atau input refleksi manual untuk diproses AI")
    st.write("---")
    
    col1, col2 = st.columns([1, 1])
    
    # Bagian Kiri: Upload Excel
    with col1:
        st.markdown("### 📊 Bulk Excel Import")
        st.info("Upload file template CSV lu di sini.")
        uploaded_file = st.file_uploader("Tarik dan lepas file di sini", type=['csv', 'xlsx'])
        
        if uploaded_file is not None:
            st.success("✅ File berhasil dibaca sistem! (Nanti kita sambungkan ke AI di sini)")
            
    # Bagian Kanan: Input Manual
    with col2:
        st.markdown("### ✍️ Manual Single Entry")
        st.warning("Input cepat untuk siswa satuan.")
        
        kelas = st.selectbox("Pilih Kelas", ["Kelas 7A", "Kelas 8B", "Kelas 9A", "Kelas 10C", "Kelas 12A"])
        nama = st.text_input("Nama Siswa")
        batin = st.radio("Dominasi Batin", ["Konsolasi", "Desolasi"], horizontal=True)
        refleksi = st.text_area("Teks Refleksi / Bundling")
        
        if st.button("Simpan Data"):
            if nama and refleksi:
                st.success(f"✅ Data {nama} dari {kelas} berhasil disimpan!")
            else:
                st.error("Nama dan Teks Refleksi harus diisi Bro!")

# 5. LOGIKA HALAMAN: AI DASHBOARD
elif menu == "AI Dashboard":
    st.title("AI Dashboard 🧠")
    st.info("Nanti di sini Gemini AI akan membaca database lu dan mengeluarkan kesimpulan tren batin (Konsolasi vs Desolasi) per unit dan per kelas.")

# 6. LOGIKA HALAMAN: STUDENT TRACKER
elif menu == "Student Tracker":
    st.title("Student Insights Directory 🔍")
    st.info("Nanti lu bisa cari nama siswa di sini, dan melihat grafik riwayat batin mereka beserta saran intervensi (Cura Personalis) dari AI.")
