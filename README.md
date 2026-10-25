# Clinic Management System

A terminal-based Clinic Management System developed using Python, Object-Oriented Programming (OOP), and MySQL. The application provides patient management, appointment scheduling, receptionist and doctor workflows, and consultation-related operations through an interactive command-line interface.

## Features

### Patient Management

- Register new patients.
- View patient records.
- Search patients using supported search criteria.
- Update patient information.
- Disable patient records when necessary.
- Validate patient details such as names, dates of birth, phone numbers, email addresses, gender, and blood groups.

### Receptionist Module

- Access the receptionist dashboard after login.
- Manage patient registrations and records.
- Schedule appointments.
- Handle appointment-related workflows.

### Appointment Scheduling

- Book appointments for new or existing patients.
- Select a department and doctor.
- Choose an appointment date.
- Check doctor availability.
- Generate appointment tokens and time slots.
- Support walk-in consultation workflows.

### Doctor Module

- View today's appointments.
- View upcoming appointments.
- Start consultations.
- Record consultation details.
- Add medicines and laboratory tests to prescriptions.
- View consultation history.
- Print prescriptions using the application's supported functionality.

### Database Management

- Store patient, staff, and appointment information in MySQL.
- Use SQL queries to retrieve and manage records.
- Organize application logic into separate Python modules.

## Technologies Used

- Python
- Object-Oriented Programming (OOP)
- MySQL
- MySQL Connector/Python
- SQL

## Project Structure

```text
python-clinic-management-system/
├── main.py
├── database.py
├── login.py
├── patient.py
├── receptionist.py
├── doctor.py
├── schedule.py
├── validations.py
├── project 1.sql
├── requirements.txt
├── README.md
├── .gitignore
└── screenshots/
    ├── main-menu.png
    ├── receptionist-dashboard.png
    └── doctor-dashboard.png
```

## Prerequisites

- Python 3.10 or later
- MySQL Server
- A MySQL account with the required database permissions

## Installation and Setup

### 1. Download the Project

Clone the repository or download the project files from GitHub.

### 2. Install Dependencies

Open the project directory in VS Code and install the required packages:

```bash
python -m pip install -r requirements.txt
```

### 3. Configure MySQL

Ensure that MySQL Server is running.

Create the database and tables using the supplied SQL setup script after reviewing its contents and removing any real credentials or personal information.

The database name used by the application is `clinic_management`.

### 4. Configure Database Credentials

Create a local `.env` file in the project directory:

```text
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=clinic_management
```

Replace the example password with your local MySQL password.

Do not upload the `.env` file to GitHub.

### 5. Run the Application

Run the main Python file:

```bash
python main.py
```

The application displays the login interface. After successful authentication, users are directed to the appropriate receptionist or doctor dashboard based on their role.

## Screenshots

Screenshots demonstrating the application's interface and functionality will be added below.

### Main Menu and Login

![Clinic Management System Login](screenshots/main-menu.png)

### Receptionist Dashboard

![Receptionist Dashboard](screenshots/receptionist-dashboard.png)

### Doctor Dashboard

![Doctor Dashboard](screenshots/doctor-dashboard.png)

## Future Enhancements

- Implement secure password hashing.
- Improve database connection management and error handling.
- Add more comprehensive reporting features.
- Improve role-based access control.
- Expand automated testing.
- Develop a graphical user interface.

## Author

Developed as a Python programming project.
