import nltk
import os
import numpy as np
import random
import requests
import string # to process standard python strings

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request


app = Flask(__name__)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

@app.route('/')
def hello_world():
	return 'Hello, World!'

messages = []

@app.route('/talk/', methods=['GET', 'POST'])
def talk():
	if request.method=='POST':
		user_response=request.form['userinput']
		messages.append((user_response, 'user'))
		user_response=user_response.lower()
		if(user_response!='bye'):
			if(user_response=='thanks' or user_response=='thank you'):
				flag=False
				response_msg='ROBO: You are welcome!'
			else:
				if(greeting(user_response)!=None):
					response_msg='ROBO: '+greeting(user_response)
				else:
					response_msg = response(user_response)
					sent_tokens.remove(user_response)
		else:
			flag=False
			response_msg='ROBO: Bye! Take care'
		messages.append((response_msg, 'bot'))

	return render_template('index.html', r=messages)

f=open('chatbot.txt', 'r', errors='ignore')

raw=f.read()
raw=raw.lower()
# print(raw)

nltk.download('punkt')
nltk.download('wordnet')

sent_tokens=nltk.sent_tokenize(raw) # converts to list of sentences 
word_tokens=nltk.word_tokenize(raw) # converts to list of words

# print(sent_tokens[:2])
# print(word_tokens[:2])

lemmer=nltk.stem.WordNetLemmatizer() #WordNet is a semantically-oriented dictionary of English included in NLTK.

# print(string.punctuation)

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
# print('Kevin georg"e ab!dsaf& &ham'.lower().translate(remove_punct_dict))

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)

GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
	for word in sentence.split():
		if word.lower() in GREETING_INPUTS:
			return random.choice(GREETING_RESPONSES)

def response(user_response):
	robo_response=''
	sent_tokens.append(user_response)

	TfidfVec=TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
	tfidf=TfidfVec.fit_transform(sent_tokens)
	vals=cosine_similarity(tfidf[-1], tfidf)
	idx=vals.argsort()[0][-2]
	flat=vals.flatten()
	flat.sort()
	req_tfidf=flat[-2]

	if(req_tfidf==0):
		robo_response=robo_response+'I am sorry! I don\'t understand you'
		return robo_response
	else:
		robo_response=robo_response+sent_tokens[idx]
		return robo_response

flag=True
print('ROBO: My name is ROBO. I will answer your queries about Chatbots. If you want to exit, type Bye!')

# while(flag==True):
	# print('hello')
	# user_response=input()
	# user_response=user_response.lower()
	# if(user_response!='bye'):
	# 	if(user_response=='thanks' or user_response=='thank you'):
	# 		flag=False
	# 		print('ROBO: You are welcome!')
	# 	else:
	# 		if(greeting(user_response)!=None):
	# 			print('ROBO: '+greeting(user_response))
	# 		else:
	# 			print('ROBO:', end='')
	# 			print(response(user_response))
	# 			sent_tokens.remove(user_response)
	# else:
	# 	flag=False
	# 	print('ROBO: Bye! Take care')
