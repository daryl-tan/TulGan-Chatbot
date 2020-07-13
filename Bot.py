from tensorflow import keras
import pickle

import nltk
from nltk.stem.lancaster import LancasterStemmer
import json
import csv

import numpy as np
import pandas as pd
import random
from DataManager import DataManager

class Bot():
    def __init__(self):
        with open("data.pickle", "rb") as files:
            self.words, self.intents, self.classes = pickle.load(files)
        with open("entity.json", "rb") as entities:
            self.entity = json.load(entities)
        self.model = keras.models.load_model('model.tflearn')
        self.stemmer = LancasterStemmer()
        self.context = None
        self.settingContext = False
        self.previous = None
        self.dataManager = DataManager()

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

    def isContextualize(self, inpt):
        inpt_words = nltk.word_tokenize(inpt)
        inpt_words = [word.lower() for word in inpt_words]
        for word in inpt_words:
            for entity, var in self.entity.items():
                if word in var:
                    self.context = entity
                    return False
        return True
            
    def respond(self, inpt):
        assert type(inpt) == str, "Input parameter must be String for respond."
        THRESHOLD = 0.7

        if self.settingContext and self.previous and self.context == None:
            return self.contextualize(inpt)
        
        result = self.classify(inpt)
        if result[1] < THRESHOLD:
            result[0] = "noanswer"
  
        for i in self.intents['intents']:
            if i['tag'] == result[0]:

                if 'context_cond' in i and self.context == None and self.isContextualize(inpt):
                    self.settingContext = True
                    self.previous = inpt
                    return "May I enquire which faculty are you referring to?" 
                
                if 'context_set' in i:
                    self.context = i['context_set']
                    self.dataManager.store(inpt, result[0])
                    return (random.choice(i['responses']))

                elif not 'context_cond' in i:
                    self.dataManager.store(inpt, result[0])
                    return (random.choice(i['responses']))
                
                elif ('context_cond' in i and i['context_cond'][0] == self.context):
                    self.previous = None
                    self.dataManager.store(inpt, result[0])
                    return (random.choice(i['responses']))

    def classify(self, inpt):
        results = self.model.predict([self.bow(inpt)])[0]
        results = [[i, r] for i, r in enumerate(results)]
        results.sort(key=lambda x: x[1], reverse = True)
        answer = [self.classes[results[0][0]], results[0][1]] 
        return answer

    def sendEmail(self, TO):
        assert type(TO) == str, "Input parameter must be String for respond."
        self.dataManager.sendEmail(TO)