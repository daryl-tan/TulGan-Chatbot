from tensorflow import keras
import pickle

import nltk
from nltk.stem.lancaster import LancasterStemmer

import csv
import numpy as np
import pandas as pd
import random
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class Bot():
    def __init__(self):
        with open("data.pickle", "rb") as f:
            self.words, self.intents, self.classes = pickle.load(f)
        self.model = keras.models.load_model('model.tflearn')
        self.stemmer = LancasterStemmer()
        self.context = None
        self.settingContext = False
        self.entity = {'Com': ["com"]}
        self.previous = None

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

    def contextualize(self, inpt):
        inpt_words = nltk.word_tokenize(inpt)
        inpt_words = [word.lower() for word in inpt_words]
        for word in inpt_words:
            for entity, var in self.entity.items():
                if word in var:
                    self.context = entity
                    self.settingContext = False 
                    return self.respond(self.previous)

    def respond(self, inpt):
        if self.settingContext and self.previous and self.context == None:
            print(1)
            return self.contextualize(inpt)
        
        results = self.classify(inpt)
        while results:
            for i in self.intents['intents']:
                if i['tag'] == results[0][0]:
                    print(results[0])
                    if 'context_set' in i and self.context == None:
                        self.settingContext = True
                        self.previous = inpt
                        return (random.choice(i['responses']))

                    elif not 'context_cond' in i and  not 'context_set' in i:
                        self.store(inpt, results[0][0])
                        return (random.choice(i['responses']))
                    
                    elif ('context_cond' in i and i['context_cond'] == self.context):
                        self.previous = None
                        self.store(inpt, results[0][0])
                        return (random.choice(i['responses']))

            results.pop(0)

    def classify(self, inpt):
        results = self.model.predict([self.bow(inpt)])[0]
        results = [[i, r] for i, r in enumerate(results)]
        results.sort(key=lambda x: x[1], reverse=True)
        lst = []
        for r in results:
            lst.append((self.classes[r[0]], r[1]))
        return lst

    # def answer(self, inpt):
    #     results = self.classify(inpt)
    #     while results:
    #         for i in self.intents['intents']:
    #             if i['tag'] == results[0][0]:
    #                 if 'context_set' in i:
    #                     self.context.append(i['context_set'])

    #                 if not 'context_cond' in i or ('context_cond' in i and i['context_cond'] in self.context):
    #                     self.store(inpt, results[0][0])
    #                     return (random.choice(i['responses']))

    #         results.pop(0)

    def store(self, inpt, tag):
        row = {
                "Date": date.today(),
                "Query": inpt,
                "Tag": tag,
                "Relevant": True
            }
        try:
            with open('data/data.csv', 'a') as file:
                csv.writer(file).writerow(list(row.values()))
        except:
            df = pd.DataFrame(row, index=[0])
            df.to_csv('data/data.csv', index=False)

    def sendEmail(self):
        FROM = "wtvdummyacc@gmail.com"
        TO = input("Please enter your email: ")
        self.analyze()
        
        data = MIMEMultipart()
        data['From'] = FROM
        data['To'] = TO
        data['Subject'] = "Query Analysis"
        body = f"Query Analysis as of {date.today()}"

        data.attach(MIMEText(body, 'plain'))
        filename = "fig.png"
        attachment = open("data/fig.png", "rb")

        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        data.attach(p)

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(FROM, "Dummy2020")
        s.sendmail(FROM, TO, data.as_string())
        s.quit()
 
    def analyze(self):
        df = pd.read_csv('data/data.csv')
        df_tag = df[["Tag", "Query"]] \
            .groupby('Tag') \
            .count() \
            .head(10)
        sns.set()
        plt.bar(x=df_tag.index, height=df_tag.Query)
        plt.xlabel('Tag')
        plt.ylabel('Frequency of Query')
        plt.title('Query Analysis')
        plt.savefig('data/fig.png')