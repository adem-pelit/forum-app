import os
from click import password_option
from flask import Flask, request, send_from_directory, session, redirect, url_for, render_template
import mysql.connector
import json
import datetime
from hashlib import sha512
import urllib

app = Flask(__name__)

#session işlemleri-----------------------
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "secret_key"


#session işlemleri-----------------------

mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database = "",
)

cursor = mydb.cursor()

"""
cursor.execute('CREATE TABLE IF NOT EXISTS students(id INT AUTO_INCREMENT primary key NOT NULL, ad TEXT NOT NULL, soyad TEXT NOT NULL)')
cursor.execute('CREATE TABLE IF NOT EXISTS users(id INT AUTO_INCREMENT primary key NOT NULL, name TEXT NOT NULL, password TEXT NOT NULL, picture TEXT NOT NULL, aboutME TEXT NOT NULL, isMod BOOLEAN NOT NULL)')
cursor.execute('CREATE TABLE IF NOT EXISTS headline(id INT AUTO_INCREMENT primary key NOT NULL, headline TEXT NOT NULL, explanation TEXT NOT NULL, likes INT DEFAULT 0, userId INT, canComment BOOLEAN NOT NULL)')
cursor.execute('CREATE TABLE IF NOT EXISTS comment(id INT AUTO_INCREMENT primary key NOT NULL, content TEXT NOT NULL, likes INT DEFAULT 0, userId INT, headId INT, responseId INT)')
"""

def dbget(query):
    cursor.execute(query)
    res = cursor.fetchall()
    result = [list(i) for i in res]
    if len(result) > 0:
        for i in result:
            for j in range(len(i)):
                if type(i[j]) == str:
                    i[j] = urllib.parse.unquote(i[j])
    return result

def dbput(query):
    cursor.execute(query)
    mydb.commit()

@app.route('/', methods=['POST','GET'])
def home():
    
    if "name" in session and "pass" in session:
        isMod = dbget(f"SELECT isMod from users where name='{urllib.parse.quote(session['name'])}';")[0][0]
        return render_template(
            "headers.html",
            headers = dbget("SELECT a.id,a.headline,a.explanation,a.likes, b.name,b.picture, a.canComment FROM headline a JOIN users b ON a.userId = b.id ORDER BY a.id DESC"),
            isMod = isMod,
            name = session['name']
        )
        
    return "<meta http-equiv='refresh' content='0; url=/login'>"

@app.route('/user', methods=['GET'])
def user():
    if request.method == "GET":
        if "name" in session and "pass" in session:
            name = request.args.get('name')
            if name != None and len(name) > 0:
                result = dbget(f"SELECT * FROM users where name='{urllib.parse.quote(name)}';")
                if len(result) == 0: return "<meta http-equiv='refresh' content='0; url=/'>"
                isMod = dbget(f"SELECT isMod from users where name='{urllib.parse.quote(session['name'])}';")[0][0]
                return render_template(
                    "aboutMe.html",
                    user = result[0] ,
                    headers = dbget(f"SELECT a.id,a.headline,a.explanation,a.likes, b.name,b.picture FROM headline a JOIN users b ON a.userId = b.id WHERE name='{name}' ORDER BY a.id DESC"),
                    isMod = isMod
                )
    return "<meta http-equiv='refresh' content='0; url=/'>"

@app.route('/post', methods=['GET'])
def forum():
    if request.method == "GET":
        if "name" in session and "pass" in session:
            id = request.args.get('id')
            if id != None and len(id) > 0:
                yorumlar = dbget(f"SELECT a.id, a.content, a.likes, b.name,b.picture, c.id, c.content, d.name, d.picture FROM comment a LEFT JOIN users b ON a.userId=b.id LEFT JOIN comment c ON a.responseId=c.id LEFT JOIN users d ON c.userId=d.id where a.headId={id}")
                i = dbget(f"SELECT a.id, a.headline, a.explanation, a.likes, b.name, b.picture, a.canComment FROM headline a JOIN users b ON a.userId = b.id WHERE a.id={id}"),
                isMod = dbget(f"SELECT isMod from users where name='{urllib.parse.quote(session['name'])}';")[0][0]
                if len(i) == 0: 
                    return "<meta http-equiv='refresh' content='0; url=/'>"
                return render_template(
                    "postlar.html",
                    i = i[0][0],
                    yorumlar = yorumlar,
                    isMod=isMod,
                    name=session['name']
                )
    return "<meta http-equiv='refresh' content='0; url=/'>"

