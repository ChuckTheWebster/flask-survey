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

    session["responses"] = []
    session["question_idx"] = 0

    questions_length = len(survey.questions)

    session["questions_length"] = questions_length

    return render_template("survey_start.html", title=title, instructions=instructions)

@app.post('/begin')
def redirect_to_question():
    """"""
    return redirect(f"/questions/0")


@app.get('/questions/<int:num>')
def show_question(num):
    """"""
    #{session['question_idx']}
    #session['question_idx']

    question = survey.questions[num]

    prompt = question.prompt
    choices = question.choices

    return render_template("question.html", prompt=prompt, choices=choices)




@app.post('/answer')
def save_answer():
    """"""
    choice = request.form["answer"]

    session["responses"].append(choice)
    print(session["responses"])

    if len(session["responses"]) == session["questions_length"]:
        return redirect("/completion")

    else:


        session["question_idx"]+=1

        next_idx = session["question_idx"]

        return redirect(f"/questions/{next_idx}")

@app.get('/completion')
def thank_you():

    questions = survey.questions

    return render_template("completion.html", questions=questions, )
