from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get('/')
def index():
    """Display survey selection form."""
    session.permanent = True
    session['selection'] = ''

    return render_template("selection.html", surveys=surveys)


@app.post('/instructions')
def display_instructions():
    """Display the instructions for a survey."""
    selection = request.form['selection']

    survey = surveys[selection]
    session['selection'] = selection

    if selection in session.get('completed', []):
        return redirect('/end')

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
    selection = session['selection']
    survey = surveys[selection]

    if num >= num_answered_questions and num_answered_questions == len(survey.questions):
        completed = session.get('completed', [])
        print(completed)
        completed.append(selection)
        print(completed)
        session['completed'] = completed

        return redirect('/end')

    if num > num_answered_questions:
        correct_question_num = num_answered_questions
        flash('Please answer next question.')
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
    selection = session['selection']
    survey = surveys[selection]

    if next_question_num == len(survey.questions):
        return redirect('/end')

    answer = request.form['answer']
    comment = request.form.get('comment', None)
    responses = session['responses']
    responses.append({
        "answer": answer,
        "comment": comment,
    })
    session['responses'] = responses

    next_question_num += 1

    return redirect(f'/questions/{next_question_num}')

@app.get('/end')
def display_completion():
    """Display completion message when survey completed."""
    selection = session['selection']
    survey = surveys[selection]
    questions = survey.questions
    num_of_questions = len(questions)
    responses = session['responses']

    return render_template(
        'completion.html',
        num_of_questions=num_of_questions,
        questions=questions,
        responses=responses
    )
    