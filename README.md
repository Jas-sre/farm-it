# Farm-It

Farm-It is a Python Tkinter desktop application that connects farmers and customers through a simple marketplace-style interface.

## Features

- Admin login and dashboard
- Farmer login and profile/product management
- Customer login and product browsing
- Customer wishlist functionality
- New farmer/customer registration
- MySQL database integration

## Tech Stack

- Python
- Tkinter
- MySQL
- Pillow
- mysql-connector-python

## Project Structure

```text
farm_it/
├── main.py          # Main app entry point
├── admin.py         # Admin dashboard
├── farmer.py        # Farmer dashboard
├── customer.py      # Customer dashboard
├── register.py      # Registration window
├── db.py            # Database connection helpers
├── sql.txt          # Database schema and sample data
├── requirements.txt # Python dependencies
└── images           # Background image files
```

## Setup Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up MySQL database

Open MySQL and run the commands from:

```text
sql.txt
```

This creates the `farmit` database, tables, and sample login data.

### 3. Configure database password

The app reads database settings from environment variables.

On Windows Command Prompt, example:

```bash
set FARMIT_DB_HOST=localhost
set FARMIT_DB_USER=root
set FARMIT_DB_PASSWORD=your_mysql_password
set FARMIT_DB_NAME=farmit
```

If your MySQL root user has no password, you can skip `FARMIT_DB_PASSWORD`.

### 4. Run the app

```bash
python main.py
```

## Sample Logins

Admin:

```text
username: admin
password: admin123
```

Sample farmer and customer accounts are available in `sql.txt`.

## About

This project was created as a Class 12 Computer Science final project and is now being improved as a real-world portfolio project.
