from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/matches', methods=['GET'])
def matches():
    """
    查看使用者的媒合成功列表。
    輸入: session['user_id']
    邏輯: 查詢該使用者參與的所有 Match
    輸出: render 'matches.html'
    """
    pass

@chat_bp.route('/chat/<int:match_id>', methods=['GET'])
def chat_room(match_id):
    """
    進入專屬匿名聊天室。
    輸入: url 參數 match_id, session['user_id']
    邏輯: 驗證使用者是否為該配對的一方，並載入歷史 ChatMessage
    輸出: render 'chat.html'
    """
    pass

@chat_bp.route('/chat/<int:match_id>/send', methods=['POST'])
def send_message(match_id):
    """
    發送聊天訊息。
    輸入: url 參數 match_id, session['user_id'], form.content (或 JSON data)
    邏輯: 將訊息存入 ChatMessage 資料表
    輸出: redirect('/chat/<match_id>') 或回傳 JSON
    """
    pass
