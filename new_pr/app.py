import io
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib
import pickle
import numpy as np
from ml_gps import send_email



app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
model = pickle.load(open("model.pkl", "rb"))


# Function to create a connection to the SQLite database
def create_connection():
    conn = sqlite3.connect('users.db')
    return conn

# Function to create a table for storing user information
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       email TEXT UNIQUE,
                       password TEXT)''')
    conn.commit()
    conn.close()

# Create the users table when the application starts
create_table()

@app.route('/')
def index():
    if 'email' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Insert user data into the database
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password_hash))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('signup.html', error="Email already exists. Please use a different email.")
    
    # Render the signup page for GET requests
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Check if the user exists in the database and the password is correct
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password_hash))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # If the user exists and the password is correct, set the session variable and redirect to the home page
            session['email'] = email
            return redirect(url_for('index'))
        else:
            # If the user doesn't exist or the password is incorrect, render the login page again with an error message
            return render_template('login.html', error="Invalid email or password. Please try again.")
    
    # Render the login page for GET requests
    return render_template('login.html')


@app.route("/predict", methods = ["POST"])
def predict():
    file = request.files['file']
    features = np.load(io.BytesIO(file.read()))
    features=features.reshape(1, 19*500)
    prediction = model.predict(features)
    pred_text =""

    if prediction == 0:
        pred_text = "normal"
    else:
        pred_text = "abnormal"
        #send_email(100,100)

    return render_template("index.html", prediction_text = "The EEG is {}".format(pred_text))

if __name__ == '__main__':
    app.run(debug=True)
