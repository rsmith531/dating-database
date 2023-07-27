from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from static.passwordhash import hash_sha256 # custom hashing functions for passwords

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'dating database'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'rsmit216'     # TODO reconfigure these values to match your credentials
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'rsmit216'

# Intialize MySQL
mysql = MySQL(app)


# ----------------------------------------------------------------------- http://localhost:5001/ --

@app.route('/')
def index():
    ''' redirect to login if logged out or to home page if logged in
    '''

    # Check if user is loggedin
    if 'loggedin' in session:

        # User is loggedin show them the home page
        return redirect(url_for('home'))

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# ------------------------------------------------------------------ http://localhost:5001/login --

@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' login page
    '''

    # Output message if something goes wrong...
    msg = ''

    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM access_control WHERE username = %s', (username,))

        # Fetch one record and return result
        account = cursor.fetchone()

        # Check if an account was returned and if the password hash matches the recalculated hash
        if account and hash_sha256(password, account['salt'], 100) == account['hashed_pw']:

            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['user_ID']
            session['username'] = account['username']

            # Redirect to home page
            return redirect(url_for('home'))

        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)


# ----------------------------------------------------------------- http://localhost:5001/logout --

@app.route('/logout')
def logout():
    ''' logout page
    '''

    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    # Redirect to login page
    return redirect(url_for('login'))


# --------------------------------------------------------------- http://localhost:5001/register --

@app.route('/register', methods=['GET', 'POST'])
def register():
    ''' registration page
    '''

    # Output message if something goes wrong...
    msg = ''

    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']


        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM access_control WHERE username = %s', (username,))
        account = cursor.fetchone()

        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'


        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'

        elif not username or not password:
            msg = 'Please fill out the form!'

        else:

            # hash the password
            hashed_pw, salt = hash_sha256(password, 100)

            # Account doesnt exists and the form data is valid, now insert new account into accounts table

            # First insert a new empty user into the user table to get a user_ID
            cursor.execute('INSERT INTO user VALUES (NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)')

            # Get the auto generated user_ID from the user table
            cursor.execute('SELECT * FROM user WHERE id = LAST_INSERT_ID()')
            new_user = cursor.fetchone()

            # Insert the new user into the access_control table using the generated user_ID
            cursor.execute('INSERT INTO access_control VALUES (%s, %s, %s, %s, %s)', (new_user['user_ID'], username, password, hashed_pw, salt))
            mysql.connection.commit()

            # Create session data to replicate login process, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = new_user['user_ID']
            session['username'] = username

            msg = 'You have successfully registered!'

            redirect(url_for('complete_profile'))

    elif request.method == 'POST':

        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'

    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


# ------------------------------------------------------- http://localhost:5001/complete_profile --

@app.route('/complete_profile', methods=['GET', 'POST'])
def complete_profile():
    ''' finish up profile details here
    '''

    # Output message if something goes wrong...
    msg = ''

    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'firstName' in request.form \
                                and 'lastName' in request.form \
                                and 'city' in request.form \
                                and 'state' in request.form \
                                and 'birthday' in request.form \
                                and 'bio' in request.form \
                                and 'gender' in request.form:

        # Create variables for easy access
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        city = request.form['city']
        state = request.form['state']                                   # TODO make this a dropdown
        birthday = request.form['birthday']                    # TODO make this a calendar selector
        bio = request.form['bio']
        gender = request.form['gender']            # TODO make into a dropdown with current options


        # query to update user with profile information
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Insert the new user into the access_control table using the generated user_ID
        cursor.execute('UPDATE user SET first_name = %s,\
                                        last_name = %s,\
                                        city = %s,\
                                        state = %s,\
                                        birthday = %s,\
                                        bio = %s,\
                                        gender = %s\
                                        WHERE user_id = session[id];',
                        (first_name, last_name, city, state, birthday, bio, gender))

        # TODO handle gender_id
        mysql.connection.commit()

    elif request.method == 'POST':

        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'

    # Show new profile form with message (if any)
    return render_template('complete_profile.html', msg=msg)


# ------------------------------------------------------------------- http://localhost:5001/home --

@app.route('/home')
def home():
    ''' home page
    '''

    # Check if user is loggedin
    if 'loggedin' in session:

        # Check if user profile is complete
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE id = %s', (session['id'],)) # get from cookie
        user = cursor.fetchone()

        # redirect to complete profile if profile is not complete
        if user['first_name'] == 0:
            return redirect(url_for('complete_profile'))

        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
       
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# ---------------------------------------------------------------- http://localhost:5001/profile --

@app.route('/profile')
def profile():
    ''' profile page
    '''

    # Check if user is loggedin
    if 'loggedin' in session:

        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()

        # Show the profile page with account info
        return render_template('profile.html', account=account)
    
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


######################
# ADD NEW PAGES HERE #
######################


# ----------------------------------------------------------------------------------------- main --

if __name__ == '__main__':
    app.run(host='localhost', port=5001)
