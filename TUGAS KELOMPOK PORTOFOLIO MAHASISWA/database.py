import sqlite3
import os

UPLOAD_FOLDER = "uploads"
conn = sqlite3.connect("portofolio.db")
cur = conn.cursor()

def init_database():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        print(f"Folder '{UPLOAD_FOLDER}' berhasil dibuat!")

    cur.execute("""CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE, 
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('mahasiswa','dosen','admin')) NOT NULL
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Mahasiswa (
        nim TEXT PRIMARY KEY, 
        nama TEXT NOT NULL, 
        tanggal_lahir TEXT, 
        alamat TEXT, 
        email TEXT UNIQUE, 
        user_id INTEGER UNIQUE NOT NULL, 
        FOREIGN KEY(user_id) REFERENCES Users(user_id)
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Dosen (
        dosen_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nama TEXT NOT NULL, 
        email TEXT UNIQUE, 
        user_id INTEGER UNIQUE NOT NULL, 
        FOREIGN KEY(user_id) REFERENCES Users(user_id)
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Portofolio (
        portofolio_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nim TEXT NOT NULL, 
        jenis TEXT NOT NULL, 
        judul TEXT NOT NULL, 
        deskripsi TEXT, 
        tanggal_input TEXT NOT NULL, 
        FOREIGN KEY(nim) REFERENCES Mahasiswa(nim)
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Bukti (
        bukti_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        portofolio_id INTEGER NOT NULL, 
        file_path TEXT NOT NULL, 
        keterangan TEXT, 
        FOREIGN KEY(portofolio_id) REFERENCES Portofolio(portofolio_id)
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Verifikasi (
        verifikasi_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        portofolio_id INTEGER UNIQUE NOT NULL, 
        dosen_id INTEGER NOT NULL, 
        status TEXT CHECK(status IN ('pending', 'approved', 'rejected')) NOT NULL, 
        FOREIGN KEY(portofolio_id) REFERENCES Portofolio(portofolio_id), 
        FOREIGN KEY(dosen_id) REFERENCES Dosen(dosen_id)
    )""")

    conn.commit()

def seed_data():
    cur.execute("SELECT * FROM Users")
    if not cur.fetchall():
        cur.execute("INSERT INTO Users (username,password,role) VALUES ('salsa','salsa123','mahasiswa')")
        cur.execute("INSERT INTO Mahasiswa (nim,nama,email,user_id,tanggal_lahir,alamat) VALUES ('K3524036','Salsabila Khoiriyatin','salsa@example.com',1,'2000-01-01','Surakarta')")
        cur.execute("INSERT INTO Users (username,password,role) VALUES ('dosen1','dosen123','dosen')")
        cur.execute("INSERT INTO Dosen (nama,email,user_id) VALUES ('Pak Dosen','dosen@example.com',2)")
        cur.execute("INSERT INTO Users (username,password,role) VALUES ('admin','superadmin1','admin')")
        conn.commit()

def clear_all_data():
    print("\n MEMULAI PENGHAPUSAN SEMUA DATA DATABASE...")
    confirm = input("PERINGATAN KERAS: Tindakan ini akan MENGHAPUS SEMUA DATA. Ketik 'YA' untuk konfirmasi: ")
    if confirm.upper() != 'YA':
        print("Pembatalan penghapusan data.")
        return
    cur.execute("DELETE FROM Bukti")
    cur.execute("DELETE FROM Verifikasi")
    cur.execute("DELETE FROM Portofolio")
    cur.execute("DELETE FROM Mahasiswa")
    cur.execute("DELETE FROM Dosen")
    cur.execute("DELETE FROM Users")
    conn.commit()
    print("Semua data di database berhasil dihapus!")
    seed_data()
    print("Akun awal berhasil dibuat ulang.")
    print("-----------------------------------------\n")

def tampilkan_semua_tabel_sql():
    tabel_list = ['Users', 'Mahasiswa', 'Dosen', 'Portofolio', 'Bukti', 'Verifikasi']
    
    print("\n==============================================")
    print("🔍 TAMPILAN LANGSUNG ISI TABEL DATABASE (SQL)")
    print("==============================================")
    
    for table in tabel_list:
        print(f"\n--- TABEL: {table} ---")
        try:
            cur.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cur.fetchall()]
            
            cur.execute(f"SELECT * FROM {table}")
            data = cur.fetchall()
            
            if not columns:
                print("Tabel tidak memiliki kolom atau tidak ditemukan.")
                continue

            widths = [len(col) for col in columns]
            for row in data:
                for i, cell in enumerate(row):
                    widths[i] = max(widths[i], len(str(cell)))

            header = " | ".join(columns).center(sum(widths) + 3 * len(columns))
            print("-" * len(header))
            print(header)
            print("-" * len(header))

            if data:
                for row in data:
                    formatted_row = []
                    for i, cell in enumerate(row):
                        formatted_row.append(str(cell).center(widths[i] + 2))
                    print("|" + "|".join(formatted_row) + "|")
            else:
                print("Tabel kosong.".center(len(header)))
            
            print("-" * len(header))
                
        except sqlite3.Error as e:
            print(f"ERROR membaca tabel {table}: {e}")
    print("\n==============================================\n")