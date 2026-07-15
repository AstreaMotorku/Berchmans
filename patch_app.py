with open("app.py", "r") as f:
    text = f.read()

# Make sure we add try-except wrapper with fallback for all the requested tables (Master Guru and Data Staff)
# while preserving the .columns.str.strip() which is currently in HEAD.

# We will regex or replace the specific blocks.

# Replace Master Guru reads:
# Block 1:
old1 = """    df_staff = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
    df_staff.columns = df_staff.columns.str.strip()"""
new1 = """    try:
        df_staff = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
        df_staff.columns = df_staff.columns.str.strip()
    except Exception:
        st.warning("Worksheet Master Guru belum dibuat di Google Sheets.")
        df_staff = pd.DataFrame(columns=["Nama Guru", "Unit"])"""
text = text.replace(old1, new1)

# Block 2: Data Staff (Input Konseling)
old2 = """                                df_staff_db = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
                                df_staff_db.columns = df_staff_db.columns.str.strip()"""
new2 = """                                try:
                                    df_staff_db = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
                                    df_staff_db.columns = df_staff_db.columns.str.strip()
                                except Exception:
                                    st.warning("Worksheet Data Staff belum dibuat di Google Sheets.")
                                    df_staff_db = pd.DataFrame(columns=["Tanggal", "Unit", "Nama Staff", "Detail Konseling", "Analisis AI", "Periode Arsip"])"""
text = text.replace(old2, new2)

# Block 3: Data Staff (Riwayat)
old3 = """            try:
                df_staff_db_all = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
                df_staff_db_all.columns = df_staff_db_all.columns.str.strip()"""
new3 = """            try:
                try:
                    df_staff_db_all = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
                    df_staff_db_all.columns = df_staff_db_all.columns.str.strip()
                except Exception:
                    st.warning("Worksheet Data Staff belum dibuat di Google Sheets.")
                    df_staff_db_all = pd.DataFrame(columns=["Tanggal", "Unit", "Nama Staff", "Detail Konseling", "Analisis AI", "Periode Arsip"])"""
text = text.replace(old3, new3)

# Block 4: Master Guru (Database Management rekap)
old4 = """        df_guru = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
        df_guru.columns = df_guru.columns.str.strip()"""
new4 = """        try:
            df_guru = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
            df_guru.columns = df_guru.columns.str.strip()
        except Exception:
            st.warning("Worksheet Master Guru belum dibuat di Google Sheets.")
            df_guru = pd.DataFrame(columns=["Nama Guru", "Unit"])"""
text = text.replace(old4, new4)

# Block 5: Master Guru (Database Management tambah)
old5 = """                        if st.button("➕ Tambah Data Guru", width='stretch'):
                            df_lama_guru = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
                            df_lama_guru.columns = df_lama_guru.columns.str.strip()"""
new5 = """                        if st.button("➕ Tambah Data Guru", width='stretch'):
                            try:
                                df_lama_guru = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
                                df_lama_guru.columns = df_lama_guru.columns.str.strip()
                            except Exception:
                                st.warning("Worksheet Master Guru belum dibuat di Google Sheets.")
                                df_lama_guru = pd.DataFrame(columns=["Nama Guru", "Unit"])"""
text = text.replace(old5, new5)

# Block 6: Master Guru (Database Management direktori)
old6 = """        try:
            df_master_guru = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
            df_master_guru.columns = df_master_guru.columns.str.strip()"""
new6 = """        try:
            try:
                df_master_guru = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
                df_master_guru.columns = df_master_guru.columns.str.strip()
            except Exception:
                st.warning("Worksheet Master Guru belum dibuat di Google Sheets.")
                df_master_guru = pd.DataFrame(columns=["Nama Guru", "Unit"])"""
text = text.replace(old6, new6)

# Block 7: Data Staff (Database Management arsip)
old7 = """                                try:
                                    df_s = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
                                    df_s.columns = df_s.columns.str.strip()
                                    df_s.loc[df_s['Periode Arsip'] == 'Aktif', 'Periode Arsip'] = periode_guru
                                    conn.update(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", data=df_s)"""
new7 = """                                try:
                                    try:
                                        df_s = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
                                        df_s.columns = df_s.columns.str.strip()
                                    except Exception:
                                        st.warning("Worksheet Data Staff belum dibuat di Google Sheets.")
                                        df_s = pd.DataFrame(columns=["Tanggal", "Unit", "Nama Staff", "Detail Konseling", "Analisis AI", "Periode Arsip"])
                                    if not df_s.empty:
                                        df_s.loc[df_s['Periode Arsip'] == 'Aktif', 'Periode Arsip'] = periode_guru
                                        conn.update(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", data=df_s)"""
text = text.replace(old7, new7)

# Block 8: Data Staff (Data Archive)
old8 = """    try:
        df_batin_all = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Refleksi", ttl=0)
        df_batin_all.columns = df_batin_all.columns.str.strip()
        df_staff_all = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
        df_staff_all.columns = df_staff_all.columns.str.strip()"""
new8 = """    try:
        df_batin_all = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Refleksi", ttl=0)
        df_batin_all.columns = df_batin_all.columns.str.strip()
        try:
            df_staff_all = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
            df_staff_all.columns = df_staff_all.columns.str.strip()
        except Exception:
            st.warning("Worksheet Data Staff belum dibuat di Google Sheets.")
            df_staff_all = pd.DataFrame(columns=["Tanggal", "Unit", "Nama Staff", "Detail Konseling", "Analisis AI", "Periode Arsip"])"""
text = text.replace(old8, new8)


with open("app.py", "w") as f:
    f.write(text)
