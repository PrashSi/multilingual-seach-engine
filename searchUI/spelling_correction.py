import re
from textblob import TextBlob
import json
from pprint import pprint

def spelling_correction(input):
	b = TextBlob(input)
	


if __name__ == "__main__":
	# calling main function
	# select our need language
	input = 'fr'
	api = TwitterClient(input)
	final = api.get_tweets()
	# already 
	pprint(final)