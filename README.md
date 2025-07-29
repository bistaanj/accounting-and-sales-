# Inventory and Sales Management System

The folder (`final Project`) contains a **Python–based desktop application** for managing product inventories and sales transactions.  
We have used [Tkinter](https://docs.python.org/3/library/tkinter.html) to build a graphical user interface and [MongoDB](https://www.mongodb.com/) as its back‑end database.  
It includes modules for user/enterprise authentication, product inventory tracking, billing, backup/recovery, and settings customization.

---

## 📌 Features

- **Authentication System**  
  - Secure login interface for enterprise users  
  - Enterprise registration and setup  
  - Password recovery and email confirmation

- **Inventory Management**  
  - Add, update, and delete product records  
  - Auto-generate barcodes for new products  
  - Low-stock alerts  
  - Product search with filters

- **Billing System**  
  - Customer checkout and invoice generation  
  - Multi-item order processing  
  - PDF bill creation  
  - Bill history archive

- **Customer & Order Details**  
  - View customer profiles and past orders  
  - Track order history and payments

- **Backup & Recovery**  
  - One-click MongoDB backup to local storage or Google Drive  
  - Restore backups for system recovery

- **Application Settings**  
  - Font style and color themes  
  - Date formats and mailing options

- **Responsive Layout**  
  - UI elements dynamically adjust based on screen resolution

---

## ⚙️ Requirements

Install the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

You’ll also need to install and run a local MongoDB server.  
Optional: Set up Google Drive API credentials if you want to enable cloud backups.

---

## 🚀 Running the Application

Launch the main interface with:

```bash
python main.py
```

The login screen will appear. Use a registered enterprise account or create a new one.

---

## 📂 Project Structure

```
final Project/
├── authentication/         # User login, signup, and enterprise creation
├── config/                 # Config files and dynamic sizing
├── Frames/
│   ├── Inventory/          # Product features: add, update, backup, etc.
│   ├── Billing/            # Billing interface and logic
│   ├── App_Settings/       # Font, color, and date formatting options
│   ├── Bill_History/       # Archived bills viewer
│   ├── Customer_Details/   # Customer database and order logs
│   └── Overview/           # Dashboard for inventory and sales summary
├── res/                    # Icons and other resource files
├── main.py                 # Entry point; launches the login window
├── requirements.txt        # Python dependencies
└── text.py                 # Example script to print inventory collection
```

---

## Contributing

We are **not accepting external contributions**.  
The project is provided as‑is for educational use, and there is no active maintenance or development roadmap.  
This project can be used for personal and educational purpose and nothing beyond that. 
If you discover any issue or would like to suggest an improvement, feel free to open an issue for discussion, but please be aware that pull requests may not be reviewed or merged.

---

## License

This project does not currently include a license file.  
If you intend to use it beyond personal or educational purposes, please contact us.
