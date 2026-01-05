from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from functools import wraps
from datetime import datetime, timedelta
from collections import defaultdict
import random

app = Flask(__name__)
app.secret_key = "kwusecret123"

# ================= Database Connection =================
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
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
            user_id = cursor.lastrowid
            
            # Create default courses for new user
            default_courses = [
                ('Mathematics', '#3b82f6', 3),
                ('Physics', '#ef4444', 3),
                ('Computer Science', '#10b981', 4),
                ('English', '#8b5cf6', 2)
            ]
            
            for course_name, color, sks in default_courses:
                cursor.execute(
                    "INSERT INTO courses (user_id, course_name, color, sks) VALUES (%s, %s, %s, %s)",
                    (user_id, course_name, color, sks)
                )
            
            # Set default weekly capacity
            cursor.execute(
                "INSERT INTO weekly_capacity (user_id, daily_hours) VALUES (%s, %s)",
                (user_id, 2)
            )
            
            conn.commit()
            flash("Registration successful! Please login.", 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            if "Duplicate entry" in str(err):
                flash("Username or email already exists.", 'danger')
            else:
                flash(f"Error: {err}", 'danger')
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
    
    # Get user's courses
    cursor.execute("""
        SELECT * FROM courses 
        WHERE user_id=%s 
        ORDER BY course_name
    """, (session['user_id'],))
    courses = cursor.fetchall()
    
    # Get all tasks with course info
    cursor.execute("""
        SELECT t.*, c.course_name, c.color 
        FROM tasks t
        LEFT JOIN courses c ON t.course_id = c.id
        WHERE t.user_id=%s
        ORDER BY t.deadline ASC
    """, (session['user_id'],))
    tasks = cursor.fetchall()
    
    cursor.close()
    conn.close()

    # =================== Collision Detection ===================
    warning_msg = ""
    week_counter = {}

    for task in tasks:
        dt = task['deadline']
        if isinstance(dt, datetime):
            dt_obj = dt
        else:
            dt_obj = datetime.combine(dt, datetime.min.time())
        year, week, _ = dt_obj.isocalendar()
        key = f"{year}-{week}"
        week_counter[key] = week_counter.get(key, 0) + 1

    now = datetime.now()
    current_week_key = f"{now.isocalendar()[0]}-{now.isocalendar()[1]}"
    if week_counter.get(current_week_key, 0) > 2:
        warning_msg = "⚠️ Minggu ini overload"

    # =================== Handle Add Task ===================
    if request.method == 'POST':
        title = request.form['title']
        deadline = request.form['deadline']
        course_id = request.form.get('course_id')
        sks = int(request.form['sks'])
        jenis = request.form['jenis']
        estimasi = int(request.form['estimasi'])
        
        # If user wants to add new course
        new_course = request.form.get('new_course')
        if new_course and not course_id:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Assign random color
            colors = ['#3b82f6', '#ef4444', '#10b981', '#8b5cf6', '#f59e0b', '#ec4899']
            color = random.choice(colors)
            
            cursor.execute("""
                INSERT INTO courses (user_id, course_name, color, sks) 
                VALUES (%s, %s, %s, %s)
            """, (session['user_id'], new_course, color, sks))
            course_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
        
        # Auto Priority Engine
        delta_days = (datetime.strptime(deadline,"%Y-%m-%d") - now).days
        priority = '🟢 Santai'
        if delta_days <=1 or sks >=3 or jenis.lower() in ['uts','uas']:
            priority = '🔴 Mendesak'
        elif delta_days <=3:
            priority = '🟡 Sedang'
        
        # Insert task
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (user_id, title, deadline, course_id, sks, jenis, estimasi_waktu, priority) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (session['user_id'], title, deadline, course_id, sks, jenis, estimasi, priority))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Task added!", 'success')
        return redirect(url_for('dashboard'))

    # =================== Group Tasks by Course ===================
    grouped_tasks = defaultdict(list)
    for task in tasks:
        course_name = task['course_name'] or 'Uncategorized'
        grouped_tasks[course_name].append(task)

    # =================== Stress Indicator ===================
    stress_score = 0
    start_week = now - timedelta(days=now.weekday())
    end_week = start_week + timedelta(days=6)

    weekly_tasks = [
        t for t in tasks
        if start_week.date() <= t['deadline'] <= end_week.date()
    ]

    stress_score += len(weekly_tasks) * 2
    total_hours = sum(t['estimasi_waktu'] for t in weekly_tasks)
    stress_score += total_hours

    for t in weekly_tasks:
        if t['jenis'].lower() in ['uts', 'uas']:
            stress_score += 5
        if t['sks'] >= 3:
            stress_score += 3

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
        courses=courses,
        grouped_tasks=grouped_tasks,
        is_premium=session['is_premium'],
        warning_msg=warning_msg,
        stress_level=stress_level,
        stress_color=stress_color,
        stress_score=stress_score
    )

