import os

BASE_DIR = os.path.dirname(__file__)

# DB접속 주소  pybo.db의 기본 경로를 {}로 삽입
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))

# 이벤트 처리
SQLALCHEMY_TRACK_MODIFICATIONS = False