from flask_restful import Resource, reqparse
from services.order_service import OrderService
from services.pricing_service import PricingService
from services.inventory_service import InventoryService

parser = reqparse.RequestParser()
parser.add_argument("product_id", type=int, required=True)
parser.add_argument("quantity", type=int, required=True)

class OrderResource(Resource):

    def post(self):
        args = parser.parse_args()

        total_price = PricingService.calculate_price(
            args["product_id"], args["quantity"]
        )

        InventoryService.reduce_stock(
            args["product_id"], args["quantity"]
        )

        order = OrderService.create_order(
            args["product_id"], args["quantity"], total_price
        )

        return {
            "order_id": order.id,
            "total_price": order.total_price
        }, 201
