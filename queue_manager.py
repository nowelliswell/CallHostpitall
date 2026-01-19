import json
from collections import deque
from tkinter import messagebox

class QueueManager:
    def __init__(self):
        self.queues = {
            "Poli Umum": deque(),
            "Poli Gigi": deque(),
            "Poli Anak": deque(),
            "Poli Kandungan": deque(),
            "Pemeriksaan BPJS": deque()
        }
        self.called_patients = []
        self.current_number = {poly: 1 for poly in self.queues.keys()}
        self.load_data()

    def save_data(self):
        """Save queue data to a JSON file."""
        try:
            data = {
                "queues": {poly: list(q) for poly, q in self.queues.items()},
                "current_number": self.current_number,
                "called_patients": self.called_patients
            }
            with open("queue_data.json", "w") as f:
                json.dump(data, f)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan data: {str(e)}")

    def load_data(self):
        """Load queue data from a JSON file."""
        try:
            with open("queue_data.json", "r") as f:
                data = json.load(f)
                self.queues = {poly: deque(q) for poly, q in data["queues"].items()}
                self.current_number = data["current_number"]
                self.called_patients = data.get("called_patients", [])
        except FileNotFoundError:
            pass
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data: {str(e)}")