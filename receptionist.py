from patient import Patient
from schedule import Scheduling


class Receptionist:
    def dashboard(self):
        while True:
            print("\n========== RECEPTIONIST DASHBOARD ==========")
            print("1. Patient Management")
            print("2. Scheduling")
            print("3. Logout")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.patient_management()
            elif choice == "2":
                self.scheduling()
            elif choice == "3":
                print("\nLogging Out...")
                return 
            else:
                print("\nInvalid Choice")


    def patient_management(self):

        patient = Patient()

        while True:

            print("\n========== PATIENT MANAGEMENT ==========")
            print("1. Register Patient")
            print("2. View Patients")
            print("3. Search Patient")
            print("4. Update Patient")
            print("5. Disable Patient")
            print("6. Back")
            choice = input("Enter your choice : ").strip()

            if choice == "1":
                patient.register_patient()
            elif choice == "2":
                patient.view_patients()
            elif choice == "3":
                patient.search_patient()
            elif choice == "4":
                patient.update_patient()
            elif choice == "5":
                patient.disable_patient()
            elif choice == "6":
                break
            else:
                print("Invalid Choice")


    def scheduling(self):
        
        scheduling =Scheduling()
        scheduling.schedule_appointment()























   