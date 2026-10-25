from database import database
from validations import Validation

class Patient:

    def __init__(self):
        self.validation = Validation() #can create object wherever we want to call another class's function.self.?

    def register_patient(self):
        print("\n========== REGISTER PATIENT ==========\n")
        print("Type 'BACK' at any time to cancel registration.\n")

        first_name = self.validation.validate_first_name()
        if first_name == "BACK":
            print("\nRegistration Cancelled.")
            return None

        last_name = self.validation.validate_last_name()
        if last_name == "BACK":
            print("\nRegistration Cancelled.")
            return None

        age = self.validation.validate_dob()
        if age == "BACK":
            print("\nRegistration Cancelled.")
            return None

        address = self.validation.validate_address()
        if address == "BACK":
            print("\nRegistration Cancelled.")
            return None

        phone = self.validation.validate_phone()
        if phone == "BACK":
            print("\nRegistration Cancelled.")
            return None

        email = self.validation.validate_email()
        if email == "BACK":
            print("\nRegistration Cancelled.")
            return None

        gender = self.validation.validate_gender()
        if gender == "BACK":
            print("\nRegistration Cancelled.")
            return None

        blood_group = self.validation.validate_blood_group()
        if blood_group == "BACK":
            print("\nRegistration Cancelled.")
            return None
        
        #phone duplicate checks at begining itself
        query = """
        SELECT
            patient_id,
            first_name,
            last_name
        FROM patient
        WHERE phone=%s
        AND is_active=TRUE
        """
        database.dbcursor.execute(query, (phone,))
        existing_patient = database.dbcursor.fetchall()

        if existing_patient:
            print("\n======================================")
            print(" Phone Number Already Registered")
            print("======================================")
            existing_patient = existing_patient[0]
            print("Patient ID :", existing_patient[0])
            print("Name       :", existing_patient[1], existing_patient[2])

            while True:
                print("\n1. Continue Registration")
                print("2. Cancel Registration")
                option = input("Enter Choice : ").strip()

                if option == "1":
                    break

                elif option == "2":
                    print("\nRegistration Cancelled.")
                    return None
                else:
                    print("Invalid Choice.")
                    
               

        # ---------- Duplicate Patient Check ----------
        duplicate_query = """
        SELECT patient_id
        FROM patient
        WHERE first_name=%s
        AND last_name=%s
        AND age=%s
        AND phone=%s
        AND is_active=TRUE
        """

        duplicate_values = (
            first_name,
            last_name,
            age,
            phone
        )

        database.dbcursor.execute(duplicate_query, duplicate_values)
        patient = database.dbcursor.fetchone()

        if patient:
            print("\nPatient already exists.")
            print("Patient ID :", patient[0])
            return patient[0]

        # ---------- Insert Patient ----------
        insert_query = """
        INSERT INTO patient
        (
            first_name,
            last_name,
            age,
            address,
            phone,
            email,
            gender,
            blood_group
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            first_name,
            last_name,
            age,
            address,
            phone,
            email,
            gender,
            blood_group
        )

        try:

            database.dbcursor.execute(insert_query, values)
            database.dbobj.commit()

            patient_id = database.dbcursor.lastrowid

            print("\n===================================")
            print("Patient Registered Successfully")
            print("Patient ID :", patient_id)
            print("===================================")

            return patient_id

        except Exception as e:

            print("\nUnable to Register Patient")
            print(e)
            return None




    def view_patients(self):

        query = """
        SELECT patient_id, first_name, last_name, age, address,
           phone, email, gender, blood_group
        FROM patient
        WHERE is_active = TRUE
        """
        database.dbcursor.execute(query)
        patients = database.dbcursor.fetchall()
        if not patients:
            print("\nNo Patients Found.")
            return

        print("-" * 133)
        print(f"{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Age':<14} {'Address':<15} {'Phone':<12} {'Email':<35} {'Gender':<8} {'Blood':<8}")
        print("-" * 133)
        for patient in patients:
            email = patient[6] if patient[6] else "-"
            print(f"{patient[0]:<5} "f"{patient[1]:<15} "f"{patient[2]:<15} "f"{str(patient[3]):<14} "f"{patient[4]:<15} "f"{patient[5]:<12} "f"{email:<35} "f"{patient[7]:<8} "f"{patient[8]:<8}")
        print("-" * 133)
        

   
    def search_patient(self):

        while True:
            print("\n========== SEARCH PATIENT ==========")
            print("Type 'BACK' at any time to cancel.\n")
            print("1. Patient ID")
            print("2. Name")
            print("3. Phone")
            print("4. Back")
            choice = input("Enter Choice : ").strip()
            if choice.upper() == "BACK" or choice == "4":
                return

            elif choice == "1":
                patient_id = input("Enter Patient ID : ").strip()
                if patient_id.upper() == "BACK":
                    continue
                query = """
                SELECT *
                FROM patient
                WHERE patient_id=%s
                AND is_active=TRUE
                """
                database.dbcursor.execute(query, (patient_id,))

            elif choice == "2":
                name = input("Enter First Name : ").strip().title()
                if name.upper() == "BACK":
                    continue
                query = """
                SELECT *
                FROM patient
                WHERE first_name=%s
                AND is_active=TRUE
                """
                database.dbcursor.execute(query, (name,))

            elif choice == "3":
                phone = input("Enter Phone Number : ").strip()
                if phone.upper() == "BACK":
                    continue
                query = """
                SELECT *
                FROM patient
                WHERE phone=%s
                AND is_active=TRUE
                """
                database.dbcursor.execute(query, (phone,))
            else:
                print("Invalid Choice.")
                continue
            patients = database.dbcursor.fetchall()

            if not patients:
                print("\nPatient Not Found.")
                input("\nPress Enter to Search Again...")
                continue

            print("\n************ PATIENT FOUND ************")
            for patient in patients:
                print("\n**************************************")
                print("Patient ID   :", patient[0])
                print("Name         :", patient[1], patient[2] if patient[2] else "")
                print("Age          :", patient[3])
                print("Address      :", patient[4])
                print("Phone        :", patient[5])
                print("Email        :", patient[6] if patient[6] else "-")
                print("Gender       :", patient[7])
                print("Blood Group  :", patient[8])
                print("**************************************")
            while True:
                print("\n1. Search Again")
                print("2. Back")

                option = input("Enter Choice : ").strip()

                if option == "1":
                    break          # Goes back to the main search menu

                elif option == "2":
                    return         # Returns to the previous menu

                else:
                    print("Invalid Choice.")






    def update_patient(self):
        print("\n========== UPDATE PATIENT ==========")
        print("Type 'BACK' at any time to cancel updating.\n")

        while True:
            patient_id = input("Enter Patient ID : ").strip()
            if patient_id.upper() == "BACK":
                return

            query = """
            SELECT *
            FROM patient
            WHERE patient_id=%s
            AND is_active=TRUE
            """
            database.dbcursor.execute(query, (patient_id,))
            patient = database.dbcursor.fetchone()
            if patient:
                break
            print("Patient Not Found. Please Enter a Valid Patient ID.")
        while True:
            print("\n========== UPDATE PATIENT ==========")
            print("choose what to update")
            print("1. First Name")
            print("2. Last Name")
            print("3. Age")
            print("4. Address")
            print("5. Phone")
            print("6. Email")
            print("7. Blood Group")
            print("8. Back")
            choice = input("Enter Choice : ").strip()

            if choice == "1":
                first_name = self.validation.validate_first_name()
                duplicate = self.check_duplicate_patient(
                patient_id,
                first_name,
                patient[2],      # existing last name
                patient[3],      # existing age
                patient[5])       # existing phone

                if duplicate:
                    print("\nAnother patient with these details already exists.")
                    print("Patient ID :", duplicate[0])
                    continue
                if first_name == "BACK":
                    continue
                query = """
                UPDATE patient
                SET first_name=%s
                WHERE patient_id=%s
                """
                database.dbcursor.execute(query, (first_name, patient_id))
                database.dbobj.commit()

                query = """SELECT *FROM patient WHERE patient_id=%s"""
                database.dbcursor.execute(query, (patient_id,))
                patient = database.dbcursor.fetchone()
                print("\nFirst Name Updated Successfully.")


            elif choice == "2":
                last_name = self.validation.validate_last_name()
                duplicate = self.check_duplicate_patient(
                patient_id,
                patient[1],
                last_name,
                patient[3],
                patient[5])
                if duplicate:
                    print("\nAnother patient with these details already exists.")
                    print("Patient ID :", duplicate[0])
                    continue
                if last_name == "BACK":
                    continue
                query = """
                UPDATE patient
                SET last_name=%s
                WHERE patient_id=%s
                """
                database.dbcursor.execute(query, (last_name, patient_id))
                database.dbobj.commit()
                query = """SELECT * FROM patient WHERE patient_id=%s"""
                database.dbcursor.execute(query, (patient_id,))
                patient = database.dbcursor.fetchone()
                print("\nLast Name Updated Successfully.")


            elif choice == "3":
                age = self.validation.validate_dob()
                duplicate = self.check_duplicate_patient(
                patient_id,
                patient[1],
                patient[2],
                age,
                patient[5])

                if duplicate:
                    print("\nAnother patient with these details already exists.")
                    print("Patient ID :", duplicate[0])
                    continue
                if age == "BACK":
                    continue
                query = """
                UPDATE patient
                SET age=%s
                WHERE patient_id=%s
                """
                database.dbcursor.execute(query, (age, patient_id))
                database.dbobj.commit()
                query = """SELECT * FROM patient WHERE patient_id=%s"""
                database.dbcursor.execute(query, (patient_id,))
                patient = database.dbcursor.fetchone()
                print("\nAge Updated Successfully.")


            elif choice == "4":
                address = self.validation.validate_address()
                if address == "BACK":
                    continue
                query = """
                UPDATE patient
                SET address=%s
                WHERE patient_id=%s
                """
                database.dbcursor.execute(query, (address, patient_id))
                database.dbobj.commit()
                query = """SELECT * FROM patient WHERE patient_id=%s"""
                database.dbcursor.execute(query, (patient_id,))
                patient = database.dbcursor.fetchone()
                print("\nAddress Updated Successfully.")


            elif choice == "5":
                phone = self.validation.validate_phone()
                duplicate = self.check_duplicate_patient(
                patient_id,
                patient[1],
                patient[2],
                patient[3],
                phone)

                if duplicate:
                    print("\nAnother patient with these details already exists.")
                    print("Patient ID :", duplicate[0])
                    continue
                if phone == "BACK":
                    continue
                query = """
                UPDATE patient
                SET phone=%s
                WHERE patient_id=%s
                """
                database.dbcursor.execute(query, (phone, patient_id))
                database.dbobj.commit()
                query = """SELECT * FROM patient WHERE patient_id=%s"""
                database.dbcursor.execute(query, (patient_id,))
                patient = database.dbcursor.fetchone()
                print("\nPhone Updated Successfully.")


            elif choice == "6":
                email = self.validation.validate_email()
                if email == "BACK":
                    continue
                query = """
                UPDATE patient
                SET email=%s
                WHERE patient_id=%s
                """
                database.dbcursor.execute(query, (email, patient_id))
                database.dbobj.commit()
                query = """SELECT * FROM patient WHERE patient_id=%s"""
                database.dbcursor.execute(query, (patient_id,))
                patient = database.dbcursor.fetchone()
                print("\nEmail Updated Successfully.")


            elif choice == "7":
                blood_group = self.validation.validate_blood_group()
                if blood_group == "BACK":
                    continue
                query = """
                UPDATE patient
                SET blood_group=%s
                WHERE patient_id=%s
                """
                database.dbcursor.execute(query, (blood_group, patient_id))
                database.dbobj.commit()
                query = """SELECT * FROM patient WHERE patient_id=%s"""
                database.dbcursor.execute(query, (patient_id,))
                patient = database.dbcursor.fetchone()
                print("\nBlood Group Updated Successfully.")


            elif choice == "8":
                return

            else:
                print("Invalid Choice.")





    def disable_patient(self):
        print("\n========== DISABLE PATIENT ==========")
        print("Type 'BACK' at any time to cancel.\n")

        while True:
            patient_id = input("Enter Patient ID : ").strip()
            if patient_id.upper() == "BACK":
                return
            query = """
            SELECT
                patient_id,
                first_name,
                last_name
            FROM patient
            WHERE patient_id=%s
            AND is_active=TRUE
            """
            database.dbcursor.execute(query, (patient_id,))
            patient = database.dbcursor.fetchone()
            if not patient:
                print("\nPatient Not Found.")
                continue
            print("\nPatient ID :", patient[0])
            print("Name       :", patient[1], patient[2] if patient[2] else "")

            confirm = input("\nAre you sure you want to disable this patient? (Y/N) : ").strip().upper()
            if confirm == "N":
                return
            elif confirm != "Y":
                print("Invalid Choice.")
                continue

            query = """
            UPDATE patient
            SET is_active=FALSE
            WHERE patient_id=%s
            """
            database.dbcursor.execute(query, (patient_id,))
            database.dbobj.commit()
            print("\nPatient Disabled Successfully.")
            return


    def check_duplicate_patient(self,patient_id,first_name,last_name,age,phone):
        query = """
        SELECT patient_id
        FROM patient
        WHERE first_name=%s
        AND last_name=%s
        AND age=%s
        AND phone=%s
        AND patient_id<>%s
        AND is_active=TRUE
        """

        values = (first_name,last_name,age,phone,patient_id)
        database.dbcursor.execute(query, values)
        return database.dbcursor.fetchone()