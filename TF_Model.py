import json
import random
import pickle
import pandas as pd
from keras.optimizers import SGD
from keras.layers import Dense, Dropout
from keras.models import Sequential
import numpy as np
import nltk
from nltk.stem.lancaster import LancasterStemmer

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

stemmer = LancasterStemmer()

with open('intents.json') as json_data:
    intents = json.load(json_data)

words = []
classes = []
docs = []

# loop through each sentence in our intents patterns
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        w = nltk.word_tokenize(pattern)
        # add to our words list
        words.extend(w)
        # add to docs in our corpus
        docs.append((w, intent['tag']))
        # add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# stem and lower each word and remove duplicates
words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

# sort classes
classes = sorted(list(set(classes)))

# create our training data
training = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in docs:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stem each word - create base word, in attempt to represent related words
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create our bag of words array with 1, if word match found in current pattern
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # output is a '0' for each tag and '1' for current tag (for each pattern)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)

# create train and test lists. X - patterns, Y - intents
train_x = list(training[:, 0])
train_y = list(training[:, 1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd, metrics=['accuracy'])


model.fit(np.array(train_x), np.array(train_y),
          epochs=1000, batch_size=5, verbose=1)
model.save("model.tflearn")


with open("data.pickle", "wb") as f:
    pickle.dump((words, intents, classes), f)
