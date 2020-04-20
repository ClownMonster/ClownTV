import sqlite3

con = sqlite3.connect('./userlogin.db')

cursor = con.execute(" select * from Users ")
for row in cursor:
    print(row)