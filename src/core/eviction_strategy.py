"""Strategy Pattern implementation for cache eviction policies."""
from abc import ABC, abstractmethod


class EvictionStrategy(ABC):
    """Abstract base class for eviction strategies."""
    
    @abstractmethod
    def evict(self):
        pass


class LRUStrategy(EvictionStrategy):
    """Least Recently Used eviction strategy."""
    
    def evict(self):
        return "Evicting least recently used items"


class FIFOStrategy(EvictionStrategy):
    """First In First Out eviction strategy."""
    
    def evict(self):
        return "Evicting oldest items first"
