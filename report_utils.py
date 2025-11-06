import os
import datetime
import mysql.connector
from tkinter import messagebox
import matplotlib.pyplot as plt
from openpyxl import Workbook

# Database connection
def get_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',  
        database='movierental'
    )

def _save_excel(filename, headers, rows):
    # 🔹 Save reports inside your Downloads folder
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads", "movierental_reports")
    os.makedirs(downloads_path, exist_ok=True)

    # 🔹 Build file path
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(downloads_path, f"{filename}_{timestamp}.xlsx")

    # 🔹 Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Report"
    ws.append(headers)
    for r in rows:
        ws.append(r)
    wb.save(filepath)

    # 🔹 Pop-up confirmation with file path
    messagebox.showinfo(
        "Report Saved",
        f"✅ Report saved successfully!\n\nLocation:\n{filepath}"
    )

# -----------------------------------------------------------------
# 1. Movies currently rented out
def export_currently_rented():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT i.IssueID, i.CustomerID, i.MovieID, i.IssueDate, i.dueDate,
               CONCAT(c.FirstName,' ',c.LastName) AS CustomerName,
               m.Title AS MovieTitle
        FROM issuetran i
        JOIN customer c ON c.CustomerID = i.CustomerID
        JOIN movies m ON m.MovieID = i.MovieID
        WHERE i.ReturnDate IS NULL
    """)
    rows = cur.fetchall()
    headers = [d[0] for d in cur.description]
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    _save_excel(f"currently_rented_{ts}.xlsx", headers, rows)
    cur.close()
    conn.close()

# -----------------------------------------------------------------
# 2. Overdue rentals
def export_overdue():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT i.IssueID, i.CustomerID, i.MovieID, i.IssueDate, i.dueDate,
               CONCAT(c.FirstName,' ',c.LastName) AS CustomerName,
               m.Title AS MovieTitle
        FROM issuetran i
        JOIN customer c ON c.CustomerID = i.CustomerID
        JOIN movies m ON m.MovieID = i.MovieID
        WHERE i.ReturnDate IS NULL AND i.dueDate < CURDATE()
    """)
    rows = cur.fetchall()
    headers = [d[0] for d in cur.description]
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    _save_excel(f"overdue_rentals_{ts}.xlsx", headers, rows)
    cur.close()
    conn.close()

# -----------------------------------------------------------------
# 3. Rentals by Genre (Excel + Chart)
def export_genre_stats():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT m.Genre, COUNT(*) AS TotalRentals
        FROM issuetran i
        JOIN movies m ON m.MovieID = i.MovieID
        GROUP BY m.Genre
    """)
    rows = cur.fetchall()
    headers = [d[0] for d in cur.description]
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    _save_excel(f"rental_stats_genre_{ts}.xlsx", headers, rows)
    cur.close()
    conn.close()

    # Plot chart
    if rows:
        genres = [r[0] for r in rows]
        totals = [r[1] for r in rows]
        plt.bar(genres, totals, color='skyblue')
        plt.title('Rentals by Genre')
        plt.xlabel('Genre')
        plt.ylabel('Total Rentals')
        plt.show()
    else:
        messagebox.showinfo("Chart", "No data available to plot.")
