"""Resource Manager with Repository pattern integration."""
from typing import Dict, Optional
from src.core.cloud_resource import CloudResource
from src.patterns.resource_factory import ResourceFactory
from src.patterns.resource_decorator import LoggingDecorator
from src.services.user_repository import UserRepository, User
from src.services.login_service import LoginService, FileLogin


class ResourceManager:
    """Manages cloud resources with user authentication and repository pattern."""
    
    def __init__(self, user_repository: UserRepository, login_service: LoginService):
        self.user_repository = user_repository
        self.login_service = login_service
        self.factory = ResourceFactory()
        self.resources: Dict[str, CloudResource] = {}
        self.next_id = 1
        self.current_user: Optional[User] = None
    
    def login(self, username: str, password: str) -> bool:
        """Login a user using the configured login service."""
        if self.login_service.authenticate(username, password):
            self.current_user = self.user_repository.find_by_username(username)
            if self.current_user is None:
                print(f"Warning: User '{username}' authenticated but not found in repository")
                return False
            print(f"Welcome, {self.current_user.username} ({self.current_user.role})")
            return True
        return False
    
    def logout(self):
        """Logout the current user."""
        if self.current_user:
            print(f"User '{self.current_user.username}' logged out")
            self.current_user = None
        else:
            print("No user is currently logged in")
    
    def is_authenticated(self) -> bool:
        """Check if a user is currently authenticated."""
        return self.current_user is not None
    
    def register_user(self, username: str, password: str, role: str = "user") -> bool:
        """Register a new user in the repository."""
        user = User(username, password, role)
        if self.user_repository.add_user(user):
            print(f"User '{username}' registered successfully")
            return True
        else:
            print(f"User '{username}' already exists")
            return False
    
    def create_resource(self, resource_type: str, config: Dict, enable_logging: bool = False) -> Optional[str]:
        """Create a new cloud resource."""
        if not self.is_authenticated():
            print("Error: You must be logged in to create resources")
            return None
        
        config['id'] = str(self.next_id)
        resource = self.factory.create_resource(resource_type, config)
        
        if enable_logging:
            resource = LoggingDecorator(resource)
        
        resource_id = str(self.next_id)
        self.resources[resource_id] = resource
        self.next_id += 1
        
        print(f"Resource created with ID: {resource_id} by user: {self.current_user.username}")
        return resource_id
    
    def get_resource(self, resource_id: str) -> Optional[CloudResource]:
        """Get a resource by ID."""
        return self.resources.get(resource_id)
    
    def list_resources(self) -> Dict[str, CloudResource]:
        """List all resources."""
        if not self.is_authenticated():
            print("Error: You must be logged in to list resources")
            return {}
        return self.resources
    
    def start_resource(self, resource_id: str) -> bool:
        """Start a resource."""
        if not self.is_authenticated():
            print("Error: You must be logged in to start resources")
            return False
        
        resource = self.get_resource(resource_id)
        if resource:
            resource.start()
            return True
        else:
            print(f"Resource {resource_id} not found")
            return False
    
    def stop_resource(self, resource_id: str) -> bool:
        """Stop a resource."""
        if not self.is_authenticated():
            print("Error: You must be logged in to stop resources")
            return False
        
        resource = self.get_resource(resource_id)
        if resource:
            resource.stop()
            return True
        else:
            print(f"Resource {resource_id} not found")
            return False
    
    def delete_resource(self, resource_id: str) -> bool:
        """Delete a resource."""
        if not self.is_authenticated():
            print("Error: You must be logged in to delete resources")
            return False
        
        resource = self.get_resource(resource_id)
        if resource:
            resource.delete()
            return True
        else:
            print(f"Resource {resource_id} not found")
            return False
    
    def get_resource_details(self, resource_id: str) -> Optional[str]:
        """Get detailed information about a resource."""
        if not self.is_authenticated():
            print("Error: You must be logged in to view resource details")
            return None
        
        resource = self.get_resource(resource_id)
        if resource:
            return resource.get_details()
        else:
            print(f"Resource {resource_id} not found")
            return None
