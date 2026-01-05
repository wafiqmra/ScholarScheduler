from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from functools import wraps
from datetime import datetime, timedelta
from collections import defaultdict

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
    cursor.execute("""
        SELECT t.*, c.course_name 
        FROM tasks t
        JOIN courses c ON t.course_id = c.id
        WHERE t.user_id=%s
        ORDER BY c.course_name, t.deadline
    """, (session['user_id'],))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()

    # =================== Collision Detection ===================
    warning_msg = ""
    week_counter = {}

    for task in tasks:
        dt = task['deadline']  # sudah datetime.date dari MySQL
        # convert ke datetime supaya bisa .isocalendar()
        if isinstance(dt, datetime):
            dt_obj = dt
        else:
            dt_obj = datetime.combine(dt, datetime.min.time())
        year, week, _ = dt_obj.isocalendar()
        key = f"{year}-{week}"
        week_counter[key] = week_counter.get(key, 0) + 1

    # Cek minggu ini
    now = datetime.now()
    current_week_key = f"{now.isocalendar()[0]}-{now.isocalendar()[1]}"
    if week_counter.get(current_week_key, 0) > 2:  # threshold >2
        warning_msg = "⚠️ Minggu ini overload"


    # =================== Handle Add Task ===================
    if request.method == 'POST':
        title = request.form['title']
        deadline = request.form['deadline']
        sks = int(request.form['sks'])
        jenis = request.form['jenis']
        estimasi = int(request.form['estimasi'])
        
        # Auto Priority Engine
        32
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
    # =================== Group Tasks by Course ===================
    grouped_tasks = defaultdict(list)
    for task in tasks:
        grouped_tasks[task['course_name']].append(task)

    # =================== Stress Indicator ===================
    stress_score = 0

    # task minggu ini
    start_week = now - timedelta(days=now.weekday())
    end_week = start_week + timedelta(days=6)

    weekly_tasks = [
        t for t in tasks
        if start_week.date() <= t['deadline'] <= end_week.date()
    ]

    # 1. jumlah task
    stress_score += len(weekly_tasks) * 2

    # 2. estimasi waktu
    total_hours = sum(t['estimasi_waktu'] for t in weekly_tasks)
    stress_score += total_hours

    # 3. task berat
    for t in weekly_tasks:
        if t['jenis'].lower() in ['uts', 'uas']:
            stress_score += 5
        if t['sks'] >= 3:
            stress_score += 3

    # Tentukan level
    stress_level = "Low"
    stress_color = "green"

    if stress_score >= 25:
        stress_level = "High"
        stress_color = "red"
    elif stress_score >= 15:
        stress_level = "Medium"
        stress_color = "orange"


    return render_template(
        'dashboard.html',
        tasks=tasks,
        grouped_tasks=grouped_tasks,
        is_premium=session['is_premium'],
        warning_msg=warning_msg,
        stress_level=stress_level,
        stress_color=stress_color,
        stress_score=stress_score
)


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

@app.route('/weekly-planner')
@login_required
def weekly_planner():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # kapasitas user
    cursor.execute(
        "SELECT daily_hours FROM weekly_capacity WHERE user_id=%s",
        (session['user_id'],)
    )
    cap = cursor.fetchone()
    daily_hours = cap['daily_hours'] if cap else 2

    # task minggu ini
    start_week = datetime.now() - timedelta(days=datetime.now().weekday())
    end_week = start_week + timedelta(days=6)

    cursor.execute("""
        SELECT * FROM tasks 
        WHERE user_id=%s 
        AND deadline BETWEEN %s AND %s
        ORDER BY priority DESC
    """, (session['user_id'], start_week.date(), end_week.date()))

    tasks = cursor.fetchall()
    cursor.close()
    conn.close()

    total_task_hours = sum(t['estimasi_waktu'] for t in tasks)
    weekly_capacity = daily_hours * 7
    remaining = weekly_capacity - total_task_hours

    # ======== Bagi tugas ke hari ========
    planner = {day: [] for day in range(7)}
    day_pointer = 0
    remaining_daily = daily_hours

    for task in tasks:
        hours = task['estimasi_waktu']
        while hours > 0:
            if remaining_daily == 0:
                day_pointer += 1
                remaining_daily = daily_hours
            if day_pointer > 6:
                break

            planner[day_pointer].append(task['title'])
            remaining_daily -= 1
            hours -= 1

    return render_template(
        "weekly_planner.html",
        planner=planner,
        remaining=remaining,
        weekly_capacity=weekly_capacity,
        total_task_hours=total_task_hours
    )


if __name__ == '__main__':
    app.run(debug=True)


