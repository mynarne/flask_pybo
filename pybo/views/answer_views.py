from datetime import datetime

from flask import Blueprint, request, redirect, url_for, render_template

from pybo import db
from pybo.forms import AnswerForm
from pybo.models import Question, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods = ['POST'])
def create(question_id):
    form = AnswerForm()
    # 답변 등록할 질문을 DB에서 조회
    question = Question.query.get_or_404(question_id)

    if form.validate_on_submit():
        # 사용자가 입력한 form 태그의 'content' 속성의 값을 변수에 호출
        content = request.form.get('content')

        # Answer 객체 생성
        answer = Answer(content = content, create_date = datetime.now())

        # 해당 질문에 답변 등록
        question.answer_set.append(answer)
        db.session.commit()
        return redirect(url_for('question.detail', question_id = question_id))
    return render_template('question/question_detail.html', question = question, form = form)
