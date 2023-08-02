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
from datetime import date
from socket import gethostname
from flask_mysqldb import MySQL
import MySQLdb.cursors
from static.passwordhash import hash_sha256 # custom hashing functions for passwords
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'dating database'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'rsmit216'
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

        # Check if an account was returned and if the password hash matches the recalculated hash
        if account:

            app.logger.info('login: access_control returned USER: '\
                        '%s PASSWORD: %s', account['username'], account['cipher_pw'])

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

            app.logger.info('register: account does not exist, creating new account')

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
            app.logger.info('register: user returned: %s', new_user['user_ID'])

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

            msg = 'You have successfully registered!'
            return redirect(url_for('complete_profile'))


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
    
    # get states and genders to populate dropdowns, hobbies to populate checkboxes
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM state')
    states = cursor.fetchall()
    cursor.execute('SELECT * FROM gender')
    genders = cursor.fetchall()
    cursor.execute('SELECT * FROM hobbies')
    hobbies = cursor.fetchall()
    app.logger.info('all hobbies: %s', hobbies)
    cursor.execute('SELECT * FROM hobby_interests WHERE user_ID = %s;', (session['id'],))
    user_hobbies = cursor.fetchall()
    app.logger.info('user hobbies: %s', user_hobbies)
    

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
        state = request.form['state']
        birthday = request.form['birthday']                    # TODO make this a calendar selector
        bio = request.form['bio']
        gender = request.form['gender']
        user_hobbies = request.form.getlist('hobbies')

        app.logger.info('UPDATED HOBBIES: %s', user_hobbies)


        # query to update user with profile information
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)


        # Insert the new user into the access_control table using the generated user_ID
        query = 'UPDATE user SET first_name = %s, '\
                                        'last_name = %s, '\
                                        'city = %s, '\
                                        'state = %s, '\
                                        'birthday = %s, '\
                                        'bio = %s, '\
                                        'gender_ID = %s '\
                                        'WHERE user_ID = %s'
        params = (first_name, last_name, city, state, birthday, bio,
                  gender, session['id'])
        app.logger.info('complete_profile: query: %s', (query, params))


        cursor.execute(query, params)
        app.logger.info('complete_profile: user profile updated with new information')


        # Delete and re-add all existing user hobbies
        cursor.execute('DELETE FROM hobby_interests WHERE user_ID = %s;', (session['id'],))

        for h in user_hobbies:
            query = 'INSERT INTO hobby_interests (user_ID, hobby_name) VALUES (%s, %s)'
            params = (session['id'], h)
            cursor.execute(query, params)


        mysql.connection.commit()
        app.logger.info('complete_profile: user profile information committed')
        return redirect(url_for('home'))

    elif request.method == 'POST':

        # Form is empty... (no POST data)
        app.logger.info('complete_profile: user submitted empty form')
        msg = 'Please fill out the form!'

    # Get existing data from user database
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE user_ID = %s', (session['id'],))
    user = cursor.fetchone()
    app.logger.info('complete_profile: user returned %s', user)

    if user['gender_ID'] is not None:

        # Get the user's gender from gender_ID
        app.logger.info('complete_profile.')
        # Show new profile form with message (if any)
        return render_template('complete_profile.html', \
                                msg=msg, user=user, states=states, genders=genders, hobbies=hobbies, user_hobbies=user_hobbies)

    user = None

    # Show new profile form with message (if any)
    return render_template('complete_profile.html', \
                           msg=msg, user=user, states=states, genders=genders, hobbies=hobbies, user_hobbies=user_hobbies)


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

        # Get the user's account details from the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM access_control WHERE user_ID = %s', (session['id'],))
        account = cursor.fetchone()
        app.logger.info('profile: access_control returned USER: '\
                        '%s PASSWORD: %s', account['username'], account['cipher_pw'])

        # Get the user's profile details from the database
        cursor.execute('SELECT * FROM user WHERE user_ID = %s', (session['id'],))
        profile_results = cursor.fetchone()
        app.logger.info('profile: user returned %s', profile_results)

        # Calculate the user's age from their birthday
        days_in_year = 365.2425
        age_calc = int((date.today() - profile_results['birthday']).days / days_in_year)

        # Get the user's gender from gender_ID
        cursor.execute('SELECT * FROM gender WHERE gender_ID = %s', (profile_results['gender_ID'],))
        gender_results = cursor.fetchone()

        # Get all user's hobbies
        cursor.execute('SELECT hobby_name FROM hobby_interests WHERE hobby_interests.user_ID = %s', (session['id'],))
        hobbies_results = cursor.fetchall()
        app.logger.info('profile: user hobbies returned %s', hobbies_results)

        # Show the profile page with account info
        return render_template('profile.html', account=account, profile=profile_results, \
                               age=age_calc, gender=gender_results['name'], hobbies=hobbies_results)

    # User is not loggedin redirect to login page
    app.logger.info('profile: user is not logged in, redirecting to login page')
    return redirect(url_for('login'))


