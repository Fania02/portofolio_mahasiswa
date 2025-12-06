import sqlite3
from database import conn, cur

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

def menu_dosen(user):
    while True:
        print("\n=== MENU DOSEN ===")
        print("1. Lihat Semua Portofolio Mahasiswa")
        print("2. Verifikasi Portofolio")
        print("3. Logout")
        
        choice = input("Pilih menu: ")
        
        if choice == "1":
            lihat_semua_portofolio()
        elif choice == "2":
            verifikasi_portofolio(user)
        elif choice == "3":
            print("Logout berhasil.\n")
            return
        else:
            print("Pilihan tidak valid.\n")