from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3



# =========================
# CREATING THE APPOINTMENTS DATABASE
# =========================
def create_appointments_database():
    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_name TEXT NOT NULL,
            dog_name TEXT NOT NULL,
            service TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()



# =========================
# CREATING THE USERS DATABASE
# =========================
def create_users_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''') 
    conn.commit()
    conn.close()      



# =========================
# SETTING UP THE FLASK APP
# =========================
app = Flask(__name__)
app.secret_key = "supersecretkey123" # Secret key for session management and flash messages




# =========================
# ROUTES
# =========================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    # Creating a function to handle the appointments
    if request.method == 'POST':  # Ensures the user is logged in
        if 'username' not in session:
            flash("Please log in to book an appointment.", "error")
            return redirect(url_for('login'))

        # Collecting data from the form
        owner = request.form['owner_name']
        dog = request.form['dog_name']
        service = request.form['service']
        date = request.form['date']
        time = request.form['time']
        phone = request.form['phone']

        try:
            # Connect to the appointments database
            conn = sqlite3.connect('appointments.db')
            cursor = conn.cursor()

            # Check if the selected date/time is already booked
            cursor.execute('SELECT * FROM appointments WHERE date=? AND time=?', (date, time))
            existing = cursor.fetchone()

            if existing:
                flash("Sorry, this date and time is already booked.", "error")
                conn.close()
                return redirect(url_for('appointments'))

            # Insert a new appointment
            cursor.execute('''
                INSERT INTO appointments (owner_name, dog_name, service, date, time, phone)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (owner, dog, service, date, time, phone))
            conn.commit()
            conn.close()

            flash("Appointment booked successfully!", "success")
            return redirect(url_for('display_page'))

        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for('appointments'))

    return render_template('appointments.html')


@app.route('/delete_appointment/<int:appointment_id>', methods=['POST'])
# Creating a function to delete a specific appointment by its ID
def delete_appointment(appointment_id):
    # Only logged in users can do this
    if 'username' not in session:
        flash("You must be logged in to delete an appointment.", "error")
        return redirect(url_for('login'))

    try:
        conn = sqlite3.connect('appointments.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM appointments WHERE id=?', (appointment_id,))
        conn.commit()
        conn.close()

        flash(f"Appointment {appointment_id} deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting appointment: {e}", "error")

    return redirect(url_for('display_page'))



# =========================
# LOGIN & REGISTRATION
# =========================
@app.route('/login', methods=['GET', 'POST'])
# Creating a log in function to get and post user inputs
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check the user information in the user database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            # Store the username in the session
            session['username'] = username
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/register', methods=['POST'])
# Creating a register function to add new users to the database
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (first_name, last_name, username, password, email)
            VALUES (?, ?, ?, ?, ?)
        ''', (first_name, last_name, username, password, email))
        conn.commit()
        conn.close()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    except sqlite3.IntegrityError:
        flash("Username already exists. Please choose a different one.", "error")
        return redirect(url_for('login'))

@app.route('/logout')
# Creating a function to log out by clearing the session
def logout():
    session.pop('username', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/display_page')
# Creatig a display function to display all the appointments and registered users to Mr. Boitumelu
def display_page():

    # Fetch the appointments from the appointments database
    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM appointments ORDER BY date, time')
    appointments = cursor.fetchall()
    conn.close()

    # Fetch the registered users from the users database
    conn_users = sqlite3.connect('users.db')
    cursor_users = conn_users.cursor()
    cursor_users.execute('SELECT * FROM users ORDER BY id')
    users = cursor_users.fetchall()
    conn_users.close()

    return render_template('display_page.html', appointments=appointments, users=users)



# =========================
# EDIT ACCOUNT
# =========================
@app.route('/edit_account', methods=['GET', 'POST'])
# Creating an edit function for logged in users to edit their account
def edit_account():
    if 'username' not in session:
        flash("You must be logged in to edit your account.", "error")
        return redirect(url_for('login'))

    username = session['username']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Collect updated info from the form
    if request.method == 'POST':
        # Get updated info from form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        email = request.form['email']

        try:
            cursor.execute('''
                UPDATE users
                SET first_name=?, last_name=?, password=?, email=?
                WHERE username=?
            ''', (first_name, last_name, password, email, username))
            conn.commit()
            flash("Your account has been updated.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for('edit_account'))
    
    # GET request fetches current user info
    cursor.execute('SELECT first_name, last_name, username, email FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    conn.close()
    return render_template('edit_account.html', user=user)



# =========================
# DELETE ACCOUNT
# =========================
@app.route('/delete_account', methods=['POST'])
# Creating a function to delete a user's account
# The user must be logged in to be able to do this
def delete_account():
    if 'username' not in session:
        flash("You must be logged in to delete your account.", "error")
        return redirect(url_for('login'))

    username = session['username']

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE username=?', (username,))
        conn.commit()
        conn.close()

        # Log the user out after deleting the account
        session.pop('username', None)
        flash("Your account has been deleted.", "success")
        return redirect(url_for('home'))
    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        return redirect(url_for('login'))



# =========================
# RUN THE APP
# =========================
if __name__ == "__main__":
    # Making sure the databases exist before running the app
    create_appointments_database()
    create_users_database()
    app.run(debug=True)