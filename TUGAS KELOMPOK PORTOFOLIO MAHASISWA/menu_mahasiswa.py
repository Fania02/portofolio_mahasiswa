import os
from datetime import date
from database import conn, cur
from utils import pilih_file, is_file_valid, save_uploaded_file, open_file

def tambah_portofolio(nim):
    print("\n=== TAMBAH PORTOFOLIO ===")
    jenis_dict = {"1": "Pendidikan", "2": "Organisasi", "3": "Prestasi", "4": "Proyek / Karya", "5": "Lain-lain"}
    print("Pilih jenis portofolio:")
    for key, value in jenis_dict.items():
        print(f"[{key}] {value}")
    
    jenis_pilihan = input("Masukkan nomor pilihan (1-5): ")
    if jenis_pilihan not in jenis_dict:
        print("Pilihan tidak valid!\n")
        return
    
    jenis = jenis_dict[jenis_pilihan]
    judul = input("Judul: ")
    deskripsi = input("Deskripsi: ")
    tanggal_input = date.today().isoformat()
    
    cur.execute("INSERT INTO Portofolio (nim,jenis,judul,deskripsi,tanggal_input) VALUES (?,?,?,?,?)", 
                (nim, jenis, judul, deskripsi, tanggal_input))
    conn.commit()
    portofolio_id = cur.lastrowid
    
    tambah_bukti = input("\nApakah Anda ingin menambahkan bukti file pendukung? (y/n): ").lower()
    if tambah_bukti == 'y':
        while True:
            print("\n📎 Tekan Enter untuk membuka file browser...")
            input("(Atau ketik 'skip' untuk lewati): ")
            
            pilihan = input().strip().lower() if False else ""
            
            print("🔍 Membuka file browser...")
            file_path = pilih_file()
            
            if not file_path:
                print("Tidak ada file yang dipilih.")
                retry = input("Coba lagi? (y/n): ").lower()
                if retry != 'y':
                    break
                continue
            
            is_valid, message = is_file_valid(file_path)
            if not is_valid:
                print(f"{message}")
                retry = input("Coba lagi? (y/n): ").lower()
                if retry != 'y':
                    break
                continue
            
            print(f"File dipilih: {os.path.basename(file_path)}")
            print(f"   Path: {file_path}")
            
            saved_path = save_uploaded_file(file_path, portofolio_id)
            if saved_path:
                keterangan = input("Keterangan bukti: ")
                cur.execute("INSERT INTO Bukti (portofolio_id, file_path, keterangan) VALUES (?,?,?)", 
                           (portofolio_id, saved_path, keterangan))
                conn.commit()
                print(f"File berhasil diupload: {os.path.basename(saved_path)}")
            
            lagi = input("\nTambah file bukti lagi? (y/n): ").lower()
            if lagi != 'y':
                break
    
    cur.execute("SELECT dosen_id FROM Dosen LIMIT 1")
    dosen_data = cur.fetchone()
    if dosen_data:
        dosen_id_default = dosen_data[0]
        cur.execute("INSERT INTO Verifikasi (portofolio_id, dosen_id, status) VALUES (?, ?, 'pending')", 
                   (portofolio_id, dosen_id_default))
        conn.commit()
    
    print(f"\n Portofolio jenis '{jenis}' berhasil ditambahkan dan menunggu verifikasi!\n")

def lihat_portofolio_mahasiswa(nim):
    cur.execute("""
        SELECT p.portofolio_id, p.judul, p.jenis, v.status FROM Portofolio p
        LEFT JOIN Verifikasi v ON p.portofolio_id = v.portofolio_id WHERE p.nim=?
    """, (nim,))
    data = cur.fetchall()
    
    if data:
        print("\n=== DAFTAR PORTOFOLIO SAYA ===")
        for d in data:
            status = d[3].upper() if d[3] else 'PENDING'
            print(f"ID: {d[0]} | {d[1]} ({d[2]}) | Status: {status}")
        
        print("\n" + "="*50)
        lihat_detail = input("Lihat detail portofolio? Masukkan ID (atau tekan Enter untuk kembali): ").strip()
        if lihat_detail:
            lihat_detail_portofolio(lihat_detail, nim)
    else:
        print("\n Belum ada portofolio.")
    print()

