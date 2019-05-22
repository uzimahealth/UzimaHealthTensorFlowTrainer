from flask import Flask, request
from flask_restful import Resource, Api
from pickle import load
from numpy import array
from numpy import argmax
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from nltk.translate.bleu_score import corpus_bleu
from keras import backend as K
import json
import requests
from pickle import load
from numpy import array
from numpy import argmax
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from nltk.translate.bleu_score import corpus_bleu

def decodePrediction(prediction, tokenizer):
	integers = [argmax(vector) for vector in prediction]
	target = list()
	for i in integers:

		word = word_for_id(i, tokenizer)
		if word is None:
			break
		target.append(word)
	return ' '.join(target)

# map an integer to a word
def word_for_id(integer, tokenizer):
	for word, index in tokenizer.word_index.items():
		if index == integer:
			return word
	return None

def create_tokenizer(lines):
	tokenizer = Tokenizer()
	tokenizer.fit_on_texts(lines)
	return tokenizer


# load a clean dataset
def load_clean_sentences(filename):
	return load(open(filename, 'rb'))

# encode and pad sequences
def encode_sequences(tokenizer, length, lines):
	# integer encode sequences
	X = tokenizer.texts_to_sequences(lines)
	# pad sequences with 0 values
	X = pad_sequences(X, maxlen=length, padding='post')
	return X

# max sentence length
def max_length(lines):
	return max(len(line.split()) for line in lines)

dataset = load_clean_sentences('english-luo-both.pkl')
eng_tokenizer = create_tokenizer(dataset[:, 0])
ger_tokenizer = create_tokenizer(dataset[:, 1])
ger_length = max_length(dataset[:, 1])

app = Flask(__name__)
api = Api(app)

class LanguageTranslator(Resource):

	def post(self):
		data = request.form['data']
		testX = encode_sequences(ger_tokenizer, ger_length, [data])
		payload = {"instances": testX.tolist()}
		r = requests.post('http://localhost:9000/v1/models/LanguageClassifier:predict', json=payload)
		pred = json.loads(r.content.decode('utf-8'))
		output = (decodePrediction(pred['predictions'][0], eng_tokenizer))
		return {'result': output}

api.add_resource(LanguageTranslator, '/')

if __name__ == '__main__':
    app.run(debug=True,threaded=True)