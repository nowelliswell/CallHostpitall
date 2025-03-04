import logging
import os
import shutil
from tkinter import messagebox

def setup_logging():
    logging.basicConfig(filename="hospital_app.log", level=logging.INFO, 
                        format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info("Application started.")

def validate_name(name):
    """Validate the patient's name."""
    if not name.replace(" ", "").isalpha() or len(name) < 2:
        messagebox.showwarning("Input Tidak Valid", "Nama pasien hanya boleh mengandung huruf dan spasi, dan harus lebih dari satu karakter.")
        return False
    return True    

def restore_data(queue_manager):
    """Restore data from backup."""
    if os.path.exists("queue_data_backup.json"):
        shutil.copy("queue_data_backup.json", "queue_data.json")
        queue_manager.load_data()
        messagebox.showinfo("Info", "Data berhasil dipulihkan dari backup.")
    else:
        messagebox.showwarning("Warning", "Backup file tidak ditemukan.")