# Zendesk Product Security (Submission by Keith Sim)
### The Zendesk Product Security Challenge

**To try out my solution, there are two possible methods to do so:**
1. If you're using a windows or linux machine, grab the respective binary in my releases page!
2. If you're using linux machine, you can build it by reading the following steps below. 

**Building on Linux**

*Prerequisites: git, python3.X, pip, python3-venv*

1. Clone the repo to your desired directory
2. Run: `python3 -m venv venv`
3. Run: `venv/bin/pip install -r requirements.txt` 
4. Run: `venv/bin/pyinstaller -F --add-data "project:project" --add-data "migrations:migrations" --add-binary "project.db;."  zendesksol.py`
5. Your binary file can now be found in the `dist/` folder!

## Running the binary
Once the binary has been started, simply visit localhost:5555 to view the welcome page. 
From there you can try to login, register a new user, reset your password, or logout.


To test out the fetures, a sample database with two users have been implemented. 
1. **Username**: admin, **Password**: password 
2. **Username**: user2, **Password**: tesr (Note: this account is currently locked out and needs to have their password reset (use email of ZDSecSolKS@gmail.com))

Note that the database will be reset everytime the binary is restarted!

## The following features have been implemented

#### 1. Input sanitization and validation
Implemented with flask's inbuilt render_template which automatically handles sanitization.
New users must have usernames of length 3 and passwords of legnth 8 with at least 1 number, 1 letter, 1 special character with no whitespaces.

#### 2. Password hashed
Implemented with Flask-Bcrypt, salting 15 rounds. 

#### 3. Logging
Implemented with flask's inbuilt logger. Creates a log file if it doesn't exist and logs information about the program, rotating once it hits a size limit of around 20MB.

#### 4. CSRF prevention
Implemented with WTForms. A hidden token has been implemented on every page where user input is allowed.

#### 5. Password reset / forget password mechanism
Implemented with `jwt`. At the login page, there's a link to submit a user's email to reset their password. A reset email will be sent to that email if it belongs to that user where they can use a token to reset their password.

#### 6. Account lockout
After a user has failed to login 5 times, they will be locked out and must reset their password to log back in.

#### 7. Cookie
Implemented with session from Flask. Closing the site and opening it back up will still show the logged in page if user is logged in.

Thank you!
