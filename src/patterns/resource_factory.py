"""Factory Method with Registry for dynamic resource creation."""
from src.core.cloud_resource import CloudResource, AppService, StorageAccount, CacheDB
from src.core.eviction_strategy import LRUStrategy, FIFOStrategy


class ResourceFactory:
    """Factory for creating cloud resources with registry mechanism."""
    
    def __init__(self):
        self.registry = {}
        self._register_defaults()
    
    def _register_defaults(self):
        """Register default resource types."""
        self.register("AppService", AppService)
        self.register("StorageAccount", StorageAccount)
        self.register("CacheDB", CacheDB)
    
    def register(self, resource_type, resource_class):
        """Register a new resource type."""
        self.registry[resource_type] = resource_class
        print(f"Registered resource type: {resource_type}")
    
    def create_resource(self, resource_type, config):
        """Create a resource based on type and configuration."""
        if resource_type not in self.registry:
            raise ValueError(f"Unknown resource type: {resource_type}")
        
        resource_class = self.registry[resource_type]
        
        # Create resource based on type
        if resource_type == "AppService":
            return resource_class(
                config['id'],
                config['name'],
                config['runtime'],
                config['region'],
                config['replica_count']
            )
        elif resource_type == "StorageAccount":
            return resource_class(
                config['id'],
                config['name'],
                config['encryption_enabled'],
                config['max_size_gb']
            )
        elif resource_type == "CacheDB":
            # Handle eviction strategy
            eviction_policy = config.get('eviction_policy', 'LRU')
            strategy = LRUStrategy() if eviction_policy == 'LRU' else FIFOStrategy()
            return resource_class(
                config['id'],
                config['name'],
                config['ttl_seconds'],
                config['capacity_mb'],
                strategy
            )
        else:
            raise ValueError(f"Cannot instantiate resource type: {resource_type}")
    
    def list_available_types(self):
        """List all registered resource types."""
        return list(self.registry.keys())
