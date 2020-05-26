from tensorflow import keras
import pickle

import nltk
from nltk.stem.lancaster import LancasterStemmer

import numpy as np
import pandas as pd
import random
from datetime import date
import matplotlib
import plotly.express as px

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Bot():
    def __init__(self):
        with open("data.pickle", "rb") as f:
            self.words, self.intents, self.classes = pickle.load(f)
        self.model = keras.models.load_model('model.tflearn')
        self.stemmer = LancasterStemmer()
        self.context = []

    def bow(self, inpt):
        # tokenize the pattern
        inpt_words = nltk.word_tokenize(inpt)
        # stem each word - create short form for word
        inpt_words = [self.stemmer.stem(word.lower())
                      for word in inpt_words]
        # bag of words - matrix of N words, vocabulary matrix
        bag = [0] * len(self.words)
        for s in inpt_words:
            for i, w in enumerate(self.words):
                if w == s:
                    bag[i] = 1
        return pd.DataFrame([np.array(bag)], dtype=float, index=['input'])

    def classify(self, inpt):
        results = self.model.predict([self.bow(inpt)])[0]
        results = [[i, r] for i, r in enumerate(results) if r > 0.5]
        results.sort(key=lambda x: x[1], reverse=True)
        lst = []
        for r in results:
            lst.append((self.classes[r[0]], r[1]))
        return lst

    def respond(self, inpt):
        results = self.classify(inpt)
        while results:
            for i in self.intents['intents']:
                if i['tag'] == results[0][0]:
                    if 'context_set' in i:
                        self.context.append(i['context_set'])

                    if not 'context_cond' in i or \
                            ('context_cond' in i and i['context_cond'] in self.context):
                        self.store(inpt, results[0][0])
                        return (random.choice(i['responses']))

            results.pop(0)

    def store(self, inpt, tag):
        row = {
                "Date": date.today(),
                "Query": inpt,
                "Tag": tag,
                "Relevant": True
            }
        try:
            df = pd.read_csv('data/data.csv')
            df = df.append(row, ignore_index=True)
        except:
            df = pd.DataFrame(row, index=[0])
        df.to_csv('data/data.csv', index=False)

    def sendEmail(self):
        FROM = "wtvdummyacc@gmail.com"
        TO = "myfriend@example.com"

        msg = MIMEMultipart('alternative')
        msg['From'] = FROM
        msg['To'] = TO
        msg['Subject'] = "Automatic Weekly Report"
        html = open("data/fig.html")
        file = MIMEText(html.read(), 'html')
        msg.attach(file)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(FROM, "Dummy2020")
        server.sendmail(FROM, TO, msg.as_string())
        server.quit()
 
    def analyze(self):
        try:
            df = pd.read_csv('data/data.csv')
            df_tag = df[["Tag", "Query"]] \
                .groupby('Tag') \
                .count() \
                .head(10)
            fig = px.bar(df_tag, x=df_tag.index, y="Query")
            fig.update_yaxes(dtick=1)
            fig.update_xaxes(title_text="Tag")
            fig.update_layout(title_text="Query Analysis")
            fig.write_html("data/fig.html")
        except:
            pass

