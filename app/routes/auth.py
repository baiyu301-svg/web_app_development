from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理登入。
    輸入: form.email, form.password
    邏輯: 檢查使用者是否存在，並驗證密碼
    輸出: 成功 -> redirect('/wishlist'), 失敗 -> 重新 render 'login.html' 並顯示錯誤
    """
    pass

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理註冊。
    輸入: form.email, form.password
    邏輯: 驗證 email 後綴 (.edu.tw)，建立新 User
    輸出: 成功 -> redirect('/wishlist'), 失敗 -> 重新 render 'register.html'
    """
    pass

@auth_bp.route('/logout')
def logout():
    """
    處理登出。
    輸入: 無
    邏輯: 清除 session 中的 user_id
    輸出: redirect('/')
    """
    pass
