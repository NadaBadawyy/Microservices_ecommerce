from Models import Notification
from extensions import db

class NotificationService:

    @staticmethod
    def get_all_notifications():
        return Notification.query.all()

    @staticmethod
    def get_notification_by_id(notification_id):
        return Notification.query.get(notification_id)

    @staticmethod
    def get_notifications_by_customer(customer_id):
        return Notification.query.filter_by(customer_id=customer_id).all()

    @staticmethod
    def create_notification(message, customer_id):
        notification = Notification(message=message, customer_id=customer_id)
        db.session.add(notification)
        db.session.commit()
        return notification

    @staticmethod
    def mark_as_sent(notification_id):
        notification = Notification.query.get(notification_id)
        if notification:
            notification.sent = True
            db.session.commit()
        return notification

    @staticmethod
    def delete_notification(notification_id):
        notification = Notification.query.get(notification_id)
        if notification:
            db.session.delete(notification)
            db.session.commit()
        return notification