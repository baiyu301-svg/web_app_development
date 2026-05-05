from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.wishlist import Wishlist
from app.models.course import Course
from app.models.match import Match
from app.models.user import User

course_bp = Blueprint('course', __name__)

@course_bp.route('/wishlist', methods=['GET'])
def wishlist():
    if 'user_id' not in session:
        flash('請先登入', 'warning')
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    wishlists = Wishlist.get_by_user(user_id)
    courses = Course.get_all()
    
    # 關聯課程詳細資料 (簡易版 O(N^2) 查詢，未來可優化為 SQL JOIN)
    for w in wishlists:
        w['held_course'] = next((c for c in courses if c['id'] == w['held_course_id']), None)
        w['target_course'] = next((c for c in courses if c['id'] == w['target_course_id']), None)
        
    return render_template('wishlist.html', wishlists=wishlists, courses=courses)

@course_bp.route('/wishlist/add', methods=['POST'])
def add_wishlist():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    held_course_id = request.form.get('held_course_id')
    target_course_id = request.form.get('target_course_id')
    
    if not held_course_id or not target_course_id:
        flash('請選擇要換出與換入的課程', 'danger')
        return redirect(url_for('course.wishlist'))
        
    wishlist_id = Wishlist.create(user_id, held_course_id, target_course_id)
    if wishlist_id:
        flash('許願清單新增成功！', 'success')
        
        # 簡易媒合邏輯檢查 (A 想要 B 的課，B 想要 A 的課)
        all_wishlists = Wishlist.get_all()
        for other in all_wishlists:
            if other['status'] == 'pending' and other['user_id'] != user_id:
                if str(other['held_course_id']) == str(target_course_id) and str(other['target_course_id']) == str(held_course_id):
                    # 配對成功
                    Match.create(wishlist_id, other['id'])
                    Wishlist.update_status(wishlist_id, 'matched')
                    Wishlist.update_status(other['id'], 'matched')
                    flash('系統發現符合條件的配對！請到「媒合列表」查看', 'info')
                    break
    else:
        flash('新增失敗', 'danger')
        
    return redirect(url_for('course.wishlist'))

@course_bp.route('/wishlist/<int:id>/delete', methods=['POST'])
def delete_wishlist(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    wishlist = Wishlist.get_by_id(id)
    if not wishlist or wishlist['user_id'] != session['user_id']:
        flash('無權限刪除', 'danger')
        return redirect(url_for('course.wishlist'))
        
    if Wishlist.delete(id):
        flash('刪除成功', 'success')
    else:
        flash('刪除失敗', 'danger')
        
    return redirect(url_for('course.wishlist'))

@course_bp.route('/matches/<int:match_id>/rate', methods=['POST'])
def rate_user(match_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    match = Match.get_by_id(match_id)
    if not match:
        flash('找不到該配對紀錄', 'danger')
        return redirect(url_for('chat.matches'))
        
    # 判斷對方 user_id
    w1 = Wishlist.get_by_id(match['wishlist_id_1'])
    w2 = Wishlist.get_by_id(match['wishlist_id_2'])
    
    target_user_id = None
    if w1['user_id'] == session['user_id']:
        target_user_id = w2['user_id']
    elif w2['user_id'] == session['user_id']:
        target_user_id = w1['user_id']
        
    if not target_user_id:
        flash('您不屬於此配對', 'danger')
        return redirect(url_for('chat.matches'))
        
    rating = request.form.get('rating')
    if rating == 'good':
        User.update_credit_score(target_user_id, 5)
        flash('已給予好評！', 'success')
    elif rating == 'bad':
        User.update_credit_score(target_user_id, -10)
        flash('已給予差評！', 'warning')
        
    # 簡單假設給完評價就完成交易 (實際應用應記錄評價狀態以防重複評價)
    Match.update_status(match_id, 'completed')
    
    return redirect(url_for('chat.matches'))
