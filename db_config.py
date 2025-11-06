
import os
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from pathlib import Path

try:
    from openpyxl import Workbook
except ImportError:
    Workbook = None

# ----------------- MySQL configuration -----------------
DB_CONFIG = {
    "user": "root",
    "password": "",      
    "host": "127.0.0.1",
    "database": "movierental",          
    "auth_plugin": "mysql_native_password"
}

# ----------------- Connection -----------------
def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

# ----------------- SQL helpers -----------------
def query_all(sql, params=None):
    conn = get_conn()
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute(sql, params or ())
            return cur.fetchall()
    finally:
        conn.close()

def execute(sql, params=None):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            conn.commit()
            return cur.rowcount
    finally:
        conn.close()

def execute_many(sql, rows):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.executemany(sql, rows)
            conn.commit()
            return cur.rowcount
    finally:
        conn.close()

# ----------------- Excel export helpers -----------------
def ensure_openpyxl():
    if Workbook is None:
        raise RuntimeError("openpyxl not installed. Please run: pip install openpyxl")

def export_to_excel(filename, headers, rows):
    """Export query results to Excel and save them in Downloads/movierental_reports."""
    ensure_openpyxl()

    # Create folder in Downloads if it doesn't exist
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads", "movierental_reports")
    os.makedirs(downloads_path, exist_ok=True)

    # Build file path with full timestamped name
    file_path = os.path.join(downloads_path, f"{filename}.xlsx")

    # Create workbook and add data
    wb = Workbook()
    ws = wb.active
    ws.title = "Report"
    ws.append(headers)

    for r in rows:
        if isinstance(r, dict):
            ws.append([r.get(h, "") for h in headers])
        else:
            ws.append(list(r))

    wb.save(file_path)
    return file_path

def timestamped(name):
    """Generate a unique filename with current date/time."""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{name}_{stamp}"
