# from crypt import methods
from email import header
import os
from dotenv import load_dotenv
from cs50 import SQL
from datetime import date, datetime
from flask_session import Session
from tempfile import mkdtemp
from flask import Flask, flash, request, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import hello, login_required, apology, generate_link, getGroupsetInfo, getGroupSetByName, getSurvey, getSurveyByToken, responseDbSave, getSurveyUrlbasedOnGroupsetId, qra_getArray, qra_getResultsSurvey

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

load_dotenv()
SUPERTOKEN1 = os.getenv('AUTH_TOKEN')

# Configure CS50 Library to use SQLite database locally
db = SQL("sqlite:///dbx.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/qra", methods=["POST"])
# @login_required
def qra():
    if request.method == "POST":
        tokenFromHeaders = request.headers['Authorization']
        print(tokenFromHeaders)
        print(SUPERTOKEN1)
        if tokenFromHeaders == SUPERTOKEN1:
            bodyRequest = request.get_json('dashboardToken')
            token = bodyRequest['token']
            array1 = qra_getArray(token)
            q = qra_getResultsSurvey(array1, token)
            return q

        else:
            print('Incorrect Token')
            return {"message": "Bad Requests"}


@app.route("/dashboard", methods=["GET","POST"])
@login_required
def dashboard():
    gs = db.execute("SELECT groupset.id, groupset.groupset_name, survey_urls.urlname FROM groupset JOIN survey_urls ON groupset.id = survey_urls.GroupsetId")
    return render_template("dashboard.html", data=gs)


@app.route("/login", methods=["GET","POST"])
def login():
    """ This is login """

    if request.method == "POST":
        print("this is login with post")

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE users_name = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in -> id is an integer! so, in different terms, the id of the rows[0]
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else: 
        return render_template("login.html")


@app.route("/questions", methods=["GET", "POST"])
@login_required
def questions():
    """ This is Questions """
    print("this is questions")

    if request.method == "POST":
        
        # checking if user provided a name
        if not request.form.get("questionName"):
            return apology("Must provide a name for the question", 400)

        # checking if user provided a question
        if not request.form.get("question"):
            return apology("Must provide a question", 400)

        # checking if user provided a type of question
        if not request.form.get("questionType"):
            return apology("Must provide a type of question", 400)

        # checking user id
        print(f'session: {session["user_id"]} started')

        # Getting all the values from 
        questionName = request.form.get("questionName")
        question = request.form.get("question")
        questionType = request.form.get("questionType")
        userHere = db.execute("select * from users where id = ?", session["user_id"])
        userHere = userHere[0]['users_name']

        db.execute("INSERT INTO questionset (questionset_name, questionset_question, questionset_type_id, questionset_user_owner, questionset_creation_datetime, is_active) VALUES (?,?,?,?,?,?)", questionName, question, questionType, userHere, datetime.now(), 1)

        # data = db.execute("select * from users")
        return redirect('/questions')

    else:
        questionsetx = db.execute("select id, questionset_name, questionset_question, questionset_user_owner, questionset_type_id from questionset")
        return render_template("questions.html", data=questionsetx)


@app.route("/campaigns")
def campaigns():
    """ This is Campaigns"""
    print("this is campaigns")
    return render_template("campaigns.html")


@app.route("/getsets/<set1>", methods=["GET", "POST"])
# @login_required
def getsets(set1):
    groupset1 = db.execute("select questionset_id from set_question where groupset_id = ?", set1)
    if len(groupset1) == 0:
        return []
    groupset_name = db.execute("select groupset_name from groupset where id = ?", set1)
    q1 = []
    t1 = {}
    for i in groupset1:
        print(i['questionset_id'])
        r1 = db.execute("select * from questionset where id = ?", i['questionset_id'])
        t1 = {'groupsetname': groupset_name[0]['groupset_name'], 'question': r1[0]['questionset_question'],'question_type': r1[0]['questionset_type_id']}
        q1.append(t1)

    results = db.execute("select * from set_question where groupset_id = ?", set1)
    if len(q1) == 0:
        return ""
    else:
        return q1


@app.route("/addsets", methods=["GET", "POST"])
# @login_required
def testinfo():
    if request.method == 'POST':
        bodyRequest = request.get_json('t')
        gs1 = bodyRequest['gsx']
        qs1 = bodyRequest['qsx']
        
        if not gs1:
            return {'message': 'Bad Request'}
        if not qs1:
            return {'message': 'Bad Request'}
        
        validation1 = db.execute("select * from set_question where groupset_id = ? and questionset_id = ?", gs1, qs1)
        if len(validation1) != 0:
            return {'message':'Record already exist'}
        
        db.execute("INSERT INTO set_question (groupset_id, questionset_id) VALUES (?, ?)", gs1, qs1)
        return {'message':'Record created.'}
    else:
        return {'message':'Operation not Successful.'}