def lihat_detail_portofolio(portofolio_id, nim):
    cur.execute("""
        SELECT p.judul, p.jenis, p.deskripsi, p.tanggal_input, v.status 
        FROM Portofolio p
        LEFT JOIN Verifikasi v ON p.portofolio_id = v.portofolio_id
        WHERE p.portofolio_id = ? AND p.nim = ?
    """, (portofolio_id, nim))
    
    data = cur.fetchone()
    if not data:
        print("Portofolio tidak ditemukan!\n")
        return
    
    print("\n" + "="*60)
    print(f"DETAIL PORTOFOLIO (ID: {portofolio_id})")
    print("="*60)
    print(f"Judul       : {data[0]}")
    print(f"Jenis       : {data[1]}")
    print(f"Deskripsi   : {data[2]}")
    print(f"Tanggal     : {data[3]}")
    print(f"Status      : {data[4].upper() if data[4] else 'PENDING'}")
    print("="*60)
    
    cur.execute("SELECT bukti_id, file_path, keterangan FROM Bukti WHERE portofolio_id = ?", (portofolio_id,))
    bukti_list = cur.fetchall()
    
    if bukti_list:
        print(f"\n📎 FILE BUKTI ({len(bukti_list)} file):")
        for i, bukti in enumerate(bukti_list, 1):
            print(f"{i}. {os.path.basename(bukti[1])} - {bukti[2]}")
        
        print("\n" + "="*60)
        buka_file = input("Buka file bukti? Masukkan nomor (atau tekan Enter untuk kembali): ").strip()
        
        if buka_file.isdigit():
            idx = int(buka_file) - 1
            if 0 <= idx < len(bukti_list):
                open_file(bukti_list[idx][1])
            else:
                print("Nomor tidak valid!")
    else:
        print("\n📎 Tidak ada file bukti untuk portofolio ini.")
    
    print()

def edit_portofolio(nim):
    print("\n=== EDIT PORTOFOLIO ===")
    lihat_portofolio_mahasiswa(nim)
    pid = input("Masukkan ID portofolio yang ingin diubah: ")
    cur.execute("SELECT judul, jenis, deskripsi FROM Portofolio WHERE portofolio_id=? AND nim=?", (pid, nim))
    data = cur.fetchone()
    if not data:
        print("Portofolio ID tidak ditemukan atau bukan milik Anda.\n")
        return
    
    print(f"\n--- Portofolio Saat Ini (ID: {pid}) ---")
    print(f"Judul: {data[0]}")
    print(f"Jenis: {data[1]}")
    print(f"Deskripsi: {data[2]}")
    print("---------------------------------------")
    
    new_judul = input(f"Masukkan Judul baru (kosongkan untuk tetap {data[0]}): ") or data[0]
    new_jenis = input(f"Masukkan Jenis baru (kosongkan untuk tetap {data[1]}): ") or data[1]
    new_deskripsi = input(f"Masukkan Deskripsi baru (kosongkan untuk tetap {data[2]}): ") or data[2]
    
    cur.execute("""UPDATE Portofolio SET judul = ?, jenis = ?, deskripsi = ? WHERE portofolio_id = ? AND nim = ?""", 
                (new_judul, new_jenis, new_deskripsi, pid, nim))
    cur.execute("""UPDATE Verifikasi SET status = 'pending' WHERE portofolio_id = ?""", (pid,))
    conn.commit()
    print("Portofolio berhasil diperbarui! Status verifikasi direset menjadi PENDING.\n")

def menu_mahasiswa(user):
    cur.execute("SELECT nim FROM Mahasiswa WHERE user_id=?", (user[0],))
    nim = cur.fetchone()[0]
    
    while True:
        print("\n=== MENU MAHASISWA ===")
        print("1. Tambah Portofolio")
        print("2. Lihat Portofolio Saya")
        print("3. Edit Portofolio")
        print("4. Hapus Portofolio")
        print("5. Logout")
        
        choice = input("Pilih menu: ")
        
        if choice == "1":
            tambah_portofolio(nim)
        elif choice == "2":
            lihat_portofolio_mahasiswa(nim)
        elif choice == "3":
            edit_portofolio(nim)
        elif choice == "4":
            pid = input("Masukkan ID portofolio yang ingin dihapus: ")
            cur.execute("DELETE FROM Portofolio WHERE portofolio_id=? AND nim=?", (pid, nim))
            cur.execute("DELETE FROM Bukti WHERE portofolio_id=?", (pid,))
            cur.execute("DELETE FROM Verifikasi WHERE portofolio_id=?", (pid,))
            conn.commit()
            print("Portofolio dan data terkait dihapus!\n")
        elif choice == "5":
            print("Logout berhasil.\n")
            return
        else:
            print("Pilihan tidak valid.\n")