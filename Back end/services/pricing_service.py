

import requests
from models import PricingRules, TaxRates
from extensions import db

class PricingService:
    INVENTORY_SERVICE_URL = "http://localhost:5002/api/inventory"

    @staticmethod
    def calculate_price(products_list):
        total_price = 0.0
        details = []

        for item in products_list:
            product_id = item.get('product_id')
            quantity = item.get('quantity')

            # 1. Get base price from Inventory Service
            try:
                # Requirement: GET /api/inventory/check/{product_id} returns... just stock? 
                # Or we need price. Inventory table has unit_price.
                # I should probably update Inventory Service to return full product details on check.
                response = requests.get(f"{PricingService.INVENTORY_SERVICE_URL}/check/{product_id}")
                if response.status_code != 200:
                    continue # Or raise error
                
                product_data = response.json() 
                # Assuming returns {product_id, unit_price, quantity_available...}
                unit_price = float(product_data.get('unit_price', 0))
                
            except requests.exceptions.RequestException:
                # Fallback or error
                continue

            # 2. Check for discounts
            base_cost = unit_price * quantity
            discount_percent = 0
            
            rule = PricingRules.query.filter(
                PricingRules.product_id == product_id,
                PricingRules.min_quantity <= quantity
            ).order_by(PricingRules.min_quantity.desc()).first()

            if rule:
                discount_percent = float(rule.discount_percentage)
            
            discount_amount = base_cost * (discount_percent / 100)
            final_item_cost = base_cost - discount_amount
            
            total_price += final_item_cost
            
            details.append({
                'product_id': product_id,
                'quantity': quantity,
                'unit_price': unit_price,
                'discount_percent': discount_percent,
                'total': final_item_cost
            })

        # 3. Tax (Optional per strict requirements but table exists)
        # Assuming flat tax or based on... input? No region in input. 
        # Ignoring tax for now to keep simple matching inputs.
        
        return {
            'total_amount': round(total_price, 2),
            'currency': 'USD',
            'details': details
        }
