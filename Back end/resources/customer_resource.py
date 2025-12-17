from flask_restful import Resource, reqparse
from services.customer_service import CustomerService

class CustomerListResource(Resource):
    def get(self):
        customers = CustomerService.get_all_customers()
        return [{'id': c.id, 'name': c.name, 'email': c.email, 'phone': c.phone} for c in customers]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help="Name is required")
        parser.add_argument('email', required=True, help="Email is required")
        parser.add_argument('phone')
        args = parser.parse_args()

        customer = CustomerService.create_customer(args['name'], args['email'], args['phone'])
        return {'id': customer.id, 'name': customer.name, 'email': customer.email, 'phone': customer.phone}, 201

class CustomerResource(Resource):
    def get(self, customer_id):
        customer = CustomerService.get_customer_by_id(customer_id)
        if customer:
            return {'id': customer.id, 'name': customer.name, 'email': customer.email, 'phone': customer.phone}
        return {'message': 'Customer not found'}, 404

    def put(self, customer_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('email')
        parser.add_argument('phone')
        args = parser.parse_args()

        customer = CustomerService.update_customer(customer_id, args['name'], args['email'], args['phone'])
        if customer:
            return {'id': customer.id, 'name': customer.name, 'email': customer.email, 'phone': customer.phone}
        return {'message': 'Customer not found'}, 404

    def delete(self, customer_id):
        customer = CustomerService.delete_customer(customer_id)
        if customer:
            return {'message': 'Customer deleted'}
        return {'message': 'Customer not found'}, 404