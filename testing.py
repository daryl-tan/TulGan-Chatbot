from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import time
from html2text import html2text

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
with open('intents.json') as json_data:
    intents = json.load(json_data)

driver.get("http://127.0.0.1:5000/")
textbox = driver.find_element_by_name("user_inpt")

def respond(text):
    assert type(text)==str, "Text has to be a String"
    textbox.send_keys(text)
    textbox.send_keys(Keys.RETURN)
    time.sleep(1)

def check(inpt, tag):
    assert type(tag)==str, "Tag has to be a String"
    assert type(inpt)==str, "Input has to be a String"

    if tag == "context":
        if inpt == "May I enquire which faculty are you referring to?":
            print(tag, "Correct")
            return 1 
        else:
            print(tag, "Incorrect")
            return 0

    for i in intents['intents']:
        if i['tag'] == tag:
            response = html2text(i['responses'][0])
            for r in ["\n", ">", "<"]:
                replacement = " " if r == '\n' else ""
                response = response.replace(r, replacement) 
            print(list(response)[:-2], "\n", list(inpt))
            print("\n")
            if response == inpt:
                print(tag, "Correct")
                return 1
            else:
                print(tag, "Incorrect")
                return 0

respond("What is the graduation requirements")
respond("Computing")
respond("What are the specialization available in computer science")
respond("What are the specialization available in business analytics")
respond("What are the degree offered by nus computing")
respond("How many modular credits is required for a major?")
respond("What is the outcome of my application")

tags = ["ComCurriculum", "context", "ComSci", "BZA",
"ComCourses", "major", "Application_Outcome"]

replies = driver.find_elements_by_id("botmsg")
responses = zip(tags, replies)

count = 0
for tag, response in responses:
    print(response.text)
    count += check(response.text, tag)
print("Total Number of Correct Respones: " + str(count) + " / 7")