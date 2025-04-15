# submittech_solutions1

---

# **MediLog - Personal Medication Tracker**  
*A secure web application for users to track medications, dosages, and schedules.*  

---

## **✨ Features**  

### **Core Functionality**  
🔐 **User Authentication**  
- Secure registration/login system  
- Password hashing for security  

💊 **Medication Management (CRUD)**  
- **Create/Edit/Delete** medications  
- Track: *Name, Dosage, Frequency, Start Date, Notes, Status*  

### **Advanced Features**  
🔍 **Smart Filtering & Sorting**  
- Filter by status (*Active/Discontinued*)  
- Sort by *Medication Name* or *Start Date*  

📊 **Dashboard Summary**  
- Real-time counts: *"Total Active Medications: X"*  
- Clean, responsive interface  

---

## **🛠️ Installation**  

### **Requirements**  
- Python 3.6+  
- XAMPP (for MySQL)  
- Modern web browser  

### **Setup**  
1. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
2. Start **MySQL** in XAMPP.  
3. Run the app:  
   ```bash
   python app.py
   ```

### **Configuration**  
Edit `config.py` if needed:  
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''  # Default XAMPP
MYSQL_DB = 'medilog_db'
```

### **First-Time Setup**  
1. Access `http://localhost:5000`  
2. Register a new account  
3. Start logging medications!  

---

## **📂 Project Structure**  
```
medilog/
├── app.py                # Main application
├── medilog.sql           # Database schema
├── config.py             # Configuration
├── requirements.txt      # Dependencies
├── static/               # Static files
│   ├── css/              # Stylesheets
│   └── images/           # App assets
└── templates/            # HTML templates
    ├── base.html         # Main template
    ├── login.html        # Login page
    ├── register.html     # Registration
    ├── medications.html  # Dashboard
    └── add_edit_medication.html  # Medication form
```

---

## **⚠️ Troubleshooting**  
| Issue | Solution |
|-------|----------|
| **MySQL Connection Failed** | Ensure XAMPP MySQL is running |  
| **ModuleNotFoundError** | Run `pip install flask flask-mysqldb` |  
| **Database Not Found** | Create `medilog_db` in phpMyAdmin |  
| **Template Errors** | Verify files exist in `/templates` |  

---

## **📜 License**  
**MIT License**  
*Free to use, modify, and distribute.*  

--- 

### **🎯 Submission Notes**  
- **Test Credentials**:  
  - Username: `hyndhavi_11`  
  - Password: `123456789`  
