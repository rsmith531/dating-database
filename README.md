# Dating Database
A group project for KSU Summer 2023 Database Design course. It uses MySQL as a DBMS to enable a front end web dating application.

## How to get this project to run on your machine

### Create a personal access token for your Github account
- Check this [Github Article](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) to create a personal access token.
- Make sure to write down the token before you navigate away from the page.

### Establish a connection to dbdev with an SSH tunnel
- Open a command line.
- `ssh (yourusername)@dbdev.cs.kent.edu -L :5001:localhost:5001`
- Accept the host authenticity if necessary.
- Enter Flashline password.

### Clone the repo into your public_html folder
- `git clone https://github.com/rsmith531/dating-database.git`
- Enter your Github account username and personal access token.
-`cd dating-database`
- If you need to check out a remote branch you are working in:
    - `git checkout --track origin/(your branch name)`

### Run the Flask server
- `cd flask`
- `./main.py`