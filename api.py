from email import message
from unicodedata import name
from flask import Flask
from flask_restful import Resource, Api, abort, fields, marshal_with, reqparse
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

    def __init__(self, name, amount, price):
        self.name = name
        self.amount = amount
        self.price = price

    def __repr__(self):
        return f'Product {self.name}'

# Serializers
ProductSerializer = {
    'id': fields.Integer,
    'name': fields.String,
    'amount': fields.Integer,
    'price': fields.Float
}

# Arguments for POST request Creating Product
create_product_args = reqparse.RequestParser()
create_product_args.add_argument('name', type=str, help="Name is required! (Name of the product to be crated)", required=True)
create_product_args.add_argument('amount', type=int, help="Amount is required! (Amount of the product to be crated)", required=True)
create_product_args.add_argument('price', type=int, help="Price if required! (Price for one product)", required=True)


# Endpoints: Base/AllProducts   Base/Status/<Product>   Base/Buy/<Product>/<Amount>

class Products(Resource):
    @marshal_with(ProductSerializer)
    def get(self):
        resProducts = Product.query.all()
        return resProducts

class Status(Resource):
    def get(self, product_name):
        resProduct = Product.query.filter_by(name = product_name).first_or_404()
        return {"Product": resProduct.name, "Status": resProduct.amount}

class BuyProduct(Resource):
    def get(self, product_name, amount):
        product = Product.query.filter_by(name = product_name).first_or_404()
        if amount > product.amount:
            abort(http_status_code=404, message=f'Not enough product amount in the shop. Available amount: {product.amount}')

        product.amount -= amount
        db.session.commit()
         
        cost = amount * product.price
        cost += cost * 0.30

        return {'message': f'{amount} {product.name} was purchased. Cost: {cost} (30% comission)'}

class CreateProduct(Resource):
    @marshal_with(ProductSerializer)
    def post(self):
        args = create_product_args.parse_args()
        newProduct = Product(name = args['name'], amount = args['amount'], price = args['price'])
        db.session.add(newProduct)
        db.session.commit()
        return newProduct, 201

api.add_resource(BuyProduct, '/Buy/<string:product_name>/<int:amount>')
api.add_resource(Products, '/AllProducts')
api.add_resource(Status, '/Status/<string:product_name>')
api.add_resource(CreateProduct, '/CreateProduct')

if __name__ == '__main__':
    app.run(debug=True)