from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    處理首頁請求。
    輸入: 無
    邏輯: 查詢熱門課程清單，並準備顯示於看板
    輸出: 渲染 'index.html'
    """
    pass
