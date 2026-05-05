from flask import Blueprint, render_template
from app.models.course import Course
from app.models.wishlist import Wishlist

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    處理首頁請求。
    輸入: 無
    邏輯: 查詢所有課程，並準備顯示於看板 (此為 MVP 簡易版)
    輸出: 渲染 'index.html'
    """
    courses = Course.get_all()
    # TODO: 計算熱門需求課程與熱門釋出課程
    return render_template('index.html', courses=courses)
