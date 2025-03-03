from flask import request, render_template, Flask, redirect, url_for, session, flash
import psycopg2 as postgres

app = Flask(__name__, static_folder="assets")

def get_db_connection():
    return postgres.connect(
        database="libsnap", user="postgres", password="root", port=5432, host="localhost"
    )


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        roll_number = request.form['roll_number']
        email = request.form['email']
        password = request.form['password']
        table_query = '''
         CREATE TABLE IF NOT EXISTS new_users (
            roll_number VARCHAR(30) NOT NULL,
            email VARCHAR(100),
            password VARCHAR(100)
        )'''
        cursor.execute(table_query)
        sql_query = '''INSERT INTO new_users (roll_number, email, password) VALUES (%s, %s, %s)'''
        cursor.execute(sql_query, (roll_number, email, password))
        print("Success!")
        conn.commit()
        cursor.close()
        return redirect(url_for('login'))

    return render_template('index.html')

@app.route("/login", methods = ['GET', 'POST'])    
def login():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        roll_number = request.form['roll_number']
        email = request.form['email']
        password = request.form['password']
        login_query = '''SELECT roll_number, email, password from new_users where roll_number = %s AND email = %s AND password = %s '''
        cursor.execute(login_query, (roll_number, email, password))
        result = cursor.fetchone()

        if result:
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run()

