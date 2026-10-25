from database import database
from datetime import datetime
from datetime import date


class Doctor:

    def __init__(self, staff_id, first_name, last_name):
        self.staff_id = staff_id
        self.first_name = first_name
        self.last_name = last_name

    #function to covert timedelta to object
    def format_time(self, time_value):
        total_seconds = int(time_value.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return datetime.strptime(
            f"{hours:02d}:{minutes:02d}",
            "%H:%M"
        ).strftime("%I:%M %p")


    def dashboard(self):
        while True:
            print("\n========== DOCTOR DASHBOARD ==========")
            print("1. View Today's Appointments")
            print("2. View Upcoming Appointments")
            print("3. Start Consultation")
            print("4. View Consultation History")
            print("5. Logout")
            choice = input("Enter Choice : ").strip()

            if choice == "1":
                self.view_today_appointments()
            elif choice == "2":
                self.view_upcoming_appointments()
            elif choice == "3":
                self.start_consultation()
            elif choice == "4":
                self.view_consultation_history()
            elif choice == "5":
                print("\nLogging Out...")
                return
            else:
                print("Invalid Choice.")




    #function to view todays appointments
    def view_today_appointments(self):

        query = """
        SELECT
            a.appointment_id,
            a.token_number,
            a.appointment_time,
            p.patient_id,
            p.first_name,
            p.last_name,
            a.appointment_type,
            a.status
        FROM appointment a
        INNER JOIN patient p
        ON a.patient_id = p.patient_id
        WHERE a.doctor_id=%s
        AND a.appointment_date= CURDATE()
        AND a.status IN ('Booked','Waiting','In Consultation')
        ORDER BY a.token_number
        """
        
        database.dbcursor.execute(query,(self.staff_id,))
        appointments = database.dbcursor.fetchall()

        if not appointments:
            print("\nNo Appointments Found For Today.")
            return

        print("\n================ TODAY'S APPOINTMENTS ================\n")
        print("{:<6} {:<8} {:<10} {:<25} {:<12} {:<15}".format(
            "Token",
            "PID",
            "Time",
            "Patient Name",
            "Type",
            "Status"
        ))
        print("-"*85)

        for appointment in appointments:
            patient_name = appointment[4] + " " + appointment[5]
            formatted_time = self.format_time(appointment[2])
            print("{:<6} {:<8} {:<10} {:<25} {:<12} {:<15}".format(
                appointment[1],
                appointment[3],
                formatted_time,
                patient_name,
                appointment[6],
                appointment[7]
            ))



    #function to view all upcoming appointments
    def view_upcoming_appointments(self):

        query = """
        SELECT
            a.appointment_id,
            a.appointment_date,
            a.token_number,
            a.appointment_time,
            p.patient_id,
            p.first_name,
            p.last_name,
            a.appointment_type,
            a.status
        FROM appointment a
        INNER JOIN patient p
        ON a.patient_id = p.patient_id
        WHERE a.doctor_id=%s
        AND a.appointment_date>%s
        AND a.status='Booked'
        ORDER BY a.appointment_date,
                 a.token_number
        """
        values = (self.staff_id,date.today())
        database.dbcursor.execute(query, values)
        appointments = database.dbcursor.fetchall()
        if not appointments:
            print("\nNo Upcoming Appointments Found.")
            return

        print("\n================ UPCOMING APPOINTMENTS ================\n") #not today
        print("{:<12} {:<6} {:<8} {:<10} {:<25} {:<12} {:<12}".format(
            "Date",
            "Token",
            "PID",
            "Time",
            "Patient Name",
            "Type",
            "Status"
        ))
        print("-"*100)
        for appointment in appointments:
            patient_name = appointment[5] + " " + appointment[6]
            formatted_time = self.format_time(appointment[3])
            print("{:<12} {:<6} {:<8} {:<10} {:<25} {:<12} {:<12}".format(
                appointment[1].strftime("%d-%m-%Y"),
                appointment[2],
                appointment[4],
                formatted_time,
                patient_name,
                appointment[7],
                appointment[8]
            ))




    #function to start consulting (today)
    def start_consultation(self):
        while True:

            query = """                              #show todays patient
            SELECT
                a.appointment_id,
                a.token_number,
                a.appointment_time,
                p.patient_id,
                p.first_name,
                p.last_name,
                p.age,
                p.gender,
                p.blood_group,
                p.phone,
                p.address,
                a.appointment_date,
                a.status
            FROM appointment a
            INNER JOIN patient p
            ON a.patient_id=p.patient_id
            WHERE a.doctor_id=%s
            AND a.appointment_date=%s
            AND a.status IN ('Booked','Waiting')
            ORDER BY a.token_number
            """
            values = (self.staff_id,date.today())
            database.dbcursor.execute(query, values)
            patients = database.dbcursor.fetchall()
            if not patients:
                print("\nNo Patients Available For Consultation.")
                return


            print("\n=========== TODAY'S PATIENTS ===========\n")
            print("{:<6} {:<8} {:<10} {:<25} {:<15}".format(
                "Token",
                "PID",
                "Time",
                "Patient Name",
                "Status"
            ))
            print("-"*70)
            for patient in patients:
                formatted_time = self.format_time(patient[2])
                patient_name = patient[4] + " " + patient[5]
                print("{:<6} {:<8} {:<10} {:<25} {:<15}".format(
                    patient[1],
                    patient[3],
                    formatted_time,
                    patient_name,
                    patient[12]
                ))

            while True:
                print("\nType 'BACK' to return.")
                token = input("Enter Token Number : ").strip()         #selects a token num
                if token.upper() == "BACK":
                    return
                if not token.isdigit():
                    print("Invalid Token.")
                    continue
                token = int(token)
                selected_patient = None
                for patient in patients:
                    if patient[1] == token:
                        selected_patient = patient
                        break
                if selected_patient:
                    break
                print("Invalid Token.")                     #shows the read only patient file.

            print("\n==========================================")
            print("             PATIENT FILE")
            print("==========================================")

            print("Appointment ID   :", selected_patient[0])
            print("Patient ID       :", selected_patient[3])
            print("Patient Name     :", selected_patient[4], selected_patient[5])
            print("Age              :", selected_patient[6])
            print("Gender           :", selected_patient[7])
            print("Blood Group      :", selected_patient[8])
            print("Phone            :", selected_patient[9])
            print("Address          :", selected_patient[10])
            print("Consult Date     :", selected_patient[11])
            print("Token Number     :", selected_patient[1])
            print("Time             :", self.format_time(selected_patient[2]))

            print("==========================================")
           

            #calling another function where the consultation details are entered by doctor(like prescription)
            next_patient = self.consultation_details(selected_patient[0],selected_patient[3])
            if next_patient:
                continue
            else:
                return



    #function for entereing details by doctor
    def consultation_details(self, appointment_id, patient_id):

        print("\n======================================")
        print("       CONSULTATION DETAILS")
        print("======================================")
        #status changes from booked to in consultation
        query = """
        UPDATE appointment
        SET status='In Consultation'                                 
        WHERE appointment_id=%s
        """
        database.dbcursor.execute(query, (appointment_id,))
        database.dbobj.commit()

        symptoms = input("\nEnter Symptoms : ").strip()   #symptoms
        while symptoms == "":
            print("Symptoms cannot be empty.")
            symptoms = input("Enter Symptoms : ").strip()


        diagnosis = input("Enter Diagnosis : ").strip()     #diagnosis
        while diagnosis == "":
            print("Diagnosis cannot be empty.")
            diagnosis = input("Enter Diagnosis : ").strip()


        notes = input("Enter Doctor Notes (Optional) : ").strip()     #notes


        consultation_id = self.save_consultation(appointment_id,patient_id,self.staff_id,symptoms,diagnosis,notes)
        if consultation_id is None:
            return


        next_step = self.add_medicines(consultation_id)

        if next_step == "LAB":
            self.add_lab_tests(consultation_id)

        query = """
        UPDATE appointment
        SET status='Completed'
        WHERE appointment_id=%s
        """
        database.dbcursor.execute(query, (appointment_id,))
        database.dbobj.commit()

        self.print_prescription(consultation_id)

        


        print("\n===================================")
        print("Consultation Completed Successfully")
        print("===================================")

        while True:                                              #to return to dashboard or consult another patient
            print("\n1. Consult Next Patient")
            print("2. Return To Dashboard")
            choice = input("Enter Choice : ")
            if choice == "1":
                return True
            elif choice == "2":
                return False
            else:
                print("Invalid Choice.")



    #function to save consultation
        #function to save consultation
    def save_consultation(
        self,
        appointment_id,
        patient_id,
        doctor_id,
        symptoms,
        diagnosis,
        notes
    ):
        query = """
        INSERT INTO consultation
        (
            appointment_id,
            patient_id,
            doctor_id,
            symptoms,
            diagnosis,
            notes,
            consultation_date
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s)
        """
        values = (
            appointment_id,
            patient_id,
            doctor_id,
            symptoms,
            diagnosis,
            notes,
            date.today()
        )
        try:
            database.dbcursor.execute(query, values)
            database.dbobj.commit()
            consultation_id = database.dbcursor.lastrowid
            return consultation_id
        except Exception as e:
            print("\nUnable to Save Consultation")
            print(e)
            database.dbobj.rollback()
            return None




    #function for adding medicines
    def add_medicines(self, consultation_id):
        while True:
            query = """
            SELECT
            medicine_id,
            medicine_name,
            medicine_type,
            strength
            FROM medicine
            WHERE is_active=TRUE
            ORDER BY medicine_name
            """
            database.dbcursor.execute(query)
            medicines = database.dbcursor.fetchall()

            if not medicines:
                print("\nNo Medicines Available.")
                return


            print("\n========== MEDICINE LIST ==========\n")
            for i, medicine in enumerate(medicines,start=1):
                print(f"{i}. {medicine[1]}   {medicine[2]}   {medicine[3]}")
            print(f"{len(medicines)+1}. Back")


            choice = input("Select Medicine : ").strip()
            if not choice.isdigit():
                print("Invalid Choice.")
                continue
            choice = int(choice)
            if choice == len(medicines)+1:
                return
            if choice < 1 or choice > len(medicines):
                print("Invalid Choice.")
                continue

            medicine_id = medicines[choice-1][0]
            medicine_name = medicines[choice-1][1]
            medicine_type = medicines[choice-1][2]
            strength = medicines[choice-1][3]

            #  Duplicate Medicine Check

            query = """
            SELECT prescription_id
            FROM prescription
            WHERE consultation_id=%s
            AND medicine_id=%s
            """
            database.dbcursor.execute(query,(consultation_id,medicine_id))
            duplicate = database.dbcursor.fetchone()
            if duplicate:
                print("\nMedicine Already Prescribed.")
                continue


            print("\n======================================")
            print("       SELECTED MEDICINE")
            print("======================================")
            print("Medicine :", medicine_name)
            print("Type     :", medicine_type)
            print("Strength :", strength)
            print("======================================")


            # Frequency adding

            frequencies = {
                "1":("1-1-1",3),
                "2":("1-0-1",2),
                "3":("1-0-0",1),
                "4":("0-1-0",1),
                "5":("0-0-1",1),
                "6":("SOS",0)
            }


            while True:

                print("\nSelect Frequency")
                print("1. Morning Afternoon Night (1-1-1)")
                print("2. Morning & Night (1-0-1)")
                print("3. Morning Only (1-0-0)")
                print("4. Afternoon Only (0-1-0)")
                print("5. Night Only (0-0-1)")
                print("6. SOS")
                print("7. Back")

                frequency_choice = input("Enter Choice : ").strip()

                if frequency_choice == "7":
                    break

                if frequency_choice not in frequencies:
                    print("Invalid Choice.")
                    continue

                frequency = frequencies[frequency_choice][0]
                tablets_per_day = frequencies[frequency_choice][1]



                # Duration adding

                durations = {
                    "1":3,
                    "2":5,
                    "3":7,
                    "4":10,
                    "5":15
                }
                while True:

                    print("\nSelect Duration")
                    print("1. 3 Days")
                    print("2. 5 Days")
                    print("3. 7 Days")
                    print("4. 10 Days")
                    print("5. 15 Days")
                    print("6. Back")

                    duration_choice = input("Enter Choice : ").strip()

                    if duration_choice == "6":
                        break

                    if duration_choice not in durations:
                        print("Invalid Choice.")
                        continue

                    duration = durations[duration_choice]


                    #  Quantity Calculation 
                    if tablets_per_day == 0:
                        quantity = 0
                    else:
                        quantity = tablets_per_day * duration

            
                    # Medicine Instructions
                    instructions = {
                        "1":"Before Food",
                        "2":"After Food",
                        "3":"With Food",
                        "4":"Empty Stomach",
                        
                    }
                    while True:

                        print("\nMedicine Instructions")
                        print("1. Before Food")
                        print("2. After Food")
                        print("3. With Food")
                        print("4. Empty Stomach")
                        print("5. Back")

                        instruction_choice = input("Enter Choice : ").strip()

                        if instruction_choice == "5":
                            break

                        if instruction_choice not in instructions:
                            print("Invalid Choice.")
                            continue

                        instruction = instructions[instruction_choice]



                        # Route of Administration adding
                        routes = {
                            "1":"Oral",
                            "2":"Injection",
                            "3":"Syrup",
                            "4":"Drops",
                            "5":"Ointment",
                            "6":"Inhalation"
                        }

                        while True:

                            print("\nRoute of Administration")
                            print("1. Oral")
                            print("2. Injection")
                            print("3. Syrup")
                            print("4. Drops")
                            print("5. Ointment")
                            print("6. Inhalation")
                            print("7. Back")

                            route_choice = input("Enter Choice : ").strip()

                            if route_choice == "7":
                                break

                            if route_choice not in routes:
                                print("Invalid Choice.")
                                continue

                            route = routes[route_choice]

                            # Everything selected successfully
                            break

                        # BACK from Route → Instructions
                        if route_choice == "7":
                            continue

                        break

                    # BACK from Instructions → Duration
                    if instruction_choice == "5":
                        continue

                    break

                # BACK from Duration → Frequency
                if duration_choice == "6":
                    continue

                break

            # BACK from Frequency → Medicine List
            if frequency_choice == "7":
                continue



            #Quantity Display
            if quantity == 0:
                print("\nQuantity : As Required (SOS Medicine)")
            else:
                if medicine_type == "Tablet":
                    unit = "Tablets"
                elif medicine_type == "Capsule":
                    unit = "Capsules"
                elif medicine_type == "Syrup":
                    unit = "Bottle"
                elif medicine_type == "Injection":
                    unit = "Vials"
                elif medicine_type == "Powder":
                    unit = "Sachets"
                elif medicine_type == "Drops":
                    unit = "Bottle"
                elif medicine_type == "Ointment":
                    unit = "Tube"
                elif medicine_type == "Inhaler":
                    unit = "Inhaler"
                else:
                    unit = "Units"
                print("\nQuantity to Dispense :", quantity, unit)



            # Save Prescription 

            query = """
            INSERT INTO prescription
            (
                consultation_id,
                medicine_id,
                frequency,
                duration,
                quantity,
                instructions,
                route
            )
            VALUES
            (%s,%s,%s,%s,%s,%s,%s)
            """
            values = (
                consultation_id,
                medicine_id,
                frequency,
                duration,
                quantity,
                instruction,
                route
            )
            database.dbcursor.execute(query, values)
            database.dbobj.commit()

            print("\n======================================")
            print("     Medicine Added Successfully")
            print("======================================")

            while True:
                print("\n1. Add Another Medicine")
                print("2. Continue To Lab Tests")
                print("3. Print Prescription")

                option = input("Enter Choice : ").strip()

                if option == "1":
                    break

                elif option == "2":
                    return "LAB"

                elif option == "3":
                    return "PRINT"

                else:
                    print("Invalid Choice.")


   
    #function for adding lab test
    def add_lab_tests(self, consultation_id):

        while True:
            departments = {
                "1":"Biochemistry",
                "2":"Cardiology",
                "3":"Hematology",
                "4":"Microbiology",
                "5":"Radiology"
            }
            print("\n========== LAB TEST DEPARTMENTS ==========\n")
            print("1. Biochemistry")
            print("2. Cardiology")
            print("3. Hematology")
            print("4. Microbiology")
            print("5. Radiology")
            print("6. Back")
            choice = input("Enter Choice : ").strip()

            if choice == "6":
                return
            if choice not in departments:
                print("Invalid Choice.")
                continue

            department = departments[choice]

            # Show Tests Under Selected Department

            query = """
            SELECT
                test_id,
                test_name,
                test_fee
            FROM lab_test
            WHERE department=%s
            AND is_active=TRUE
            ORDER BY test_name
            """
            database.dbcursor.execute(query,(department,))
            tests = database.dbcursor.fetchall()
            if not tests:
                print("\nNo Lab Tests Available.")
                continue

            print(f"\n========== {department.upper()} TESTS ==========\n")
            for i, test in enumerate(tests, start=1):
                print(f"{i}. {test[1]} (Rs.{test[2]})")
            print(f"{len(tests)+1}. Back")

            test_choice = input("Select Test : ").strip()
            if not test_choice.isdigit():
                print("Invalid Choice.")
                continue
            test_choice = int(test_choice)

            if test_choice == len(tests)+1:
                continue

            if test_choice < 1 or test_choice > len(tests):
                print("Invalid Choice.")
                continue

            test_id = tests[test_choice-1][0]
            test_name = tests[test_choice-1][1]
            test_fee = tests[test_choice-1][2]

            # Duplicate Test Check 
            query = """
            SELECT lab_request_id
            FROM lab_request
            WHERE consultation_id=%s
            AND test_id=%s
            """
            database.dbcursor.execute(query,(consultation_id,test_id))
            duplicate = database.dbcursor.fetchone()

            if duplicate:
                print("\nLab Test Already Added.")
                continue

            print("\n======================================")
            print("       SELECTED LAB TEST")
            print("======================================")
            print("Department :", department)
            print("Test       :", test_name)
            print("Fee        : Rs.", test_fee)
            print("======================================")



           # Save Lab Test
            query = """
            INSERT INTO lab_request
            (consultation_id,test_id,status)
            VALUES
            (%s,%s,%s)
            """
            values = (consultation_id,test_id,"Pending")
            database.dbcursor.execute(query, values)
            database.dbobj.commit()

            print("\n======================================")
            print("      Lab Test Added Successfully")
            print("======================================")


            while True:
                print("\nWhat would you like to do next?")
                print("1. Add Another Lab Test")
                print("2. Continue To Print Prescription")
                option = input("Enter Choice : ").strip()
                if option == "1":
                    break
                elif option == "2":
                    return
                else:
                    print("Invalid Choice.")



    #function to print prescription
    def print_prescription(self, consultation_id):
        # including Patient & Consultation Details 
        query = """
        SELECT
            p.patient_id,
            p.first_name,
            p.last_name,
            p.age,
            p.gender,
            p.blood_group,
            p.phone,

            s.first_name,
            s.last_name,

            c.symptoms,
            c.diagnosis,
            c.notes,
            c.consultation_date,

            a.token_number,
            a.appointment_time

        FROM consultation c

        INNER JOIN patient p
        ON c.patient_id=p.patient_id
        INNER JOIN appointment a
        ON c.appointment_id=a.appointment_id
        INNER JOIN staff s
        ON c.doctor_id=s.staff_id

        WHERE c.consultation_id=%s
        """
        database.dbcursor.execute(query,(consultation_id,))
        details=database.dbcursor.fetchone()
        if not details:
            print("\nUnable to Print Prescription.")
            return

        # including Medicines
        query="""
        SELECT
            m.medicine_name,
            m.medicine_type,
            m.strength,

            p.frequency,
            p.duration,
            p.quantity,
            p.instructions,
            p.route

        FROM prescription p
        INNER JOIN medicine m
        ON p.medicine_id=m.medicine_id
        WHERE consultation_id=%s
        ORDER BY prescription_id
        """
        database.dbcursor.execute(query,(consultation_id,))
        medicines=database.dbcursor.fetchall()
        
        # including Lab Tests

        query="""
        SELECT
            l.test_name,
            l.department
        FROM lab_request r
        INNER JOIN lab_test l
        ON r.test_id=l.test_id
        WHERE consultation_id=%s
        ORDER BY l.department,l.test_name
        """

        database.dbcursor.execute(query,(consultation_id,))
        tests=database.dbcursor.fetchall()

        print("\n")
        print("="*70)
        print("                 CLINIC PRESCRIPTION")
        print("="*70)
        print("Patient ID      :",details[0])
        print("Patient Name    :",details[1],details[2])
        print("Age             :",details[3])
        print("Gender          :",details[4])
        print("Blood Group     :",details[5])
        print("Phone           :",details[6])

        print()

        print("Doctor          : Dr.",details[7],details[8])
        print("Consult Date    :",details[12])
        print("Token Number    :",details[13])
        print("Appointment Time:",self.format_time(details[14]))

        print("-"*70)

        print("\nSYMPTOMS")
        print(details[9])

        print("\nDIAGNOSIS")
        print(details[10])

        print("\nDOCTOR NOTES")
        print(details[11] if details[11] else "Nil")

        print("\n")
        print("="*70)
        print("MEDICINES")
        print("="*70)



        if medicines:
            print("{:<20}{:<12}{:<10}{:<10}{:<10}".format(
                "Medicine",
                "Strength",
                "Freq",
                "Days",
                "Qty"
            ))

            print("-"*70)

            for medicine in medicines:
                print("{:<20}{:<12}{:<10}{:<10}{:<10}".format(
                    medicine[0],
                    medicine[2],
                    medicine[3],
                    medicine[4],
                    medicine[5]
                ))
                print("   Route        :",medicine[7])
                print("   Instructions :",medicine[6])
                print()
        else:
            print("No Medicines Prescribed.")

        print("\n")
        print("="*70)
        print("LAB TESTS")
        print("="*70)

        if tests:
            for i,test in enumerate(tests,start=1):
                print(f"{i}. {test[0]} ({test[1]})")
        else:
            print("No Lab Tests Prescribed.")

        print("\n")
        print("="*70)
        print("        GET WELL SOON")
        print("="*70)
        input("\nPress Enter to Continue...")



    #function to view consultation history
    def view_consultation_history(self):

        while True:
            print("\n========== CONSULTATION HISTORY ==========")
            print("1. Search By Patient ID")
            print("2. Search By Patient Name")
            print("3. Back")
            choice = input("Enter Choice : ").strip()

            if choice == "1":
                print("Type 'BACK' at any time to cancel.")
                patient_id = input("Enter Patient ID : ").strip()
                if patient_id.upper() == "BACK":
                    return

                query = """
                SELECT
                    c.consultation_id,
                    c.consultation_date,
                    p.patient_id,
                    p.first_name,
                    p.last_name,
                    c.diagnosis
                FROM consultation c
                INNER JOIN patient p
                ON c.patient_id=p.patient_id
                WHERE c.patient_id=%s
                AND c.doctor_id=%s
                ORDER BY c.consultation_date DESC
                """
                database.dbcursor.execute(query,(patient_id,self.staff_id))
                consultations = database.dbcursor.fetchall()

            elif choice == "2":
                print("Type 'BACK' at any time to cancel.")
                name = input("Enter First Name : ").strip()
                if name.upper() == "BACK":
                    return

                query = """
                SELECT
                    c.consultation_id,
                    c.consultation_date,
                    p.patient_id,
                    p.first_name,
                    p.last_name,
                    c.diagnosis
                FROM consultation c
                INNER JOIN patient p
                ON c.patient_id=p.patient_id
                WHERE p.first_name=%s
                AND c.doctor_id=%s
                ORDER BY c.consultation_date DESC
                """
                database.dbcursor.execute(query,(name,self.staff_id))
                consultations = database.dbcursor.fetchall()

            elif choice == "3":
                return
            else:
                print("Invalid Choice.")
                continue

            if not consultations:
                print("\nNo Consultation History Found.")
                continue
            print("\n========== CONSULTATION HISTORY ==========\n")
            for i, consultation in enumerate(consultations, start=1):
                print(
                    f"{i}. {consultation[1]} | "
                    f"{consultation[3]} {consultation[4]} | "
                    f"{consultation[5]}"
                )
            print(f"{len(consultations)+1}. Back")

            select = input("Select Consultation : ").strip()
            if not select.isdigit():
                print("Invalid Choice.")
                continue
            select = int(select)
            if select == len(consultations)+1:
                continue
            if select < 1 or select > len(consultations):
                print("Invalid Choice.")
                continue

            consultation_id = consultations[select-1][0]

            self.view_consultation_details( consultation_id)

    def view_consultation_details(self, consultation_id):
        #  Patient & Consultation Details 
        query = """
        SELECT
            p.patient_id,
            p.first_name,
            p.last_name,
            p.age,
            p.gender,
            p.blood_group,
            p.phone,

            s.first_name,
            s.last_name,

            c.symptoms,
            c.diagnosis,
            c.notes,
            c.consultation_date,

            a.token_number,
            a.appointment_time

        FROM consultation c

        INNER JOIN patient p
        ON c.patient_id = p.patient_id

        INNER JOIN appointment a
        ON c.appointment_id = a.appointment_id

        INNER JOIN staff s
        ON c.doctor_id = s.staff_id

        WHERE c.consultation_id = %s
        """
        database.dbcursor.execute(query, (consultation_id,))
        details = database.dbcursor.fetchone()
        if not details:
            print("\nConsultation Record Not Found.")
            return

        #  Medicines 
        query = """
        SELECT
            m.medicine_name,
            m.medicine_type,
            m.strength,

            p.frequency,
            p.duration,
            p.quantity,
            p.instructions,
            p.route

        FROM prescription p

        INNER JOIN medicine m
        ON p.medicine_id = m.medicine_id

        WHERE consultation_id = %s

        ORDER BY prescription_id
        """
        database.dbcursor.execute(query, (consultation_id,))
        medicines = database.dbcursor.fetchall()

        # Lab Tests 
        query = """
        SELECT
            l.test_name,
            l.department
        FROM lab_request r
        INNER JOIN lab_test l
        ON r.test_id = l.test_id
        WHERE consultation_id = %s
        ORDER BY l.department, l.test_name
        """
        database.dbcursor.execute(query, (consultation_id,))
        tests = database.dbcursor.fetchall()
        print("\n")
        print("=" * 70)
        print("             CONSULTATION RECORD")
        print("=" * 70)
        print("Patient ID       :", details[0])
        print("Patient Name     :", details[1], details[2])
        print("Age              :", details[3])
        print("Gender           :", details[4])
        print("Blood Group      :", details[5])
        print("Phone            :", details[6])

        print()

        print("Doctor           : Dr.", details[7], details[8])
        print("Consult Date     :", details[12])
        print("Token Number     :", details[13])
        print("Appointment Time :", self.format_time(details[14]))

        print("-" * 70)

        print("\nSYMPTOMS")
        print(details[9])

        print("\nDIAGNOSIS")
        print(details[10])

        print("\nDOCTOR NOTES")
        print(details[11] if details[11] else "Nil")

        print("\n")
        print("=" * 70)
        print("MEDICINES")
        print("=" * 70)

        if medicines:
            print("{:<20}{:<12}{:<10}{:<8}{:<10}".format(
                "Medicine",
                "Strength",
                "Freq",
                "Days",
                "Qty"
            ))

            print("-" * 70)

            for medicine in medicines:
                print("{:<20}{:<12}{:<10}{:<8}{:<10}".format(
                    medicine[0],
                    medicine[2],
                    medicine[3],
                    medicine[4],
                    medicine[5]
                ))
                print("   Route        :", medicine[7])
                print("   Instructions :", medicine[6])
                print()
        else:
            print("No Medicines Prescribed.")
        print("\n")
        print("=" * 70)
        print("LAB TESTS")
        print("=" * 70)

        if tests:
            for i, test in enumerate(tests, start=1):
                print(f"{i}. {test[0]} ({test[1]})")
        else:
            print("No Lab Tests Prescribed.")
        print("\n")
        print("=" * 70)
        input("\nPress Enter To Continue...").strip()