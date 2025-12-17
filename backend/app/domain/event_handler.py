from domain.event_bus import event_bus
from services.notification_service import NotificationService
import models

notification_service = NotificationService()


def handle_event_created(payload: dict):
    event: models.Event = payload["event"]
    notification_service.send_invitations_for_event(event)


event_bus.subscribe("event_created", handle_event_created)
