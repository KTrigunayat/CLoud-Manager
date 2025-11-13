"""Login service classes for authentication."""
from abc import ABC, abstractmethod
from typing import Optional
from src.services.user_repository import UserRepository, User


class LoginService(ABC):
    """Abstract base class for login services."""
    
    @abstractmethod
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate a user."""
        pass
    
    @abstractmethod
    def get_service_name(self) -> str:
        """Get the name of the login service."""
        pass


class FileLogin(LoginService):
    """File-based login service using UserRepository."""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user against file-based storage."""
        user = self.repository.find_by_username(username)
        
        if user is None:
            print(f"[FileLogin] User '{username}' not found")
            return False
        
        if user.password == password:
            print(f"[FileLogin] User '{username}' authenticated successfully")
            return True
        else:
            print(f"[FileLogin] Invalid password for user '{username}'")
            return False
    
    def get_service_name(self) -> str:
        return "File-Based Authentication"


class ServiceLogin(LoginService):
    """Service-based login for external authentication systems."""
    
    def __init__(self, service_url: str, api_key: str):
        self.service_url = service_url
        self.api_key = api_key
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user against external service."""
        # Simulated external service authentication
        print(f"[ServiceLogin] Connecting to {self.service_url}")
        print(f"[ServiceLogin] Authenticating user '{username}' with API key")
        
        # In a real implementation, this would make an HTTP request
        # For now, we'll simulate a successful authentication
        if username and password:
            print(f"[ServiceLogin] User '{username}' authenticated via external service")
            return True
        
        print(f"[ServiceLogin] Authentication failed for user '{username}'")
        return False
    
    def get_service_name(self) -> str:
        return f"Service Authentication ({self.service_url})"
