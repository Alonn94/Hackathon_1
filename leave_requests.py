import psycopg2

connection = psycopg2.connect(database='Hackathon', 
                            user='alonnbarthels',
                            password = '310103',
                            host = 'localhost',
                            port = '5432')

cursor = connection.cursor()
cursor.execute('''CREATE TABLE if not exists absence_requests(
                id SERIAL PRIMARY KEY,
                employee_id INTEGER,
                leave_type VARCHAR(50),
                request_date TIMESTAMP,
                duration INTEGER,
                request_details TEXT,
                status VARCHAR (20) DEFAULT 'Pending',
                FOREIGN KEY (employee_id) REFERENCES r_employees(employee_id) ON DELETE CASCADE)''')
connection.commit()
cursor.close()

class Absencerequest():
    def __init__(self,employee_id,leave_type,duration,request_details):
            self.employee_id=employee_id
            self.leave_type = leave_type
            self.duration = duration
            self.request_details= request_details
#functions that can be called after creation of object (Request)

    def save(self):

        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO absence_requests (employee_id, leave_type, request_date, duration, request_details) 
            VALUES (%s, %s, NOW(), %s, %s) RETURNING id
            ''', (self.employee_id, self.leave_type, self.duration, self.request_details)) 
         
        request_id=cursor.fetchone()[0]

        connection.commit()
        cursor.close()

        return request_id

    def delete(self,request_id):
        
        connection.commit()
        cursor=connection.cursor()

        cursor.execute("SELECT id FROM absence_requests WHERE id = %s AND employee_id = %s", (request_id, self.employee_id))        #to check if request id exists first
        existing_request = cursor.fetchone()

        if not existing_request:
            print(f"\n Request ID {request_id} not found. Can not be deleted.")
            cursor.close()
            connection.close()
            return  

        cursor.execute(f"DELETE FROM absence_requests WHERE employee_id = '{self.employee_id}'  and id= '{request_id}'")
     
        connection.commit()
        cursor.close()

@staticmethod
def view_employee_requests(employee_id):
    cursor = connection.cursor()

    cursor.execute(f'''
        SELECT id, leave_type, request_date, duration, status,request_details
        FROM absence_requests
        WHERE employee_id = '{employee_id}'
        ORDER BY request_date DESC
    ''',)
    
    leave_requests = cursor.fetchall()
    cursor.close()

    if not leave_requests:
        print("======You have no leave requests yet.========\n")
        return

    print("\n  **  Your past/pending Requests:  **  \n")
    for r in leave_requests:
        request_id, leave_type, request_date, duration, status,request_details = r
        print(f"Request ID: {request_id} with Leave Type:{ leave_type}\n Submitted on: {str(request_date)}\n Request for {duration} days,\n Info:{request_details} \n \n Current Status: {status}\n\n*****************\n")
    



