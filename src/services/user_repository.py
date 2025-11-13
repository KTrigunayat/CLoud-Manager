"""Repository Pattern implementation for user data persistence."""
import json
import os
from typing import Optional, Dict, List


class User:
    """User entity."""
    
    def __init__(self, username: str, password: str, role: str = "user"):
        self.username = username
        self.password = password
        self.role = role
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary."""
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'User':
        """Create user from dictionary."""
        return User(
            username=data["username"],
            password=data["password"],
            role=data.get("role", "user")
        )


class UserRepository:
    """Repository for managing user data with JSON persistence."""
    
    def __init__(self, filepath: str = "users.json"):
        self.filepath = filepath
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create the JSON file if it doesn't exist."""
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump({"users": []}, f, indent=2)
    
    def _read_data(self) -> Dict:
        """Read data from JSON file."""
        with open(self.filepath, 'r') as f:
            return json.load(f)
    
    def _write_data(self, data: Dict):
        """Write data to JSON file."""
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_user(self, user: User) -> bool:
        """Add a new user to the repository."""
        data = self._read_data()
        
        # Check if user already exists
        if any(u["username"] == user.username for u in data["users"]):
            return False
        
        data["users"].append(user.to_dict())
        self._write_data(data)
        return True
    
    def find_by_username(self, username: str) -> Optional[User]:
        """Find a user by username."""
        data = self._read_data()
        
        for user_data in data["users"]:
            if user_data["username"] == username:
                return User.from_dict(user_data)
        
        return None
    
    def get_all_users(self) -> List[User]:
        """Get all users."""
        data = self._read_data()
        return [User.from_dict(u) for u in data["users"]]
    
    def update_user(self, user: User) -> bool:
        """Update an existing user."""
        data = self._read_data()
        
        for i, user_data in enumerate(data["users"]):
            if user_data["username"] == user.username:
                data["users"][i] = user.to_dict()
                self._write_data(data)
                return True
        
        return False
    
    def delete_user(self, username: str) -> bool:
        """Delete a user by username."""
        data = self._read_data()
        original_count = len(data["users"])
        
        data["users"] = [u for u in data["users"] if u["username"] != username]
        
        if len(data["users"]) < original_count:
            self._write_data(data)
            return True
        
        return False
