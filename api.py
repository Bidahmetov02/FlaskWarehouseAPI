from flask import Flask
from flask_restful import Resource, Api, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from request_parsers import create_product_args, update_product_args

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://picktmdg:W_USRUDLLBPJ03s4RCUyuaxLLxnRm5IU@dumbo.db.elephantsql.com/picktmdg'
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

def Get_product_by_name_or_abort(name):
    product = Product.query.filter_by(name = name).first()
    if not product:
        return abort(http_status_code=404, message=f"Product with the name {name} doesn't exist")
    return product

# Endpoints: Base/AllProducts   Base/Status/<Product>   Base/Buy/<Product>/<Amount>
class Info(Resource):
    def get(self):
        return {
            'Required Funtionality Endpoints': {
                'GET All Products': '[Base_URL]/AllProducts',
                'GET Check Status': '[Base_URL]/Status/<Product_Name>',
                'GET Buy Products': '[Base_URL]/Buy/<Product_Name>/<Amount>',
            },
            'Additional Functionality Endpoints': {
                'POST Create Product': {
                    'URL': '[Base_URL]/CreateProduct',
                    'Required Arguments': 'Body: name, amount, price'
                },
                'POST Update Product': {
                    'URL': '[Base_URL]/ModifyProduct/<Product_Name>',
                    'Required Arguments': 'Body: Field to be updated (name, amount, price)'
                },
                'DELETE Delete Product': {
                    'URL': '[Base_URL]/ModifyProduct/<Product_Name>',
                }
            }
        }

class Products(Resource):
    @marshal_with(ProductSerializer)
    def get(self):
        resProducts = Product.query.all()
        return resProducts

class Status(Resource):
    def get(self, product_name):
        resProduct = Get_product_by_name_or_abort(product_name)
        return {"Product": resProduct.name, "Amount Available": resProduct.amount}

class BuyProduct(Resource):
    def get(self, product_name, amount):
        product = Get_product_by_name_or_abort(product_name)

        if amount > product.amount:
            abort(http_status_code=404, message=f'Not enough product amount in the shop. Available amount: {product.amount}')

        product.amount -= amount
        db.session.commit()
         
        cost = amount * product.price
        cost += cost * 0.30

        return {'message': f"{amount} {product.name}'s was purchased. Cost is calculated with 30% comission)",
                'cost': cost
        }

class CreateProduct(Resource):
    @marshal_with(ProductSerializer)
    def post(self):
        args = create_product_args.parse_args()

        existingProductList = Product.query.filter_by(name = args['name']).all()
        if len(existingProductList) > 0:
            abort(http_status_code=409, message=f"Product with the name {args['name']} already exists")

        newProduct = Product(name = args['name'], amount = args['amount'], price = args['price'])
        db.session.add(newProduct)
        db.session.commit()
        return newProduct, 201


class UpdateOrDeleteProduct(Resource):
    @marshal_with(ProductSerializer)
    def post(self, product_name):
        args = update_product_args.parse_args()
        product = Get_product_by_name_or_abort(product_name)
        
        if args['name'] == None and args['amount'] == None and args['price'] == None:
            abort(http_status_code=404, message="Any of the required filds are not specified.")

        if args['name']:
            product.name = args['name']
        if args['amount']:
            product.amount = args['amount']
        if args['price']:
            product.price = args['price']
        
        db.session.commit()
        return product

    def delete(self, product_name):
        product = Get_product_by_name_or_abort(product_name)
        db.session.delete(product)
        db.session.commit()
        return {'message': "Product deleted succesfully!"}, 204
    

api.add_resource(Info, '/')
api.add_resource(BuyProduct, '/Buy/<string:product_name>/<int:amount>')
api.add_resource(Products, '/AllProducts')
api.add_resource(Status, '/Status/<string:product_name>')
# Additional
api.add_resource(CreateProduct, '/CreateProduct')
api.add_resource(UpdateOrDeleteProduct, '/ModifyProduct/<string:product_name>')

if __name__ == '__main__':
    app.run(debug=True)