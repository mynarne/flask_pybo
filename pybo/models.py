from sqlalchemy.orm import backref

from pybo import db


# table 구조 생성
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable = False)  # string 200자 제한
    content = db.Column(db.Text(), nullable = False)
    create_date =  db.Column(db.DateTime(), nullable = False)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete = 'CASCADE', onupdate = 'CASCADE'))  # Question의 id를 가져옴
    question = db.relationship('Question', backref = db.backref('answer_set'))  # Question table과 연결
    content = db.Column(db.Text(), nullable = False)
    create_date = db.Column(db.DateTime(), nullable = False)