# 🎬 Movie Rental Management System (MRMS)

A complete database-driven application built with **Python Tkinter** and **MySQL** to manage movies, customers, and rental transactions in a video rental business.

This project was developed as part of the **ITAP3010 – Developing Data Access Solutions** unit.

---

## 📘 Project Overview

The **Movie Rental Management System** automates rental operations by integrating database management, GUI-based controls, and automated reporting.

**Core Features:**
- 🔑 Secure employee login & authentication  
- 🎞️ Movie CRUD operations (Add, Update, Delete, Search)  
- 👥 Customer management with full data validation  
- 💽 Rental management (Issue, Return, Late Fees)  
- 📊 Automated Excel report generation (using `openpyxl`)  
- 📈 Visualization of rental statistics (using `matplotlib`)

---

## 🏗️ System Architecture

| Layer | Technology | Description |
|-------|-------------|-------------|
| GUI Layer | Tkinter | User interface for employees |
| Logic Layer | Python | Handles CRUD and business logic |
| Data Layer | MySQL | Stores movies, customers, rentals |
| Reporting | OpenPyXL & Matplotlib | Exports reports and charts |

**Architecture Diagram:**  
Architecture Diagram
<img width="940" height="675" alt="image" src="https://github.com/user-attachments/assets/df7e20d7-8407-462d-9d60-be0099b0cb12" />


---

## 🗄️ Database Schema

**Tables:**
- `movies`  
- `customer`  
- `employees`  
- `issuetran`  
- `producer`

**ER Diagram:**  
ER Diagram
<img width="948" height="1121" alt="image" src="https://github.com/user-attachments/assets/630d8214-1d03-4b14-afdd-a73d1bf92781" />


---

## ⚙️ Functional Modules

### 🔐 Login & Authentication
- Secure employee login interface with username and password validation  
- Restricted access levels for administrators and staff  
- Error handling for invalid login attempts  
- Session-based access control to prevent unauthorized usage

<img width="940" height="528" alt="image" src="https://github.com/user-attachments/assets/4c8e0595-68e9-41e2-a96f-2ff82e88dbbc" />


### 🎞️ Movie Management
- Add / Update / Delete movies
- Filter by title, genre, or price
- Generate reports by genre or producer

<img width="940" height="528" alt="image" src="https://github.com/user-attachments/assets/71dfadac-ec4c-4da0-9a78-f96df38c046d" />


### 👥 Customer Management
- Add / Update / Delete customers
- Validate entries before saving
- Prevent deletion if active rentals exist

<img width="940" height="528" alt="image" src="https://github.com/user-attachments/assets/551cd3fa-8382-4e49-bb1a-19cbbaecb065" />


### 💽 Rental Management
- Issue & return movies with automatic due dates
- Calculate late fees ($2/day)
- Export overdue and active rentals to Excel

<img width="940" height="528" alt="image" src="https://github.com/user-attachments/assets/91a7dd8e-fe21-4500-a01c-c19a5961ea8f" />


### 📊 Reporting & Visualization
- Movies currently rented out  
- Overdue rentals  
- Rentals by genre (Excel + Chart)

---

## 🧪 Testing & Validation

| Test ID | Test Description | Status |
|----------|------------------|---------|
| TC01 | Login with valid credentials | ✅ Passed |
| TC02 | Add / Update / Delete movies | ✅ Passed |
| TC03 | Generate Excel report | ✅ Passed |
| TC04 | Late return fee validation | ✅ Passed |

---

## 🧰 Technologies Used

| Component | Technology |
|------------|-------------|
| Programming | Python 3.x |
| Database | MySQL |
| GUI | Tkinter |
| Reporting | OpenPyXL, Matplotlib |
| IDE | VS Code |
| OS | Windows 11 |

---

## 🏁 Conclusion

The **Movie Rental Management System** successfully demonstrates how a database-driven desktop application can simplify day-to-day rental operations.  
It integrates **Python Tkinter** for a user-friendly interface, **MySQL** for robust data management, and **OpenPyXL** for automated reporting.  

Through this project, I strengthened my understanding of GUI-based programming, database integration, and system modularization.  
Key outcomes include secure login authentication, structured CRUD operations, data visualization, and Excel report automation — all combined into a seamless management tool.  

This project reflects practical experience in **application design, database connectivity, and cybersecurity awareness**, providing a strong foundation for future professional and academic development in IT and cybersecurity.