@app.route('/addComment', methods=['GET'])
def addComment():
    if "name" in session and "pass" in session:
        if request.method == "GET":
            userID = dbget("SELECT id FROM users WHERE name='"+ session["name"] +"'")[0][0]
            content = urllib.parse.quote(request.args["content"])
            headId = urllib.parse.quote(request.args["headId"])
            responseId = urllib.parse.quote(request.args["responseId"])
            print(f"VALUES('{content}','{userID}','{headId}','{responseId}')")
            try:
                dbput(f"INSERT INTO comment(content,userId,headId,responseId) VALUES('{content}','{userID}','{headId}','{responseId}');")
                result = dbget(f"SELECT a.id, a.content, a.likes, b.name,b.picture, c.id, c.content, d.name, d.picture FROM comment a LEFT JOIN users b ON a.userId=b.id LEFT JOIN comment c ON a.responseId=c.id LEFT JOIN users d ON c.userId=d.id where a.id=(SELECT max(id) FROM comment);")[0]
                "a.id, a.content, a.likes, b.name,b.picture, c.id, c.content, d.name, d.picture"
                "   0,         1,       2,      3,        4,    5,         6,      7,         8"
                print("rasul:", result)
                if result[5] != None and result[5] != 0:
                    result = {
                        "id": result[0],
                        "content": result[1],
                        "likes":result[2],
                        "name": result[3],
                        "pp": result[4],
                        "response": {
                            "id": result[5],
                            "content": result[6],
                            "name": result[7],
                            "pp": result[8],
                        }
                    }
                else:
                    result = {
                        "id": result[0],
                        "content": result[1],
                        "likes":result[2],
                        "name": result[3],
                        "pp": result[4]
                    }
                return json.dumps(result)
            except Exception as e:
                return "ERROR : " + str(e)

        return json.dumps(result)
    else:
        return "<meta http-equiv='refresh' content='0; url=/'>"

@app.route('/delComment', methods=['GET'])
def delComment():
    if "name" in session and "pass" in session:
        if request.method == "GET":
            try:
                id = urllib.parse.quote(request.args["id"])
                name = dbget("SELECT b.name FROM comment a LEFT JOIN users b ON a.userId=b.id WHERE a.id="+ id +"")[0][0]
                isMod = dbget("SELECT isMod FROM users WHERE name='"+ session["name"] +"'")[0][0]
                if isMod == 0 or session["name"] == name:
                    dbput(f"DELETE FROM comment WHERE id="+id+";")
                    result = dbget(f"SELECT * FROM comment WHERE id="+id+";")
                    if len(result) == 0:
                        return "true"
                    else: 
                        return "false"
                else: return "false"
            except Exception as e:
                return "ERROR : " + str(e)

        return "false"
    else:
        return "<meta http-equiv='refresh' content='0; url=/'>"

@app.route('/canComment', methods=['GET'])
def canComment():
    if "name" in session and "pass" in session:
        if request.method == "GET":
            try:
                id = urllib.parse.quote(request.args["id"])
                val = urllib.parse.quote(request.args["val"])
                name = dbget("SELECT b.name FROM headline a LEFT JOIN users b ON a.userId=b.id WHERE a.id="+ id +"")[0][0]
                isMod = dbget("SELECT isMod FROM users WHERE name='"+ session["name"] +"'")[0][0]
                if isMod == 0 or session["name"] == name:
                    print(f"UPDATE headline SET canComment = {val} WHERE id = {id};")
                    dbput(f"UPDATE headline SET canComment = {val} WHERE id = {id};")
                    return "true"
                else: return "false"
            except Exception as e:
                return "ERROR : " + str(e)

        return "false"
    else:
        return "<meta http-equiv='refresh' content='0; url=/'>"

