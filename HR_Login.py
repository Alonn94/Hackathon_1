import psycopg2
from leave_approvals import view_pending_requests, approval_request, export_leave_requests

def hr_login():
    while True:
        connection = psycopg2.connect(database='Hackathon',
                                  user='alonnbarthels',
                                  password='310103',
                                  host='localhost',
                                  port='5432')
       
        cursor = connection.cursor()

        name = input("Enter HR Username: ")
        password = input("Enter Password: ")

        cursor.execute("SELECT hr_id, name FROM hr_users WHERE name = %s AND password = %s", (name, password))
        hr_user = cursor.fetchone()

        cursor.close()
        connection.close()

        if hr_user:
            print(f"\n Welcome, {hr_user[1]}! You are logged in as HR.\n")
            return hr_user[0]  

        else: 
            print("Invalid credentials, please try again or contact technical department") 

def hr_menu(hr_id):
    while True:
        print(" ** HR Menu **\n")
        print("(1️) View Pending Requests")
        print("(2️) Approve/Reject Requests")
        print("(3️) Export Leave Requests")
        print("(4) Log Out")

        choice = input("Select an option: \n").strip()

        if choice == "1":
            view_pending_requests()
        elif choice == "2":
            approval_request(hr_id)
        elif choice == "3":
            export_leave_requests()
        elif choice == "4":
            print("Logging out, have a good day!")
            break
        else:
            print("Invalid choice. Please try again.")

hr_id = hr_login()
if hr_id:
    hr_menu(hr_id)