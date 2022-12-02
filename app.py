from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get('/')
def show_home():
    """Show start survey and initiate session"""

    title = survey.title
    instructions = survey.instructions

    session["responses"] = []
    session["question_idx"] = 0
    session["questions_length"] = len(survey.questions)

    return render_template("survey_start.html", title=title, instructions=instructions)


@app.post('/begin')
def redirect_to_question():
    """Redirects to first question"""
    return redirect(f"/questions/0")


@app.get('/questions/<int:num>')
def show_question(num):
    """Shows question to answer"""
    question = survey.questions[num]
    prompt = question.prompt
    choices = question.choices

    return render_template("question.html", prompt=prompt, choices=choices)


@app.post('/answer')
def save_answer():
    """Saves answer to session. If reached end of survey, redirect to Thank You page else, redirect to next question"""
    choice = request.form["answer"]

    responses = session["responses"]

    responses.append(choice)

    session["responses"] = responses

    if len(session["responses"]) >= session["questions_length"]:
        return redirect("/completion")

    else:
        session["question_idx"]+=1
        next_idx = session["question_idx"]

        return redirect(f"/questions/{next_idx}")


@app.get('/completion')
def thank_you():
    """Displays thank you page and all questions and answers"""
    questions = survey.questions

    return render_template("completion.html", questions=questions)
