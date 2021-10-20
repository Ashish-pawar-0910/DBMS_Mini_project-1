from os import curdir
from flask import *
# from flask.scaffold import _matching_loader_thinks_module_is_package
from werkzeug.utils import redirect
from flask_mysqldb import MySQL #pip install flask_mysqldb
import yaml                     #pip install pyyaml
import MySQLdb.cursors
import re
import inspect
import validators
import requests
from datetime import datetime

mydata=yaml.load(open('private.yaml'))
app=Flask(__name__)
app.secret_key = mydata['sec_key']

app.config['MYSQL_HOST']=mydata['mysql_host']
app.config['MYSQL_USER']=mydata['mysql_user']
app.config['MYSQL_PASSWORD']=mydata['mysql_password']
app.config['MYSQL_DB']=mydata['mysql_db']

mysql=MySQL(app)

# create database MiniProject
# create table RegisterStudent
# CREATE TABLE RegisterStudent ( 
#     ParticipantId int NOT NULL AUTO_INCREMENT,
#     fname varchar(20) NOT NULL,  
#     lname varchar(20) NOT NULL,  
#     dept varchar(20) NOT NULL,  
#     division varchar(10) NOT NULL,  
#     rollno varchar(20) NOT NULL, 
#     email varchar(40) NOT NULL,  
#     username varchar(20) NOT NULL,  
#     pswd varchar(20) NOT NULL, 
#     PRIMARY KEY (ParticipantId) 
# )
# CREATE TABLE adminDetails ( 
#     adminuser varchar(20) NOT NULL,  
#     pswrd varchar(20) NOT NULL, 
#     PRIMARY KEY (adminuser) 
# )
# add register method with its updated form in index
# add log in method with its updated form in index
# add logout mrthod and its button in new logged in page
# INSERT INTO RegisterStudent(adminuser, pswrd) VALUES('admin','admin@123');
@app.route('/', methods=['GET','POST'])
def base():
    case=0
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'dept' in request.form and 'div' in request.form and 'rollno' in request.form and 'email' in request.form  and 'username' in request.form and 'password' in request.form :
        student=request.form
        fname=student['fname']
        lname=student['lname']
        dept=student['dept']
        div=student['div']
        rollno=student['rollno']
        email=student['email']
        response = requests.get("https://isitarealemail.com/api/email/validate",params = {'email': email})
        status = response.json()['status']
        mails=email.split('@')
        if status == "invalid":
            # flash("Email does not exist. Enter valid email!!")
            return render_template('index.html',case=1)
        elif mails[1]!='pccoepune.org':
            # flash("Enter Official email id only!!")
            return render_template('index.html', case=2)
        username=student['username']
        pswd=student['password']
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM RegisterStudent WHERE username = % s', (username, ))
        participant= cur.fetchone()
        
        # users_email=email
        if participant:
            # flash('Account already exists !')
            return render_template('index.html', case=3)
        elif not re.match(r'[A-Za-z0-9]+', username):
            # flash('Username must contain only characters and numbers !') 
            return render_template('index.html', case=4)
        else:
            cur.execute("INSERT INTO RegisterStudent(fname, lname, dept, division, rollno, email, username, pswd) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",(fname,lname,dept,div,rollno,email,username,pswd))
            mysql.connection.commit()
            # flash('You have successfully registered !')
            return render_template('index.html', case=5)
        redirect('/login')
    elif request.method == 'POST':
        flash('Please fill out the form !')
    case=0
    return render_template('index.html')

#Student login

#Admin login

#Logout

if __name__=="__main__":
    app.run(debug=True)