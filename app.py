from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = "kwusecret123"

# ================= Database Connection =================
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',       # ganti sesuai MySQL
        password='',       # ganti sesuai MySQL
        database='scholar'
    )
    return conn

# ================= Login Required =================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ================= Routes =================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username,email,password) VALUES (%s,%s,%s)",
                           (username,email,password))
            conn.commit()
            flash("Registration successful! Please login.", 'success')
            return redirect(url_for('login'))
        except:
            flash("Username or email already exists.", 'danger')
        finally:
            cursor.close()
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username,password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_premium'] = user['is_premium']
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials.", 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ================= Dashboard =================
@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE user_id=%s", (session['user_id'],))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()

    if request.method == 'POST':
        title = request.form['title']
        deadline = request.form['deadline']
        sks = int(request.form['sks'])
        jenis = request.form['jenis']
        estimasi = int(request.form['estimasi'])
        
        # Auto Priority Engine
        now = datetime.now()
        delta_days = (datetime.strptime(deadline,"%Y-%m-%d") - now).days
        priority = '🟢 Santai'
        if delta_days <=1 or sks >=3 or jenis.lower() in ['uts','uas']:
            priority = '🔴 Mendesak'
        elif delta_days <=3:
            priority = '🟡 Sedang'
        
        # Insert task
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (user_id,title,deadline,sks,jenis,estimasi_waktu,priority) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                       (session['user_id'],title,deadline,sks,jenis,estimasi,priority))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Task added!", 'success')
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', tasks=tasks, is_premium=session['is_premium'])

# ================= Upgrade =================
@app.route('/upgrade', methods=['GET','POST'])
@login_required
def upgrade():
    if request.method == 'POST':
        # Dummy payment: langsung upgrade
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_premium=1 WHERE id=%s", (session['user_id'],))
        conn.commit()
        cursor.close()
        conn.close()
        session['is_premium'] = 1
        flash("Payment successful! You are now Premium.",'success')
        return redirect(url_for('dashboard'))
    return render_template('upgrade.html')

# ================= Delete Task =================
@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=%s AND user_id=%s", (task_id, session['user_id']))
    conn.commit()
    cursor.close()
    conn.close()
    return "Deleted"

# ================= Edit Task =================
@app.route('/edit_task/<int:task_id>', methods=['POST'])
@login_required
def edit_task(task_id):
    data = request.get_json()
    title = data.get("title")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title=%s WHERE id=%s AND user_id=%s", (title, task_id, session['user_id']))
    conn.commit()
    cursor.close()
    conn.close()
    return "Updated"


if __name__ == '__main__':
    app.run(debug=True)