@app.route("/groupsets", methods=["GET", "POST"])
@login_required
def groupsets():
    """ This is groupsets """
    print("this is groupsets")

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("groupset"):
            return apology("must provide groupset name", 400)

        checkingForExistingGroupset = getGroupSetByName(request.form.get("groupset"))

        if len(checkingForExistingGroupset) > 0:
            return apology("groupset already exists", 400)

        userHere = db.execute("select * from users where id = ?", session["user_id"])
        userHere = userHere[0]['users_name']
        gs = request.form.get('groupset')
        url_string = generate_link(8)

        db.execute("INSERT INTO groupset (groupset_name, groupset_user_owner, groupset_creation_datetime, is_active) VALUES (?,?,?,?)", gs, userHere, datetime.now(), 1)
        groupSetId = db.execute("select id from groupset where groupset_name = ?", gs)
        db.execute("insert into survey_urls (urlname, is_active, CreationDate, GroupsetId) values (?,?,?,?)", url_string, True, datetime.now(), groupSetId[0]['id'])

        return redirect('/groupsets')

    else:
        groupsetx = getSurveyUrlbasedOnGroupsetId()
        questionsx = db.execute("select id, questionset_question, questionset_type_id from questionset")
        return render_template("groupsets.html", data=groupsetx, data2=questionsx)


@app.route("/register", methods=["GET", "POST"])
def register():
    """ This is Register """
    hello("this is register")

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        checkingForExistingUsernames = db.execute("SELECT users_name from users where users_name = ?", request.form.get("username"))

        if len(checkingForExistingUsernames) > 0:
            return apology("username already exists", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure verification password was submitted
        elif not request.form.get("password_confirmation"):
            return apology("must verify password", 400)


        elif request.form.get("password_confirmation") != request.form.get("password"):
            return apology("invalid username and/or password", 400)

        userProvided = request.form.get("username")
 
        db.execute("INSERT INTO users (users_name, hash, users_creation_datetime, is_active) VALUES (?,?,?,?)", userProvided, generate_password_hash(request.form.get('password')), datetime.now(), 1)

        data = db.execute("select * from users")
        return render_template("register.html")

    else:
        return render_template("register.html")


@app.route("/createSurvey", methods=["POST"])
def createSurvey():
    """Test url shortener"""

    bodyRequest = request.get_json('t')

    groupSetId = bodyRequest['gs']

    if(len(getGroupsetInfo(groupSetId)) == 0):
        return apology("Group Set not found",400)

    url_string = generate_link(8)
    rows = db.execute("insert into survey_urls (urlname, is_active, CreationDate, GroupsetId) values (?,?,?,?)", url_string, True, datetime.now(), groupSetId)
    data = F'http://127.0.0.1:5000/survey/{url_string}'
    return {'url': data}


@app.route("/survey/<surveyToken>", methods=["GET"])
def LoadSurvey(surveyToken):
    """Test url shortener"""

    data = getSurveyByToken(surveyToken)
    r = ''

    for item in data:
        match item['questionset_type_id']:
            case 'radio':
                r += render_template("u_radio.html", question1=item)
            case 'text':
                r += render_template("u_text.html", question1=item)
            case 'bool':
                r += render_template("u_bool.html", question1=item)
            case 'list':
                r += render_template("u_list.html", question1=item)

    return render_template('u_survey_user.html', data=r)


@app.route("/survey2/<surveyToken>", methods=["GET"])
def LoadSurvey2(surveyToken):
    """Test url shortener"""

    data = getSurveyByToken(surveyToken)
    return data


@app.route("/basic/<qid>", methods=["GET"])
def basics(qid):
    """Test url shortener"""
    print(qid)
    return render_template("basic.html", data=qid)


@app.route("/userview", methods=["GET"])
def userview():
    """Test url shortener"""

    return render_template("survey1.html")


@app.route("/userresponses", methods=["GET", "POST"])
@login_required
def userresponses():
    """ This is userresponses """

    if request.method == "POST":
        x = 1
        bodyRequest = request.get_json('arrayResult')
        print(bodyRequest)
        responseDbSave(bodyRequest)
        return ''

    else:
        redirect('/')


@app.route("/usermanagement", methods=["GET", "POST"])
@login_required
def usermanagement():
    """ This is usermanagement """

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        checkingForExistingUsernames = db.execute("SELECT users_name from users where users_name = ?", request.form.get("username"))

        if len(checkingForExistingUsernames) == 0:
            return apology("username does not exists", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        userProvided = request.form.get("username")
 
        db.execute("update users set hash = ? where users_name = ?", generate_password_hash(request.form.get('password')), userProvided)
        return redirect('/usermanagement')

    else:
        data = db.execute("select * from users")
        return render_template("usermanagement.html", data=data)


@app.route("/logout", methods=["GET","POST"])
def logout():
    """ This is logout """
    session.clear()
    print(f'session : {session["user_id"]} was cleared.')
    return redirect('/')





