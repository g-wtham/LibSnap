from flask import request, render_template, Flask, redirect, url_for, session
import psycopg2 as postgres

app = Flask(__name__, static_folder="assets")
app.secret_key = 'libsnap_database_updates'

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
        password = request.form['password']
        login_query = '''SELECT roll_number, email, password from new_users where roll_number = %s AND password = %s '''
        cursor.execute(login_query, (roll_number, password))
        result = cursor.fetchone()

        if result:
            session['roll_number'] = result[0]
            session['email'] = result[1]
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route("/dashboard")
def dashboard():
    if 'roll_number' not in session:
        return redirect(url_for('login')) # should RETURN the redirected url
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    roll_number_session = session['roll_number']
    email_session = session['email']
    
    sql_query_session = '''SELECT DISTINCT title, authors from scanned_records WHERE roll_number = %s '''
    cursor.execute(sql_query_session, (roll_number_session, ))
    result = cursor.fetchall()
    print(result) 
    conn.commit()
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', roll_num=roll_number_session, book_data=result, user_email = email_session )

if __name__ == '__main__':
    app.run()