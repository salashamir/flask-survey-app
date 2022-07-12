from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

# routes
@app.route('/')
def root():
    """home route, to begin survey"""
    return render_template('home.html', survey=satisfaction_survey)


@app.route('/start', methods=["POST"])
def start():
    """start route, sets session variable"""
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')


@app.route('/questions/<int:question_id>')
def question_asked(question_id):
    """display individual question route"""
    responses = session.get(RESPONSES_KEY)
    if responses is None:
        return redirect('/')
    # if survey completed, always redirect to thank you page
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thankyou')
    # if user tries to go to a diff question (or invalid idex question) via url, always redierct to curent question
    if len(responses) != question_id:
        flash(f'Invalid question id: {question_id}')
        return redirect(f'/questions/{len(responses)}')
    # retrieve question from survey object
    question = satisfaction_survey.questions[question_id]
    return render_template('question.html', question=question, qid=question_id)


@app.route('/answer', methods=["POST"])
def answer_recorded():
    """post route that receives answer and adds it to global list"""
    answer_submitted = request.form.get("answer")
    responses = session[RESPONSES_KEY]
    responses.append(answer_submitted)
    session[RESPONSES_KEY] = responses
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thankyou')
    else:
        return redirect(f'/questions/{len(responses)}')


@app.route('/thankyou')
def thank_you():
    """thank you route once survey completed"""
    print("********************")
    print(session["responses"])
    print("********************")
    return render_template('thankyou.html')


    


