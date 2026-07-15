with open("app.py", "r") as f:
    text = f.read()

# Conflict 1
c1 = """<<<<<<< HEAD
    df_staff = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
    df_staff.columns = df_staff.columns.str.strip()
=======
    try:
        df_staff = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
    except Exception:
        st.warning("Worksheet Master Guru belum dibuat di Google Sheets.")
        df_staff = pd.DataFrame(columns=["Nama Guru", "Unit"])
>>>>>>> origin/fix-missing-worksheet-crash-8619920544425409189"""

r1 = """    try:
        df_staff = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
        df_staff.columns = df_staff.columns.str.strip()
    except Exception:
        st.warning("Worksheet Master Guru belum dibuat di Google Sheets.")
        df_staff = pd.DataFrame(columns=["Nama Guru", "Unit"])"""

text = text.replace(c1, r1)

# Conflict 2
c2 = """<<<<<<< HEAD
                                df_staff_db = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
                                df_staff_db.columns = df_staff_db.columns.str.strip()
=======
                                try:
                                    df_staff_db = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
                                except Exception:
                                    st.warning("Worksheet Data Staff belum dibuat di Google Sheets.")
                                    df_staff_db = pd.DataFrame(columns=["Tanggal", "Unit", "Nama Staff", "Detail Konseling", "Analisis AI", "Periode Arsip"])
>>>>>>> origin/fix-missing-worksheet-crash-8619920544425409189"""

r2 = """                                try:
                                    df_staff_db = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
                                    df_staff_db.columns = df_staff_db.columns.str.strip()
                                except Exception:
                                    st.warning("Worksheet Data Staff belum dibuat di Google Sheets.")
                                    df_staff_db = pd.DataFrame(columns=["Tanggal", "Unit", "Nama Staff", "Detail Konseling", "Analisis AI", "Periode Arsip"])"""

text = text.replace(c2, r2)

# Conflict 3
c3 = """<<<<<<< HEAD
                df_staff_db_all = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
                df_staff_db_all.columns = df_staff_db_all.columns.str.strip()
=======
                try:
                    df_staff_db_all = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
                except Exception:
                    st.warning("Worksheet Data Staff belum dibuat di Google Sheets.")
                    df_staff_db_all = pd.DataFrame(columns=["Tanggal", "Unit", "Nama Staff", "Detail Konseling", "Analisis AI", "Periode Arsip"])
>>>>>>> origin/fix-missing-worksheet-crash-8619920544425409189"""

r3 = """                try:
                    df_staff_db_all = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
                    df_staff_db_all.columns = df_staff_db_all.columns.str.strip()
                except Exception:
                    st.warning("Worksheet Data Staff belum dibuat di Google Sheets.")
                    df_staff_db_all = pd.DataFrame(columns=["Tanggal", "Unit", "Nama Staff", "Detail Konseling", "Analisis AI", "Periode Arsip"])"""

text = text.replace(c3, r3)

# Conflict 4
c4 = """<<<<<<< HEAD
        df_guru = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
        df_guru.columns = df_guru.columns.str.strip()
=======
        try:
            df_guru = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
        except Exception:
            st.warning("Worksheet Master Guru belum dibuat di Google Sheets.")
            df_guru = pd.DataFrame(columns=["Nama Guru", "Unit"])
>>>>>>> origin/fix-missing-worksheet-crash-8619920544425409189"""

r4 = """        try:
            df_guru = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
            df_guru.columns = df_guru.columns.str.strip()
        except Exception:
            st.warning("Worksheet Master Guru belum dibuat di Google Sheets.")
            df_guru = pd.DataFrame(columns=["Nama Guru", "Unit"])"""

text = text.replace(c4, r4)

# Conflict 5
c5 = """<<<<<<< HEAD
                        if st.button("➕ Tambah Data Guru", width='stretch'):
                            df_lama_guru = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
                            df_lama_guru.columns = df_lama_guru.columns.str.strip()
=======
                        if st.button("➕ Tambah Data Guru", use_container_width=True):
                            try:
                                df_lama_guru = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
                            except Exception:
                                st.warning("Worksheet Master Guru belum dibuat di Google Sheets.")
                                df_lama_guru = pd.DataFrame(columns=["Nama Guru", "Unit"])
>>>>>>> origin/fix-missing-worksheet-crash-8619920544425409189"""

