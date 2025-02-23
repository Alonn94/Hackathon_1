import psycopg2
from leave_requests import Absencerequest, view_employee_requests

connection = psycopg2.connect(database='Hackathon',
                                  user='alonnbarthels',
                                  password='310103',
                                  host='localhost',
                                  port='5432')

def employee_login():
    while True:
    
        cursor = connection.cursor()

        name= input('\nPlease enter your name: ')
        password = input('Enter your password to log in: ')

        cursor.execute("SELECT employee_id,first_name,last_name,total_leave,used_leave,leave_balance FROM r_employees WHERE first_name = %s and password =%s", (name,password))

        employee= cursor.fetchone()
        cursor.close()

        if employee:
            employee_id=employee[0]
            print(f"\nWelcome {employee[1]} {employee[2]},\nGreat to see you again!")
            print(f"Find here a snipped of your profile:\n")
            print(f"Total leave days: {employee[3]}")
            print(f"Until today, you used up {employee[4]} day(s)")
            print(f"Remaining leavebalance: {employee[5]} day(s)")
            return employee_id
        else: print(f"Invalid credentials, please try again or contact your admin")
employee_id=employee_login()

def get_employee_balance(employee_id):

    cursor = connection.cursor()

    cursor.execute("SELECT leave_balance FROM r_employees WHERE employee_id = %s", (employee_id,))
    result = cursor.fetchone()

    cursor.close()
    return result[0]

def employee_menu(employee_id):
    if not employee_id:
        print("Employee ID not found, Please log in again")
        return
    while True:
        print("\n  ** Employee Menu **  \n")
        print("(1️) Request Leave")
        print("(2️) View Past/Pending Requests")
        print("(3️) Delete a leave request")
        print("(4) Log Out")

        choice = input("\nSelect an option:").strip()

        if choice == "1":
         while True:
            current_balance = get_employee_balance(employee_id)
            print(f"\n~Your current leave balance: {current_balance} days~")

            leave_type= input("\nEnter the type of leave you wanna take (Vacation,Sick leave, etc.):").strip()
            if leave_type.isdigit():
                print("Please enter a valid leave type!")
                continue
            duration= int(input("\nPlease enter the number of days:").strip())
            if  duration > current_balance:
                print(f"\nYou only have {current_balance} days available. Request denied. Please re-initiater.")
                continue

            request_detail = input("\nPlease mention dates and information if needed: ")

            request = Absencerequest(employee_id,leave_type,duration,request_detail)
            request_id= request.save()

            if request_id:
                 print(f"\nYour leave request with the ID : {request_id} has been submitted!")
            break
        elif choice == "2":
             view_employee_requests(employee_id)

        elif choice == "3":

            cursor=connection.cursor()

            cursor.execute(f'''
                SELECT id, leave_type, request_date, duration, status,request_details
                FROM absence_requests
                WHERE employee_id = '{employee_id}' and status='Pending'
                ORDER BY request_date DESC
                ''',)
    
            leave_requests = cursor.fetchall()
            cursor.close()

            if not leave_requests:
                print("\n======You have no pending requests that could be deleted.========\n")
                continue
            request_id = int(input("\nEnter the request ID that was shared with you to delete: ").strip())
            request= Absencerequest(employee_id,None,None,None)
            request.delete(request_id)
            if request_id:
             print(f"\nYour request with ID: {request_id} was successfully deleted")

        elif choice == "4":
                print("You are logging out, see you next time!")
                break
        else: print("Invalid choice. Please try again")
        
employee_menu(employee_id)
