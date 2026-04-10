import os

from datetime import datetime
from tkinter import Image

from flask import Blueprint, render_template, request, redirect, url_for, g, flash, current_app
from werkzeug.utils import secure_filename

from pybo import db
from pybo.forms import QuestionForm, AnswerForm
from pybo.models import Question, Answer, User
from pybo.views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def _list():   #  함수명 앞에 언더바 붙으면 직접 실행x
    page = request.args.get('page', default=1, type=int)  # 페이지 쿼리 스트링 값(url 페이지 값) 가져오기
    kw = request.args.get('kw', default=None, type=str)   # 검색 키워드 추가 (쿼리 스트링 값 받아오기)
    question_list = Question.query.order_by(Question.create_date.desc())

    if kw:
        search = f'%{kw}%';
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username)\
                .join(User, Answer.user_id == User.id).subquery()

        question_list = question_list.join(User)\
                .outerjoin(sub_query, sub_query.c.question_id == Question.id)\
                .filter(
            Question.subject.ilike(search) |    # 질문 제목
            Question.content.ilike(search) |    # 질문 내용
            User.username.ilike(search) |        # 질문 작성자
            sub_query.c.content.ilike(search) | # 답변 내용
            sub_query.c.username.ilike(search)  # 답변 작성자
        ).distinct()


    question_list = question_list.paginate(page=page, per_page=10)   # page 값 받아온 뒤 한 페이지에 10개 씩 출력

    return render_template('question/question_list.html', question_list = question_list, page = page, kw = kw)


#                  url 파라미터를 변수로 받음
@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get(question_id)
    return render_template('question/question_detail.html', question = question, form = form)


@bp.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():

        # form에 전송된 이미지 파일 받아오기
        image_file = form.image.data
        image_path = None

        if image_file:
            # 저장 경로 설정 : 오늘 날짜로 폴더 설정
            today = datetime.now().strftime('%Y%m%d')
            upload_folder = os.path.join(current_app.root_path, 'static/photos', today)
            os.makedirs(upload_folder, exist_ok=True)
                                        # 경로가 없으면 만들고 있다면 해당 경로에 이미지 저장

            # 파일 저장
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(upload_folder, filename)
            image_file.save(file_path)

            # db에 저장할 파일 경로 ( static 기준 상대경로 )
            image_path = f'photos/{today}/{filename}'

        question = Question(subject = form.subject.data, content=form.content.data, create_date=datetime.now(), user = g.user, image_path = image_path)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form = form)

@bp.route('/modify/<int:question_id>/', methods = ['GET', 'POST'])
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)

    if g.user != question.user:
        flash('수정 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id = question_id))

    if request.method == 'POST':   # POST방식
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)   # FORM에 있는 객체들을 update

            question.modify_date = datetime.now()   # 수정 날짜 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id = question_id))

    else:                           # GET 방식
        form = QuestionForm(obj = question)
    return render_template('question/question_form.html', form = form)

@bp.route('/delete/<int:question_id>/')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id = question_id))

    db.session.delete(question)
    db.session.commit()

    return redirect(url_for('question._list'))