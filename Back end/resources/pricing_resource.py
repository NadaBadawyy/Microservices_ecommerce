from flask import request
from flask_restful import Resource
from services.pricing_service import PricingService

class PricingCalculateResource(Resource):
    def post(self):
        data = request.get_json()
        if not data or 'products' not in data:
            return {'message': 'Invalid input, products list required'}, 400
            
        products = data['products']
        result = PricingService.calculate_price(products)
        return result, 200
