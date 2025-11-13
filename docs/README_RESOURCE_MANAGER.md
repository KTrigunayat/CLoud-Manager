# Resource Manager with Repository Pattern

This extension adds user authentication and resource management capabilities using the Repository pattern and JSON-based persistence.

## New Components

### 1. User Repository (`user_repository.py`)
Implements the Repository pattern for user data management with JSON file persistence.

**Classes:**
- `User`: Entity class representing a user with username, password, and role
- `UserRepository`: Repository for CRUD operations on user data

**Features:**
- JSON file-based persistence
- CRUD operations: add, find, update, delete users
- Automatic file creation if not exists

### 2. Login Services (`login_service.py`)
Separate login classes (not decorators) for different authentication methods.

**Classes:**
- `LoginService`: Abstract base class for login services
- `FileLogin`: File-based authentication using UserRepository
- `ServiceLogin`: External service authentication (simulated)

**Key Difference:** These are separate service classes, not decorators. Each implements its own authentication logic independently.

### 3. Resource Manager (`resource_manager.py`)
Manages cloud resources with integrated user authentication.

**Features:**
- User authentication required for resource operations
- Integration with UserRepository and LoginService
- User registration and login/logout
- Resource lifecycle management (create, start, stop, delete)
- Support for logging decorator

## Usage

### Basic Example

```python
from resource_manager import ResourceManager
from user_repository import UserRepository
from login_service import FileLogin

# Initialize components
repo = UserRepository("users.json")
login_service = FileLogin(repo)
manager = ResourceManager(repo, login_service)

# Register a user
manager.register_user("alice", "password123", "admin")

# Login
manager.login("alice", "password123")

# Create a resource
config = {
    'name': 'MyApp',
    'runtime': 'Python',
    'region': 'us-east-1',
    'replica_count': 3
}
resource_id = manager.create_resource("AppService", config, enable_logging=True)

# Manage resource
manager.start_resource(resource_id)
manager.stop_resource(resource_id)
manager.delete_resource(resource_id)

# Logout
manager.logout()
```

### Running the Demo

```bash
python demo_resource_manager.py
```

This demonstrates:
- File-based login with repository
- Service-based login
- Repository CRUD operations
- Resource management with authentication

### Running the Full Application

```bash
python main_with_auth.py
```

Default users:
- Username: `admin`, Password: `admin123`, Role: `admin`
- Username: `user`, Password: `user123`, Role: `user`

## Architecture

### Repository Pattern
The `UserRepository` class abstracts data access, making it easy to switch storage backends (e.g., from JSON to database) without changing business logic.

### Login Services (Not Decorators)
Unlike the `LoggingDecorator` which wraps resources, `FileLogin` and `ServiceLogin` are separate service classes:
- They implement the `LoginService` interface
- Each has its own authentication logic
- They can be swapped at runtime
- No wrapping or delegation involved

### Resource Manager
Acts as a facade that coordinates:
- User authentication via LoginService
- User data persistence via UserRepository
- Resource creation via ResourceFactory
- Resource lifecycle management

## File Structure

```
user_repository.py       - Repository pattern for user data
login_service.py         - Login service classes (FileLogin, ServiceLogin)
resource_manager.py      - Resource manager with authentication
main_with_auth.py        - CLI application with auth
demo_resource_manager.py - Demo script
users.json              - User data storage (created automatically)
```

## Design Patterns Used

1. **Repository Pattern**: `UserRepository` abstracts data access
2. **Strategy Pattern**: `LoginService` with different implementations
3. **Facade Pattern**: `ResourceManager` simplifies complex subsystem interactions
4. **Factory Pattern**: `ResourceFactory` for resource creation (existing)
5. **State Pattern**: Resource lifecycle management (existing)
6. **Decorator Pattern**: `LoggingDecorator` for cross-cutting concerns (existing)

## Key Differences from Decorator Pattern

The login services are **NOT decorators** because:
- They don't wrap or enhance existing objects
- They provide standalone authentication functionality
- They implement a service interface, not wrap another service
- They follow the Strategy pattern, not Decorator pattern
