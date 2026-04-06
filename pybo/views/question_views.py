from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for

from pybo import db
from pybo.forms import QuestionForm, AnswerForm
from pybo.models import Question

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def _list():   #  함수명 앞에 언더바 붙으면 직접 실행x
    page = request.args.get('page', default=1, type=int)  # 페이지 쿼리 스트링 값(url 페이지 값) 가져오기
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page=page, per_page=10)   # page 값 받아온 뒤 한 페이지에 10개 씩 출력
    return render_template('question/question_list.html', question_list = question_list)


#                  url 파라미터를 변수로 받음
@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get(question_id)
    return render_template('question/question_detail.html', question = question, form = form)


@bp.route('/create/', methods=['GET', 'POST'])
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form = form)