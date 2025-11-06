import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
from datetime import datetime, timedelta
from db_config import query_all, execute, export_to_excel, timestamped
import matplotlib.pyplot as plt

DARK_BG = "#22313a"
DARK_PANEL = "#1d2a31"
BTN = "#3f90c6"
TEXT = "#e8eef2"


# --------------------- CUSTOMER MANAGEMENT ---------------------
class CustomerManagement(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Movies - Customer Management")
        self.geometry("1000x640")
        self.configure(bg=DARK_BG)
        self._style()
        self._topbar()
        self._search_bar()
        self._table()
        self.view_all()

    def _style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TFrame", background=DARK_BG)
        s.configure("Panel.TFrame", background=DARK_PANEL)
        s.configure("TLabel", background=DARK_BG, foreground=TEXT, font=("Segoe UI", 10))
        s.configure("Header.TLabel", background=DARK_BG, foreground=TEXT, font=("Segoe UI Semibold", 18))
        s.configure("TButton", padding=6)
        s.map("TButton",
              background=[("!disabled", BTN), ("pressed", "#2a6b91"), ("active", "#4ca0d6")],
              foreground=[("!disabled", "white")])
        s.configure("Treeview", background="white", fieldbackground="white", rowheight=22)
        s.configure("Treeview.Heading", font=("Segoe UI Semibold", 10))

    def _topbar(self):
        top = ttk.Frame(self, style="Panel.TFrame")
        top.pack(fill="x")
        ttk.Label(top, text="Customer Management", style="Header.TLabel").pack(side="left", padx=12, pady=10)
        ttk.Button(top, text="Movie Management",
                   command=lambda: __import__("movie_mgmt").movie_mgmt.MovieManagement(self)).pack(side="right", padx=6, pady=6)
        ttk.Button(top, text="Rental Management",
                   command=lambda: RentalManagement(self)).pack(side="right", padx=6, pady=6)

        bar = ttk.Frame(self, style="Panel.TFrame")
        bar.pack(fill="x", pady=(8, 0))
        ttk.Button(bar, text="View Customers", command=self.view_all).pack(side="left", padx=6, pady=6)
        ttk.Button(bar, text="Add Customer", command=self.add_customer).pack(side="left", padx=6, pady=6)
        ttk.Button(bar, text="Update Customer", command=self.update_customer).pack(side="left", padx=6, pady=6)
        ttk.Button(bar, text="Delete Customer", command=self.delete_customer).pack(side="left", padx=6, pady=6)
        ttk.Button(bar, text="Generate Reports", command=self.reports_menu).pack(side="left", padx=6, pady=6)

    def _search_bar(self):
        s = ttk.Frame(self, style="Panel.TFrame")
        s.pack(fill="x", padx=8, pady=8)
        self.fname = tk.StringVar()
        self.lname = tk.StringVar()
        self.email = tk.StringVar()
        ttk.Label(s, text="First Name:").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        ttk.Entry(s, textvariable=self.fname, width=20).grid(row=0, column=1, padx=6, pady=6)
        ttk.Label(s, text="Last Name:").grid(row=0, column=2, padx=6, pady=6, sticky="e")
        ttk.Entry(s, textvariable=self.lname, width=20).grid(row=0, column=3, padx=6, pady=6)
        ttk.Label(s, text="Email:").grid(row=0, column=4, padx=6, pady=6, sticky="e")
        ttk.Entry(s, textvariable=self.email, width=26).grid(row=0, column=5, padx=6, pady=6)
        ttk.Button(s, text="Search", command=self.search).grid(row=0, column=6, padx=10)
        ttk.Button(s, text="Clear Search", command=self.view_all).grid(row=0, column=7, padx=10)

    def _table(self):
        cols = ("CustomerID", "Title", "FirstName", "LastName", "Phone", "Email")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=130 if c not in ("Email", "FirstName", "LastName") else 180)
        self.tree.pack(expand=True, fill="both", padx=8, pady=(0, 8))

    def view_all(self):
        rows = query_all("SELECT CustomerID, Title, FirstName, LastName, Phone, Email FROM customer ORDER BY CustomerID")
        self._fill(rows)
        self.fname.set(""); self.lname.set(""); self.email.set("")

    def search(self):
        sql = """
        SELECT CustomerID, Title, FirstName, LastName, Phone, Email
        FROM customer
        WHERE (%s='' OR FirstName LIKE CONCAT('%%',%s,'%%'))
          AND (%s='' OR LastName  LIKE CONCAT('%%',%s,'%%'))
          AND (%s='' OR Email     LIKE CONCAT('%%',%s,'%%'))
        ORDER BY CustomerID
        """
        p = (self.fname.get(), self.fname.get(), self.lname.get(), self.lname.get(), self.email.get(), self.email.get())
        self._fill(query_all(sql, p))

    def add_customer(self):
        try:
            cid = int(askstring("Add Customer", "CustomerID (int):"))
            title = askstring("Add Customer", "Title (Mr/Ms/Dr...):") or ""
            fn = askstring("Add Customer", "First Name:") or ""
            ln = askstring("Add Customer", "Last Name:") or ""
            ph = askstring("Add Customer", "Phone (10 digits):") or ""
            em = askstring("Add Customer", "Email:") or ""
        except (TypeError, ValueError):
            messagebox.showerror("Invalid", "Please provide valid values.")
            return
        execute("INSERT INTO customer (CustomerID, Title, FirstName, LastName, Phone, Email) VALUES (%s,%s,%s,%s,%s,%s)",
                (cid, title, fn, ln, ph, em))
        self.view_all()

    def update_customer(self):
        item = self._selected()
        if not item: return
        vals = self.tree.item(item, "values")
        cid = int(vals[0])
        title = askstring("Update Customer", "Title:", initialvalue=vals[1]) or vals[1]
        fn = askstring("Update Customer", "First Name:", initialvalue=vals[2]) or vals[2]
        ln = askstring("Update Customer", "Last Name:", initialvalue=vals[3]) or vals[3]
        ph = askstring("Update Customer", "Phone:", initialvalue=vals[4]) or vals[4]
        em = askstring("Update Customer", "Email:", initialvalue=vals[5]) or vals[5]
        execute("UPDATE customer SET Title=%s, FirstName=%s, LastName=%s, Phone=%s, Email=%s WHERE CustomerID=%s",
                (title, fn, ln, ph, em, cid))
        self.view_all()

    def delete_customer(self):
        item = self._selected()
        if not item: return
        cid = int(self.tree.item(item, "values")[0])
        used = query_all("SELECT COUNT(*) c FROM issuetran WHERE CustomerID=%s AND ReturnDate IS NULL", (cid,))
        if used and used[0]["c"] > 0:
            messagebox.showerror("Blocked", "This customer has active rentals.")
            return
        if messagebox.askyesno("Confirm", f"Delete CustomerID {cid}?"):
            execute("DELETE FROM customer WHERE CustomerID=%s", (cid,))
            self.view_all()

    def reports_menu(self):
        menu = tk.Menu(self, tearoff=False)
        menu.add_command(label="Customers with active rentals (Excel)", command=self.report_active_customers)
        try:
            menu.tk_popup(self.winfo_rootx() + 200, self.winfo_rooty() + 90)
        finally:
            menu.grab_release()

    def report_active_customers(self):
        rows = query_all("""
            SELECT DISTINCT c.CustomerID, CONCAT(c.FirstName,' ',c.LastName) AS CustomerName, c.Email, c.Phone
            FROM issuetran i
            JOIN customer c ON c.CustomerID = i.CustomerID
            WHERE i.ReturnDate IS NULL
            ORDER BY c.CustomerID
        """)
        file = export_to_excel(timestamped("customers_with_active_rentals"),
                               ["CustomerID", "CustomerName", "Email", "Phone"], rows)
        messagebox.showinfo("Excel", f"Saved: {file}")

    def _fill(self, rows):
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert("", "end", values=(r["CustomerID"], r["Title"], r["FirstName"], r["LastName"], r["Phone"], r["Email"]))

    def _selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Please select a row first.")
            return None
        return sel[0]


