from Models import Pricing

class PricingService:

    @staticmethod
    def calculate_price(product_id, quantity):
        pricing = Pricing.query.filter_by(product_id=product_id).first_or_404()
        return pricing.price * quantity
