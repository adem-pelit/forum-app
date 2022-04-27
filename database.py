"""
import mysql.connector

#connection---------------------
mydb = mysql.connector.connect(
  host="sql11.freesqldatabase.com",
  user="sql11487633",
  password="fxBbXP8cYw",
  database = "sql11487633",
)
"""
"""
mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database = "FORUM"
)
"""
#connection---------------------
"""
cursor = mydb.cursor()

#cursor.execute('CREATE TABLE IF NOT EXISTS students(id INT AUTO_INCREMENT primary key NOT NULL, ad TEXT NOT NULL, soyad TEXT NOT NULL)')
cursor.execute('CREATE TABLE IF NOT EXISTS users(id INT AUTO_INCREMENT primary key NOT NULL, name TEXT NOT NULL, password TEXT NOT NULL, picture TEXT NOT NULL, aboutME TEXT NOT NULL, isMod BOOLEAN NOT NULL)')
cursor.execute('CREATE TABLE IF NOT EXISTS headline(id INT AUTO_INCREMENT primary key NOT NULL, headline TEXT NOT NULL, explanation TEXT NOT NULL, likes INT DEFAULT 0, userId INT, canComment BOOLEAN NOT NULL)')
cursor.execute('CREATE TABLE IF NOT EXISTS comment(id INT AUTO_INCREMENT primary key NOT NULL, content TEXT NOT NULL, likes INT DEFAULT 0, userId INT, headId INT, responseId INT)')
"""
#cursor.execute("INSERT INTO students(ad,soyad) VALUES('ADEM','PELIT')")
#res = cursor.execute('SELECT * FROM FORUM')

#database start-------------------









"""import sqlite3

con = sqlite3.connect("deneme.db")

cursor = con.cursor()

#cursor.execute('CREATE TABLE students(id INT AUTO INCREMENT, ad TEXT, soyad TEXT)')

#cursor.execute("INSERT INTO students(ad,soyad) VALUES('ADEM','PELIT')")

res = cursor.execute("SELECT rowid,* FROM students")

for i in res.fetchall():
    print(i[2])

con.commit()

con.close()"""