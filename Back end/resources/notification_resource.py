from flask_restful import Resource, reqparse
from services.notification_service import NotificationService

class NotificationListResource(Resource):
    def get(self):
        notifications = NotificationService.get_all_notifications()
        return [{'id': n.id, 'message': n.message, 'customer_id': n.customer_id, 'sent': n.sent} for n in notifications]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('message', required=True, help="Message is required")
        parser.add_argument('customer_id', type=int, required=True, help="Customer ID is required")
        args = parser.parse_args()

        notification = NotificationService.create_notification(args['message'], args['customer_id'])
        return {'id': notification.id, 'message': notification.message, 'customer_id': notification.customer_id, 'sent': notification.sent}, 201

class NotificationResource(Resource):
    def get(self, notification_id):
        notification = NotificationService.get_notification_by_id(notification_id)
        if notification:
            return {'id': notification.id, 'message': notification.message, 'customer_id': notification.customer_id, 'sent': notification.sent}
        return {'message': 'Notification not found'}, 404

    def put(self, notification_id):
        parser = reqparse.RequestParser()
        parser.add_argument('sent', type=bool)
        args = parser.parse_args()

        if args['sent'] is not None:
            notification = NotificationService.mark_as_sent(notification_id)
            if notification:
                return {'id': notification.id, 'message': notification.message, 'customer_id': notification.customer_id, 'sent': notification.sent}
        return {'message': 'Notification not found'}, 404

    def delete(self, notification_id):
        notification = NotificationService.delete_notification(notification_id)
        if notification:
            return {'message': 'Notification deleted'}
        return {'message': 'Notification not found'}, 404

class CustomerNotificationsResource(Resource):
    def get(self, customer_id):
        notifications = NotificationService.get_notifications_by_customer(customer_id)
        return [{'id': n.id, 'message': n.message, 'customer_id': n.customer_id, 'sent': n.sent} for n in notifications]