# --------------------- RENTAL MANAGEMENT ---------------------
class RentalManagement(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Movies - Rental Management")
        self.geometry("1000x640")
        self.configure(bg=DARK_BG)
        self._style()
        self._topbar()
        self._filters()
        self._table()
        self.view_all()

    def _style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TFrame", background=DARK_BG)
        s.configure("Panel.TFrame", background=DARK_PANEL)
        s.configure("TLabel", background=DARK_BG, foreground=TEXT, font=("Segoe UI", 10))
        s.configure("Header.TLabel", background=DARK_BG, foreground=TEXT, font=("Segoe UI Semibold", 18))
        s.configure("TButton", padding=6)
        s.map("TButton", background=[("!disabled", BTN), ("pressed", "#2a6b91"), ("active", "#4ca0d6")],
              foreground=[("!disabled", "white")])
        s.configure("Treeview", background="white", fieldbackground="white", rowheight=22)
        s.configure("Treeview.Heading", font=("Segoe UI Semibold", 10))

    def _topbar(self):
        top = ttk.Frame(self, style="Panel.TFrame"); top.pack(fill="x")
        ttk.Label(top, text="Rental Management", style="Header.TLabel").pack(side="left", padx=12, pady=10)
        ttk.Button(top, text="Customer Management", command=lambda: CustomerManagement(self)).pack(side="right", padx=6, pady=6)
        ttk.Button(top, text="Movie Management",
                   command=lambda: __import__("movie_mgmt").movie_mgmt.MovieManagement(self)).pack(side="right", padx=6, pady=6)

        bar = ttk.Frame(self, style="Panel.TFrame"); bar.pack(fill="x", pady=(8, 4))
        ttk.Button(bar, text="View Rentals", command=self.view_all).pack(side="left", padx=6, pady=6)
        ttk.Button(bar, text="Issue Movie", command=self.open_issue_window).pack(side="left", padx=6, pady=6)
        ttk.Button(bar, text="Return Movie", command=self.open_return_window).pack(side="left", padx=6, pady=6)
        ttk.Button(bar, text="Generate Reports", command=self.report_menu).pack(side="left", padx=6, pady=6)

    def _filters(self):
        s = ttk.Frame(self, style="Panel.TFrame"); s.pack(fill="x", padx=8, pady=8)
        self.name = tk.StringVar()
        self.title = tk.StringVar()
        ttk.Label(s, text="Customer Name:").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        ttk.Entry(s, textvariable=self.name, width=24).grid(row=0, column=1, padx=6, pady=6)
        ttk.Label(s, text="Movie Title:").grid(row=0, column=2, padx=6, pady=6, sticky="e")
        ttk.Entry(s, textvariable=self.title, width=24).grid(row=0, column=3, padx=6, pady=6)
        ttk.Button(s, text="Search", command=self.search).grid(row=0, column=4, padx=10)
        ttk.Button(s, text="Clear Search", command=self.view_all).grid(row=0, column=5, padx=10)

    def _table(self):
        cols = ("IssueID", "CustomerID", "CustomerName", "MovieID", "MovieTitle", "IssueDate", "ReturnDate", "dueDate")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120 if c not in ("CustomerName", "MovieTitle") else 200)
        self.tree.pack(expand=True, fill="both", padx=8, pady=(0, 8))

    # --------------- Rentals Logic ---------------
    def view_all(self):
        sql = """
        SELECT i.IssueID, c.CustomerID, CONCAT(c.FirstName,' ',c.LastName) AS CustomerName,
               m.MovieID, m.Title AS MovieTitle, i.IssueDate, i.ReturnDate, i.dueDate
        FROM issuetran i
        JOIN customer c ON c.CustomerID = i.CustomerID
        JOIN movies m ON m.MovieID = i.MovieID
        ORDER BY i.IssueID
        """
        self._fill(query_all(sql))

    def search(self):
        sql = """
        SELECT i.IssueID, c.CustomerID, CONCAT(c.FirstName,' ',c.LastName) AS CustomerName,
               m.MovieID, m.Title AS MovieTitle, i.IssueDate, i.ReturnDate, i.dueDate
        FROM issuetran i
        JOIN customer c ON c.CustomerID = i.CustomerID
        JOIN movies m ON m.MovieID = i.MovieID
        WHERE (%s='' OR CONCAT(c.FirstName,' ',c.LastName) LIKE CONCAT('%%',%s,'%%'))
          AND (%s='' OR m.Title LIKE CONCAT('%%',%s,'%%'))
        ORDER BY i.IssueID
        """
        p = (self.name.get(), self.name.get(), self.title.get(), self.title.get())
        self._fill(query_all(sql, p))

    # ---------- GUI-based issue ----------
    def open_issue_window(self):
        win = tk.Toplevel(self)
        win.title("Issue a Movie")
        win.geometry("400x320")
        win.configure(bg=DARK_BG)

        ttk.Label(win, text="Customer:", style="TLabel").pack(pady=8)
        customers = query_all("SELECT CustomerID, CONCAT(FirstName,' ',LastName) AS Name FROM customer")
        self.customer_cb = ttk.Combobox(win, values=[f"{r['CustomerID']} - {r['Name']}" for r in customers], width=35)
        self.customer_cb.pack(pady=5)

        ttk.Label(win, text="Movie:", style="TLabel").pack(pady=8)
        movies = query_all("SELECT MovieID, Title FROM movies")
        self.movie_cb = ttk.Combobox(win, values=[f"{r['MovieID']} - {r['Title']}" for r in movies], width=35)
        self.movie_cb.pack(pady=5)

        ttk.Label(win, text="Issue Date (YYYY-MM-DD):", style="TLabel").pack(pady=8)
        issue_entry = ttk.Entry(win)
        issue_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
        issue_entry.pack(pady=5)

        ttk.Label(win, text="Due Date (YYYY-MM-DD):", style="TLabel").pack(pady=8)
        due_entry = ttk.Entry(win)
        due_entry.insert(0, (datetime.today() + timedelta(days=7)).strftime("%Y-%m-%d"))
        due_entry.pack(pady=5)

        ttk.Button(win, text="Confirm Issue",
                   command=lambda: self._confirm_issue(win, issue_entry.get(), due_entry.get())).pack(pady=15)

    def _confirm_issue(self, win, issue_date, due_date):
        try:
            cid = int(self.customer_cb.get().split(" - ")[0])
            mid = int(self.movie_cb.get().split(" - ")[0])
        except:
            messagebox.showerror("Missing", "Please select both customer and movie.")
            return

        execute("INSERT INTO issuetran (IssueID, CustomerID, MovieID, IssueDate, ReturnDate, dueDate) "
                "VALUES ((SELECT COALESCE(MAX(IssueID),0)+1 FROM issuetran), %s, %s, %s, NULL, %s)",
                (cid, mid, issue_date, due_date))
        messagebox.showinfo("Issued", f"Movie issued successfully!\nDue on: {due_date}")
        win.destroy()
        self.view_all()

    # ---------- GUI-based return ----------
    def open_return_window(self):
        win = tk.Toplevel(self)
        win.title("Return a Movie")
        win.geometry("400x260")
        win.configure(bg=DARK_BG)

        ttk.Label(win, text="Select IssueID to return:", style="TLabel").pack(pady=8)
        rentals = query_all("""
            SELECT i.IssueID, CONCAT(c.FirstName,' ',c.LastName,' - ',m.Title) AS Info
            FROM issuetran i
            JOIN customer c ON c.CustomerID=i.CustomerID
            JOIN movies m ON m.MovieID=i.MovieID
            WHERE i.ReturnDate IS NULL
        """)
        self.return_cb = ttk.Combobox(win, values=[f"{r['IssueID']} - {r['Info']}" for r in rentals], width=40)
        self.return_cb.pack(pady=5)

        ttk.Label(win, text="Return Date (YYYY-MM-DD):", style="TLabel").pack(pady=8)
        ret_entry = ttk.Entry(win)
        ret_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
        ret_entry.pack(pady=5)

        ttk.Button(win, text="Confirm Return", command=lambda: self._confirm_return(win, ret_entry.get())).pack(pady=15)

    def _confirm_return(self, win, return_date):
        try:
            iid = int(self.return_cb.get().split(" - ")[0])
        except:
            messagebox.showerror("Missing", "Please select a rental to return.")
            return

        rows = query_all("SELECT dueDate FROM issuetran WHERE IssueID=%s", (iid,))
        if not rows:
            messagebox.showerror("Not Found", "Issue record not found.")
            return

        due_date = rows[0]["dueDate"]
        due_dt = datetime.strptime(str(due_date), "%Y-%m-%d")
        ret_dt = datetime.strptime(str(return_date), "%Y-%m-%d")

        late_days = (ret_dt - due_dt).days
        fee = 0
        if late_days > 0:
            fee = late_days * 2
            messagebox.showwarning("Late Return", f"Movie is {late_days} day(s) late.\nLate fee: ${fee:.2f}")

        execute("UPDATE issuetran SET ReturnDate=%s WHERE IssueID=%s", (return_date, iid))
        win.destroy()
        self.view_all()
        messagebox.showinfo("Return Complete", f"Movie returned.\nLate Fee: ${fee:.2f}")

    # --------------- Reports ---------------
    def report_menu(self):
        menu = tk.Menu(self, tearoff=False)
        menu.add_command(label="Currently rented (Excel)", command=self.currently_rented)
        menu.add_command(label="Overdue rentals (Excel)", command=self.overdue_rentals)
        menu.add_command(label="Rentals by Genre (Chart+Excel)", command=self.genre_chart)
        try:
            menu.tk_popup(self.winfo_rootx() + 200, self.winfo_rooty() + 90)
        finally:
            menu.grab_release()

    def currently_rented(self):
        rows = query_all("""
            SELECT i.IssueID, CONCAT(c.FirstName,' ',c.LastName) AS CustomerName, m.Title AS MovieTitle,
                   i.IssueDate, i.dueDate
            FROM issuetran i
            JOIN customer c ON c.CustomerID = i.CustomerID
            JOIN movies m ON m.MovieID = i.MovieID
            WHERE i.ReturnDate IS NULL
            ORDER BY i.dueDate
        """)
        file = export_to_excel(timestamped("currently_rented_from_rentals"),
                               ["IssueID", "CustomerName", "MovieTitle", "IssueDate", "dueDate"], rows)
        messagebox.showinfo("Excel", f"Saved: {file}")

    def overdue_rentals(self):
        sql = """
            SELECT CONCAT(c.FirstName,' ',c.LastName) AS CustomerName, m.Title AS MovieTitle,
                   i.IssueDate, i.dueDate
            FROM issuetran i
            JOIN customer c ON c.CustomerID = i.CustomerID
            JOIN movies m ON m.MovieID = i.MovieID
            WHERE i.ReturnDate IS NULL AND i.dueDate < CURDATE()
            ORDER BY i.dueDate
        """
        rows = query_all(sql)
        file = export_to_excel(timestamped("overdue_from_rentals"),
                               ["CustomerName", "MovieTitle", "IssueDate", "dueDate"], rows)
        messagebox.showinfo("Excel", f"Saved: {file}")

    def genre_chart(self):
        rows = query_all("""
            SELECT m.Genre, COUNT(*) AS TotalRentals
            FROM issuetran i
            JOIN movies m ON m.MovieID = i.MovieID
            GROUP BY m.Genre
            ORDER BY TotalRentals DESC
        """)
        file = export_to_excel(timestamped("rentals_by_genre_rentals"), ["Genre", "TotalRentals"], rows)
        genres = [r["Genre"] for r in rows]
        totals = [r["TotalRentals"] for r in rows]
        plt.figure()
        plt.bar(genres, totals)
        plt.title("Rentals by Genre")
        plt.xlabel("Genre")
        plt.ylabel("Total rentals")
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.show()
        messagebox.showinfo("Excel", f"Saved: {file}")

    # ---------- Helpers ----------
    def _fill(self, rows):
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert("", "end", values=(
                r["IssueID"], r["CustomerID"], r["CustomerName"], r["MovieID"], r["MovieTitle"],
                r["IssueDate"], r["ReturnDate"], r["dueDate"]
            ))
