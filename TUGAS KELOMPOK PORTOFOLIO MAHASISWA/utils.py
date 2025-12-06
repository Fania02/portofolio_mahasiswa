import re
import os
import shutil
import platform
import subprocess
from datetime import date
from tkinter import Tk, filedialog
from database import UPLOAD_FOLDER

def is_password_valid(password):
    if re.search(r"(?=.*[0-9])(?=.*[a-zA-Z])", password):
        return True
    return False

def pilih_file():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    file_types = [
        ('Semua File Gambar', '*.jpg *.jpeg *.png *.gif *.bmp'),
        ('JPEG', '*.jpg *.jpeg'),
        ('PNG', '*.png'),
        ('PDF', '*.pdf'),
        ('Word', '*.docx *.doc'),
        ('Text', '*.txt'),
        ('Semua File', '*.*')
    ]
    
    file_path = filedialog.askopenfilename(
        title="Pilih File Bukti",
        filetypes=file_types
    )
    
    root.destroy()
    return file_path

def is_file_valid(file_path):
    if not file_path or not os.path.exists(file_path):
        return False, "File tidak ditemukan!"
    
    valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf', '.docx', '.doc', '.txt', '.gif', '.bmp']
    _, ext = os.path.splitext(file_path)
    
    if ext.lower() not in valid_extensions:
        return False, f"Format file tidak didukung! Hanya menerima: {', '.join(valid_extensions)}"
    
    return True, "OK"

def save_uploaded_file(file_path, portofolio_id):
    try:
        original_filename = os.path.basename(file_path)
        name, ext = os.path.splitext(original_filename)
        
        timestamp = date.today().strftime("%Y%m%d")
        new_filename = f"p{portofolio_id}_{name}_{timestamp}{ext}"
        destination = os.path.join(UPLOAD_FOLDER, new_filename)
        
        shutil.copy2(file_path, destination)
        return destination
    except Exception as e:
        print(f"❌ Error saat menyimpan file: {e}")
        return None

def open_file(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File tidak ditemukan: {file_path}")
        return
    
    try:
        if platform.system() == 'Windows':
            os.startfile(file_path)
        elif platform.system() == 'Darwin':
            subprocess.call(['open', file_path])
        else:
            subprocess.call(['xdg-open', file_path])
        print(f"✅ File dibuka: {file_path}")
    except Exception as e:
        print(f"❌ Error membuka file: {e}")