from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Model Product: Id, Name, Amount, Price
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'Product {self.name}'

# Endpoints: Base/AllProducts   Base/Status/<Product>   Base/Buy/<Product>/<Amount>

class Products(Resource):
    def get(self):
        return {'message': 'Api works!'}

class Status(Resource):
    def get(self, product_name):
        return {'Product': product_name}

api.add_resource(Products, '/')
api.add_resource(Status, '/Status/<string:product_name>')

if __name__ == '__main__':
    app.run(debug=True)