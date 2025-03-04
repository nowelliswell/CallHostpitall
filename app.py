import tkinter as tk
from tkinter import ttk, messagebox
import pygame
import threading
from queue_manager import QueueManager
from database import save_data_to_db
from tts import speak
from utils import setup_logging, validate_name, restore_data
from styles import configure_styles
import os 
import shutil
from datetime import datetime, timedelta
import logging

class HospitalApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Pemanggilan Rumah Sakit")
        self.root.geometry("800x600")
        self.root.configure(bg="#e9ecef")
        
        self.queue_manager = QueueManager()
        pygame.mixer.init()
        
        setup_logging()
        self.setup_ui()
        self.update_queue_display()
        self.update_called_display()
        
        # Bind poly selection change
        self.poly_combobox.bind("<<ComboboxSelected>>", lambda e: self.update_queue_display())

    def setup_ui(self):
        """Set up the user interface."""
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        title_label = ttk.Label(main_frame, 
                             text="Sistem Pemanggilan Rumah Sakit",
                             font=("Helvetica", 24, "bold"),
                             background="#007bff",
                             foreground="white",
                             padding=10)
        title_label.grid(row=0, column=0, columnspan=3, sticky="ew", pady=10)

        # Controls Frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky="ew")

        ttk.Label(control_frame, text="Pilih Poli:", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        self.poly_var = tk.StringVar()
        self.poly_combobox = ttk.Combobox(control_frame, 
                                       textvariable=self.poly_var,
                                       values=list(self.queue_manager.queues.keys()),
                                       font=("Helvetica", 12),
                                       state="readonly",
                                       width=20)
        self.poly_combobox.pack(side=tk.LEFT, padx=5)
        self.poly_combobox.current(0)

        ttk.Label(control_frame, text="Nama Pasien:", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        self.name_entry = ttk.Entry(control_frame, font=("Helvetica", 12), width=25)
        self.name_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame, 
                    text="Tambahkan Ke Antrian",
                    command=self.add_to_queue,
                    style="Primary.TButton").pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame,
                    text="Panggil Berikutnya",
                    command=self.call_next,
                    style="Success.TButton").pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame,
                    text="CLEAR HISTORY",
                    command=self.clear_called_history,
                    style="Danger.TButton").pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame,
                    text="Restore Data",
                    command=self.restore_data,
                    style="Primary.TButton").pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame,
            text="Panggil Ulang Pasien",
            command=self.recall_patient,
            style="Primary.TButton").pack(side=tk.LEFT, padx=5)

        # Queue Displays
        display_frame = ttk.Frame(main_frame)
        display_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=10)

        # Current Queue (Using Treeview)
        current_queue_frame = ttk.LabelFrame(display_frame, text="Antrian Saat Ini", padding=10)
        current_queue_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
    
        self.queue_tree = ttk.Treeview(current_queue_frame, columns=("Poly", "Number", "Name"), show="headings")
        self.queue_tree.heading("Poly", text="Poli")
        self.queue_tree.heading("Number", text="Nomor")
        self.queue_tree.heading("Name", text="Nama")
        self.queue_tree.column("Poly", width=150, anchor="center")
        self.queue_tree.column("Number", width=100, anchor="center")
        self.queue_tree.column("Name", width=200, anchor="center")
        self.queue_tree.pack(fill=tk.BOTH, expand=True)

        # Called Patients (Using Listbox)
        called_patients_frame = ttk.LabelFrame(display_frame, text="Riwayat Pemanggilan", padding=10)
        called_patients_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
    
        self.called_listbox = tk.Listbox(called_patients_frame,
                                     font=("Helvetica", 12),
                                     height=15,
                                     selectbackground="#d4edda")
        self.called_listbox.pack(fill=tk.BOTH, expand=True)

        # Delete Selected History Button
        delete_button = ttk.Button(called_patients_frame,
                                text="DELETE HISTORY",
                                command=self.delete_selected_history,
                                style="Danger.TButton")
        delete_button.pack(pady=5)

        # Configure Styles
        configure_styles()

    def setup_logging():
        log_file = "hospital_app.log"
        last_reset_file = "last_reset.txt"

        # Cek apakah file last_reset.txt ada
        if os.path.exists(last_reset_file):
            with open(last_reset_file, 'r') as f:
                last_reset_date = f.read().strip()
        else:
            last_reset_date = None

        # Dapatkan tanggal hari ini dan waktu saat ini
        today = datetime.now().date()
        current_time = datetime.now().time()

        # Jika sudah melewati tengah malam dan tanggal hari ini berbeda dari tanggal terakhir reset, reset log
        if current_time >= datetime.strptime("00:00:00", "%H:%M:%S").time() and last_reset_date != str(today):
            if os.path.exists(log_file):
                os.remove(log_file)  # Menghapus file log yang ada

        # Simpan tanggal reset terakhir
        with open(last_reset_file, 'w') as f:
            f.write(str(today))

        # Konfigurasi logging
        logging.basicConfig(filename=log_file, level=logging.INFO, 
                        format="%(asctime)s - %(levelname)s - %(message)s")
        logging.info("Application started.")

    def recall_patient(self):
        """Recall a patient from the called history."""
        selected_index = self.called_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Peringatan", "Silakan pilih pasien dari riwayat pemanggilan.")
            return

        # Retrieve the selected patient's data
        patient_data = self.queue_manager.called_patients[selected_index[0]]
        poly = patient_data[2]  # Get the poly from patient data
        number = patient_data[0]  # Get the queue number from patient data
        name = patient_data[1]  # Get the patient's name from patient data

        # Add the patient back to the queue
        self.queue_manager.queues[poly].append((number, name, poly))
        self.queue_manager.current_number[poly] = max(self.queue_manager.current_number[poly], number + 1)

        # Tampilkan informasi pasien
        messagebox.showinfo("Informasi Pasien", f"Nama: {name}\nNomor Antrian: {number}\nPoli: {poly}")

        # Voice announcement
        announcement = f"Nomor antrian {number}, {name}, silahkan ke {poly}"
        threading.Thread(target=speak, args=(announcement,), daemon=True).start()

    def add_to_queue(self):
        """Add a patient to the queue."""
        poly = self.poly_var.get()
        name = self.name_entry.get().strip()
        
        if not name:
            messagebox.showwarning("Input Kosong", "Silahkan masukkan nama pasien")
            return
            
        if not validate_name(name):
            return
            
        number = self.queue_manager.current_number[poly]
        patient_data = (number, name, poly)
        
        self.queue_manager.queues[poly].append(patient_data)
        self.queue_manager.current_number[poly] += 1
        self.name_entry.delete(0, tk.END)
        self.update_queue_display()
        self.queue_manager.save_data()
        save_data_to_db(self.queue_manager)  # Save to database after adding

    def call_next(self):
        """Call the next patient in the queue."""
        poly = self.poly_var.get()
        if not self.queue_manager.queues[poly]:
            messagebox.showinfo("Info", "Tidak ada antrian di poli ini")
            return
            
        patient_data = self.queue_manager.queues[poly].popleft()
        self.queue_manager.called_patients.insert(0, patient_data)
        
        self.update_queue_display()
        self.update_called_display()
        self.queue_manager.save_data()
        save_data_to_db(self.queue_manager)  # Save to database after calling
        
        # Voice announcement
        announcement = f"Nomor antrian {patient_data[0]}, {patient_data[1]}, silahkan ke {poly}"
        threading.Thread(target=speak, args=(announcement,), daemon=True).start()

    def update_queue_display(self):
        """Update the current queue display."""
        # Clear the Treeview
        for row in self.queue_tree.get_children():
            self.queue_tree.delete(row)
    
        # Add current queue data to the Treeview
        current_poly = self.poly_var.get()
        for patient in self.queue_manager.queues[current_poly]:
            self.queue_tree.insert("", "end", values=(patient[2], f"{patient[0]:03d}", patient[1]))

    def update_called_display(self):
        """Update the called patients display."""
        self.called_listbox.delete(0, tk.END)
        for patient in self.queue_manager.called_patients[:20]:  # Show last 20
            self.called_listbox.insert(tk.END, f"{patient[2]} - {patient[0]:03d} - {patient[1]}")

    def clear_called_history(self):
        """Clear all called patients' history."""
        if not self.queue_manager.called_patients:
            messagebox.showinfo("Info", "Tidak ada riwayat pemanggilan untuk dihapus")
            return

        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus semua riwayat pemanggilan?")
        if confirm:
            self.queue_manager.called_patients.clear()
            self.update_called_display()
            self.queue_manager.save_data()
            save_data_to_db(self.queue_manager)  # Save to database after clearing

    def restore_data(self):
        """Restore data from backup."""
        if os.path.exists("queue_data_backup.json"):
            shutil.copy("queue_data_backup.json", "queue_data.json")
            self.queue_manager.load_data()
            self.update_queue_display()
            self.update_called_display()
            messagebox.showinfo("Info", "Data berhasil dipulihkan dari backup.")
        else:
            messagebox.showwarning("Warning", "Backup file tidak ditemukan.")

    def delete_selected_history(self):
        """Delete the selected patient's history."""
        selected_index = self.called_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Peringatan", "Silakan pilih pasien dari riwayat pemanggilan.")
            return

        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus riwayat ini?")
        if confirm:
            selected_patient = self.queue_manager.called_patients.pop(selected_index[0])
            self.update_called_display()
            self.queue_manager.save_data()
            save_data_to_db(self.queue_manager)  # Save to database after deletion
            messagebox.showinfo("Sukses", f"Riwayat untuk {selected_patient[1]} telah dihapus.")

    def on_closing(self):
        """Handle the application closing event."""
        self.queue_manager.save_data()
        save_data_to_db(self.queue_manager)  # Save to database on closing
        self.root.destroy()