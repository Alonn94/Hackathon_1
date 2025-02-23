import psycopg2
import json
connection = psycopg2.connect(database='Hackathon',
                                  user='alonnbarthels',
                                  password='310103',
                                  host='localhost',
                                  port='5432')

def view_pending_requests():

    cursor = connection.cursor()

    cursor.execute('''
        SELECT id, employee_id, leave_type, request_date, duration, status 
        FROM absence_requests
        WHERE status = 'Pending'
        ORDER BY request_date DESC
    ''')

    requests = cursor.fetchall()
    cursor.close()

    if not requests:
        print("No pending leave requests.")
        return
        
    print("** Pending Leave Requests: **\n")

    for req in requests:
        request_id, employee_id, leave_type, request_date, duration, status = req
        print(f"Request ID: {request_id} from Employee ID: {employee_id}\n Leave type: {leave_type} Submission date: {str(request_date)} For a duration of {duration} days \n Current Status:{status}\n")

    return requests  


def approval_request(hr_id):
    requests = view_pending_requests()  
    cursor = connection.cursor()

    if not requests:
        print(" Currently there are no pending requests waiting to be processed")
        return

    request_id = input("Enter the Request ID to approve/reject: ").strip()

    decision = input("Approve (A) or Reject (R)? ").strip().upper()

#was after the if==A before,but not anymoore
    cursor.execute('''
        SELECT employee_id, duration FROM absence_requests WHERE id = %s 
    ''', (request_id,))
    
    request_data = cursor.fetchone()
    employee_id,duration=request_data

    if decision == "A":
        status = "Approved"

        cursor = connection.cursor()
                                                #update of leave balance and used leave
        cursor.execute('''
        UPDATE r_employees
        SET leave_balance = leave_balance - %s,
        used_leave = used_leave + %s
        WHERE employee_id = %s
        ''', (duration, duration, employee_id))
        cursor.close()

    elif decision == "R":
        status = "Rejected"
    else:
        print("invalid choice. Please enter (A) or (R).")
        return

    cursor = connection.cursor()

    cursor.execute('''
        UPDATE absence_requests
        SET status = %s, processed_by = %s, process_date = NOW()
        WHERE id = %s
    ''', (status, hr_id, request_id))

    connection.commit()
    cursor.close()

    print(f"Request {request_id} has been {status}!")


def export_leave_requests():
    cursor=connection.cursor()
    cursor.execute('''
                   SELECT id,employee_id,leave_type,duration,request_details,status,processed_by
                   FROM absence_requests
                   ORDER BY request_date DESC
                   ''')
    
    leave_requests = cursor.fetchall()
    cursor.close
    connection.close

    request_list=[]
    for r in leave_requests:
        request_def = {}
        for i,column in enumerate(cursor.description):
            request_def[column.name]=r[i]
        request_list.append(request_def)

    with open('output.json','w') as f:
        json.dump(request_list,f,indent=4)

#    for r in leave_requests:
        # request_id, employee_id, leave_type, request_date, duration, status, request_details = r
        # requests_list.append({
        #     "Request ID": request_id,
        #     "Employee ID": employee_id,
        #     "Leave Type": leave_type,
        #     "Request Date": request_date.strftime('%Y-%m-%d'),
        #     "Duration":duration,
        #     "Status": status,
        #     "Request Details": request_details
        # })


    with open('output.json','w') as f:
        json.dump(request_list,f,indent=4)
        
    cursor.close
    connection.close