# -------------------------------------------------------- http://localhost:5001/change_password --

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    ''' for updating the user's password
    '''
    app.logger.info('change_password: user at change password page')

    # Output message if something goes wrong...
    msg = ''

    # Check if user is loggedin
    if 'loggedin' not in session:

        # User is not loggedin redirect to login page
        app.logger.info('change_password: user is not logged in, redirecting to login page')
        return redirect(url_for('login'))

    if request.method == 'POST' and 'old_pw' in request.form\
        and 'new_pw_1' in request.form\
            and 'new_pw_2' in request.form:

        app.logger.info('change_password: user submitted good change_password form')

        # Create variables for easy access
        old_pw = request.form['old_pw']
        new_pw_1 = request.form['new_pw_1']
        new_pw_2 = request.form['new_pw_2']

        # Check if new password matches the repeated new password
        if new_pw_1 != new_pw_2:

            app.logger.info('change_password: new passwords do not match')
            msg = 'New passwords do not match!'
            return render_template('change_password.html', msg=msg)

        # Get account details from the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM access_control WHERE user_ID = %s', (session['id'],))
        account = cursor.fetchone()

        # Check if the old password matches the stored password
        hash_check, salt_check = hash_sha256(old_pw, account['salt'], 100)
        app.logger.info('hash_sha256: HASHED PASSWORD: %s', hash_check)
        app.logger.info('hash_sha256: SALT: %s', salt_check)
        if hash_check != account['cipher_pw']:

            app.logger.info('change_password: old password does not match')
            msg = 'Password change could not be completed'
            return render_template('change_password.html', msg=msg)

        # hash the new password and update the database
        hashed_pw, salt = hash_sha256(new_pw_1, rounds=100)
        app.logger.info('hash_sha256: HASHED PASSWORD: %s', hashed_pw)
        app.logger.info('hash_sha_256: SALT: %s', salt)
        cursor.execute('UPDATE access_control SET clear_pw = %s, \
                    cipher_pw = %s, salt = %s \
                    WHERE user_ID = %s',
                        (new_pw_1, hashed_pw, salt, session['id']))
        mysql.connection.commit()
        app.logger.info('change_password: password updated in database')
        msg = 'Password changed successfully!'

    return render_template('change_password.html', msg=msg)


# --------------------------------------------------------- http://localhost:5001/delete_account --

@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    ''' This page lets you delete your account
    '''
    app.logger.info('delete_account: user at delete account page')

    # Output message if something goes wrong...
    msg = ''

    # Check if user is loggedin
    if 'loggedin' not in session:

        # User is not loggedin redirect to login page
        app.logger.info('delete_account: user is not logged in, redirecting to login page')
        return redirect(url_for('login'))

    # Check if the form is fully completed
    if request.method == 'POST' and 'password' in request.form:

        # Create variables for easy access
        password = request.form['password']

        # Get account details from the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM access_control WHERE user_ID = %s', (session['id'],))
        account = cursor.fetchone()

        # Check if the old password matches the stored password
        hash_check, salt_check = hash_sha256(password, account['salt'], 100)
        app.logger.info('hash_sha256: HASHED PASSWORD: %s', hash_check)
        app.logger.info('hash_sha256: SALT: %s', salt_check)
        if hash_check != account['cipher_pw']:

            app.logger.info('delete_account: password does not match')
            msg = 'This account could not be deleted'
            return render_template('delete_account.html', msg=msg)

        # Delete the user from the database
        cursor.execute('DELETE FROM access_control WHERE user_ID = %s', (session['id'],))
        cursor.execute('DELETE FROM user WHERE user_ID = %s', (session['id'],))
        # TODO I think this won't delete items from misc tables. Maybe CASCADING keyword?
        mysql.connection.commit()
        app.logger.info('delete_account: user deleted from database')
        return redirect(url_for('logout'))

    return render_template('delete_account.html', msg=msg)


# ----------------------------------------------------------------- http://localhost:5001/browse --

@app.route('/browse', methods=['GET', 'POST'])
def browse():
    ''' browse potential matches for the logged-in user
    '''
    app.logger.info('browse: user at browse page')

    # Check if user is logged in
    if 'loggedin' in session:

        # create cursor to interact with DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if request.method == 'POST':
            # updates status
            cursor.execute("""
                INSERT INTO user_interaction 
                (user_ID_1, user_ID_2, status) VALUES (%s, %s, %s)
            """, (session['id'], request.form['user_id'], request.form['status']))
            mysql.connection.commit()

        # Query to get users that have not been interacted with
        cursor.execute("""
            SELECT user_ID, first_name, last_name, TIMESTAMPDIFF(YEAR, birthday, CURDATE()) AS age, city, state
            FROM user
            WHERE user_ID NOT IN (
                SELECT user_ID_2 FROM user_interaction WHERE user_ID_1 = %s
            ) AND user_ID NOT IN (
                SELECT user_ID_1 FROM user_interaction WHERE user_ID_2 = %s AND status = 'block'
            )
            LIMIT 1
        """, (session['id'], session['id'],))

        # Fetch one record and return result
        user = cursor.fetchone()

        if user:
            return render_template('browse.html', user=user)
        else:
            return render_template('browse.html')

    # User is not loggedin redirect to login page
    app.logger.info('browse: user rerouted to login page')
    return redirect(url_for('login'))


