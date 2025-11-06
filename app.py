import tkinter as tk
from tkinter import ttk, messagebox
from db_config import query_all
from movie_mgmt import MovieManagement
from cust_rental_mgmt import CustomerManagement, RentalManagement

DARK_BG = "#22313a"
DARK_PANEL = "#1d2a31"
BTN = "#3f90c6"
TEXT = "#e8eef2"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("480x360")
        self.configure(bg=DARK_BG)
        self.resizable(False, False)
        self._style()

        LoginFrame(self).pack(expand=True, fill="both")

    def _style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=DARK_BG)
        style.configure("Panel.TFrame", background=DARK_PANEL)
        style.configure("TLabel", background=DARK_BG, foreground=TEXT, font=("Segoe UI", 11))
        style.configure("Header.TLabel", font=("Segoe UI Semibold", 24))
        style.configure("TEntry", fieldbackground="#dfe6ec", bordercolor="#444")
        style.configure("TButton", padding=8)
        style.map("TButton",
                  background=[("!disabled", BTN), ("pressed", "#2a6b91"), ("active", "#4ca0d6")],
                  foreground=[("!disabled", "white")])

class LoginFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, style="TFrame")
        ttk.Label(self, text="Login", style="Header.TLabel").pack(pady=20)

        form = ttk.Frame(self, style="Panel.TFrame")
        form.pack(padx=30, pady=10, fill="x")

        ttk.Label(form, text="Employee ID:").grid(row=0, column=0, padx=12, pady=12, sticky="e")
        ttk.Label(form, text="Password:").grid(row=1, column=0, padx=12, pady=12, sticky="e")

        self.emp = ttk.Entry(form)
        self.pwd = ttk.Entry(form, show="*")
        self.emp.grid(row=0, column=1, padx=12, pady=12, sticky="ew")
        self.pwd.grid(row=1, column=1, padx=12, pady=12, sticky="ew")
        form.columnconfigure(1, weight=1)

        ttk.Button(self, text="Login", command=self._login).pack(pady=16)

    def _login(self):
        emp = self.emp.get().strip()
        pwd = self.pwd.get().strip()
        if not emp or not pwd:
            messagebox.showwarning("Missing", "Please enter both Employee ID and Password.")
            return

        # Employees table with plaintext 'Password' in the dump (abc@123) – parameterized for safety.
        rows = query_all(
            "SELECT EmployeeID FROM employees WHERE EmployeeID=%s AND Password=%s",
            (emp, pwd),
        )
        if rows:
            Options(self.master)
            self.destroy()
        else:
            messagebox.showerror("Login failed", "Invalid Employee ID or Password.")

class Options(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, style="TFrame")
        self.master = master
        self.pack(expand=True, fill="both")   # <-- this line ensures the frame shows up
        self.create_widgets()

    def create_widgets(self):
        self.master.title("Management Options")
        self.master.geometry("520x300")
        
        ttk.Label(self, text="Select Management Option", style="Header.TLabel").pack(pady=24)

        btn_frame = ttk.Frame(self, style="Panel.TFrame")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Movie Management", command=self.open_movies).pack(pady=6)
        ttk.Button(btn_frame, text="Customer Management", command=self.open_customers).pack(pady=6)
        ttk.Button(btn_frame, text="Rental Management", command=self.open_rentals).pack(pady=6)

    def open_movies(self):
        from movie_mgmt import MovieManagement
        MovieManagement(self.master)

    def open_customers(self):
        from cust_rental_mgmt import CustomerManagement
        CustomerManagement(self.master)

    def open_rentals(self):
        from cust_rental_mgmt import RentalManagement
        RentalManagement(self.master)


if __name__ == "__main__":
    App().mainloop()
