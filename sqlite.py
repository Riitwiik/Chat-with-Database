import sqlite3

connection=sqlite3.connect("student.db")

cursor=connection.cursor()

table_info="""create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION VARCHAR(25),MARKS INT )"""

cursor.execute(table_info)

cursor.execute('''Insert Into STUDENT values('Ritwik','AI','A',97)''')
cursor.execute('''Insert Into STUDENT values('Shrey','AI','D',90)''')
cursor.execute('''Insert Into STUDENT values('Rajat','English','C',99)''')
cursor.execute('''Insert Into STUDENT values('Sudarshan','Bio','B',87)''')

print("Inserted record")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)
connection.commit()
connection.close()