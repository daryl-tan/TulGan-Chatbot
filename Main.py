from flask import Flask, render_template, request
from Bot import Bot

bot = Bot()
app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
	user_inpt = request.form["user_inpt"]
	bot_response = bot.respond(user_inpt)
	return render_template('index.html', 
		user_inpt=user_inpt, bot_response=bot_response)

if __name__ == "__main__":
	app.run(debug=True, port=5002)