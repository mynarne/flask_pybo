from flask import Blueprint


# url_prefix = '/' - root로 시작하는 경로 정보를 입력
bp = Blueprint('main', __name__, url_prefix='/')

# root 경로 실행
@bp.route('/')
def index():
    return 'Pybo Index!'

@bp.route('/hello')
def hello_world():
    return 'Hello Pybo!'

@bp.route('/bye')
def bye():
    return 'Bye Pybo!'