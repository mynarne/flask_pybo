import config

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


# key 이름 설정   / SQLite 사용하는 경우에만 작성(에러방지)
naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}


db = SQLAlchemy(metadata = MetaData(naming_convention = naming_convention))    # ORM 도구
migrate = Migrate()  # 테이블 구조 변경 시 DB에 반영해주는 도구


# 팩토리
def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)   # init.app -> 초기 설정
    migrate.init_app(app, db)

    from . import models

    # 블루프린트 등록
    from .views import main_views, question_views, answer_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    # 필터 등록
    from .filter import format_datetime
    # pipeline
    app.jinja_env.filters['datetime'] = format_datetime

    return app