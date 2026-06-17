from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Notification


def notification_group(user):
    return f"notifications_{user.id}"


def create_notification(user, message):
    if not user or not user.is_authenticated:
        return None

    notification = Notification.objects.create(
        user=user,
        message=message
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        notification_group(user),
        {
            "type": "send_notification",
            "id": notification.id,
            "message": notification.message,
            "created_at": notification.created_at.strftime("%b %d, %Y %I:%M %p"),
        }
    )

    return notification
