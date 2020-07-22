from flask import Flask, request
from flask_restful import Resource, Api
from Bot import Bot
import json 

bot = Bot()
app = Flask(__name__)
api = Api(app)

class Response(Resource):
    def post(self):
        print('invoke')
        inpt = request.json['msg']
        return {"response": bot.respond(inpt)}, 201

class Analysis(Resource):
    def post(self):
        email = request.json['email']
        bot.sendEmail(email)
        return {"response":"sent"}, 201

api.add_resource(Response, '/response')
api.add_resource(Analysis, '/analysis')

if __name__ == '__main__':
    app.run(debug=True)