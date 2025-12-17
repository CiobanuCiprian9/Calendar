from collections import defaultdict
from typing import Callable, Dict, List


class DomainEventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[dict], None]]] = defaultdict(list)

    def subscribe(self, event_name: str, handler: Callable[[dict], None]):
        self._subscribers[event_name].append(handler)

    def publish(self, event_name: str, payload: dict):
        for handler in self._subscribers[event_name]:
            handler(payload)


event_bus = DomainEventBus()
