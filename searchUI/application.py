from flask import Flask, abort, redirect, render_template, request
from html import escape
from werkzeug.exceptions import default_exceptions, HTTPException
import json
import all_in_one
import re
from textblob import TextBlob
def spelling(input):
    b = TextBlob(input)
    return str(b.correct())

app = Flask(__name__)


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

    with open("new.json", 'rb') as f:
        data = json.load(f)

    
        
    query = request.form['key_word']
    lang = request.form['lang_f']
    topic = request.form['topic_f']
    city = request.form['city_f']
    date_s = request.form['date_f1']
    date_e = request.form['date_f2']
    facet = request.form['facet_f']
    filters = {'query': query, 'lang_f': lang, 'topic_f': topic, 
            'city_f': city, 'date_f1': date_s, 'date_f2': date_e, 'facet_f': facet}
            
    # results = solr_search(filters)
    results = data

    visual = all_in_one.visualize('new.json', 'figs')
    density, pie = visual.sentiment()
    analytics = {'timeline': visual.timeline(), 'tagcloud': visual.tagcloud(), 
                'density': density, 'pie': pie, 'heatmap': visual.setMap()}
    # analytics = []
    return render_template("search.html", query=query, filters=filters, 
                            results=results, analytics=analytics, sp_corr = spelling(query))


@app.errorhandler(HTTPException)
def errorhandler(error):
    """Handle errors"""
    return render_template("error.html", error=error), error.code

# https://github.com/pallets/flask/pull/2314
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
