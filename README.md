# Cloud Resource Management System

A modular, extensible system for managing cloud resources with user authentication, lifecycle management, and logging capabilities.

## Project Structure

```
.
├── src/                          # Source code
│   ├── core/                     # Core domain models
│   │   ├── cloud_resource.py     # Resource abstractions (AppService, StorageAccount, CacheDB)
│   │   ├── resource_state.py     # State pattern for lifecycle management
│   │   └── eviction_strategy.py  # Strategy pattern for cache eviction
│   ├── patterns/                 # Design pattern implementations
│   │   ├── resource_factory.py   # Factory pattern with registry
│   │   └── resource_decorator.py # Decorator pattern for logging
│   ├── services/                 # Service layer
│   │   ├── user_repository.py    # Repository pattern for user data
│   │   ├── login_service.py      # Authentication services
│   │   └── resource_manager.py   # Facade for resource operations
│   └── cli/                      # Command-line interfaces
│       ├── main.py               # Simple CLI without auth
│       ├── main_with_auth.py     # Full CLI with authentication
│       └── demo_resource_manager.py # Demo script
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md           # Detailed architecture documentation
│   ├── Design.md                 # Design patterns and UML diagrams
│   └── README_RESOURCE_MANAGER.md # Resource manager guide
├── data/                         # Data storage
│   ├── users.json                # User data
│   └── demo_users.json           # Demo user data
└── tests/                        # Test files (to be added)
```

## Features

- **Multi-resource support**: AppService, StorageAccount, CacheDB
- **User authentication**: File-based and service-based login
- **Lifecycle management**: State-based transitions (Created → Running → Stopped → Deleted)
- **Extensibility**: Plugin architecture for new resource types
- **Cross-cutting concerns**: Optional logging via decorators
- **Persistence**: JSON-based user repository

## Design Patterns

1. **Factory Method**: Dynamic resource creation with registry
2. **State Pattern**: Resource lifecycle management
3. **Decorator Pattern**: Logging functionality
4. **Strategy Pattern**: Cache eviction algorithms (LRU/FIFO)
5. **Repository Pattern**: User data persistence
6. **Facade Pattern**: Simplified resource management interface

## Quick Start

### Run the simple CLI (no authentication)
```bash
python -m src.cli.main
```

### Run the full CLI with authentication
```bash
python -m src.cli.main_with_auth
```

Default users:
- Username: `admin`, Password: `admin123`, Role: `admin`
- Username: `user`, Password: `user123`, Role: `user`

### Run the demo
```bash
python -m src.cli.demo_resource_manager
```

## Usage Example

```python
from src.services.resource_manager import ResourceManager
from src.services.user_repository import UserRepository
from src.services.login_service import FileLogin

# Initialize
repo = UserRepository("data/users.json")
login_service = FileLogin(repo)
manager = ResourceManager(repo, login_service)

# Register and login
manager.register_user("alice", "password123", "admin")
manager.login("alice", "password123")

# Create resource
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
```

## Documentation

- [Architecture Documentation](docs/ARCHITECTURE.md) - Detailed system architecture
- [Design Patterns](docs/Design.md) - UML diagrams and pattern justification
- [Resource Manager Guide](docs/README_RESOURCE_MANAGER.md) - Usage guide

## SOLID Principles

The system adheres to SOLID principles:
- **Single Responsibility**: Each class has one clear purpose
- **Open/Closed**: Extensible without modifying existing code
- **Liskov Substitution**: All implementations are interchangeable
- **Interface Segregation**: Focused, minimal interfaces
- **Dependency Inversion**: Depends on abstractions, not concretions

## Extension Points

### Add New Resource Type
```python
from src.core.cloud_resource import CloudResource

class DatabaseService(CloudResource):
    def __init__(self, resource_id, name, engine, size):
        super().__init__(resource_id, name)
        self.engine = engine
        self.size = size
    
    def get_details(self):
        return f"DatabaseService[{self.id}]: {self.name}\n  Engine: {self.engine}"

# Register
factory.register("DatabaseService", DatabaseService)
```

### Add New Authentication Method
```python
from src.services.login_service import LoginService

class OAuthLogin(LoginService):
    def authenticate(self, username, password):
        # OAuth implementation
        pass
    
    def get_service_name(self):
        return "OAuth 2.0 Authentication"
```

## License

This project is for educational purposes.
