from Models import Customer
from extensions import db

class CustomerService:

    @staticmethod
    def get_all_customers():
        return Customer.query.all()

    @staticmethod
    def get_customer_by_id(customer_id):
        return Customer.query.get(customer_id)

    @staticmethod
    def create_customer(name, email, phone=None):
        customer = Customer(name=name, email=email, phone=phone)
        db.session.add(customer)
        db.session.commit()
        return customer

    @staticmethod
    def update_customer(customer_id, name=None, email=None, phone=None):
        customer = Customer.query.get(customer_id)
        if customer:
            if name:
                customer.name = name
            if email:
                customer.email = email
            if phone is not None:
                customer.phone = phone
            db.session.commit()
        return customer

    @staticmethod
    def delete_customer(customer_id):
        customer = Customer.query.get(customer_id)
        if customer:
            db.session.delete(customer)
            db.session.commit()
        return customer