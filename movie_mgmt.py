import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
from datetime import date
import matplotlib.pyplot as plt

# import your custom modules
from db_config import query_all, execute, export_to_excel, timestamped


DARK_BG = "#22313a"
DARK_PANEL = "#1d2a31"
BTN = "#3f90c6"
TEXT = "#e8eef2"


class MovieManagement(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Movies - Movie Management")
        self.geometry("1000x640")
        self.configure(bg=DARK_BG)

        self._style()
        self._topbar()
        self._search_bar()
        self._table()
        self.view_all()

    # ---------- UI Setup ----------
    def _style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=DARK_BG)
        style.configure("Panel.TFrame", background=DARK_PANEL)
        style.configure("TLabel", background=DARK_BG, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("Header.TLabel", background=DARK_BG, foreground=TEXT, font=("Segoe UI Semibold", 18))
        style.configure("TEntry", fieldbackground="#dfe6ec", bordercolor="#444")
        style.configure("TButton", padding=6)
        style.map("TButton",
                  background=[("!disabled", BTN), ("pressed", "#2a6b91"), ("active", "#4ca0d6")],
                  foreground=[("!disabled", "white")])
        style.configure("Treeview", background="white", fieldbackground="white", rowheight=22)
        style.configure("Treeview.Heading", font=("Segoe UI Semibold", 10))

    def _topbar(self):
        top = ttk.Frame(self, style="Panel.TFrame")
        top.pack(fill="x")
        ttk.Label(top, text="Movie Management", style="Header.TLabel").pack(side="left", padx=12, pady=10)

        # Switch to other management windows
        ttk.Button(top, text="Customer Management",
                   command=lambda: __import__("cust_rental_mgmt").cust_rental_mgmt.CustomerManagement(self)).pack(side="right", padx=6, pady=6)
        ttk.Button(top, text="Rental Management",
                   command=lambda: __import__("cust_rental_mgmt").cust_rental_mgmt.RentalManagement(self)).pack(side="right", padx=6, pady=6)

        # Action buttons bar
        bar = ttk.Frame(self, style="Panel.TFrame")
        bar.pack(fill="x", pady=(8, 0))
        ttk.Button(bar, text="View Movies", command=self.view_all).pack(side="left", padx=6, pady=6)
        ttk.Button(bar, text="Add Movie", command=self.add_movie).pack(side="left", padx=6, pady=6)
        ttk.Button(bar, text="Update Movie", command=self.update_movie).pack(side="left", padx=6, pady=6)
        ttk.Button(bar, text="Delete Movie", command=self.delete_movie).pack(side="left", padx=6, pady=6)
        ttk.Button(bar, text="Generate Reports", command=self.report_menu).pack(side="left", padx=6, pady=6)

    def _search_bar(self):
        s = ttk.Frame(self, style="Panel.TFrame")
        s.pack(fill="x", padx=8, pady=8)

        self.title_var = tk.StringVar()
        self.genre_var = tk.StringVar()
        self.producer_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.price_min = tk.StringVar()
        self.price_max = tk.StringVar()

        ttk.Label(s, text="Title:").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        ttk.Entry(s, textvariable=self.title_var, width=24).grid(row=0, column=1, padx=6, pady=6)
        ttk.Label(s, text="Genre:").grid(row=0, column=2, padx=6, pady=6, sticky="e")
        ttk.Entry(s, textvariable=self.genre_var, width=18).grid(row=0, column=3, padx=6, pady=6)
        ttk.Label(s, text="Producer:").grid(row=0, column=4, padx=6, pady=6, sticky="e")
        ttk.Entry(s, textvariable=self.producer_var, width=18).grid(row=0, column=5, padx=6, pady=6)

        ttk.Label(s, text="Release Year:").grid(row=1, column=0, padx=6, pady=6, sticky="e")
        ttk.Entry(s, textvariable=self.year_var, width=12).grid(row=1, column=1, padx=6, pady=6, sticky="w")
        ttk.Label(s, text="Price Range:").grid(row=1, column=2, padx=6, pady=6, sticky="e")
        ttk.Entry(s, textvariable=self.price_min, width=10).grid(row=1, column=3, padx=6, pady=6, sticky="w")
        ttk.Label(s, text="to").grid(row=1, column=4, padx=2, pady=6, sticky="e")
        ttk.Entry(s, textvariable=self.price_max, width=10).grid(row=1, column=5, padx=6, pady=6, sticky="w")

        ttk.Button(s, text="Search", command=self.search).grid(row=0, column=6, padx=10)
        ttk.Button(s, text="Clear Search", command=self.view_all).grid(row=1, column=6, padx=10)
        for i in range(7):
            s.columnconfigure(i, weight=1)

    def _table(self):
        cols = ("MovieID", "Title", "Genre", "ReleaseYear", "RentalPrice", "ProducerID")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=130 if c != "Title" else 280)
        self.tree.pack(expand=True, fill="both", padx=8, pady=(0, 8))

    # ---------- Database Actions ----------
    def view_all(self):
        self._fill(query_all("SELECT MovieID, Title, Genre, ReleaseYear, RentalPrice, ProducerID FROM movies ORDER BY MovieID"))
        # Clear search inputs
        for v in (self.title_var, self.genre_var, self.producer_var, self.year_var, self.price_min, self.price_max):
            v.set("")

    def search(self):
        sql = """
        SELECT m.MovieID, m.Title, m.Genre, m.ReleaseYear, m.RentalPrice, m.ProducerID
        FROM movies m
        LEFT JOIN producer p ON p.ProducerID = m.ProducerID
        WHERE (%s='' OR m.Title LIKE CONCAT('%%', %s, '%%'))
          AND (%s='' OR m.Genre LIKE CONCAT('%%', %s, '%%'))
          AND (%s='' OR p.ProducerName LIKE CONCAT('%%', %s, '%%') OR m.ProducerID=%s)
          AND (%s='' OR m.ReleaseYear=%s)
          AND (%s='' OR m.RentalPrice >= %s)
          AND (%s='' OR m.RentalPrice <= %s)
        ORDER BY m.MovieID
        """
        p = (self.title_var.get(), self.title_var.get(),
             self.genre_var.get(), self.genre_var.get(),
             self.producer_var.get(), self.producer_var.get(), self.producer_var.get(),
             self.year_var.get(), self.year_var.get(),
             self.price_min.get(), self.price_min.get(),
             self.price_max.get(), self.price_max.get())
        self._fill(query_all(sql, p))

    def add_movie(self):
        try:
            mid = int(askstring("Add Movie", "MovieID (integer):"))
            title = askstring("Add Movie", "Title:") or ""
            genre = askstring("Add Movie", "Genre:") or ""
            year = int(askstring("Add Movie", "Release Year (YYYY):") or "0")
            price = float(askstring("Add Movie", "Rental Price:") or "0")
            prod = int(askstring("Add Movie", "ProducerID (int):") or "0")
        except (TypeError, ValueError):
            messagebox.showerror("Invalid", "Please provide valid values.")
            return

        execute("INSERT INTO movies (MovieID, Title, Genre, ReleaseYear, RentalPrice, ProducerID) VALUES (%s,%s,%s,%s,%s,%s)",
                (mid, title, genre, year, price, prod))
        self.view_all()

    def update_movie(self):
        item = self._selected()
        if not item: return
        vals = self.tree.item(item, "values")
        mid = int(vals[0])
        title = askstring("Update Movie", "Title:", initialvalue=vals[1]) or vals[1]
        genre = askstring("Update Movie", "Genre:", initialvalue=vals[2]) or vals[2]
        year = askstring("Update Movie", "Release Year:", initialvalue=vals[3]) or vals[3]
        price = askstring("Update Movie", "Rental Price:", initialvalue=vals[4]) or vals[4]
        prod = askstring("Update Movie", "ProducerID:", initialvalue=vals[5]) or vals[5]
        execute("UPDATE movies SET Title=%s, Genre=%s, ReleaseYear=%s, RentalPrice=%s, ProducerID=%s WHERE MovieID=%s",
                (title, genre, year, price, prod, mid))
        self.view_all()

    def delete_movie(self):
        item = self._selected()
        if not item: return
        mid = int(self.tree.item(item, "values")[0])
        used = query_all("SELECT COUNT(*) c FROM issuetran WHERE MovieID=%s AND ReturnDate IS NULL", (mid,))
        if used and used[0]["c"] > 0:
            messagebox.showerror("Blocked", "This movie is currently rented out and cannot be deleted.")
            return
        if messagebox.askyesno("Confirm", f"Delete MovieID {mid}?"):
            execute("DELETE FROM movies WHERE MovieID=%s", (mid,))
            self.view_all()

    # ---------- Reports ----------
    def report_menu(self):
        menu = tk.Menu(self, tearoff=False)
        menu.add_command(label="Movies currently rented out", command=self.report_currently_rented)
        menu.add_command(label="Overdue rentals", command=self.report_overdue)
        menu.add_command(label="Rental stats by Genre (Excel + Chart)", command=self.report_genre_stats)
        try:
            menu.tk_popup(self.winfo_rootx() + 200, self.winfo_rooty() + 90)
        finally:
            menu.grab_release()

    def report_currently_rented(self):
        rows = query_all("""
            SELECT i.IssueID, i.CustomerID, i.MovieID, i.IssueDate, i.dueDate,
                   CONCAT(c.FirstName,' ',c.LastName) AS CustomerName, m.Title AS MovieTitle
            FROM issuetran i
            JOIN customer c ON c.CustomerID = i.CustomerID
            JOIN movies m   ON m.MovieID = i.MovieID
            WHERE i.ReturnDate IS NULL
            ORDER BY i.dueDate
        """)
        file = export_to_excel(timestamped("currently_rented"),
                               ["IssueID","CustomerID","MovieID","IssueDate","dueDate","CustomerName","MovieTitle"],
                               rows)
        messagebox.showinfo("Excel", f"✅ Report saved successfully!\n\nLocation:\n{file}")

    def report_overdue(self):
        rows = query_all("""
            SELECT i.IssueID, i.CustomerID, i.MovieID, i.IssueDate, i.dueDate,
                   CONCAT(c.FirstName,' ',c.LastName) AS CustomerName, m.Title AS MovieTitle
            FROM issuetran i
            JOIN customer c ON c.CustomerID = i.CustomerID
            JOIN movies m   ON m.MovieID = i.MovieID
            WHERE i.ReturnDate IS NULL AND i.dueDate < CURDATE()
            ORDER BY i.dueDate
        """)
        file = export_to_excel(timestamped("overdue_rentals"),
                               ["IssueID","CustomerID","MovieID","IssueDate","dueDate","CustomerName","MovieTitle"],
                               rows)
        messagebox.showinfo("Excel", f"✅ Report saved successfully!\n\nLocation:\n{file}")

    def report_genre_stats(self):
        rows = query_all("""
            SELECT m.Genre, COUNT(*) AS TotalRentals
            FROM issuetran i
            JOIN movies m ON m.MovieID = i.MovieID
            GROUP BY m.Genre
            ORDER BY TotalRentals DESC
        """)
        file = export_to_excel(timestamped("rentals_by_genre"), ["Genre","TotalRentals"], rows)

        # Chart display
        genres = [r["Genre"] for r in rows]
        totals = [r["TotalRentals"] for r in rows]
        plt.figure()
        plt.bar(genres, totals)
        plt.title("Rentals by Genre")
        plt.xlabel("Genre")
        plt.ylabel("Total Rentals")
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.show()
        messagebox.showinfo("Excel", f"✅ Report saved successfully!\n\nLocation:\n{file}")

    # ---------- Helpers ----------
    def _fill(self, rows):
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert("", "end", values=(r["MovieID"], r["Title"], r["Genre"], r["ReleaseYear"], r["RentalPrice"], r["ProducerID"]))

    def _selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Please select a row first.")
            return None
        return sel[0]
