import psycopg2
import requests
import random
import string

connection=psycopg2.connect(database='Hackathon',
                            user='alonnbarthels',
                            password='310103',
                            host='localhost',
                            port='5432')


cursor= connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS r_employees (
               employee_id SERIAL PRIMARY KEY,
               first_name VARCHAR (50) NOT NULL,
               last_name VARCHAR (50) NOT NULL,
               total_leave INTEGER,
               used_leave INTEGER,
               leave_balance INTEGER,
               password VARCHAR(50))''')
connection.commit()  
cursor.close()  

employees_api = requests.get("https://fakerapi.it/api/v1/persons?_quantity=15")

data= employees_api.json()
employees = data["data"]


def generate_random_password(length=6):
    characters = string.ascii_letters + string.digits 
    return ''.join(random.choice(characters) for _ in range(length))

for i in employees:
    first_name = i['firstname']
    last_name= i['lastname']
    total_leave= random.randint(15,30)
    used_leave= random.randint(0,total_leave)
    leave_balance = total_leave - used_leave
    password = generate_random_password()  

    cursor.execute(f''' INSERT INTO r_employees (first_name, last_name, total_leave, used_leave,leave_balance,password)
                   VALUES ('{first_name}','{last_name}','{total_leave}','{used_leave}','{leave_balance}','{password}')''')
    
connection.commit()
