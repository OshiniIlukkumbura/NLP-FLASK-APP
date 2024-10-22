from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import flask
import pickle
import pandas as pd
import numpy as np
import nltk
import string
import re


# Use pickle to load in the pre-trained model.
with open(f'model/twitter_predictions.pkl', 'rb') as f:
    model = pickle.load(f)


with open(f'model/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)


# Removing URLs
def remove_url(text):
    return re.sub(r"http\S+", "", text)

# Removing Punctuations


def remove_punct(text):
    new_text = []
    for t in text:
        if t not in string.punctuation:
            new_text.append(t)
    return ''.join(new_text)


# Tokenizer
tokenizer = RegexpTokenizer(r'\w+')


# Removing Stop words


def remove_sw(text):
    new_text = []
    for t in text:
        if t not in stopwords.words('english'):
            new_text.append(t)
    return new_text


# Lemmatizaion

lemmatizer = WordNetLemmatizer()


def word_lemmatizer(text):
    new_text = []
    for t in text:
        lem_text = lemmatizer.lemmatize(t)
        new_text.append(lem_text)
    return new_text


app = flask.Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def index():

    if flask.request.method == 'GET':
        return (flask.render_template('index.html'))

    if flask.request.method == 'POST':

        tweet = flask.request.form['tweet']

        df = pd.DataFrame([tweet], columns=['tweet'])

        df['tweet'] = df['tweet'].apply(lambda t: remove_url(t))

        df['tweet'] = df['tweet'].apply(lambda t: remove_punct(t))

        df['tweet'] = df['tweet'].apply(
            lambda t: tokenizer.tokenize(t.lower()))

        df['tweet'] = df['tweet'].apply(lambda t: remove_sw(t))

        df['tweet'] = df['tweet'].apply(lambda t: word_lemmatizer(t))

        final_text = df['tweet']

        final_text.iloc[0] = ' '.join(final_text.iloc[0])

        final_text = vectorizer.transform(final_text)

        prediction = model.predict(final_text)

        return flask.render_template('index.html', result=prediction, original_input={'Mobile Review': tweet})


if __name__ == '__main__':
    app.run()


# import flask

# app = flask.Flask(__name__)

# @app.route('/')
# def index():
#  return "<h1>Hello World</h1>"
# import flask
# import pickle

# #Use pickle to load in the pre-trained model.

# with open(f'model/twitter_predictions.pkl', 'rb') as f:
#     model = pickle.load(f)

# with open(f'model/vectorizer.pkl', 'rb') as f:
#     vectorizer = pickle.load(f)

# app = flask.Flask(__name__, template_folder='templates')

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     return "<h1>Hello World</h1>"

# import flask

# # Use pickle to load in the pre-trained model.
# with open(f'model/twitter_predictions.pkl', 'rb') as f:
#     model = pickle.load(f)

# with open(f'model/vectorizer.pkl', 'rb') as f:
#     vectorizer = pickle.load(f)

# app = flask.Flask(__name__, template_folder='templates')


# @app.route('/', methods=['GET', 'POST'])
# def index():

#     if flask.request.method == 'GET':
#         return (flask.render_template('index.html'))

#     if flask.request.method == 'POST':

#         tweet = flask.request.form['tweet']
