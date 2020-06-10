from flask import Flask, render_template, request
from Bot import Bot

bot = Bot()
app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/process")
def process():
	user_inpt = request.args.get('msg') 
	bot_response = bot.respond(user_inpt)
	return str(bot_response)

if __name__ == "__main__":
	app.run()