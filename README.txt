
📂 CONTENTS:
- app.py
- movie_mgmt.py
- cust_rental_mgmt.py
- db_config.py
- report_utils.py
- movierental.sql
- screenshots/ (all GUI and database screenshots)

⚙️ REQUIREMENTS:
- Python 3.9 or higher
- MySQL Server (“movierental” database imported)
- Packages required:
  - mysql-connector-python
  - openpyxl
  - matplotlib
  - tkinter (built in with Python)

💻 HOW TO RUN:
1. Open VS Code.
2. Make sure MySQL service is running.
3. Import the database:
   CREATE DATABASE movierental;
   USE movierental;
   SOURCE movierental.sql;
4. In db_config.py, update your MySQL password if needed:
   "password": "your_mysql_password"
5. Run the application:
   python app.py
6. Login using:
   - Employee ID: 1
   - Password: abc@123

🧩 FEATURES:
- Secure employee login
- Movie, Customer & Rental management modules
- Issue and return movies with automatic late fee calculation
- Generate Excel reports and charts (saved in Downloads/movierental_reports)
- Data validation and error handling

📝 NOTES:
- All screenshots and explanations are included in the Project Report (ITAP3010 Developing Data Access Solutions).docx.
- Database passwords and sample credentials are for demonstration only.
- Developed and tested in VS Code and MySQL Workbench.

------------------------------------------------------------
End of README
