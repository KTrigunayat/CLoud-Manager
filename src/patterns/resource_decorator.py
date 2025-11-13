"""Decorator Pattern implementation for logging."""
from src.core.cloud_resource import CloudResource
from datetime import datetime


class ResourceDecorator(CloudResource):
    """Abstract decorator for cloud resources."""
    
    def __init__(self, wrapped_resource: CloudResource):
        self.wrapped_resource = wrapped_resource
        # Delegate attributes to wrapped resource
        self.id = wrapped_resource.id
        self.name = wrapped_resource.name
        self.current_state = wrapped_resource.current_state
    
    def start(self):
        self.wrapped_resource.start()
    
    def stop(self):
        self.wrapped_resource.stop()
    
    def delete(self):
        self.wrapped_resource.delete()
    
    def get_details(self):
        return self.wrapped_resource.get_details()
    
    def set_state(self, state):
        self.wrapped_resource.set_state(state)
    
    def get_state(self):
        return self.wrapped_resource.get_state()


class LoggingDecorator(ResourceDecorator):
    """Decorator that adds logging to resource operations."""
    
    def __init__(self, wrapped_resource: CloudResource):
        super().__init__(wrapped_resource)
    
    def _log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[LOG {timestamp}] {message}")
    
    def start(self):
        self._log(f"Attempting to start resource: {self.name}")
        try:
            self.wrapped_resource.start()
            self._log(f"Successfully started resource: {self.name}")
        except Exception as e:
            self._log(f"Failed to start resource: {self.name} - {str(e)}")
            raise
    
    def stop(self):
        self._log(f"Attempting to stop resource: {self.name}")
        try:
            self.wrapped_resource.stop()
            self._log(f"Successfully stopped resource: {self.name}")
        except Exception as e:
            self._log(f"Failed to stop resource: {self.name} - {str(e)}")
            raise
    
    def delete(self):
        self._log(f"Attempting to delete resource: {self.name}")
        try:
            self.wrapped_resource.delete()
            self._log(f"Successfully deleted resource: {self.name}")
        except Exception as e:
            self._log(f"Failed to delete resource: {self.name} - {str(e)}")
            raise
