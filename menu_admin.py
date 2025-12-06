import sqlite3
from database import conn, cur
from database import clear_all_data, tampilkan_semua_tabel_sql, user_delete

def menu_admin(user):
    while True:
        print("\n=== MENU ADMIN ===")
        print("1. Lihat Semua Portofolio Mahasiswa")
        print("2. Tampilkan Data Portofolio Mahasiswa")
        print("3. Verifikasi Portofolio")
        print("4. Hapus Data Portofolio")
        print("5. View Database (Lihat Semua Tabel Data)")
        print("6. Reset Database (Hapus Semua Data)")
        print("7. Hapus User")
        print("8. Logout")
        
        choice = input("Pilih menu: ")
        
        if choice == "1":
            lihat_semua_portofolio()
        elif choice == "2":
            data_portofolio_mahasiswa()
        elif choice == "3":
            verifikasi_portofolio(user)
        elif choice == "4":
            Hapus_data_portofolio_mahasiswa()
        elif choice == "5":
            tampilkan_semua_tabel_sql()
        elif choice == "6":
            clear_all_data()
        elif choice == "7":
            user_delete()
        elif choice == "8":
            print("Logout berhasil.\n")
            return
        else:
            print("Pilihan tidak valid.\n")

def lihat_semua_portofolio():
    cur.execute("""
        SELECT p.portofolio_id, m.nama, p.judul, p.jenis, v.status
        FROM Portofolio p JOIN Mahasiswa m ON p.nim = m.nim
        LEFT JOIN Verifikasi v ON p.portofolio_id = v.portofolio_id
    """)
    data = cur.fetchall()
    print("\n=== DAFTAR SEMUA PORTOFOLIO ===")
    for d in data:
        status = d[4].upper() if d[4] else 'BELUM ADA VERIFIKASI'
        print(f"ID: {d[0]} | Nama: {d[1]} | Judul: {d[2]} | Jenis: {d[3]} | Status: {status}")
    print()

def data_portofolio_mahasiswa():
    print("\n=== TAMPILKAN PORTOFOLIO MAHASISWA TERTENTU ===")
    username = input("Masukkan username mahasiswa: ")
    cur.execute("SELECT user_id FROM Users WHERE username=? AND role='mahasiswa'", (username,))
    user = cur.fetchone()

    if not user:
        print("Username mahasiswa tidak ditemukan!\n")
        return

    user_id = user[0]
    cur.execute("SELECT nim, nama FROM Mahasiswa WHERE user_id=?", (user_id,))
    mhs = cur.fetchone()

    if not mhs:
        print("Mahasiswa tidak memiliki data NIM!\n")
        return

    nim, nama = mhs
    cur.execute("""
        SELECT p.portofolio_id, p.judul, p.jenis, v.status
        FROM Portofolio p
        LEFT JOIN Verifikasi v ON p.portofolio_id = v.portofolio_id
        WHERE p.nim=?
    """, (nim,))
    data = cur.fetchall()

    print(f"\n=== DAFTAR PORTOFOLIO MILIK {nama} ({username}) ===")
    if not data:
        print("Mahasiswa belum memiliki portofolio.\n")
        return

    for d in data:
        status = d[3].upper() if d[3] else 'BELUM DIVERIFIKASI'
        print(f"ID: {d[0]} | Judul: {d[1]} | Jenis: {d[2]} | Status: {status}")
    print()


def Hapus_data_portofolio_mahasiswa():
    print("\n=== HAPUS PORTOFOLIO MAHASISWA ===")
    username = input("Masukkan username mahasiswa: ")
    cur.execute("SELECT user_id FROM Users WHERE username=? AND role='mahasiswa'", (username,))
    user = cur.fetchone()

    if not user:
        print("Username mahasiswa tidak ditemukan!\n")
        return

    user_id = user[0]
    cur.execute("SELECT nim, nama FROM Mahasiswa WHERE user_id=?", (user_id,))
    mhs = cur.fetchone()

    if not mhs:
        print("Mahasiswa tidak memiliki data NIM!\n")
        return

    nim, nama = mhs
    cur.execute("""
        SELECT p.portofolio_id, p.judul, p.jenis, v.status
        FROM Portofolio p
        LEFT JOIN Verifikasi v ON p.portofolio_id = v.portofolio_id
        WHERE p.nim=?
    """, (nim,))
    data = cur.fetchall()

    if not data:
        print("Mahasiswa belum memiliki portofolio.\n")
        return

    print(f"\n=== DAFTAR PORTOFOLIO MILIK {nama} ({username}) ===")
    for d in data:
        status = d[3].upper() if d[3] else 'BELUM DIVERIFIKASI'
        print(f"ID: {d[0]} | Judul: {d[1]} | Jenis: {d[2]} | Status: {status}")

    print("\n-----------------------------------")
    pid = input("Masukkan ID portofolio yang ingin dihapus: ")

    cur.execute("SELECT portofolio_id FROM Portofolio WHERE portofolio_id=? AND nim=?", (pid, nim))
    if not cur.fetchone():
        print(" ID portofolio tidak valid untuk mahasiswa ini!\n")
        return

    konfirmasi = input(f"Yakin ingin menghapus portofolio ID {pid}? (YA untuk lanjut): ")
    if konfirmasi.upper() != "YA":
        print("Penghapusan dibatalkan.\n")
        return

    cur.execute("DELETE FROM Bukti WHERE portofolio_id=?", (pid,))
    cur.execute("DELETE FROM Verifikasi WHERE portofolio_id=?", (pid,))
    cur.execute("DELETE FROM Portofolio WHERE portofolio_id=?", (pid,))
    conn.commit()

    print(f"Portofolio ID {pid} berhasil dihapus beserta semua buktinya!\n")


