# -*- coding: utf-8 -*-


import json
from datetime import datetime

import urllib.request
import urllib.parse

q = '' # free text filter.
fq = '' # advance filters

def search( query):

	solr = 'http://18.222.230.12:8984/solr/IRF18P1/select?wt=json'

	month_first = True
	fl = 'id tweet_lang source tweet_text topic city text tweet_date hashtags'

	
	qfilter = query;
	# free text
	if qfilter['query']:
		solr +=  '&q='+qfilter['query']
	else:
		solr +=  '&q=*'

	#specific filters

	if qfilter['topic_f']:
		solr +=  '&fq=topic:' + qfilter['topic_f']

	if qfilter['city_f']:
		solr +=  '&fq=city:' + qfilter['city_f']

	if qfilter['lang_f']:
		solr +=  '&fq=tweet_lang:' + qfilter['lang_f']

	if qfilter['date_f1']:
		solr +=  '&fq=tweet_date:' + urllib.parse.quote('[' +qfilter['date_f1'] +' TO ' + qfilter['date_f2'] + ']')


	if qfilter['start']:
		solr +=  '&start=' + qfilter['start']

	if qfilter['rows']:
		solr +=  '&rows=' + qfilter['rows']
	
		# append the response set
	fl = urllib.parse.quote(fl)
	solr += '&fl='+fl
	
	# print (solr)
	result = urllib.request.urlopen(solr)

	data =  json.load(result)['response']	
	return data

	# return json.load(result)['response']

# call function like this

# dic = {'query': '', 'lang_f': 'en', 'topic_f': 'politics',
#            'city_f': 'nyc', 'date_f1':'2018-08-08T00:00:00Z' , 'date_f2': 'NOW', 'start':'0' , 'rows':'15'}
# data = search(dic)

# for dat in data['docs']:
		# print (dat)