# ================= Manage Courses =================
@app.route('/courses')
@login_required
def manage_courses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get user's courses with task count
    cursor.execute("""
        SELECT c.*, COUNT(t.id) as task_count 
        FROM courses c
        LEFT JOIN tasks t ON c.id = t.course_id AND t.user_id = c.user_id
        WHERE c.user_id=%s
        GROUP BY c.id
        ORDER BY c.course_name
    """, (session['user_id'],))
    courses = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('courses.html', courses=courses)

@app.route('/add_course', methods=['POST'])
@login_required
def add_course():
    course_name = request.form['course_name']
    color = request.form.get('color', '#3b82f6')
    sks = int(request.form.get('sks', 2))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO courses (user_id, course_name, color, sks) 
            VALUES (%s, %s, %s, %s)
        """, (session['user_id'], course_name, color, sks))
        conn.commit()
        flash(f"Course '{course_name}' added successfully!", 'success')
    except mysql.connector.Error as err:
        flash(f"Error: Course already exists", 'danger')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('manage_courses'))

@app.route('/delete_course/<int:course_id>', methods=['POST'])
@login_required
def delete_course(course_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # First, update tasks to remove course association
    cursor.execute("""
        UPDATE tasks SET course_id = NULL 
        WHERE course_id=%s AND user_id=%s
    """, (course_id, session['user_id']))
    
    # Delete the course
    cursor.execute("DELETE FROM courses WHERE id=%s AND user_id=%s", 
                   (course_id, session['user_id']))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'success': True})

# ================= Upgrade =================
@app.route('/upgrade', methods=['GET','POST'])
@login_required
def upgrade():
    if request.method == 'POST':
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

# ================= Task Management =================
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

# ================= Weekly Planner =================
@app.route('/weekly-planner')
@login_required
def weekly_planner():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get user capacity
    cursor.execute(
        "SELECT daily_hours FROM weekly_capacity WHERE user_id=%s",
        (session['user_id'],)
    )
    cap = cursor.fetchone()
    daily_hours = cap['daily_hours'] if cap else 2

    # Get tasks for this week
    start_week = datetime.now() - timedelta(days=datetime.now().weekday())
    end_week = start_week + timedelta(days=6)

    cursor.execute("""
        SELECT t.*, c.course_name, c.color 
        FROM tasks t
        LEFT JOIN courses c ON t.course_id = c.id
        WHERE t.user_id=%s 
        AND deadline BETWEEN %s AND %s
        ORDER BY priority DESC
    """, (session['user_id'], start_week.date(), end_week.date()))

    tasks = cursor.fetchall()
    cursor.close()
    conn.close()

    total_task_hours = sum(t['estimasi_waktu'] for t in tasks)
    weekly_capacity = daily_hours * 7
    remaining = weekly_capacity - total_task_hours

    # Distribute tasks across days
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

            planner[day_pointer].append({
                'title': task['title'],
                'course': task['course_name'] or 'Uncategorized',
                'color': task['color'] or '#6b7280'
            })
            remaining_daily -= 1
            hours -= 1

    return render_template(
        "weekly_planner.html",
        planner=planner,
        remaining=remaining,
        weekly_capacity=weekly_capacity,
        total_task_hours=total_task_hours,
        daily_hours=daily_hours
    )

# ================= Set Capacity =================
@app.route('/set_capacity', methods=['POST'])
@login_required
def set_capacity():
    daily_hours = int(request.form['daily_hours'])
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Update or insert capacity
    cursor.execute("SELECT id FROM weekly_capacity WHERE user_id=%s", (session['user_id'],))
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute(
            "UPDATE weekly_capacity SET daily_hours=%s WHERE user_id=%s",
            (daily_hours, session['user_id'])
        )
    else:
        cursor.execute(
            "INSERT INTO weekly_capacity (user_id, daily_hours) VALUES (%s, %s)",
            (session['user_id'], daily_hours)
        )
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash(f"Daily capacity set to {daily_hours} hours", 'success')
    return redirect(url_for('weekly_planner'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)