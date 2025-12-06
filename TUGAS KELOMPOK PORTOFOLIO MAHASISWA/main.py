from database import init_database, seed_data
from auth import login, register
from menu_mahasiswa import menu_mahasiswa
from menu_dosen import menu_dosen
from menu_admin import menu_admin

init_database()
seed_data()

def main_menu():
    while True:
        print("=========================================")
        print(" SISTEM INFORMASI PORTOFOLIO MAHASISWA ")
        print("=========================================")
        print("1. Login")
        print("2. Buat Akun (Sign Up)")
        print("3. Keluar")
        
        choice = input("Pilih menu: ")

        if choice == "1":
            user = login()
            if user:
                if user[3] == "mahasiswa":
                    menu_mahasiswa(user)
                elif user[3] == "dosen":
                    menu_dosen(user)
                elif user[3] == "admin":
                    menu_admin(user)
        elif choice == "2":
            register()
        elif choice == "3":
            print("Terima kasih telah menggunakan sistem ini!")
            break
        else:
            print("Pilihan tidak valid.\n")

if __name__ == "__main__":
        main_menu()