import models
from notifications.email_sender import EmailSender
from notifications.strategies import EmailNotificationStrategy, NotificationStrategy

class NotificationService:
    def __init__(self, strategy: NotificationStrategy | None = None):
        if strategy is None:
            sender = EmailSender()
            strategy = EmailNotificationStrategy(sender)
        self.strategy = strategy

    def send_invitations_for_event(self, event: models.Event) -> None:
        for participant in event.participants:
            user = participant.user
            self.strategy.send_event_invitation(user, event)