r5 = """                        if st.button("➕ Tambah Data Guru", width='stretch'):
                            try:
                                df_lama_guru = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
                                df_lama_guru.columns = df_lama_guru.columns.str.strip()
                            except Exception:
                                st.warning("Worksheet Master Guru belum dibuat di Google Sheets.")
                                df_lama_guru = pd.DataFrame(columns=["Nama Guru", "Unit"])"""

text = text.replace(c5, r5)

# Conflict 6
c6 = """<<<<<<< HEAD
                        if st.button("🔄 Reset Data Guru", width='stretch'):
=======
                        if st.button("🔄 Reset Data Guru", use_container_width=True):
>>>>>>> origin/fix-missing-worksheet-crash-8619920544425409189"""

r6 = """                        if st.button("🔄 Reset Data Guru", width='stretch'):"""

text = text.replace(c6, r6)

# Conflict 7
c7 = """<<<<<<< HEAD
            df_master_guru = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
            df_master_guru.columns = df_master_guru.columns.str.strip()
=======
            try:
                df_master_guru = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
            except Exception:
                st.warning("Worksheet Master Guru belum dibuat di Google Sheets.")
                df_master_guru = pd.DataFrame(columns=["Nama Guru", "Unit"])

>>>>>>> origin/fix-missing-worksheet-crash-8619920544425409189"""

r7 = """            try:
                df_master_guru = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Master Guru", ttl=0)
                df_master_guru.columns = df_master_guru.columns.str.strip()
            except Exception:
                st.warning("Worksheet Master Guru belum dibuat di Google Sheets.")
                df_master_guru = pd.DataFrame(columns=["Nama Guru", "Unit"])"""

text = text.replace(c7, r7)

# Conflict 8
c8 = """<<<<<<< HEAD
                st.dataframe(df_tampil_guru, width='stretch', hide_index=True)
=======
                st.dataframe(df_tampil_guru, use_container_width=True, hide_index=True)
>>>>>>> origin/fix-missing-worksheet-crash-8619920544425409189"""

r8 = """                st.dataframe(df_tampil_guru, width='stretch', hide_index=True)"""

text = text.replace(c8, r8)

# Conflict 9
c9 = """<<<<<<< HEAD
                        if st.button("Ya, Arsipkan Data Guru", type="primary", width='stretch'):
=======
                        if st.button("Ya, Arsipkan Data Guru", type="primary", use_container_width=True):
>>>>>>> origin/fix-missing-worksheet-crash-8619920544425409189"""

r9 = """                        if st.button("Ya, Arsipkan Data Guru", type="primary", width='stretch'):"""

text = text.replace(c9, r9)

# Conflict 10
c10 = """<<<<<<< HEAD
                                    df_s = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
                                    df_s.columns = df_s.columns.str.strip()
                                    df_s.loc[df_s['Periode Arsip'] == 'Aktif', 'Periode Arsip'] = periode_guru
                                    conn.update(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", data=df_s)
=======
                                    try:
                                        df_s = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
                                    except Exception:
                                        st.warning("Worksheet Data Staff belum dibuat di Google Sheets.")
                                        df_s = pd.DataFrame(columns=["Tanggal", "Unit", "Nama Staff", "Detail Konseling", "Analisis AI", "Periode Arsip"])
                                    if not df_s.empty:
                                        df_s.loc[df_s['Periode Arsip'] == 'Aktif', 'Periode Arsip'] = periode_guru
                                        conn.update(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", data=df_s)
>>>>>>> origin/fix-missing-worksheet-crash-8619920544425409189"""

r10 = """                                    try:
                                        df_s = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
                                        df_s.columns = df_s.columns.str.strip()
                                    except Exception:
                                        st.warning("Worksheet Data Staff belum dibuat di Google Sheets.")
                                        df_s = pd.DataFrame(columns=["Tanggal", "Unit", "Nama Staff", "Detail Konseling", "Analisis AI", "Periode Arsip"])
                                    if not df_s.empty:
                                        df_s.loc[df_s['Periode Arsip'] == 'Aktif', 'Periode Arsip'] = periode_guru
                                        conn.update(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", data=df_s)"""

text = text.replace(c10, r10)

