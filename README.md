🏥 Medical Store Management System (Flask)

A Flask-based web application for managing medical stores, medicines, admins, and medical users.
The system supports admin and medical user roles, authentication, profile management, medicine CRUD operations, and image uploads.

🚀 Features
👤 Authentication & Authorization

Admin and Medical user login

Session-based authentication

Role-based access control

Change password functionality

Logout support

🛠 Admin Module

Admin registration

View and manage admin profile

Upload / change admin profile photo

Register medical stores

View, edit, and delete medical stores

View all registered admins and medical stores

🏪 Medical Store Module

Medical store profile management

Upload / change medical store photo

Register medicines

View, edit, and delete medicines

Search medicines by name

💊 Medicine Management

Add medicine details

Edit medicine information

Delete medicines

View medicines per medical store

Public medicine search functionality

📸 Photo Management

Secure image upload

Profile photo update and delete

Stored in /static/photos

🧰 Tech Stack

Backend: Python, Flask

Database: MySQL (via PyMySQL)

Frontend: HTML, CSS, Jinja2 Templates

File Uploads: Werkzeug

Session Management: Flask Sessions

📁 Project Structure
project/
│
├── app.py
├── MyLib.py
├── static/
│   └── photos/
├── templates/
│   ├── *.html
│
└── README.md

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/medical-store-flask.git
cd medical-store-flask

2️⃣ Create Virtual Environment (Optional)
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install flask pymysql werkzeug

4️⃣ Configure Database

Create a MySQL database

Create required tables:

logindata

admindata

medicaldata

medicinedata

photodata

Update database connection in MyLib.py

▶️ Run the Application
python app.py


Then open your browser and go to:

http://127.0.0.1:5000/

🔐 Default Roles
Role	Access
Admin	Full control (medical stores, admins, medicines)
Medical	Manage own profile & medicines
⚠️ Security Notes

⚠️ Current version uses string-based SQL queries, which are vulnerable to SQL Injection.

Recommended Improvements:

Use parameterized queries

Hash passwords using werkzeug.security

Add CSRF protection

Validate file upload types

Add pagination for large datasets

📌 Future Enhancements

REST API support

Password encryption

Email verification

Medicine stock management

Sales and billing module

Search filters & pagination

🤝 Contributing

Contributions are welcome!
Feel free to fork the repo, open issues, or submit pull requests.

📄 License

This project is for educational purposes.
You may modify and use it freely.
