''' A flask implementation of a database-connected website

    Developed by:
        Sidney Raabe
        Dennis Saralino
        Ryan Smith
        Eric Stauss
        Erik Zavarelli

    For:
        CS 33007 Database Systems
        Summer 2023
        Kent State University
'''

import re
from logging.config import dictConfig
from flask_mysqldb import MySQL
import MySQLdb.cursors
from static.passwordhash import hash_sha256 # custom hashing functions for passwords
from flask import Flask, render_template, request, redirect, url_for, session

# Configure application logging

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

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
    app.logger.info('index: user at index page')

    # Check if user is loggedin
    if 'loggedin' in session:

        # User is loggedin show them the home page
        app.logger.info('index: user rerouted to home page')
        return redirect(url_for('home'))

    # User is not loggedin redirect to login page
    app.logger.info('index: user rerouted to login page')
    return redirect(url_for('login'))


# ------------------------------------------------------------------ http://localhost:5001/login --

@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' login page
    '''
    app.logger.info('login: user at login page')

    # Output message if something goes wrong...
    msg = ''

    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        app.logger.info('login: user submitted good login form')

        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM access_control WHERE username = %s', (username,))
        app.logger.info('login: access_control queried for username')

        # Fetch one record and return result
        account = cursor.fetchone()
        app.logger.info('login: access_control returned USER: '\
                        '%s PASSWORD: %s', account['username'], account['cipher_pw'])

        # Check if an account was returned and if the password hash matches the recalculated hash
        if account:

            app.logger.info('login: account found, checking password')

            hash_check, salt_check = hash_sha256(password, account['salt'], 100)
            app.logger.info('hash_sha256: HASHED PASSWORD: %s', hash_check)
            app.logger.info('hash_sha256: SALT: %s', salt_check)

            if hash_check == account['cipher_pw']:

                app.logger.info('login: password matches, logging in')

                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['user_ID']
                session['username'] = account['username']
                app.logger.info('login: session information created: USERNAME: %s, ID: %s',
                                session['username'], session['id'])

                # Redirect to home page
                app.logger.info('login: user rerouted to home page')
                return redirect(url_for('home'))

        else:
            # Account doesnt exist or username/password incorrect
            app.logger.info('login: account not found or password incorrect')
            msg = 'Incorrect username/password!'

    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)


# ----------------------------------------------------------------- http://localhost:5001/logout --

@app.route('/logout')
def logout():
    ''' logout page
    '''
    app.logger.info('logout: user at logout page')

    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    # Redirect to login page
    app.logger.info('logout: user logged out and rerouted to login page')
    return redirect(url_for('login'))


# --------------------------------------------------------------- http://localhost:5001/register --

@app.route('/register', methods=['GET', 'POST'])
def register():
    ''' registration page
    '''
    app.logger.info('register: user at registration page')

    # Output message if something goes wrong...
    msg = ''

    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        app.logger.info('register: user submitted good registration form')

        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']


        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM access_control WHERE username = %s', (username,))
        account = cursor.fetchone()
        app.logger.info('register: access_control returned USER: '\
                        '%s', account['username'])

        # If account exists show error and validation checks
        if account:

            app.logger.info('register: account already exists')
            msg = 'Account already exists!'


        elif not re.match(r'[A-Za-z0-9]+', username):

            app.logger.info('register: username contains invalid characters')
            msg = 'Username must contain only characters and numbers!'

        elif not username or not password:

            app.logger.info('register: username or password is empty')
            msg = 'Please fill out the form!'

        else:

            # hash the password
            hashed_pw, salt = hash_sha256(password, rounds=100)
            app.logger.info('hash_sha256: HASHED PASSWORD: %s', hashed_pw)
            app.logger.info('hash_sha256: SALT: %s', salt)

            # Insert new user into access_control table

            # First insert a new empty user into the user table to get a user_ID
            cursor.execute('INSERT INTO user VALUES \
                           (NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)')
            app.logger.info('register: new user inserted into user table')

            # Get the auto generated user_ID from the user table
            cursor.execute('SELECT * FROM user WHERE user_id = LAST_INSERT_ID()')
            new_user = cursor.fetchone()
            app.logger.info('register: user returned USER: '\
                            '%s', new_user['username'])

            # Insert the new user into the access_control table using the generated user_ID
            cursor.execute('INSERT INTO access_control VALUES (%s, %s, %s, %s, %s)',
                           (new_user['user_ID'], username, password, hashed_pw, salt))
            app.logger.info('register: new user inserted into access_control table')
            mysql.connection.commit()
            app.logger.info('register: new user information committed')

            # Create session data to replicate login process
            session['loggedin'] = True
            session['id'] = new_user['user_ID']
            session['username'] = username
            app.logger.info('register: session information created: USERNAME: %s, ID: %s',
                            session['username'], session['id'])

            redirect(url_for('complete_profile'))
            msg = 'You have successfully registered!'


    elif request.method == 'POST':

        # Form is empty... (no POST data)
        app.logger.info('register: user submitted empty form')
        msg = 'Please fill out the form!'

    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


# ------------------------------------------------------- http://localhost:5001/complete_profile --

@app.route('/complete_profile', methods=['GET', 'POST'])
def complete_profile():
    ''' finish up profile details here
    '''
    app.logger.info('complete_profile: user at complete profile page')

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

        app.logger.info('complete_profile: user submitted good complete profile form')

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

        # Check if the gender is new for the table
        cursor.execute ('SELECT * FROM gender WHERE name = %s;', (gender,))
        gender_fetch = cursor.fetchone()

        if not gender_fetch:

            app.logger.info('complete_profile: gender returned no results')
            cursor.execute('INSERT INTO gender VALUES (NULL, %s)', (gender,))
            cursor.execute ('SELECT * FROM gender WHERE name = %s;', (gender,))
            gender_fetch = cursor.fetchone()

        app.logger.info('complete_profile: gender returned %s', gender_fetch)


        # Insert the new user into the access_control table using the generated user_ID
        cursor.execute('UPDATE user SET first_name = %s,\
                                        last_name = %s,\
                                        city = %s,\
                                        state = %s,\
                                        birthday = %s,\
                                        bio = %s,\
                                        gender = %s\
                                        WHERE user_id = %s;',
                    (first_name, last_name, city, state, birthday, bio, 
                     gender_fetch['gender_ID'], session[id]))
        app.logger.info('complete_profile: user profile updated with new information')

        mysql.connection.commit()
        app.logger.info('complete_profile: user profile information committed')

    elif request.method == 'POST':

        # Form is empty... (no POST data)
        app.logger.info('complete_profile: user submitted empty form')
        msg = 'Please fill out the form!'

    # Show new profile form with message (if any)
    return render_template('complete_profile.html', msg=msg)


# ------------------------------------------------------------------- http://localhost:5001/home --

@app.route('/home')
def home():
    ''' home page
    '''
    app.logger.info('home: user at home page')

    # Check if user is loggedin
    if 'loggedin' in session:

        app.logger.info('home: user is logged in')

        # Check if user profile is complete
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE user_id = %s', (session['id'],)) # get from cookie
        user = cursor.fetchone()
        app.logger.info('home: user returned %s', user)

        # redirect to complete profile if profile is not complete
        if user['first_name'] is None or user['last_name'] is None or user['city'] is None \
            or user['state'] is None or user['birthday'] is None or user['bio'] is None:

            app.logger.info('home: user profile is not complete, redirecting to complete profile')
            return redirect(url_for('complete_profile'))

        # User is loggedin show them the home page
        app.logger.info('home: user profile is complete, showing home page')
        return render_template('home.html', username=session['username'])

    # User is not loggedin redirect to login page
    app.logger.info('home: user is not logged in, redirecting to login page')
    return redirect(url_for('login'))


# ---------------------------------------------------------------- http://localhost:5001/profile --

@app.route('/profile')
def profile():
    ''' profile page
    '''
    app.logger.info('profile: user at profile page')

    # Check if user is loggedin
    if 'loggedin' in session:

        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM access_control WHERE user_id = %s', (session['id'],))
        account = cursor.fetchone()
        app.logger.info('profile: access_control returned USER: '\
                        '%s PASSWORD: %s', account['username'], account['cipher_pw'])

        # Show the profile page with account info
        return render_template('profile.html', account=account)

    # User is not loggedin redirect to login page
    app.logger.info('profile: user is not logged in, redirecting to login page')
    return redirect(url_for('login'))


########################
## ADD NEW PAGES HERE ##
########################

@app.route('/newpage')
def newpage():
    ''' describe the function of the page
    '''


# ----------------------------------------------------------------------------------------- main --

if __name__ == '__main__':
    app.run(host='localhost', port=5001)