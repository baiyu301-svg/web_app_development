from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('請填寫所有必填欄位！', 'danger')
            return render_template('login.html')

        user = User.get_by_email(email)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            flash('登入成功！', 'success')
            return redirect(url_for('course.wishlist'))
        else:
            flash('Email 或密碼錯誤', 'danger')
            return render_template('login.html')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('請填寫所有必填欄位！', 'danger')
            return render_template('register.html')

        if not email.endswith('.edu.tw'):
            flash('必須使用學校信箱 (.edu.tw) 註冊！', 'danger')
            return render_template('register.html')

        if User.get_by_email(email):
            flash('該信箱已被註冊！', 'danger')
            return render_template('register.html')

        user_id = User.create(email, generate_password_hash(password))
        if user_id:
            session['user_id'] = user_id
            flash('註冊成功！', 'success')
            return redirect(url_for('course.wishlist'))
        else:
            flash('註冊失敗，請稍後再試。', 'danger')
            return render_template('register.html')

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('您已登出。', 'info')
    return redirect(url_for('main.index'))
