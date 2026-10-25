from database import database
from patient import Patient
from datetime import datetime
from datetime import date
from datetime import timedelta
from datetime import time
from decimal import Decimal


class Scheduling:

    def schedule_appointment(self):

        while True:

            print("\n========== SCHEDULING ==========")
            print("1. Book Appointment")
            print("2. Consultation (Walk-in)")
            print("3. Back")
            choice = input("Enter Choice : ").strip()

            if choice == "1":
                self.book_appointment()

            elif choice == "2":
                self.consultation()

            elif choice == "3":
                return
            
            else:
                print("Invalid Choice.")





#1)-------------book appointment--------------

    def book_appointment(self):

        patient = Patient()
        while True:

            print("\n========== BOOK APPOINTMENT ==========")
            print("1. New Patient")
            print("2. Existing Patient")
            print("3. Back")
            choice = input("Enter Choice : ").strip()

            if choice == "1":   # Register New Patient
                patient_id = patient.register_patient()
                if patient_id is None:
                    # Registration cancelled
                    continue
                break

            elif choice == "2":                                                             #existing patient
                patient_found = False
                while True:
                    print("\nSearch Existing Patient By")
                    print("1. Patient ID")
                    print("2. Patient Name")
                    print("3. Back")
                    search_choice = input("Enter Choice : ").strip()

                    if search_choice == "1":                                                                    #search by id
                        print("Type 'BACK' at any time to cancel booking appointment")
                        patient_id = input("Enter Patient ID : ").strip()
                        if patient_id.upper() == "BACK":
                            break
                        query = """
                        SELECT patient_id,
                               first_name,
                               last_name
                        FROM patient
                        WHERE patient_id=%s
                        AND is_active=TRUE
                        """
                        database.dbcursor.execute(query, (patient_id,))
                        result = database.dbcursor.fetchone()
                        if result:
                            print("\nPatient Found")
                            print("Patient ID :", result[0])
                            print("Name :", result[1], result[2])
                            patient_found = True
                            break
                        else:
                            print("Patient Not Found.")


                    elif search_choice == "2":                                                               #search by name
                        print("Type 'BACK' at any time to cancel booking appointment")
                        name = input("Enter First Name : ").title().strip()
                        if name.upper() == "BACK":
                            break
                        query = """
                        SELECT patient_id,
                               first_name,
                               last_name
                        FROM patient
                        WHERE first_name=%s
                        AND is_active=TRUE
                        """
                        database.dbcursor.execute(query, (name,))
                        patients = database.dbcursor.fetchall()
                        if not patients:
                            print("Patient Not Found.")
                            continue
                        print("\nPatients Found\n")
                        for i, p in enumerate(patients, start=1):            #if same names..choose from it.
                            print(f"{i}. {p[0]} - {p[1]} {p[2]}")
                        print(f"{len(patients)+1}. Back")
                        select = input("Select Patient : ").strip()
                        if not select.isdigit():
                            print("Invalid Choice.")
                            continue
                        select = int(select)
                        if select == len(patients)+1:
                            continue
                        if select < 1 or select > len(patients):
                            print("Invalid Choice.")
                            continue
                        patient_id = patients[select-1][0]
                        patient_found = True
                        break


                    elif search_choice == "3":                                        #back
                        break
                    else:
                        print("Invalid Choice.")
                if patient_found:
                    break


            elif choice == "3":       #back
                return
            else:
                print("Invalid Choice.")
     





        while True:

            department = self.choose_department()

            if department is None:
                return

            while True:

                doctor = self.choose_doctor(department)

                if doctor is None:
                    break          # Back to Department Menu

                doctor_id = doctor[0]
                doctor_name = doctor[1] + " " + doctor[2]
                consultation_fee = doctor[3]

                while True:

                    appointment_date = self.choose_appointment_date()

                    if appointment_date is None:
                        break      # Back to Doctor Menu

                    appointment_date = self.check_doctor_availability(doctor_id,appointment_date)

                    if appointment_date is None:
                        continue

                    break

                if appointment_date is None:
                    continue       # Go back to Doctor Menu

                break              # Doctor and Date selected successfully

            if doctor is None:
                continue           # Go back to Department Menu

            break                  # Exit Department loop



        token = self.generate_token(doctor_id,appointment_date)    #calling token generation funct


        appointment_time = self.generate_time_slot(token)    #calling time slot function


        appointment_id = self.save_appointment(patient_id,doctor_id,appointment_date,appointment_time,token,"Appointment")      #calling save appointment function
        if appointment_id is None:
            return


                               
        self.generate_bill(appointment_id,patient_id,doctor_id,doctor_name,department,consultation_fee,appointment_date,appointment_time,token)  #calling generate bill funct





    #choose department function
    def choose_department(self):

        departments = {                        #creating a dictionary for all departments
            "1":"General Medicine",
            "2":"Orthopaedics",
            "3":"Cardiology",
            "4":"Neurology",
            "5":"Dermatology"
        }
        while True:
            print("\n========== SELECT DEPARTMENT ==========")
            print("1. General Medicine")
            print("2. Orthopaedics")
            print("3. Cardiology")
            print("4. Neurology")
            print("5. Dermatology")
            print("6. Back")
            choice = input("Enter Choice : ")

            if choice == "6":
                return None
            elif choice in departments:
                return departments[choice]
            else:
                print("Invalid Choice.")





    #choose doctor function
    def choose_doctor(self, department):
        query = """
        SELECT
        staff_id,
        first_name,
        last_name,
        consultation_fee
        FROM staff
        WHERE role='Doctor'
        AND department=%s
        AND is_active=TRUE
        """
        database.dbcursor.execute(query, (department,))
        doctors = database.dbcursor.fetchall()

        if not doctors:
            print("No Doctors Available.")
            return None
        
        while True:
            print(f"\n========== {department.upper()} ==========\n")
            for i, doctor in enumerate(doctors, start=1):
                print(f"{i}. Dr. {doctor[1]} {doctor[2]}")
                print(f"   Consultation Fee : ₹{doctor[3]}")
            print(f"{len(doctors)+1}. Back")
            choice = input("Select Doctor : ").strip()

            if not choice.isdigit():
                print("Invalid Choice.")
                continue
            choice = int(choice)

            if choice == len(doctors)+1:
                return None

            if choice < 1 or choice > len(doctors):
                print("Invalid Choice.")
                continue

            return doctors[choice-1]
        

    
    #choose appointment date function(>2 days)
    def choose_appointment_date(self):

        while True:
            print("Type 'BACK' at any time to cancel.")
            appointment_date = input("Enter Appointment Date (YYYY-MM-DD) : ").strip()
            if appointment_date.upper() == "BACK":
                return None

            try:

                appointment_date = datetime.strptime(appointment_date,"%Y-%m-%d").date()

                minimum_date = date.today() + timedelta(days=2)
                if appointment_date < minimum_date:
                    print("\nAppointment can only be booked")
                    print("at least TWO DAYS in advance.")
                    continue

                return appointment_date

            except ValueError:
                print("Invalid Date Format.")



    #if >28 tokens,choose next date function
    def check_doctor_availability(self, doctor_id, appointment_date):    
        
        MAX_TOKENS = 28

        while True:

            query = """
            SELECT COUNT(*)
            FROM appointment
            WHERE doctor_id=%s
            AND appointment_date=%s
            AND status!='Cancelled'
            """
            values = (doctor_id,appointment_date)
            database.dbcursor.execute(query, values)
            result = database.dbcursor.fetchone()

            booked_slots = result[0]
            if booked_slots < MAX_TOKENS:
                return appointment_date

            print("\n====================================")
            print("No Appointment Slots Available")
            print("for the selected doctor on")
            print(appointment_date)
            print("====================================")
            print("\nPlease choose another date.")

            appointment_date = self.choose_appointment_date()
            if appointment_date is None:
                return None



    #generate token function
    def generate_token(self, doctor_id, appointment_date):

        query = """
        SELECT MAX(token_number)
        FROM appointment
        WHERE doctor_id=%s
        AND appointment_date=%s
        AND status!='Cancelled'
        """
        values = (doctor_id,appointment_date)
        database.dbcursor.execute(query, values)
        result = database.dbcursor.fetchone()

        # First appointment of the day
        if result[0] is None:
            token = 1

        # Next available token
        else:
            token = result[0] + 1
        return token
    



    #time_slot function
    def generate_time_slot(self, token):

            clinic_start = datetime.combine(date.today(),time(9,0))   #from 9 am
            # Time according to token
            appointment_time = clinic_start + timedelta(minutes=(token-1)*15)  #15 minutes gap

            # Skip lunch break
            if appointment_time.time() >= time(13,0):    #1 hr lunch break
                appointment_time += timedelta(hours=1)     
                                                        #no closing time because only 28 tokens for a day. so ends at 5.45 or somnth
            return appointment_time.time()
    


    #save appointment function
    def save_appointment(self,patient_id,doctor_id,appointment_date,appointment_time,token,appointment_type):

        # ---------- Duplicate Appointment Check ----------

        query = """
        SELECT
            appointment_id,
            token_number,
            appointment_time,
            status
        FROM appointment
        WHERE patient_id=%s
        AND doctor_id=%s
        AND appointment_date=%s
        AND status IN ('Booked','Waiting','In Consultation')
        """

        values = (
            patient_id,
            doctor_id,
            appointment_date
        )

        database.dbcursor.execute(query, values)
        duplicates = database.dbcursor.fetchall()
        if duplicates:
            duplicate = duplicates[0]

            print("\n======================================")
            print("     APPOINTMENT ALREADY EXISTS")
            print("======================================")
            print("Appointment ID :", duplicate[0])
            print("Token Number   :", duplicate[1])
            print("Time           :", self.format_time(duplicate[2]))
            print("Status         :", duplicate[3])
            print("\nBooking Cancelled.")

            return None


        query = """
        INSERT INTO appointment(
            patient_id,
            doctor_id,
            appointment_date,
            appointment_time,
            token_number,
            appointment_type,
            status
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            patient_id,
            doctor_id,
            appointment_date,
            appointment_time,
            token,
            appointment_type,
            "Booked"
        )

        try:

            database.dbcursor.execute(query, values)
            database.dbobj.commit()

            appointment_id = database.dbcursor.lastrowid

            return appointment_id

        except Exception as e:

            print("\nUnable to Book Appointment")
            print(e)

            database.dbobj.rollback()

            return None

    #bill generation and printing function

    def generate_bill(
        self,
        appointment_id,
        patient_id,
        doctor_id,
        doctor_name,
        department,
        consultation_fee,
        appointment_date,
        appointment_time,
        token
    ):
        #calculating bill
        
        gst = consultation_fee * Decimal("0.18")
        total_amount = consultation_fee + gst

        #saving bill
        query = """
        INSERT INTO bill
        (
            appointment_id,
            patient_id,
            doctor_id,
            consultation_fee,
            gst,
            total_amount,
            bill_date
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            appointment_id,
            patient_id,
            doctor_id,
            consultation_fee,
            gst,
            total_amount,
            date.today()
        )

        try:
            database.dbcursor.execute(query, values)
            database.dbobj.commit()
            bill_no = database.dbcursor.lastrowid

        except Exception as e:
            database.dbobj.rollback()
            print("\nUnable to Generate Bill")
            print(e)
            return


        #retrieving patients name

        query = """
        SELECT first_name,
               last_name
        FROM patient
        WHERE patient_id=%s
        """
        database.dbcursor.execute(query, (patient_id,))
        patient = database.dbcursor.fetchone()
        patient_name = patient[0]
        if patient[1]:
            patient_name += " " + patient[1]


        #PRINTING BILL

        print("\n==============================================")
        print("           CLINIC MANAGEMENT SYSTEM")
        print("==============================================")

        print("Bill No             :", bill_no)
        print("Appointment ID      :", appointment_id)

        print("----------------------------------------------")

        print("Patient ID          :", patient_id)
        print("Patient Name        :", patient_name)

        print("----------------------------------------------")

        print("Doctor              : Dr.", doctor_name)
        print("Department          :", department)

        print("----------------------------------------------")

        print("Appointment Date    :", appointment_date)
        print("Time Slot           :", appointment_time.strftime("%I:%M %p"))
        print("Token Number        :", token)

        print("----------------------------------------------")

        print("Consultation Fee    : ₹", consultation_fee)
        print("GST (18%)           : ₹", round(gst,2))
        print("Total Amount        : ₹", round(total_amount,2))

        print("----------------------------------------------")

        print("Payment Status      : Pending")

        print("==============================================")

        print("\nAppointment Booked Successfully.")

        print("Patient File Sent To")

        print("Dr.", doctor_name)

        print("==============================================")










    #CONSULTATION FUNCTION

    def consultation(self):

        patient = Patient()

        while True:
            print("\n========== WALK-IN CONSULTATION ==========")
            print("\nSearch Patient By")
            print("1. Patient ID")
            print("2. Patient Name")
            print("3. Back")
            search_choice = input("Enter Choice : ").strip()

            if search_choice == "1":
                print("Type 'BACK' at any time to cancel.")
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
                result = database.dbcursor.fetchone()
                if result:
                    print("\nPatient Found")
                    print("Patient ID :", result[0])
                    print("Name :", result[1], result[2])
                    break

                else:
                    print("\nPatient Not Found.")
                    print("\n1. Register New Patient")
                    print("2. Search Again")
                    print("3. Back")
                    option = input("Enter Choice : ").strip()

                    if option == "1":
                        patient_id = patient.register_patient()
                        if patient_id is None:
                            continue
                        break
                    elif option == "2":
                        continue
                    else:
                        return

            elif search_choice == "2":
                print("Type 'BACK' at any time to cancel.")
                name = input("Enter First Name : ").strip()
                if name.upper() == "BACK":
                    return
                query = """
                SELECT
                patient_id,
                first_name,
                last_name
                FROM patient
                WHERE first_name=%s
                AND is_active=TRUE
                """
                database.dbcursor.execute(query, (name,))
                patients = database.dbcursor.fetchall()
                if not patients:
                    print("\nPatient Not Found.")
                    print("\n1. Register New Patient")
                    print("2. Search Again")
                    print("3. Back")
                    option = input("Enter Choice : ").strip()

                    if option == "1":
                        patient_id = patient.register_patient()
                        if patient_id is None:
                            continue
                        break

                    elif option == "2":
                        continue
                    else:
                        return
                print("\nPatients Found\n")
                for i, p in enumerate(patients, start=1):
                    print(f"{i}. {p[0]} - {p[1]} {p[2]}")
                print(f"{len(patients)+1}. Back")
                select = input("Select Patient : ").strip()

                if not select.isdigit():
                    print("Invalid Choice.")
                    continue
                select = int(select)
                if select == len(patients)+1:
                    continue
                if select < 1 or select > len(patients):
                    print("Invalid Choice.")
                    continue
                patient_id = patients[select-1][0]
                break

            elif search_choice == "3":
                return
            else:
                print("Invalid Choice.")

        


        department = self.choose_department() #calling choose departmnt funct
        if department is None:
            return


        doctor = self.choose_doctor(department) #calling choose doctor function
        if doctor is None:
            return

        doctor_id = doctor[0]
        doctor_name = doctor[1] + " " + doctor[2]
        consultation_fee = doctor[3]


        appointment_date = date.today() #calling choose date function (2 days prior)
        
        appointment_date = self.check_doctor_availability(doctor_id,appointment_date) #calling doctor availabilty for that choosen date.(if gretaer than x no of appointments)
        if appointment_date is None:
            return



        token = self.generate_token(doctor_id,appointment_date)    #calling token generation funct


        appointment_time = self.generate_time_slot(token)    #calling time slot function


        appointment_id = self.save_appointment(patient_id,doctor_id,appointment_date,appointment_time,token,"Walk-in")      #calling save appointment function
        if appointment_id is None:
            return


                               
        self.generate_bill(appointment_id,patient_id,doctor_id,doctor_name,department,consultation_fee,appointment_date,appointment_time,token)  #calling generate bill funct



    def format_time(self, time_value):

        total_seconds = int(time_value.total_seconds())

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        return datetime.strptime(
            f"{hours:02d}:{minutes:02d}",
            "%H:%M"
        ).strftime("%I:%M %p")