@app.route('/deleteHeadline', methods=['GET'])
def deleteHeadline():
    if "name" in session and "pass" in session:
        if request.method == "GET":
            try:
                id = urllib.parse.quote(request.args["id"])
                name = dbget("SELECT b.name FROM headline a LEFT JOIN users b ON a.userId=b.id WHERE a.id="+ id +"")[0][0]
                isMod = dbget("SELECT isMod FROM users WHERE name='"+ session["name"] +"'")[0][0]
                if isMod == 1 or session["name"] == name:
                    dbput(f"DELETE FROM headline WHERE id="+id+";")
                    result = dbget(f"SELECT * FROM headline WHERE id="+id+";")
                    if len(result) == 0:
                        return "true"
                    else: 
                        return "false"
                else: return "false " + session["name"] +" : "+ name + " isMod: " + str(isMod)
            except Exception as e:
                return "ERROR : " + str(e)

        return "false"
    else:
        return "<meta http-equiv='refresh' content='0; url=/'>"

@app.route('/addHeadline', methods=['GET', 'POST'])
def addHeadline():
    
    if "name" in session and "pass" in session:
        if request.method == "POST":
            userID = dbget("SELECT id FROM users WHERE name='"+ session["name"] +"'")[0][0]
            title = urllib.parse.quote(request.form["title"])
            explanation = urllib.parse.quote(request.form["message"])
            
            dbput("INSERT INTO headline(headline,explanation,userId,canComment) VALUES ('"+title+"','"+explanation+"',"+str(userID)+",1)")

        return "<meta http-equiv='refresh' content='0; url=/'>"
    else:
        return "<meta http-equiv='refresh' content='0; url=/login'>"

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == "POST":
        if request.form.get('name') != None and request.form.get('pass') != None:
            isim = urllib.parse.quote(request.form.get('name'))
            password = urllib.parse.quote(request.form.get('pass'))
            cursor.execute('SELECT password FROM users WHERE name="'+isim+'";')
            result = cursor.fetchall()
            if len(result) == 0:
                return " <meta http-equiv='refresh' content='0; url=/login?message=User is not found!'>"
            if result[0][0] == password:
                session["name"] = urllib.parse.quote(request.form.get('name'))
                session["pass"] = urllib.parse.quote(request.form.get('pass'))
                return " <meta http-equiv='refresh' content='0; url=/'>"
            else:
                return " <meta http-equiv='refresh' content='0; url=/login?message=Wrong password!'>"
    if "name" in session:
        if session["name"] != "":
            print("name: '"+ session["name"]+"'")
            return " <meta http-equiv='refresh' content='0; url=/'>"
    #session["id"] = "Server saat: " + str(datetime.datetime.now())
    #cursor.execute('SELECT * FROM students')
    return render_template("login.html", message= "Please Login!" if request.args.get('message') == None else request.args.get('message'))

@app.route('/signin', methods=['POST','GET'])
def signin():
    
    if request.method == "POST":
        if request.form.get('name') != None and request.form.get('pass') != None:
            isim = urllib.parse.quote(request.form.get('name'))
            password = urllib.parse.quote(request.form.get('pass'))
            if len(password) < 8:
                return "<meta http-equiv='refresh' content='0; url=/signin?message=password must be more than 8 letters!'>"
            result = dbget('SELECT password FROM users WHERE name="'+isim+'";')
            if len(result) == 0:
                dbput(f"INSERT INTO users(name,password,picture,aboutME) VALUES('{isim}','{password}','static/pps/defaultpp.png','edit about me');")
                result = dbget('SELECT password FROM users WHERE name="'+isim+'";')
                if len(result) != 0:
                    session["name"] = urllib.parse.quote(request.form.get('name'))
                    session["pass"] = urllib.parse.quote(request.form.get('pass'))
                    return "<meta http-equiv='refresh' content='0; url=/'>"
                else:
                    return "<meta http-equiv='refresh' content='0; url=/signin?message=something is happened!'>"
            else:
                return " <meta http-equiv='refresh' content='0; url=/signin?message=this username is already taken!'>"

    if "name" in session:
        if session["name"] != "":
            print("name: '"+ session["name"]+"'")
            return " <meta http-equiv='refresh' content='0; url=/'>"
    
    #session["id"] = "Server saat: " + str(datetime.datetime.now())
    #cursor.execute('SELECT * FROM students')
    return render_template("signin.html", message= "Create Account!" if request.args.get('message') == None else request.args.get('message'))

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return  "<meta http-equiv='refresh' content='0; url=/login'>"

@app.errorhandler(404)
def not_found(e):
    return "<meta http-equiv='refresh' content='0; url=/'>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

"@app\.route\('(.*)', m"