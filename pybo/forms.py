from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, TextAreaField
from wtforms.validators import DataRequired

# form 모듈의 질문 form 클래스
class QuestionForm(FlaskForm):
    # 사용자 입력 2개 생성
    # validators: 검증을 위한 도구
    # StringField:  문자열 입력
    # DataRequired: 데이터 요청 (필수 항목인지 체크함)
    # 질문 제목
    subject = StringField('제목', validators=[DataRequired('제목은 필수 입력 항목입니다.')])

    # TextArea: HTML form 태그의 TextArea
    # 질문 내용
    content = TextAreaField('내용', validators=[DataRequired('질문 내용은 필수 입력 항목입니다.')])


# form 모듈의 대답 form 클래스
class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('답변 내용은 필수 입력 항목입니다.')])