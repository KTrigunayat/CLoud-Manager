"""State Pattern implementation for resource lifecycle management."""
from abc import ABC, abstractmethod


class ResourceState(ABC):
    """Abstract base class for resource states."""
    
    @abstractmethod
    def start(self, resource):
        pass
    
    @abstractmethod
    def stop(self, resource):
        pass
    
    @abstractmethod
    def delete(self, resource):
        pass
    
    @abstractmethod
    def get_state_name(self):
        pass


class CreatedState(ResourceState):
    def start(self, resource):
        print(f"Starting {resource.name}...")
        resource.set_state(RunningState())
    
    def stop(self, resource):
        raise ValueError("Cannot stop a resource that hasn't been started")
    
    def delete(self, resource):
        print(f"Deleting {resource.name}...")
        resource.set_state(DeletedState())
    
    def get_state_name(self):
        return "CREATED"


class RunningState(ResourceState):
    def start(self, resource):
        raise ValueError("Resource is already running")
    
    def stop(self, resource):
        print(f"Stopping {resource.name}...")
        resource.set_state(StoppedState())
    
    def delete(self, resource):
        raise ValueError("Cannot delete a running resource. Stop it first")
    
    def get_state_name(self):
        return "RUNNING"


class StoppedState(ResourceState):
    def start(self, resource):
        print(f"Restarting {resource.name}...")
        resource.set_state(RunningState())
    
    def stop(self, resource):
        raise ValueError("Resource is already stopped")
    
    def delete(self, resource):
        print(f"Deleting {resource.name}...")
        resource.set_state(DeletedState())
    
    def get_state_name(self):
        return "STOPPED"


class DeletedState(ResourceState):
    def start(self, resource):
        raise ValueError("Cannot start a deleted resource")
    
    def stop(self, resource):
        raise ValueError("Cannot stop a deleted resource")
    
    def delete(self, resource):
        raise ValueError("Resource is already deleted")
    
    def get_state_name(self):
        return "DELETED"
