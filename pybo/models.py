from pybo import db


# table 구조 생성
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable = False)  # string 200자 제한
    content = db.Column(db.Text(), nullable = False)
    create_date =  db.Column(db.DateTime(), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE', onupdate = 'CASCADE'), nullable = False) #, server_default = '1') 
                                                                                                                # server_default 기존 데이터에도 기본값 지정됨
    user = db.relationship('User', backref = db.backref('question_set'))  # User table 연결 - user가 올린 게시물 바로 확인
    modify_date = db.Column(db.DateTime(), nullable = True)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete = 'CASCADE', onupdate = 'CASCADE'))  # Question의 id를 가져옴
    question = db.relationship('Question', backref = db.backref('answer_set'))  # Question table과 연결
    content = db.Column(db.Text(), nullable = False)
    create_date = db.Column(db.DateTime(), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE', onupdate = 'CASCADE'), nullable = False)
    user = db.relationship('User', backref = db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable = True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)