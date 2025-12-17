from flask_restful import Resource
from Models import Pricing

class PricingListResource(Resource):
    def get(self):
        return [
            {"product_id": p.product_id, "price": p.price}
            for p in Pricing.query.all()
        ]