# Conflict 11
c11 = """<<<<<<< HEAD
        df_batin_all.columns = df_batin_all.columns.str.strip()
        df_staff_all = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
        df_staff_all.columns = df_staff_all.columns.str.strip()
=======
        df_batin_all = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Refleksi", ttl=0)
        try:
            df_staff_all = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
        except Exception:
            st.warning("Worksheet Data Staff belum dibuat di Google Sheets.")
            df_staff_all = pd.DataFrame(columns=["Tanggal", "Unit", "Nama Staff", "Detail Konseling", "Analisis AI", "Periode Arsip"])
>>>>>>> origin/fix-missing-worksheet-crash-8619920544425409189"""

r11 = """        df_batin_all.columns = df_batin_all.columns.str.strip()
        try:
            df_staff_all = conn.read(spreadsheet=st.secrets["spreadsheet_url"], worksheet="Data Staff", ttl=0)
            df_staff_all.columns = df_staff_all.columns.str.strip()
        except Exception:
            st.warning("Worksheet Data Staff belum dibuat di Google Sheets.")
            df_staff_all = pd.DataFrame(columns=["Tanggal", "Unit", "Nama Staff", "Detail Konseling", "Analisis AI", "Periode Arsip"])"""

text = text.replace(c11, r11)

# Conflict 12
c12_real = """<<<<<<< HEAD

            if st.button("Backup Arsip ke Google Drive"):
                with st.spinner("Mencadangkan data ke Google Drive..."):
                    df_arsip_siswa = df_batin_all[df_batin_all['Periode Arsip'] == periode_pilih]
                    df_arsip_staff = df_staff_all[df_staff_all['Periode Arsip'] == periode_pilih]

                    success_siswa, msg_siswa = upload_to_drive(df_arsip_siswa, f"Arsip_Siswa_{periode_pilih}.csv")
                    success_staff, msg_staff = upload_to_drive(df_arsip_staff, f"Arsip_Staff_{periode_pilih}.csv")

                    if success_siswa and success_staff:
                        st.success(f"Berhasil mencadangkan arsip periode {periode_pilih} ke Google Drive!")
                    else:
                        st.error("Gagal mencadangkan data.")
                        if not success_siswa:
                            st.error(f"Error Siswa: {msg_siswa}")
                        if not success_staff:
                            st.error(f"Error Staff: {msg_staff}")

=======
>>>>>>> origin/fix-missing-worksheet-crash-8619920544425409189"""

r12 = """
            if st.button("Backup Arsip ke Google Drive"):
                with st.spinner("Mencadangkan data ke Google Drive..."):
                    df_arsip_siswa = df_batin_all[df_batin_all['Periode Arsip'] == periode_pilih]
                    df_arsip_staff = df_staff_all[df_staff_all['Periode Arsip'] == periode_pilih]

                    success_siswa, msg_siswa = upload_to_drive(df_arsip_siswa, f"Arsip_Siswa_{periode_pilih}.csv")
                    success_staff, msg_staff = upload_to_drive(df_arsip_staff, f"Arsip_Staff_{periode_pilih}.csv")

                    if success_siswa and success_staff:
                        st.success(f"Berhasil mencadangkan arsip periode {periode_pilih} ke Google Drive!")
                    else:
                        st.error("Gagal mencadangkan data.")
                        if not success_siswa:
                            st.error(f"Error Siswa: {msg_siswa}")
                        if not success_staff:
                            st.error(f"Error Staff: {msg_staff}")
"""
text = text.replace(c12_real, r12)

# Conflict 13
c13 = """<<<<<<< HEAD
                    st.dataframe(df_tampil_arsip_siswa, width='stretch', hide_index=True)
=======
                    st.dataframe(df_tampil_arsip_siswa, use_container_width=True, hide_index=True)
>>>>>>> origin/fix-missing-worksheet-crash-8619920544425409189"""

r13 = """                    st.dataframe(df_tampil_arsip_siswa, width='stretch', hide_index=True)"""
text = text.replace(c13, r13)

# Conflict 14
c14 = """<<<<<<< HEAD
                    st.dataframe(df_tampil_arsip_staff, width='stretch', hide_index=True)
=======
                    st.dataframe(df_tampil_arsip_staff, use_container_width=True, hide_index=True)
>>>>>>> origin/fix-missing-worksheet-crash-8619920544425409189"""

r14 = """                    st.dataframe(df_tampil_arsip_staff, width='stretch', hide_index=True)"""
text = text.replace(c14, r14)

with open("app.py", "w") as f:
    f.write(text)
