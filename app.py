from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get('/')
def index():
    """Display the instructions for a survey."""

    return render_template("survey_start.html", survey=survey)


@app.post('/begin')
def start_survey():
    """Redirect user to the first question of the survey."""
    session["responses"] = []
    first_question_num = len(session["responses"])

    return redirect(f'/questions/{first_question_num}')


@app.get('/questions/<int:num>')
def display_question(num):
    """Display a survey question."""
    num_answered_questions = len(session['responses'])

    if num >= num_answered_questions and num_answered_questions == len(survey.questions):
        return redirect('/end')

    if num > num_answered_questions:
        correct_question_num = num_answered_questions
        return redirect(f'/questions/{correct_question_num}')

    question = survey.questions[num]

    return render_template("question.html", question=question)


@app.post('/answer')
def handle_answer():
    """
    Store answer for a survey question.
    
    Redirect user to next question or completion message.
    """
    next_question_num = len(session['responses'])

    if next_question_num == len(survey.questions):
        return redirect('/end')

    answer = request.form['answer']
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    next_question_num += 1

    return redirect(f'/questions/{next_question_num}')

@app.get('/end')
def display_completion():
    """Display completion message when survey completed."""

    return render_template('completion.html')