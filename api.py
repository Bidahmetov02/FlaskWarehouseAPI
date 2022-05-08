from re import A
from unicodedata import name
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Model Product: Id, Name, Amount, Price

class Main(Resource):
    def get(self):
        return {'message': 'Api works!'}

api.add_resource(Main, '/')

if __name__ == '__main__':
    app.run(debug=True)