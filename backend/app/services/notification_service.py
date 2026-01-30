from app import db
from app.models import Notification, Member
from datetime import datetime, timezone

class NotificationService:
    """ Сервис для работы с уведомлениями """

    @staticmethod
    def send_like_notification(liker_id, target_type, target_id, target_owner_id):
        ''' Уведомление о лайке '''

        if liker_id == target_owner_id:
            return None
        
        liker = Member.query.get(liker_id)
        if not liker:
            return None
        
        notification_type = f'like_{target_type}'

        titles = {
            'post': 'Новый лайк на вашем посте',
            'comment': 'Ваш комментарий оценили',
            'product': 'Кто-то заинтересовался вашим объявлением'
        }

        title = titles.get(target_type, 'Новый лайк')

        notification = Notification(
            user_id=target_owner_id,
            notification_type=notification_type,
            title=title,
            message=f'Пользователь {liker.username} поставил лайк вашему {target_type}',
            target_type=target_type,
            target_id=target_id,
            metadata={
                'liker_id': liker_id,
                'liker_username': liker.username
            }
        )

        db.session.add(notification)
        db.session.commit()

        return notification
    
    @staticmethod
    def send_admin_report(user_id, admin_id, target_type, target_id, reason, action_taken=None):
        ''' Отправить уведомление о жалобе от администратора '''

        admin = Member.query.get(admin_id)
        if not admin:
            return None
        
        target_info = {} # TODO: получение деталей

        notification = Notification(
            user_id=user_id,
            notification_type='admin_report',
            title='Жалоба на контент',
            message=f'Администратор {admin.username} оставил жалобу на ваш {target_type}. Причина: {reason}',
            target_type=target_type,
            target_id=target_id,
            priority='high',
            admin_id=admin_id,
            metadata={
                'reason': reason,
                'action_taken': action_taken,
                'admin_username': admin.username,
                'target_info': target_info
            }
        )

        db.session.add(notification)
        db.session.commit()

        return notification
    
    @staticmethod
    def send_admin_broadcast(user_id, admin_id, title, message, priority='normal'):
        ''' Отправить админское уведомление '''

        admin = Member.query.get(admin_id)

        notification = Notification(
            user_id=user_id,
            notification_type='admin_broadcast',
            title=title,
            message=message,
            target_type='admin',
            priority=priority,
            admin_id=admin_id,
            metadata={
                'admin_username': admin.username if admin else 'Администрация'
            }
        )

        db.session.add(notification)
        db.session.commit()

        return notification
    
    @staticmethod
    def get_unread_count(user_id):
        ''' Получить кол-во непрочитанных сообщений '''
        return Notification.query.filter_by(
            user_id=user_id,
            is_read=False,
            is_archived=False
        ).count()