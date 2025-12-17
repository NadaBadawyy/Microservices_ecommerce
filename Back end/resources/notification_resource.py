from flask import request
from flask_restful import Resource
from services.notification_service import NotificationService

class NotificationSendResource(Resource):
    def post(self):
        data = request.get_json()
        order_id = data.get('order_id')
        
        if not order_id:
            return {'message': 'Missing order_id'}, 400
            
        success, msg = NotificationService.send_notification(order_id)
        if success:
            return {'message': msg}, 200
        return {'message': msg}, 500 