from datetime import datetime
from pybo import create_app, db
from pybo.models import Question

def insert_test_data(n = 300):
    """ 테스트용 질문 데이터 n개 생성 """
    # pybo 디렉토리 내부 생성자 함수 create_app()
    app = create_app()    # flask context 필요
    with app.app_context():    # with 사용 : db open, close 스스로 실행
        for i in range(n):
            q = Question(
                subject = "텍스트 데이터: [%03d]"%i,
                content = "내용 없음",
                create_date = datetime.now()
            )
            db.session.add(q)

        db.session.commit()   # 300개 전부 커밋
        print(f"{n}개의 테스트 데이터 생성됨")

if __name__ == '__main__':
    insert_test_data()

