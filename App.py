###########################################################################################

#imports
from flask import Flask, render_template, redirect, request, url_for, session 

# For Security
from flask_wtf.csrf import CSRFProtect

# For DataBase Connection
import sqlite3

############################################################################################

''' 
Initial Setup for the Applications
if securtiy key is removed then session will not work
during deployment change the debug to false

'''
app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = '97^%^&*()(*&^(*&^%$%^&*(*&^%'
app.debug = True


############################################################################################


# Login Route if session not registered redirect to here
@app.route('/', methods = ['GET', 'POST'])
@app.route('/login/', methods = ['GET', 'POST'])
def login_page():
    msg = "We'll never share your email with anyone else."
    return render_template('login.html', msg = msg)


#############################################################################################


# Home rendered after login or already logged in
'''
Id is autoincremented data in the db
each user has unique id,
future development should restirct the number of browser windows with same id 

'''
@app.route('/Home/<id>', methods = ['GET', 'POST'])
def home(id):
    user_data = {
        'email': " ",
        'FirstName':" ",
        'LastName' : " "
    }
    global session
    if  not  session.get('email'):
        return redirect("/login")
    else:
        with sqlite3.connect('./userlogin.db') as con:
            cursor = con.execute(f' select * from Users where ID = "{id}" ')
            for row in cursor:
                user_data = {
                    'email':row[1],
                    'FirstName':row[3],
                    'LastName' : row[4]

                }
            return render_template('home.html',context = user_data)

    return render_template('home.html', context = user_data)




##############################################################################################

# Route to validate the login data 
@app.route('/validate' , methods = ['GET' ,'POST'])
def validate():
    if request.method == 'POST':
        email = request.form['mailId']
        password = request.form['passwd']
        try:
            with sqlite3.connect('./userlogin.db') as con:
                cursor = con.execute(f' select * from Users where email = "{email}"  ')
                for row in cursor:
                    if row[2] == password:
                        print('varified')
                        user_data = {
                            'id':row[0],
                            'email' : email,
                            'Password' : password,
                            'FirstName' : row[3],
                            'LastName' : row[4]
                            }
                        global session
                        session['email'] = email
                        return redirect(f'/Home/{user_data["id"]}')

        except Exception as e:
            print(e)
            err = f"Invalid email {email} or password {password} "
            return render_template('login.html', msg = err)


    err = "Enter your proper email Id and password"
    return render_template('login.html', msg = err)
        

##############################################################################################

# singn up route for new users gets the route to add
@app.route('/Signup',methods = ['GET' ,'POST'])
def user_signup():
    return render_template('signup.html')

@app.route('/add',methods = ['GET' ,'POST'])
def add():
    try:
        with sqlite3.connect('./userlogin.db') as con:
            con.execute(f" insert into Users (email,Password,FirstName,LastName) VALUES('{email}','{Password}', '{FirstName}', '{LastName}' );  ")
            con.commit()
    except:
        err = 'User could not be added'
    return render_template('signup.html',msg = err)

##############################################################################################


# Invalid urls routings handled
@app.errorhandler(404)
def page_not_found(error):
    # future developemt to render custom 404 error page
    return 'This Page Does Not Exists',404




################################################################################################
if __name__ == "__main__":
    app.run()