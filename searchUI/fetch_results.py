# -*- coding: utf-8 -*-


import json
from datetime import datetime
import urllib2
import urllib

q = '' # free text filter.
fq = '' # advance filters



def search( query):

	solr = 'http://localhost:8983/solr/IRF18P1/select?wt=json'

	month_first = True
	fl = 'tweet_lang source tweet_text topic city text tweet_date hashtags'

	
	qfilter = json.loads(query)
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

	# if qfilter['date_f']:
	# 	format = '%m/%d/%Y' if month_first else '%d/%m/%Y'
	# 	now = datetime.combine(datetime.strptime(qfilter['date_f'], format).date(), time())
	# 	print now
		# solr +=  '&fq=tweet_date:' + qfilter['date_f']
	if qfilter['start']:
		solr +=  '&start=' + qfilter['start']

	if qfilter['rows']:
		solr +=  '&rows=' + qfilter['rows']
	
		# append the response set
	fl = urllib.quote(fl)
	solr += '&fl='+fl
	
	print solr
	result = urllib2.urlopen(solr)

	data =  json.load(result)['response']	
	return data

	# return json.load(result)['response']

# call function like this
data = search('{"query":"*", "topic_f":"politics" , "date_f":"07/27/2012" , "lang_f":"en" , "city_f":"nyc" , "start":"0" , "rows":"15"}' )

for dat in data['docs']:
		print dat
