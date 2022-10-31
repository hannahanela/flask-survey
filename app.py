import re
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.get('/')
def index():
    """Display the start page of a survey."""

    return render_template("survey_start.html", survey=survey)


@app.post('/begin')
def start_survey():
    """Redirect user to the first question of the survey."""
    survey_start_num = len(responses)

    return redirect(f'/questions/{survey_start_num}')


@app.get('/questions/<int:num>')
def display_question(num):
    """Display a survey question."""
    question = survey.questions[num]

    return render_template("question.html", question=question)


@app.post('/answer')
def store_answer():
    """Store answer for a survey question."""
    answer = request.form["answer"]
    responses.append(answer)
    next_question_num = len(responses)
    print(responses)

    return redirect(f'/questions/{next_question_num}')