# ---------------------------------------------------------------- http://localhost:5001/matches1 --

@app.route('/matches1')
def matches1():
    ''' This page allows you to view your matches
    '''
    app.logger.info('home: user at matches page')

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

        # Query database for matches
        cursor.execute('SELECT user_ID_2 AS user_ID FROM user_interaction ' \
               'WHERE status LIKE \'like\' AND user_ID_1 = %s ' \
               'INTERSECT ' \
               'SELECT user_ID_1 AS user_ID FROM user_interaction ' \
               'WHERE status LIKE \'like\' AND user_ID_2 = %s;', (session['id'], session['id'],))
        match_userIDs = cursor.fetchall()
        app.logger.info('match query returned %s', match_userIDs)

        # Query database for matched user info
        matches_info = []
        for match_userID in match_userIDs:
            user_ID = match_userID['user_ID']
            cursor.execute('SELECT user.*, user_email.email FROM user ' \
               'LEFT JOIN user_email ON user.user_ID = user_email.user_ID ' \
               'WHERE user.user_ID = %s', (user_ID,))
            matched_user = cursor.fetchone()
            if matched_user:
                matches_info.append(matched_user)
        app.logger.info('matches info: %s', matches_info)

        # User is loggedin, show the matched page
        app.logger.info('home: user profile is complete, matches page')
        return render_template('matches1.html', username=session['username'], matches_info = matches_info)
    

    # User is not loggedin redirect to login page
    app.logger.info('home: user is not logged in, redirecting to login page')
    return redirect(url_for('login'))


# ---------------------------------------------------------------- http://localhost:5001/matches2 --

@app.route('/matches2')
def matches2():
    ''' show matches for the logged-in user
    '''
    app.logger.info('matches: user at matches page')

    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the matches page

        # create cursor to interact with MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Query to get the matches 
        cursor.execute("""
            SELECT 
            U.user_ID, U.first_name, U.last_name, 
            TIMESTAMPDIFF(YEAR, U.birthday, CURDATE()) AS age, 
            U.city, U.state 
            FROM 
            user_interaction I1 
            INNER JOIN 
            user_interaction I2 
            ON I1.user_ID_1 = I2.user_ID_2 AND I1.user_ID_2 = I2.user_ID_1 
            INNER JOIN 
            user U 
            ON U.user_ID = I1.user_ID_2 
            WHERE 
            I1.user_ID_1 = %s AND I1.status = 'like' AND I2.status = 'like'
        """, (session['id'],))


        # Fetch all records and return result
        matches = cursor.fetchall()

        return render_template('matches2.html', matches=matches)

    # User is not loggedin redirect to login page
    app.logger.info('matches: user rerouted to login page')
    return redirect(url_for('login'))


# ---------------------------------------------------------------- http://localhost:5001/unmatch --

@app.route('/unmatch/<int:user_id>', methods=['POST'])
def unmatch(user_id):
    ''' unmatch a user
    '''
    app.logger.info('unmatch: user attempting to unmatch')

    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin perform the unmatch

        # create cursor to interact with MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Query to update the user_interaction status 
        cursor.execute("""
            UPDATE user_interaction
            SET status = 'dislike'
            WHERE (user_ID_1 = %s AND user_ID_2 = %s) OR (user_ID_1 = %s AND user_ID_2 = %s)
        """, (session['id'], user_id, user_id, session['id'],))

        # Commit the transaction
        mysql.connection.commit()

        app.logger.info('unmatch: user successfully unmatched')
        return redirect(url_for('matches'))

    # User is not loggedin redirect to login page
    app.logger.info('unmatch: user rerouted to login page')
    return redirect(url_for('login'))


########################
## ADD NEW PAGES HERE ##
########################

# ---------------------------------------------------------------- http://localhost:5001/newpage --

@app.route('/newpage')
def newpage():
    ''' describe the function of the page
    '''
    app.logger.info('newpage: user at new page')
    return redirect(url_for('home'))


# ----------------------------------------------------------------------------------------- main --

if __name__ == '__main__':
    if 'liveconsole' not in gethostname():
        app.run(host='localhost', port=5010, debug=True)
