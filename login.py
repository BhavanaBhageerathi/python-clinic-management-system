from database import database
from receptionist import Receptionist
from doctor import Doctor


class Login:
        
    def login(self):
        while True:
            print("""
+----------------------------------------+
|        CLINIC MANAGEMENT SYSTEM        |
+----------------------------------------+
""")
            print('''
====================
    LOGIN PAGE    
====================
              ''')
            username=input("\nENTER YOUR USERNAME:").strip()
            password=input("\nENTER YOUR PASSWORD:").strip()
            myquery = """
            SELECT staff_id,first_name, last_name, role
            FROM staff
            WHERE  BINARY username = %s
            AND BINARY password = %s
            AND is_active = TRUE
            """
            values=(username,password)
        
            database.dbcursor.execute(myquery,values)
            result = database.dbcursor.fetchone()

            if result:  
                staff_id=result[0]            #if result has atleast one value then if statement becomes true(we are selecting role here)
                first_name = result[1]
                last_name = result[2]
                role = result[3]    #result will be in tuple ('dctor',) or ('receptionist) so result[0] meand doctor or receptionist.tuple because dbcursor always returns row and that row has multiple columns and is always represented as a tuple by python

                if role == "Doctor":
                    print("\n==============================================")
                    print("           LOGIN SUCCESSFUL")
                    print("==============================================")
                    print(f"Welcome, Dr. {first_name} {last_name}")
                    print("Wishing you a productive consultation session.\n")
                    Doctor(staff_id,first_name,last_name).dashboard()

                elif role == "Receptionist":
                    print("\n==============================================")
                    print("           LOGIN SUCCESSFUL")
                    print("==============================================")
                    print(f"Welcome, {first_name} {last_name}")
                    print("Reception Desk is Ready.\n")
                    Receptionist().dashboard()
               
                
            else:
                print("Invalid Username or Password")