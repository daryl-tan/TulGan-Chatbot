from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import time
from html2text import html2text
from Bot import Bot

bot = Bot()
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
    time.sleep(3)

def check(inpt, tag):
    assert type(tag)==str, "Tag has to be a String"
    assert type(inpt)==str, "Input has to be a String"

    respondedTag = bot.respond(inpt, True)

    if tag == "context" and respondedTag == "May I enquire which faculty are you referring to?":
        print(tag, "Correct\n")
        return 1 
    elif tag == respondedTag:
        print(tag, "Correct\n")
        return 1
    else:
        print(tag, respondedTag, "Incorrect\n")
        return 0

respond("What are the double major offered by nus")
respond("Computing")
respond("What are the specialization available in computer science")
respond("What are the specialization available in business analytics")
respond("What are the degree offered by nus computing")
respond("How many modular credits is required for a major?")
respond("What is the outcome of my application")

tags = ["context", "DoubleMajorOffered", "ComSci", "BZA",
"ComCourses", "major", "Application_Outcome"]

queries = driver.find_elements_by_id("usermsg")
queries = zip(tags, queries)

count = 0
for tag, query in queries:
    print("\n", query.text, "\n")
    count += check(query.text, tag)
print("Total Number of Correct Respones: " + str(count) + " / 7")