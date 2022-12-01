from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []
global current_index

current_index = 0
#we will append answers to responses

@app.get('/')
def show_home():

    title = survey.title
    instructions = survey.instructions

    return render_template("survey_start.html", title=title, instructions=instructions)

@app.post('/questions')
def redirect_to_question():
    return redirect(f"/questions/{current_index}")

@app.get('/questions/<num>')
def show_question(num):

    question = survey.questions[int(num)]
    prompt = question.prompt
    choices = question.choices

    return render_template("question.html", prompt=prompt, choices=choices)

@app.post('/answer')
def save_answer():
    choice = request.form["answer"]

    responses.append(choice)

    current_index += 1

    return redirect(f"/questions/{current_index}")
