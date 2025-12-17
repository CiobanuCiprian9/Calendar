from typing import Dict, Any
import models

def _map_participants(event: models.Event):
    return [
        {
            "user_id": p.user.id,
            "first_name": p.user.first_name,
            "last_name": p.user.last_name,
            "email": p.user.email,
        }
        for p in event.participants
    ]

def _build_full_description(event: models.Event, participants_json) -> str | None:
    lines = []

    if event.description:
        lines.append(event.description)

    if participants_json:
        participants_str = ", ".join(
            f"{p['email']}"
            for p in participants_json
        )
        lines.append(f"Participants: {participants_str}")

    if not lines:
        return None

    return "\n".join(lines)

def event_to_response(event: models.Event) -> Dict[str, Any]:
    participants_json = _map_participants(event)

    start_str = event.start_time.isoformat() + "[Europe/Bucharest]"
    end_str = event.end_time.isoformat() + "[Europe/Bucharest]"

    full_description = _build_full_description(event, participants_json)

    return {
        "id": event.id,
        "owner_id": event.owner_id,
        "title": event.title,
        "description": full_description,
        "start_time": start_str,
        "end_time": end_str,
        "location": event.location,
        "participants": participants_json,
    }