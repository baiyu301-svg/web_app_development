from dotenv import load_dotenv
from app import create_app, init_db

load_dotenv()

app = create_app()

def setup_database():
    """初始化資料庫。供命令列或腳本呼叫。"""
    with app.app_context():
        init_db(app)

if __name__ == '__main__':
    app.run(debug=True)
