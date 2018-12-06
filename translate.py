import re
from textblob import TextBlob
import json
from pprint import pprint

class TwitterClient():
	def __init__(self, language):
		self.language = language

	def get_tweets(self):
		tweets=[]
		data = {}
		with open('new.json') as f:
			tweets = json.load(f)

		for i in range(len(tweets)):
			new = tweets[i]['tweet_text']
			lan = TextBlob(str(new))
			final = lan.translate(from_lang = lan.detect_language(), to = self.language)
			tweets[i]['tweet_text'] = str(final)
		return tweets


	# def translate(self):
	# 	tweets=self.get_tweets()
	# 	print(tweets)
if __name__ == "__main__":
	# calling main function
	# select our need language
	input = 'fr'
	api = TwitterClient(input)
	final = api.get_tweets()
	# already 
	pprint(final)