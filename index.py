from flask import Flask 
from flask import render_template
from flask import request
from flask import session   
from random import * 
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
import datetime
from werkzeug.utils import secure_filename

import random 
from flask_pymongo import PyMongo
from flask import redirect, url_for
import datetime

app = Flask(__name__)
app.secret_key="secret key"

UPLOAD_FOLDER = 'static/uploads/'



app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','webp'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

mongodb_client = PyMongo(app, uri="mongodb+srv://papaipratihar01:papai727241@cluster0.fuhbr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = mongodb_client.db
 
@app.route('/')  
def indexpage():  
    return render_template('index.html')

@app.route('/about')  
def aboutpage():  
    return render_template('about.html')

@app.route('/registration')  
def registrationpage():  
    return render_template('registration.html')

@app.route('/studentregistration', methods=["GET", "POST"])  
def studentregistrationpage():
    if request.method == 'GET':
        return render_template('studentregistration.html')
    else:
        x = datetime.datetime.now() 
        x = ''+str(x)
        
        userobj = db.student.find_one(
        {'useremail': request.form['email']})
        print(userobj)
        
        if userobj:
            #print(userobj['username'])
            return render_template('studentregistration.html',msg=' User Already Registered')
       
        db.student.insert_one(
        {'username1': request.form['firstname'],
        'username2': request.form['middlename'],
        'username3': request.form['lastname'],
        'userroll': request.form['rollno'],
        'usermobile': request.form['mobno'],
        'userdateofbirth': request.form['dateofbirth'],
        'useremail': request.form['email'],
        'userdepertment': request.form['dept'],
        'usergender': request.form['gen'],
        'userpass': request.form['pass'],
        'userlanguage': request.form['lang'],
        'usermentor': request.form['mentor'],
        'usermentoremail': request.form['mentoremail'],
        
        'regdate':x

        })
       
        
        return render_template('studentregistration.html',msg = "REGISTRATION SUCCESSFUL")

@app.route('/userupdateprofile', methods=["GET", "POST"])  
def userupdateprofile():
    if request.method == 'GET':
        uemail = session['umail']      
        userobj = db.student.find_one({'useremail': uemail})
        return render_template('userupdateprofile.html',userdata = userobj,uname=session['uname'])
    else:
        db.student.update_one( {'useremail': session['umail'] },
        { "$set": { 'usermobile': request.form['mobno'],
                    'userpass': request.form['pass'], 
                  } 
        })
    return redirect(url_for('userupdateprofile'))



@app.route('/mentorasign', methods=["GET", "POST"])  
def mentorasign():
    if request.method == 'GET':
        return render_template('asignmentor.html')
    else:
        x = datetime.datetime.now() 
        x = ''+str(x)
        
       
        db.asignmentor.insert_one(
        {'username': request.form['name'],
        'userroll': request.form['rollno'],
        'useremail': request.form['email'],
        'usermentor': request.form['mentor'],
        'usermentoremail': request.form['mentoremail'],
        
        'regdate':x

        })
        return render_template('asignmentor.html',msg = "UPDATE SUCCESSFUL")


@app.route('/facultyregistration', methods=["GET", "POST"])  
def facultyregistrationpage():
    if request.method == 'GET':
        return render_template('facultyregistration.html')
    else:
        x = datetime.datetime.now() 
        x = ''+str(x)
        
        userobj = db.student.find_one(
        {'useremail': request.form['email']})
        print(userobj)
        
        if userobj:
            #print(userobj['username'])
            return render_template('facultyregistrationhtml',msg=' User Already Registered')
       
        db.teacher.insert_one(
        {'username1': request.form['firstname'],
        'username2': request.form['middlename'],
        'username3': request.form['lastname'],
        'userid': request.form['idno'],
        'usermobile': request.form['mobno'],
        'userdateofbirth': request.form['dateofbirth'],
        'useremail': request.form['email'],
        'usergender': request.form['gen'],
        'userpass': request.form['pass'],
        'registrationdate':datetime.datetime.now(),
        'regdate':x
        })
        return render_template('facultyregistration.html',msg = "REGISTRATION SUCCESSFUL")
        
@app.route('/login')  
def loginpage():  
    return render_template('login.html')




@app.route('/studentlogin', methods=["GET", "POST"])  
def studentpage(): 
    if request.method == 'GET': 
        return render_template('studentlogin.html')
    else:
        user = db.student.find_one(
        {'useremail': request.form['email'],
         'userpass': request.form['pass']
        })
        print(user)
        
        if user:
            #print(user['username1'])
            session['umail']=user['useremail']
            session['uname']=['username']
            session['usertype']= 'USER'
            return render_template('studentafterlogin.html',userdata=user)
        else:
            return render_template('studentlogin.html', msg = "INVALID UID OR PASSWORD")

@app.route('/studentafterlogin')  
def studentafterloginpage():
    userobj = db.student.find({session['umail']:['useremail']})
    print(userobj)
    return render_template('studentafterlogin.html', userdata = userobj)



        
        
    
@app.route('/viewresult')    
def viewresultpage():
    userobj = db.uploadresult.find({})
    print(userobj)
    return render_template('viewresult.html', userdata = userobj)

    


@app.route('/facultylogin', methods=["GET", "POST"])  
def facultyloginpage(): 
    if request.method == 'GET': 
        return render_template('facultylogin.html')
    else:
        user = db.teacher.find_one(
        {'useremail': request.form['email'],
         'userpass': request.form['pass']
        })
        print(user) 
        
        if user:
            #print(user['username1'])
            session['umail']=user['useremail']
            session['uname']=['username']
            session['usertype']= 'USER'
            return render_template('facultyafterlogin.html', userdata=user)
        else:
            return render_template('facultylogin.html', msg = "INVALID UID OR PASSWORD")
@app.route('/tarcherdashboard')  
def teacherafterloginpage():
    userobj = db.teacher.find({})
    print(userobj)
    return render_template('facultyafterlogin.html', userdata = userobj)
   
@app.route('/teacherupdateprofile', methods=["GET", "POST"])  
def updateteacherProfile():
    if request.method == 'GET':
        uemail = session['umail']      
        userobj = db.teacher.find_one({'useremail': uemail})
        return render_template('teacherupdateprofile.html',userdata = userobj)
    else:
        db.teacher.update_one( {'useremail': session['umail'] },
        { "$set": { 'usermobile': request.form['mobno'],
                    'userpass': request.form['pass'],
                  } 
        })
        return redirect(url_for('updateteacherProfile'))

@app.route('/teacherhome')    
def teacherhomepage():
    userobj = db.teacher.find({})
    print(userobj)
    return render_template('teacherhome.html', userdata = userobj)




@app.route('/mentielist', methods=['GET','POST'])  
def mentielist(): 
    if request.method == 'GET':
        return render_template('mentielist.html')
    else:      
        userobj = db.asignmentor.find({'usermentoremail': request.form['mentoremail']})
                
        if userobj:
            return render_template('mentielist.html', userdata = userobj,show_results=1)
        else:
            return render_template('mentielist.html', errormsg = "INVALID EMAIL ID")


@app.route('/searchmentie', methods=['GET','POST'])  
def searchmentie(): 
    if request.method == 'GET':
        return render_template('searchmentie.html')
    else:      
        userobj = db.student.find({'useremail': request.form['mentoremail']})
                
        if userobj:
            return render_template('searchmentie.html', userdata = userobj,show_results=1)
        else:
            return render_template('searchmentie.html', errormsg = "INVALID EMAIL ID")



@app.route('/contactstudent')  
def contactwithmentor(): 
    userobj = db.contact.find({})
    print(userobj)
    return render_template('mentorcontact.html', userdata = userobj)


@app.route('/mentorupdateprofile', methods=["GET", "POST"])  
def mentorupdateprofile():
    if request.method == 'GET':
        uemail = session['umail']      
        userobj = db.student.find_one({'useremail': uemail})
        return render_template('mentorupdateprofile.html',userdata = userobj,uname=session['uname'])
    else:
        db.student.update_one( {'useremail': session['umail'] },
        { "$set": { 'userweeklyperformence': request.form['performence'],
                    'userattendence': request.form['attendence'], 
                    'userassignment': request.form['assignment'],
                  } 
        })
    return redirect(url_for('mentorupdateprofile'))


    
@app.route('/adminlogin', methods=['GET','POST'])  
def adminloginpage(): 
    if request.method == 'GET':
        return render_template('adminlogin.html')
    else:      
        adminuid = request.form['fullname']
        adminpass = request.form['password']
    if(adminuid == 'admin' and adminpass == 'admin'):
        session['umail']=['useremail']
        session['uname']=['username']
        session['usertype']= 'USER'
        return render_template('adminafterlogin.html')
    else:
        return render_template('adminlogin.html', errormsg = "INVALID UID OR PASSWORD")
@app.route('/adminhome')  
def adminafterloginpage(): 
    return render_template('adminafterlogin.html')
@app.route('/viewall')  
def viewallpage():  
    return render_template('viewall.html')

@app.route('/studentdetails')  
def studentdetails(): 
    userobj = db.student.find({})
    print(userobj)
    return render_template('studentdetails.html', userdata = userobj)
@app.route('/facultydetails')  
def facultydetails(): 
    userobj = db.teacher.find({})
    print(userobj)
    return render_template('facultydetails.html', userdata = userobj)
@app.route('/contact',  methods=["GET", "POST"])  
def contactpage():
    if request.method == 'GET':
        return render_template('contact.html')
    else:
        uname = request.form['firstname']
        db.contact.insert_one(
        {'username1': request.form['firstname'],
        'username2': request.form['middlename'],
        'username3': request.form['lastname'],
        'usermobile': request.form['mobno'],
        'useremail': request.form['email'],
        'subject': request.form['subject'],
        'feedback': request.form['message'],
        'contactdate':datetime.datetime.now()
        })
        return render_template('contact.html',msg = "THANKS FOR YOUR FEEDBACK. WE WILL CONTACK YOU SOON.")
        
@app.route('/admincontact')  
def admincontact(): 
    userobj = db.contact.find({})
    print(userobj)
    return render_template('admincontact.html', userdata = userobj)




@app.route('/search', methods=['GET','POST'])  
def searchUser(): 
    if request.method == 'GET':
        return render_template('search.html')
    else:      
        userobj = db.student.find({'useremail': request.form['email']})
                
        if userobj:
            return render_template('search.html', userdata = userobj,show_results=1)
        else:
            return render_template('search.html', errormsg = "INVALID EMAIL ID")




@app.route('/delete', methods=['GET','POST'])  
def deleteUser(): 
    if request.method == 'GET':
        return render_template('deleteuser.html')
    else:      
        responsefrommongodb = db.student.find_one_and_delete(
        {'useremail': request.form['email']})
        print(responsefrommongodb)
        if responsefrommongodb is not None:
            return render_template('deleteuser.html', msg = "SUCCESSFULLY DETELED")
        return render_template('deleteuser.html', msg = "INVALID EMAIL ID")
        
        
@app.route('/addphoto', methods = ['GET','POST']) 
def studentresultpage():  
    if request.method == 'GET': 
        return render_template('addphoto.html')
    else:
        x=datetime.datetime.now()
        x = ''+str(x)

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('upload_image filename: ' +filename)
            flash('Image successfully uploaded')
            path = 'static/UPLOADS/' +filename
            uemail=session['umail']
            uname=session['uname']
            n=str(random.randint(0,999))
            db.uploadresult.insert_one(
                {
                    'useremail': uemail,
                    'username': uname,
                    'userdes':request.form['des'],
                    'userdob':x,
                    'image':path
                }
            )  
            return render_template("addphoto.html")  
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif,webp')
            return redirect(request.url)

    
if __name__ == '__main__':  
   app.run(debug = True)


    






  