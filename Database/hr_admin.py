import psycopg2

connection = psycopg2.connect(database='Hackathon', 
                              user='alonnbarthels',
                              password='310103',
                              host='localhost',
                              port='5432')

cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS hr_users (
        hr_id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL
    )
''')

cursor.execute('''
    ALTER TABLE absence_requests
    ADD COLUMN IF NOT EXISTS processed_by INTEGER REFERENCES hr_users(hr_id),
    ADD COLUMN IF NOT EXISTS process_date TIMESTAMP
''')

cursor.execute('''
    INSERT INTO hr_users (name, password) 
    VALUES ('Alonn', '1234')
    ''',)

connection.commit()
cursor.close()
connection.close()
