# Project Structure

## Directory Organization

The project follows a clean, modular architecture with clear separation of concerns:

```
cloud-resource-management/
│
├── src/                          # All source code
│   ├── __init__.py
│   │
│   ├── core/                     # Domain Layer - Core Business Logic
│   │   ├── __init__.py
│   │   ├── cloud_resource.py     # Abstract CloudResource + concrete implementations
│   │   ├── resource_state.py     # State Pattern: Created, Running, Stopped, Deleted
│   │   └── eviction_strategy.py  # Strategy Pattern: LRU, FIFO
│   │
│   ├── patterns/                 # Design Pattern Implementations
│   │   ├── __init__.py
│   │   ├── resource_factory.py   # Factory Method with Registry
│   │   └── resource_decorator.py # Decorator Pattern for Logging
│   │
│   ├── services/                 # Service Layer - Business Services
│   │   ├── __init__.py
│   │   ├── user_repository.py    # Repository Pattern for User Data
│   │   ├── login_service.py      # Authentication Services (File, Service)
│   │   └── resource_manager.py   # Facade Pattern - Main Orchestrator
│   │
│   └── cli/                      # Presentation Layer - User Interfaces
│       ├── __init__.py
│       ├── main.py               # Simple CLI without authentication
│       ├── main_with_auth.py     # Full-featured CLI with auth
│       └── demo_resource_manager.py # Demo and examples
│
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md           # System architecture details
│   ├── Design.md                 # Design patterns and UML
│   ├── README_RESOURCE_MANAGER.md # Usage guide
│   └── PROJECT_STRUCTURE.md      # This file
│
├── data/                         # Data Storage
│   ├── users.json                # Production user data
│   └── demo_users.json           # Demo user data
│
├── tests/                        # Test Suite (to be implemented)
│   └── (test files)
│
├── README.md                     # Main project README
└── run.py                        # Launcher script
```

## Layer Responsibilities

### Core Layer (`src/core/`)
**Purpose**: Contains the fundamental domain models and business rules

- **cloud_resource.py**: Defines the abstract `CloudResource` class and concrete implementations:
  - `AppService`: Application hosting service
  - `StorageAccount`: Cloud storage service
  - `CacheDB`: Caching database service

- **resource_state.py**: Implements the State Pattern for resource lifecycle:
  - `CreatedState`: Initial state after creation
  - `RunningState`: Active/running state
  - `StoppedState`: Paused/stopped state
  - `DeletedState`: Terminal state

- **eviction_strategy.py**: Implements the Strategy Pattern for cache eviction:
  - `LRUStrategy`: Least Recently Used
  - `FIFOStrategy`: First In First Out

### Patterns Layer (`src/patterns/`)
**Purpose**: Encapsulates reusable design pattern implementations

- **resource_factory.py**: Factory Method with Registry
  - Dynamic resource creation
  - Runtime type registration
  - Decouples client from concrete classes

- **resource_decorator.py**: Decorator Pattern
  - `ResourceDecorator`: Abstract decorator base
  - `LoggingDecorator`: Adds logging to any resource
  - Enables cross-cutting concerns without modifying core logic

### Services Layer (`src/services/`)
**Purpose**: Provides business services and orchestration

- **user_repository.py**: Repository Pattern
  - `User`: User entity
  - `UserRepository`: CRUD operations for user data
  - JSON-based persistence

- **login_service.py**: Authentication services
  - `LoginService`: Abstract authentication interface
  - `FileLogin`: File-based authentication
  - `ServiceLogin`: External service authentication

- **resource_manager.py**: Facade Pattern
  - Main entry point for all operations
  - Coordinates authentication, factory, and resources
  - Enforces authentication requirements

### CLI Layer (`src/cli/`)
**Purpose**: User-facing interfaces

- **main.py**: Simple CLI for basic resource management (no auth)
- **main_with_auth.py**: Full-featured CLI with user authentication
- **demo_resource_manager.py**: Demonstration scripts and examples

## Module Dependencies

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Layer                            │
│  (main.py, main_with_auth.py, demo_resource_manager)   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 Services Layer                          │
│        (resource_manager, user_repository,              │
│              login_service)                             │
└────────────┬──────────────────────┬─────────────────────┘
             │                      │
             ▼                      ▼
┌────────────────────┐    ┌────────────────────────────┐
│  Patterns Layer    │    │      Core Layer            │
│  (factory,         │    │  (cloud_resource,          │
│   decorator)       │    │   resource_state,          │
│                    │    │   eviction_strategy)       │
└────────────────────┘    └────────────────────────────┘
```

## Import Conventions

All imports use absolute paths from the project root:

```python
# Core imports
from src.core.cloud_resource import CloudResource, AppService
from src.core.resource_state import CreatedState, RunningState
from src.core.eviction_strategy import LRUStrategy

# Pattern imports
from src.patterns.resource_factory import ResourceFactory
from src.patterns.resource_decorator import LoggingDecorator

# Service imports
from src.services.user_repository import User, UserRepository
from src.services.login_service import FileLogin, ServiceLogin
from src.services.resource_manager import ResourceManager
```

## Benefits of This Structure

1. **Clear Separation of Concerns**: Each layer has a distinct responsibility
2. **Easy Navigation**: Related files are grouped together
3. **Scalability**: Easy to add new resources, patterns, or services
4. **Testability**: Each layer can be tested independently
5. **Maintainability**: Changes in one layer don't affect others
6. **Documentation**: Structure mirrors the architecture documentation
7. **Reusability**: Patterns and core logic can be reused in other projects

## Adding New Components

### New Resource Type
Add to `src/core/cloud_resource.py` and register in `src/patterns/resource_factory.py`

### New Design Pattern
Create new file in `src/patterns/` and update `__init__.py`

### New Service
Add to `src/services/` and update `__init__.py`

### New CLI Interface
Add to `src/cli/` for different use cases

## Running the Application

```bash
# Using the launcher
python run.py

# Direct execution
python -m src.cli.main
python -m src.cli.main_with_auth
python -m src.cli.demo_resource_manager
```
