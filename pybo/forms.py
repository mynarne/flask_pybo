from email import message

from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms.fields.simple import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, equal_to, EqualTo, Email


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


# form 모듈 - 회원가입
class UserCreateForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired('아이디는 필수 입력 항목입니다.'), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired('비밀번호는 필수 입력 항목입니다.'), EqualTo('password2', message='비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired('비밀번호 확인은 필수 입력 항목입니다.')])
    email = EmailField('이메일', validators=[DataRequired('이메일은 필수 입력 항목입니다.'), Email()])

# 로그인
class UserLoginForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired('아이디는 필수 입력 항목입니다.'), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired('비밀번호는 필수 입력 항목입니다.')])