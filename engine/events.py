from collections import defaultdict
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class DomainEvent:
    name: str
    payload: dict

class EventBus:
    """Small synchronous event bus; handlers should remain deterministic."""
    def __init__(self):
        self._handlers = defaultdict(list)

    def subscribe(self, event_name: str, handler: Callable):
        self._handlers[event_name].append(handler)

    def publish(self, event: DomainEvent):
        for handler in tuple(self._handlers[event.name]):
            handler(event)
