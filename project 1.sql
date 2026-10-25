-- creating database --
CREATE DATABASE clinic_management;
USE clinic_management;

-- creating staff table(containing all staff details) --

CREATE TABLE staff
(
    staff_id VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20),
    dob DATE NOT NULL,
    address VARCHAR(100) NOT NULL,
    phone CHAR(10) NOT NULL UNIQUE,
    email VARCHAR(50) UNIQUE,
    gender ENUM('M','F','Other') NOT NULL,
    role ENUM('Receptionist','Doctor','Pharmacist','Lab Technician') NOT NULL,
	department VARCHAR(50),
	consultation_fee DECIMAL(8,2),
	username VARCHAR(30) NOT NULL UNIQUE,
	password VARCHAR(50) NOT NULL,
	is_active BOOLEAN DEFAULT TRUE
);

-- inserting into staff table --
INSERT INTO staff
(staff_id, first_name, last_name, dob, address, phone, email, gender, role, department, consultation_fee, username, password)
VALUES
('RE001','Priya','Nair','1998-05-12','Trivandrum','9876543210','priya@gmail.com','F','Receptionist',NULL,NULL,'recep1','recep123'),
('RE002','Anjali','Menon','1997-09-18','Kollam','9876543211','anjali@gmail.com','F','Receptionist',NULL,NULL,'recep2','recep123'),
('DO001','Rahul','Menon','1984-06-15','Kochi','9876543212','rahul@gmail.com','M','Doctor','General Medicine',500,'doctor1','doctor123'),
('DO002','Akhil','Nair','1982-03-20','Thrissur','9876543213','akhil@gmail.com','M','Doctor','General Medicine',600,'doctor2','doctor123'),
('DO003','Meera','Thomas','1985-11-25','Kottayam','9876543214','meera@gmail.com','F','Doctor','Cardiology',800,'doctor3','doctor123'),
('DO004','Arjun','Varma','1980-07-10','Kozhikode','9876543215','arjun@gmail.com','M','Doctor','Cardiology',900,'doctor4','doctor123'),
('DO005','Sneha','Pillai','1987-02-15','Alappuzha','9876543216','sneha@gmail.com','F','Doctor','Orthopaedics',700,'doctor5','doctor123'),
('DO006','Vishnu','Krishnan','1983-09-30','Kannur','9876543217','vishnu@gmail.com','M','Doctor','Orthopaedics',750,'doctor6','doctor123'),
('DO007','Neha','Joseph','1986-01-18','Ernakulam','9876543220','neha@gmail.com','F','Doctor','Neurology',850,'doctor7','doctor123'),
('DO008','Adithya','Rajan','1981-12-05','Malappuram','9876543221','adithya@gmail.com','M','Doctor','Dermatology',650,'doctor8','doctor123');

select * from staff;

-- creating a patients table structure --(values entered through python with validation.mysql does second layer of validation) --
CREATE TABLE patient(
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
	first_name VARCHAR(20) NOT NULL,
	last_name VARCHAR(20),
	age DATE NOT NULL,
	address VARCHAR(100) NOT NULL,
	phone CHAR(10) NOT NULL,
    CHECK (phone REGEXP '^[6-9][0-9]{9}$'),-- starts with 6,7,8,9 followed by 0-9 with 9 nums
	email VARCHAR(50) NOT NULL,
	gender ENUM('M','F','Other') NOT NULL,
	blood_group ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
	is_active BOOLEAN DEFAULT TRUE
);

drop table patient;

