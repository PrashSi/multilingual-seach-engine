from flask import Flask, abort, redirect, render_template, request
from html import escape
from werkzeug.exceptions import default_exceptions, HTTPException
import json
import all_in_one
import re
import datetime

from textblob import TextBlob
import fetch_results

def spelling(input):
    b = TextBlob(input)
    return str(b.correct())

app = Flask(__name__)

def formatDate(data):
    date = data.split('-')
    if len(date) == 3:

        hour = 0
        minute = 0
        sec = 0

        month = int(date[1])
        year = int(date[0])
        day = int(date[2])

        d = datetime.datetime(year, month, day, hour, minute, sec)
        date = '{:%Y-%m-%dT%H:%M:%SZ}'.format(d)
    else:
        date = 'NOW'
    return date

@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.form['key_word']
    lang = request.form['lang_f']
    topic = request.form['topic_f']
    city = request.form['city_f']
    date_s = formatDate(request.form['date_f1'])
    if date_s == 'NOW':
        date_s = '*'
    date_e = formatDate(request.form['date_f2'])
    filters = {'query': query, 'lang_f': lang, 'topic_f': topic, 
            'city_f': city, 'date_f1': date_s, 'date_f2': date_e, 'start': '0', 'rows': '15'}

    # results = []
    results = fetch_results.search(filters)
    visual = all_in_one.visualize('new.json', 'figs')
    density, pie = visual.sentiment()
    # analytics = {'timeline': visual.timeline(), 'tagcloud': visual.tagcloud(), 
                # 'density': density, 'pie': pie, 'heatmap': visual.setMap()}
    analytics = []
    return render_template("search.html", query=query, filters=filters, 
                            results=results['docs'], analytics=analytics, sp_corr = spelling(query))


@app.errorhandler(HTTPException)
def errorhandler(error):
    """Handle errors"""
    return render_template("error.html", error=error), error.code

# https://github.com/pallets/flask/pull/2314
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
