from abc import ABC, abstractmethod
import models
from .email_sender import EmailSender


class NotificationStrategy(ABC):
    @abstractmethod
    def send_event_invitation(self, user: models.User, event: models.Event) -> None:
        pass


class EmailNotificationStrategy(NotificationStrategy):
    def __init__(self, email_sender: EmailSender):
        self.email_sender = email_sender

    def send_event_invitation(self, user: models.User, event: models.Event) -> None:
        subject = f"[Calendar] New event: {event.title}"

        body_lines = [
            f"Hello {user.first_name},",
            "",
            f"You've been invited to: '{event.title}'",
            "",
            f"Start: {event.start_time}",
            f"End:   {event.end_time}",
        ]
        if event.location:
            body_lines.append(f"Location: {event.location}")
        if event.description:
            body_lines.append("")
            body_lines.append("Description:")
            body_lines.append(event.description)

        body = "\n".join(body_lines)
        self.email_sender.send_email(user.email, subject, body)


class SMSNotification(NotificationStrategy):
    pass