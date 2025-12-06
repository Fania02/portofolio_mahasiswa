import sqlite3
from database import conn, cur
from utils import is_password_valid

def is_username_exists(username):
    cur.execute("SELECT user_id FROM Users WHERE username=?", (username,))
    return cur.fetchone() is not None

def is_nim_exists(nim):
    cur.execute("SELECT nim FROM Mahasiswa WHERE nim=?", (nim,))
    return cur.fetchone() is not None

def register():
    print("\n=== BUAT AKUN BARU ===")
    role = input("Daftar sebagai (mahasiswa/dosen/admin): ").lower()
    if role not in ["mahasiswa", "dosen", "admin"]:
        print("Role tidak valid!\n")
        return
    
    username = input("Username baru: ")
    if is_username_exists(username):
        print("Username sudah digunakan.\n")
        return
    
    password = input("Password (Harus mengandung angka dan huruf): ")
    if not is_password_valid(password):
        print("Password tidak valid!\n")
        return
    
    cur.execute("INSERT INTO Users (username,password,role) VALUES (?,?,?)", (username, password, role))
    conn.commit()
    user_id = cur.lastrowid
    
    try:
        if role == "mahasiswa":
            nim = input("Masukkan NIM: ")
            if is_nim_exists(nim):
                cur.execute("DELETE FROM Users WHERE user_id=?", (user_id,))
                conn.commit()
                print("NIM sudah terdaftar. Registrasi dibatalkan.\n")
                return
            nama = input("Nama lengkap: ")
            email = input("Email: ")
            tanggal_lahir = input("Tanggal Lahir (YYYY-MM-DD): ")
            alamat = input("Alamat: ")
            prodi = input("Prodi: ")
            angkatan = input("Angkatan: ")
            cur.execute("INSERT INTO Mahasiswa (nim,nama,email,user_id,tanggal_lahir,alamat,prodi,angkatan) VALUES (?,?,?,?,?,?,?,?)", 
                       (nim, nama, email, user_id, tanggal_lahir, alamat, prodi, angkatan))
        elif role == "dosen":
            nama = input("Nama dosen: ")
            email = input("Email: ")
            cur.execute("INSERT INTO Dosen (nama,email,user_id) VALUES (?,?,?)", (nama, email, user_id))
        
        conn.commit()
        print("Akun berhasil dibuat!\n")
    except sqlite3.Error as e:
        cur.execute("DELETE FROM Users WHERE user_id=?", (user_id,))
        conn.commit()
        print(f"Terjadi kesalahan saat menyimpan data detail: {e}. Registrasi dibatalkan.\n")

def login():
    print("\n=== LOGIN SISTEM PORTOFOLIO MAHASISWA ===")
    username = input("Username: ")
    password = input("Password: ")
    cur.execute("SELECT * FROM Users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()
    if user:
        print(f"\n Login berhasil sebagai {user[3].upper()}!\n")
        return user
    else:
        print("\n Login gagal! Username atau password salah.\n")
        return None