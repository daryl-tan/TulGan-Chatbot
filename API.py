from flask import Flask
from flask_restful import Resource, Api
from Bot import Bot

bot = Bot()
app = Flask(__name__)
api = Api(app)

class Response(Resource):
    def post(self, inpt):
        print(inpt)
        return {"response": bot.respond(inpt)}, 201

class Analysis(Resource):
    def put(self, email):
        bot.sendEmail(email)
        return 201

api.add_resource(Response, '/response/<inpt>')
api.add_resource(Analysis, '/analysis/<email>')

if __name__ == '__main__':
    app.run(debug=True)