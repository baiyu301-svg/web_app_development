from flask import Blueprint, render_template, request, redirect, url_for, session, flash

course_bp = Blueprint('course', __name__)

@course_bp.route('/wishlist', methods=['GET'])
def wishlist():
    """
    查看個人許願清單。
    輸入: session['user_id']
    邏輯: 查詢該使用者所有的 Wishlist，並關聯 Course 詳細資料
    輸出: render 'wishlist.html'
    """
    pass

@course_bp.route('/wishlist/add', methods=['POST'])
def add_wishlist():
    """
    新增願望清單。
    輸入: form.held_course_id, form.target_course_id
    邏輯: 建立 Wishlist 紀錄，並觸發 Match 檢查邏輯
    輸出: redirect('/wishlist')
    """
    pass

@course_bp.route('/wishlist/<int:id>/delete', methods=['POST'])
def delete_wishlist(id):
    """
    刪除特定願望。
    輸入: url 參數 id, session['user_id']
    邏輯: 驗證擁有者，並刪除該筆 Wishlist
    輸出: redirect('/wishlist')
    """
    pass

@course_bp.route('/matches/<int:match_id>/rate', methods=['POST'])
def rate_user(match_id):
    """
    對換課對象給予評價。
    輸入: url 參數 match_id, form.rating (例如：+1 或 -1)
    邏輯: 更新目標對象的 credit_score
    輸出: redirect('/matches')
    """
    pass
