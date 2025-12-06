from database import clear_all_data, tampilkan_semua_tabel_sql
from menu_dosen import lihat_semua_portofolio, verifikasi_portofolio

def menu_admin(user):
    while True:
        print("\n=== MENU ADMIN ===")
        print("1. Lihat Semua Portofolio Mahasiswa")
        print("2. Verifikasi Portofolio")
        print("3. Akses SQL (Lihat Semua Tabel Data)")
        print("4. Reset Database (Hapus Semua Data)")
        print("5. Logout")
        
        choice = input("Pilih menu: ")
        
        if choice == "1":
            lihat_semua_portofolio()
        elif choice == "2":
            verifikasi_portofolio(user)
        elif choice == "3":
            tampilkan_semua_tabel_sql()
        elif choice == "4":
            clear_all_data()
        elif choice == "5":
            print("Logout berhasil.\n")
            return
        else:
            print("Pilihan tidak valid.\n")