def verifikasi_portofolio(user):
    cur.execute("SELECT user_id FROM Users WHERE user_id=?", (user[0],))
    current_user_id = cur.fetchone()[0]
    cur.execute("SELECT dosen_id FROM Dosen WHERE user_id=?", (current_user_id,))
    dosen_data = cur.fetchone()
    dosen_id = dosen_data[0] if dosen_data else cur.execute("SELECT dosen_id FROM Dosen LIMIT 1").fetchone()[0]
    
    while True:
        print("\n=== VERIFIKASI PORTOFOLIO ===")
        
        cur.execute("""
            SELECT p.portofolio_id, m.nama, p.judul, p.jenis, v.status
            FROM Portofolio p 
            JOIN Mahasiswa m ON p.nim = m.nim
            LEFT JOIN Verifikasi v ON p.portofolio_id = v.portofolio_id
            ORDER BY p.portofolio_id
        """)
        data = cur.fetchall()
        
        if not data:
            print("Belum ada portofolio yang perlu diverifikasi.\n")
            return
        
        print("\n--- DAFTAR PORTOFOLIO ---")
        for d in data:
            status = d[4].upper() if d[4] else 'PENDING'
            status_icon = "" if status == "PENDING" else ("" if status == "APPROVED" else "")
            print(f"{status_icon} ID: {d[0]} | {d[1]} | {d[2]} ({d[3]}) | Status: {status}")
        print("-" * 70)
        
        pid_input = input("\nMasukkan ID portofolio (pisahkan dengan koma untuk banyak ID, contoh: 1,2,3)\natau ketik 'batal' untuk kembali: ").strip()
        
        if pid_input.lower() == 'batal':
            print("Verifikasi dibatalkan.\n")
            return
        
        try:
            pid_list = [pid.strip() for pid in pid_input.split(',')]
        except:
            print("Format input tidak valid!\n")
            continue
        
        valid_ids = []
        for pid in pid_list:
            cur.execute("SELECT portofolio_id FROM Portofolio WHERE portofolio_id=?", (pid,))
            if cur.fetchone():
                valid_ids.append(pid)
            else:
                print(f"ID {pid} tidak ditemukan, dilewati.")
        
        if not valid_ids:
            print("Tidak ada ID valid yang dipilih!\n")
            continue
        
        print(f"\n ID yang akan diverifikasi: {', '.join(valid_ids)}")
        status = input("Status untuk semua ID di atas (approved/rejected): ").lower()
        
        if status not in ['approved', 'rejected']:
            print("Status tidak valid. Harus 'approved' atau 'rejected'.\n")
            continue
        
        success_count = 0
        try:
            for pid in valid_ids:
                cur.execute("UPDATE Verifikasi SET status=?, dosen_id=? WHERE portofolio_id=?", (status, dosen_id, pid))
                if cur.rowcount == 0:
                    cur.execute("INSERT INTO Verifikasi (portofolio_id, dosen_id, status) VALUES (?, ?, ?)", (pid, dosen_id, status))
                success_count += 1
            
            conn.commit()
            print(f"\n Berhasil memverifikasi {success_count} portofolio menjadi {status.upper()}!")
            print(f"   ID yang diverifikasi: {', '.join(valid_ids)}\n")
        except sqlite3.Error as e:
            print(f"Terjadi kesalahan: {e}\n")
            continue
        
        lagi = input("Verifikasi portofolio lain? (y/n): ").lower()
        if lagi != 'y':
            print("Selesai verifikasi.\n")
            return


