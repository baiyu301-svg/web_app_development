from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.models.match import Match
from app.models.chat_message import ChatMessage
from app.models.wishlist import Wishlist
from app.models.course import Course

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/matches', methods=['GET'])
def matches():
    if 'user_id' not in session:
        flash('請先登入', 'warning')
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    user_matches = Match.get_user_matches(user_id)
    
    # 關聯課程資料以供顯示
    courses = {c['id']: c for c in Course.get_all()}
    
    for m in user_matches:
        w1 = Wishlist.get_by_id(m['wishlist_id_1'])
        w2 = Wishlist.get_by_id(m['wishlist_id_2'])
        
        if w1['user_id'] == user_id:
            m['my_wishlist'] = w1
            m['their_wishlist'] = w2
        else:
            m['my_wishlist'] = w2
            m['their_wishlist'] = w1
            
        m['get_course'] = courses.get(m['my_wishlist']['target_course_id'])
        m['give_course'] = courses.get(m['my_wishlist']['held_course_id'])

    return render_template('matches.html', matches=user_matches)

@chat_bp.route('/chat/<int:match_id>', methods=['GET'])
def chat_room(match_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    match = Match.get_by_id(match_id)
    
    if not match:
        flash('找不到該配對紀錄', 'danger')
        return redirect(url_for('chat.matches'))
        
    # 驗證權限
    w1 = Wishlist.get_by_id(match['wishlist_id_1'])
    w2 = Wishlist.get_by_id(match['wishlist_id_2'])
    if w1['user_id'] != user_id and w2['user_id'] != user_id:
        flash('無權限進入此聊天室', 'danger')
        return redirect(url_for('chat.matches'))
        
    messages = ChatMessage.get_by_match_id(match_id)
    
    # 為了畫面顯示判斷是自己還是對方的訊息
    for msg in messages:
        msg['is_mine'] = (msg['sender_id'] == user_id)
        
    return render_template('chat.html', match=match, messages=messages)

@chat_bp.route('/chat/<int:match_id>/send', methods=['POST'])
def send_message(match_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    user_id = session['user_id']
    content = request.form.get('content')
    
    if not content:
        flash('不能發送空白訊息', 'warning')
        return redirect(url_for('chat.chat_room', match_id=match_id))
        
    # 驗證權限
    match = Match.get_by_id(match_id)
    w1 = Wishlist.get_by_id(match['wishlist_id_1'])
    w2 = Wishlist.get_by_id(match['wishlist_id_2'])
    if w1['user_id'] != user_id and w2['user_id'] != user_id:
        return jsonify({'error': 'Forbidden'}), 403
        
    ChatMessage.create(match_id, user_id, content)
    
    return redirect(url_for('chat.chat_room', match_id=match_id))
