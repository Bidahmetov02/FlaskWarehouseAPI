from flask_restful import reqparse

# Arguments for POST request Creating Product
create_product_args = reqparse.RequestParser()
create_product_args.add_argument('name', type=str, help="Name is required! (Name of the product to be crated)", required=True)
create_product_args.add_argument('amount', type=int, help="Amount is required! (Amount of the product to be crated)", required=True)
create_product_args.add_argument('price', type=int, help="Price if required! (Price for one product)", required=True)

# Arguments for POST request Updating Product
update_product_args = reqparse.RequestParser()
update_product_args.add_argument('name', type=str, help="Name is required! (Name of the product to be crated)")
update_product_args.add_argument('amount', type=int, help="Amount is required! (Amount of the product to be crated)")
update_product_args.add_argument('price', type=int, help="Price if required! (Price for one product)")
