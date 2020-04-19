import sqlite3

con = sqlite3.connect('./userlogin.db')
con.execute(" create table if not exists Users(ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                email TEXT NOT NULL, Password TEXT NOT NULL, FirstName TEXT NOT NULL,\
                 LastName TEXT NOT NULL)  ")

email = "mk876678@gmail.com"
Password = 'ajithkumar@2'
FirstName = 'Clown'
LastName = 'Monster'
con.execute(f" insert into Users (email,Password,FirstName,LastName) VALUES('{email}','{Password}', '{FirstName}', '{LastName}' );  ")
con.commit()

cursor = con.execute(" select * from Users ")
for row in cursor:
    print(row)