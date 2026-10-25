from datetime import datetime, date
from calendar import monthrange
from datetime import datetime, date


class Validation:

    # ---------------- FIRST NAME ----------------

    def validate_first_name(self):
        while True:
            first_name = input("Enter First Name : ").strip().title()
            if first_name.upper() == "BACK":
                return "BACK"
            if len(first_name) == 0:
                print("First Name cannot be empty.")
            elif not first_name.isalpha():
                print("First Name should contain only letters.")
            elif len(first_name) < 3 or len(first_name) > 20:
                print("First Name should contain 3 to 20 characters.")
            else:
                return first_name


    # ---------------- LAST NAME ----------------

    def validate_last_name(self):
        while True:
            last_name = input("Enter Last Name (Optional) : ").strip().title()
            if last_name.upper() == "BACK":
                return "BACK"
            if last_name == "":
                return ""
            elif not last_name.isalpha():
                print("Last Name should contain only letters.")
            elif len(last_name) < 1 or len(last_name) > 20:
                print("Last Name should contain 1 to 20 characters.")
            else:
                return last_name


    # ---------------- AGE ----------------

    def validate_dob(self):

        while True:
            dob = input("Enter Date of Birth (YYYY-MM-DD) : ").strip()
            if dob.upper() == "BACK":
                return "BACK"
            try:
                dob = datetime.strptime(dob, "%Y-%m-%d").date()
                today = date.today()

                if dob > today:
                    print("Future Date is not allowed.")
                    continue

                years = today.year - dob.year
                months = today.month - dob.month
                days = today.day - dob.day

                if days < 0:
                    months -= 1
                    previous_month = today.month - 1 if today.month > 1 else 12
                    previous_year = today.year if today.month > 1 else today.year - 1
                    days += monthrange(previous_year, previous_month)[1]

                if months < 0:
                    years -= 1
                    months += 12

                if years > 150:
                    print("Invalid Age.")
                    continue

                if years == 0 and months == 0:
                    age = f"{days} Day(s)"

                elif years == 0:
                    age = f"{months} Month(s)"

                else:
                    age = f"{years} Year(s)"

                return age

            except ValueError:
                print("Invalid Date Format.")


    # ---------------- ADDRESS ----------------

    def validate_address(self):
        while True:
            address = input("Enter Address : ").strip().upper()
            if address.upper() == "BACK":
                return "BACK"
            if address == "":
                print("Address cannot be empty.")
            elif len(address) < 5:
                print("Address is too short.")
            else:
                return address


    # ---------------- PHONE ----------------

    def validate_phone(self):
        while True:
            phone = input("Enter Phone Number : ")
            if phone.upper() == "BACK":
                return "BACK"
            if len(phone) != 10:
                print("Phone Number should contain exactly 10 digits.")
            elif not phone.isdigit():
                print("Phone Number should contain only digits.")
            elif phone[0] not in "9876":
                print("Phone Number should start with 9,8,7 or 6.")
            else:
                return phone


    # ---------------- EMAIL ----------------

    def validate_email(self):
        while True:
            email = input("Enter Email (Optional) : ").strip().lower()
            if email.upper() == "BACK":
                return "BACK"
            if email == "":
                return ""
            elif "@" not in email:
                print("Email should contain @.")
            elif not (email.endswith(".com") or email.endswith(".in")):
                print("Email should end with .com or .in")
            else:
                return email


    # ---------------- GENDER ----------------

    def validate_gender(self):
        while True:
            print("\nGender")
            print("1. Male")
            print("2. Female")
            print("3. Other")
            choice = input("Enter Choice : ").strip()
            if choice.upper() == "BACK":
                return "BACK"
            if choice == "1":
                return "M"
            elif choice == "2":
                return "F"
            elif choice == "3":
                return "Other"
            else:
                print("Invalid Choice.")


    # ---------------- BLOOD GROUP ----------------

    def validate_blood_group(self):
        blood_groups = {
            "1": "A+",
            "2": "A-",
            "3": "B+",
            "4": "B-",
            "5": "AB+",
            "6": "AB-",
            "7": "O+",
            "8": "O-"
        }

        while True:
            print("\nBlood Group")
            print("1. A+")
            print("2. A-")
            print("3. B+")
            print("4. B-")
            print("5. AB+")
            print("6. AB-")
            print("7. O+")
            print("8. O-")
            choice = input("Enter Choice : ").strip()
            if choice.upper() == "BACK":
                return "BACK"
            if choice in blood_groups:
                return blood_groups[choice]
            else:
                print("Invalid Blood Group.")