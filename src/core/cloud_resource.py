"""Core resource abstraction and concrete implementations."""
from abc import ABC, abstractmethod
from src.core.resource_state import CreatedState
from src.core.eviction_strategy import EvictionStrategy


class CloudResource(ABC):
    """Abstract base class for all cloud resources."""
    
    def __init__(self, resource_id, name):
        self.id = resource_id
        self.name = name
        self.current_state = CreatedState()
    
    def start(self):
        self.current_state.start(self)
    
    def stop(self):
        self.current_state.stop(self)
    
    def delete(self):
        self.current_state.delete(self)
    
    def set_state(self, state):
        self.current_state = state
    
    def get_state(self):
        return self.current_state.get_state_name()
    
    @abstractmethod
    def get_details(self):
        pass


class AppService(CloudResource):
    """Application Service resource."""
    
    def __init__(self, resource_id, name, runtime, region, replica_count):
        super().__init__(resource_id, name)
        self.runtime = runtime
        self.region = region
        self.replica_count = replica_count
    
    def get_details(self):
        return (f"AppService[{self.id}]: {self.name}\n"
                f"  State: {self.get_state()}\n"
                f"  Runtime: {self.runtime}\n"
                f"  Region: {self.region}\n"
                f"  Replicas: {self.replica_count}")


class StorageAccount(CloudResource):
    """Storage Account resource."""
    
    def __init__(self, resource_id, name, encryption_enabled, max_size_gb):
        super().__init__(resource_id, name)
        self.encryption_enabled = encryption_enabled
        self.max_size_gb = max_size_gb
    
    def get_details(self):
        return (f"StorageAccount[{self.id}]: {self.name}\n"
                f"  State: {self.get_state()}\n"
                f"  Encryption: {'Enabled' if self.encryption_enabled else 'Disabled'}\n"
                f"  Max Size: {self.max_size_gb}GB")


class CacheDB(CloudResource):
    """Cache Database resource."""
    
    def __init__(self, resource_id, name, ttl_seconds, capacity_mb, eviction_policy: EvictionStrategy):
        super().__init__(resource_id, name)
        self.ttl_seconds = ttl_seconds
        self.capacity_mb = capacity_mb
        self.eviction_policy = eviction_policy
    
    def get_details(self):
        return (f"CacheDB[{self.id}]: {self.name}\n"
                f"  State: {self.get_state()}\n"
                f"  TTL: {self.ttl_seconds}s\n"
                f"  Capacity: {self.capacity_mb}MB\n"
                f"  Eviction: {self.eviction_policy.__class__.__name__}")
