from tensorflow import keras
import pickle

import nltk
from nltk.stem.lancaster import LancasterStemmer

import numpy as np
import pandas as pd
import random

class Bot():
    def __init__(self):
        with open("data.pickle", "rb") as f:
            self.words, self.intents, self.classes = pickle.load(f)
        self.model = keras.models.load_model('model.tflearn')
        self.stemmer = LancasterStemmer()

    def bow(self, sentence, show_details=True):
        # tokenize the pattern
        sentence_words = nltk.word_tokenize(sentence)
        # stem each word - create short form for word
        sentence_words = [self.stemmer.stem(word.lower()) 
        for word in sentence_words]
        # bag of words - matrix of N words, vocabulary matrix

        bag = [0] * len(self.words)
        for s in sentence_words:
            for i, w in enumerate(self.words):
                if w == s:
                   bag[i] = 1
        return pd.DataFrame([np.array(bag)], dtype=float, index=['input'])


    def respond(self, inpt):
        results = self.model.predict(self.bow(inpt))
        results_index = np.argmax(results)
        tag = self.classes[results_index]

        for tg in self.intents["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
                #print(tag, '\n')
                break

        return (random.choice(responses))