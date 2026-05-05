import os
import sqlite3
from flask import Flask

def init_db(app):
    db_path = os.path.join(app.instance_path, 'database.db')
    schema_path = os.path.join(os.path.dirname(app.root_path), 'database', 'schema.sql')
    
    os.makedirs(app.instance_path, exist_ok=True)
    
    with sqlite3.connect(db_path) as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev'),
    )

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊 Blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.course import course_bp
    from app.routes.chat import chat_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(chat_bp)

    return app
