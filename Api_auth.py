from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from ..db import get_db_connection

api_bp = Blueprint('api', __name__)

@api_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = 'user'  # Usuário comum, você pode implementar uma escolha de role

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, %s)', 
                       (username, generate_password_hash(password), email, role))
        conn.commit()
        cursor.close()
        conn.close()
        flash("User created successfully", "success")
        return redirect(url_for('api.login'))
    return render_template('register.html')

@api_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash("Login successful", "success")
            return redirect(url_for('main.index'))
        flash("Invalid credentials", "danger")
    return render_template('login.html')

@api_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out", "info")
    return redirect(url_for('api.login'))
