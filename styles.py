from tkinter import ttk

def configure_styles():
    """Configure the application styles."""
    style = ttk.Style()
    style.theme_use("clam")
    
    # Button Styles
    style.configure("Primary.TButton",
                    foreground="white",
                    background="#007bff",
                    font=("Helvetica", 12, "bold"),
                    padding=8)
    style.map("Primary.TButton",
              background=[("active", "#0069d9")])
    
    style.configure("Success.TButton",
                    foreground="white",
                    background="#28a745",
                    font=("Helvetica", 12, "bold"),
                    padding=8)
    style.map("Success.TButton",
              background=[("active", "#218838")])
    
    style.configure("Danger.TButton",
                    foreground="white",
                    background="#dc3545",
                    font=("Helvetica", 12, "bold"),
                    padding=8)
    style.map("Danger.TButton",
              background=[("active", "#c82333")])
    
    # Frame Styles
    style.configure("TFrame", background="#f8f9fa")
    style.configure("TLabelFrame", background="white", font=("Helvetica", 14, "bold"))
    style.configure("TLabelFrame.Label", background="white")