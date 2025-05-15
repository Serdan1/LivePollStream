from abc import ABC, abstractmethod
from typing import Dict, Any

class Observer(ABC):
    @abstractmethod
    def update(self, event: Dict[str, Any]):
        pass

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def _notify_observers(self, event: Dict[str, Any]):
        for observer in self._observers:
            observer.update(event)