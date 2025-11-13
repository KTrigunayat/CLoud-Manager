"""Demo script showing the resource manager with repository pattern."""
from src.services.resource_manager import ResourceManager
from src.services.user_repository import UserRepository, User
from src.services.login_service import FileLogin, ServiceLogin


def demo_file_login():
    """Demonstrate file-based login."""
    print("="*60)
    print("DEMO: File-Based Login with Repository Pattern")
    print("="*60)
    
    # Initialize repository and login service
    repo = UserRepository("data/demo_users.json")
    file_login = FileLogin(repo)
    
    # Create resource manager
    manager = ResourceManager(repo, file_login)
    
    # Register users
    print("\n1. Registering users...")
    manager.register_user("alice", "password123", "admin")
    manager.register_user("bob", "secret456", "user")
    
    # Try to login with wrong credentials
    print("\n2. Attempting login with wrong password...")
    success = manager.login("alice", "wrongpassword")
    print(f"Login result: {success}")
    
    # Login successfully
    print("\n3. Logging in with correct credentials...")
    success = manager.login("alice", "password123")
    print(f"Login result: {success}")
    
    # Create a resource
    print("\n4. Creating an AppService resource...")
    config = {
        'name': 'MyWebApp',
        'runtime': 'Python',
        'region': 'us-east-1',
        'replica_count': 3
    }
    resource_id = manager.create_resource("AppService", config, enable_logging=True)
    
    # List resources
    print("\n5. Listing all resources...")
    resources = manager.list_resources()
    for rid, resource in resources.items():
        print(f"  [{rid}] {resource.name} - State: {resource.get_state()}")
    
    # Start the resource
    print("\n6. Starting the resource...")
    manager.start_resource(resource_id)
    
    # View details
    print("\n7. Viewing resource details...")
    details = manager.get_resource_details(resource_id)
    print(details)
    
    # Logout
    print("\n8. Logging out...")
    manager.logout()
    
    # Try to create resource without login
    print("\n9. Attempting to create resource without authentication...")
    config2 = {
        'name': 'UnauthorizedResource',
        'runtime': 'Node.js',
        'region': 'us-west-2',
        'replica_count': 1
    }
    result = manager.create_resource("AppService", config2)
    print(f"Result: {result}")


def demo_service_login():
    """Demonstrate service-based login."""
    print("\n\n" + "="*60)
    print("DEMO: Service-Based Login")
    print("="*60)
    
    # Initialize repository and service login
    repo = UserRepository("data/demo_users.json")
    service_login = ServiceLogin("https://auth.example.com", "api-key-xyz")
    
    # Create resource manager with service login
    manager = ResourceManager(repo, service_login)
    
    # Note: For service login to work with the repository,
    # the user must still exist in the repository
    print("\n1. Ensuring user exists in repository...")
    manager.register_user("charlie", "servicepass", "user")
    
    print("\n2. Authenticating via external service...")
    success = manager.login("charlie", "servicepass")
    print(f"Login result: {success}")
    
    if success:
        print("\n3. Creating a CacheDB resource...")
        config = {
            'name': 'SessionCache',
            'ttl_seconds': 3600,
            'capacity_mb': 512,
            'eviction_policy': 'LRU'
        }
        resource_id = manager.create_resource("CacheDB", config, enable_logging=False)
        
        print("\n4. Resource created successfully!")
        details = manager.get_resource_details(resource_id)
        print(details)


def demo_repository_operations():
    """Demonstrate repository CRUD operations."""
    print("\n\n" + "="*60)
    print("DEMO: Repository CRUD Operations")
    print("="*60)
    
    repo = UserRepository("data/demo_users.json")
    
    print("\n1. Getting all users...")
    users = repo.get_all_users()
    for user in users:
        print(f"  - {user.username} ({user.role})")
    
    print("\n2. Finding user by username...")
    user = repo.find_by_username("alice")
    if user:
        print(f"  Found: {user.username} - Role: {user.role}")
    
    print("\n3. Updating user...")
    user.role = "superadmin"
    success = repo.update_user(user)
    print(f"  Update result: {success}")
    
    print("\n4. Verifying update...")
    updated_user = repo.find_by_username("alice")
    print(f"  New role: {updated_user.role}")
    
    print("\n5. Deleting user...")
    success = repo.delete_user("bob")
    print(f"  Delete result: {success}")
    
    print("\n6. Final user list...")
    users = repo.get_all_users()
    for user in users:
        print(f"  - {user.username} ({user.role})")


if __name__ == "__main__":
    demo_file_login()
    demo_service_login()
    demo_repository_operations()
    
    print("\n\n" + "="*60)
    print("Demo completed! Check 'demo_users.json' for persisted data.")
    print("="*60)
