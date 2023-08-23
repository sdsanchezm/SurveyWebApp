import os
import requests
import random
import urllib.parse
from cs50 import SQL
from datetime import date, datetime

from flask import redirect, render_template, request, session
from functools import wraps

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///dbx.db")

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message))


def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            # return redirect("/login")
            return render_template("login.html")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def hello(name):
    print(f"hello here! {name}")
    return True

def generate_link(limit1):
    sourceChars = '1234567890abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnopqrstuvwxyz'
    rand1 = random.randint(0,len(sourceChars))
    print(sourceChars[rand1])
    array1 = []
    string1 = ''
    for i in range(1, limit1 + 1):
        rand1 = random.randint(0,len(sourceChars) - 1)
        string1 += sourceChars[rand1]
    return string1

def getGroupsetInfo(groupSetId):
    return db.execute("SELECT * from groupset where id = ?", groupSetId)

def getGroupSetByName(groupSetName):
    return db.execute("SELECT groupset_name from groupset where groupset_name = ?", groupSetName)

def getSurvey(urlToken):
    return db.execute("select * from survey_urls as a left join groupset b on a.GroupsetId = b.id where a.urlname = ?", urlToken)

def getSurveyUrlbasedOnGroupsetId():
    return db.execute("select groupset.id, groupset.groupset_name, survey_urls.urlname from groupset join survey_urls on survey_urls.GroupsetId = groupset.id order by groupset.id")

def getSurveyByToken(urlToken):
    groupsetResult = getSurvey(urlToken)
    queryResult = db.execute("select qs.* from groupset as g left join set_question as sq on g.id = sq.groupset_id left join questionset as qs on qs.id = sq.questionset_id where g.id = ?;", groupsetResult[0]['GroupsetId'])
    return queryResult

def responseDbSave(data):
    for item in data:
        try:
            db.execute("INSERT INTO responseSet (response, questionId, timex, token) VALUES (?,?,?,?)", item['answer'], item['questionId'], datetime.now(), item['token'])
        except ConnectionError:
            raise RuntimeError('Failed to open database')


def qra_getArray(tokenX):
    res1 = db.execute("select questionId from responseSet where token = ? group by questionId", tokenX)
    array1 = []
    for item in res1:
        array1.append(item['questionId'])
        
    return array1

def qra_getResultsSurvey(array1, token):
    r = []
    for item in array1:
        q = db.execute("select questionset.id, questionset.questionset_question as question1, responseSet.response, count(responseSet.response) as count,  responseSet.token \
from questionset join responseSet on responseSet.questionId = questionset.id where responseSet.questionid = ? \
and responseSet.token = ? group by responseSet.response;", item, token)
        r.append(q)
        
    return r