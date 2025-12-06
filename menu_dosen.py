from menu_admin import lihat_semua_portofolio
def menu_dosen(user):
    while True:
        print("\n=== MENU DOSEN ===")
        print("1. Lihat Semua Portofolio Mahasiswa")
        print("2. Verifikasi Portofolio")
        print("3. Logout")
        
        choice = input("Pilih menu: ")
        
        if choice == "1":
            lihat_semua_portofolio()
        elif choice == "3":
            print("Logout berhasil.\n")
            return
        else:
            print("Pilihan tidak valid.\n")