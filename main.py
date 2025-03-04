import tkinter as tk
from app import HospitalApp

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()