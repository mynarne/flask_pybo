from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for

from pybo import db
from pybo.forms import QuestionForm, AnswerForm
from pybo.models import Question

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def _list():   #  함수명 앞에 언더바 붙으면 직접 실행x
    question_list = Question.query.order_by(Question.create_date.desc())
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