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
        print("{}: Correct".format(tag))
        return 1 
    elif tag == respondedTag:
        print("{}: Correct".format(tag))
        return 1
    else:
        print("{}: Incorrect \n Returned: {}".format(tag, respondedTag))
        return 0

respond("What are the double major offered by NUS?")
respond("NUS Computing")
respond("What are the specialization available in computer science?")
respond("What are the specialization available in bussinness analytics?")
respond("What are the degree offered by nus computing?")
respond("How many modular credits is required for a major?")
respond("What is the outcome of my application?")
respond("What are the specialization available in information system?")
respond("Who do I contact for more information on admission?")

tags = ["context", "DoubleMajorOffered", "ComSci", "BZA",
"ComCourses", "Major", "ApplicationOutcome", "InfoSys",
"AdmissionInfo"]

queries = driver.find_elements_by_id("usermsg")
queries = zip(tags, queries)

score = 0
for tag, query in queries:
    print("\n", query.text)
    score += check(query.text, tag)
    
print("\nTotal Number of Correct Respones: {}/{}".format(score, len(tags)))