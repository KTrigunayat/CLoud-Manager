"""Main CLI application with authentication and resource management."""
from src.services.resource_manager import ResourceManager
from src.services.user_repository import UserRepository
from src.services.login_service import FileLogin, ServiceLogin


class CloudResourceManagerApp:
    """Main application with user authentication."""
    
    def __init__(self):
        # Initialize repository and login service
        self.user_repo = UserRepository("data/users.json")
        self.file_login = FileLogin(self.user_repo)
        
        # Initialize resource manager with file-based login
        self.manager = ResourceManager(self.user_repo, self.file_login)
        
        # Create default admin user if repository is empty
        self._initialize_default_users()
    
    def _initialize_default_users(self):
        """Create default users if none exist."""
        users = self.user_repo.get_all_users()
        if not users:
            print("Initializing default users...")
            self.user_repo.add_user(User("admin", "admin123", "admin"))
            self.user_repo.add_user(User("user", "user123", "user"))
            print("Default users created: admin/admin123, user/user123")
    
    def run(self):
        """Run the main menu loop."""
        while True:
            if not self.manager.is_authenticated():
                self.show_auth_menu()
            else:
                self.show_main_menu()
    
    def show_auth_menu(self):
        """Show authentication menu."""
        print("\n" + "="*50)
        print("Cloud Resource Management System - Login")
        print("="*50)
        print("1. Login")
        print("2. Register")
        print("3. Switch to Service Login (Demo)")
        print("4. Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        try:
            if choice == "1":
                self.handle_login()
            elif choice == "2":
                self.handle_register()
            elif choice == "3":
                self.switch_to_service_login()
            elif choice == "4":
                print("Exiting...")
                exit(0)
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def show_main_menu(self):
        """Show main resource management menu."""
        print("\n" + "="*50)
        print("Cloud Resource Management System")
        print(f"Logged in as: {self.manager.current_user.username} ({self.manager.current_user.role})")
        print("="*50)
        print("1. Create Resource")
        print("2. List Resources")
        print("3. Start Resource")
        print("4. Stop Resource")
        print("5. Delete Resource")
        print("6. View Resource Details")
        print("7. Logout")
        print("8. Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        try:
            if choice == "1":
                self.create_resource()
            elif choice == "2":
                self.list_resources()
            elif choice == "3":
                self.start_resource()
            elif choice == "4":
                self.stop_resource()
            elif choice == "5":
                self.delete_resource()
            elif choice == "6":
                self.view_details()
            elif choice == "7":
                self.manager.logout()
            elif choice == "8":
                print("Exiting...")
                exit(0)
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def handle_login(self):
        """Handle user login."""
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        if not self.manager.login(username, password):
            print("Login failed. Please check your credentials.")
    
    def handle_register(self):
        """Handle user registration."""
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        role = input("Role (user/admin) [user]: ").strip() or "user"
        
        self.manager.register_user(username, password, role)
    
    def switch_to_service_login(self):
        """Switch to service-based login (demo)."""
        print("\nSwitching to Service Login...")
        service_url = "https://auth.example.com"
        api_key = "demo-api-key-12345"
        
        service_login = ServiceLogin(service_url, api_key)
        self.manager.login_service = service_login
        
        print(f"Now using: {service_login.get_service_name()}")
        print("Note: Service login is in demo mode and will authenticate any non-empty credentials")
    
    def create_resource(self):
        """Create a new resource."""
        print("\nAvailable resource types:")
        types = self.manager.factory.list_available_types()
        for i, rtype in enumerate(types, 1):
            print(f"{i}. {rtype}")
        
        type_choice = input("Select resource type: ").strip()
        try:
            resource_type = types[int(type_choice) - 1]
        except (ValueError, IndexError):
            print("Invalid selection")
            return
        
        name = input("Enter resource name: ").strip()
        
        config = {'name': name}
        
        if resource_type == "AppService":
            config['runtime'] = input("Enter runtime (e.g., Python, Node.js): ").strip()
            config['region'] = input("Enter region (e.g., us-east-1): ").strip()
            config['replica_count'] = int(input("Enter replica count: ").strip())
        elif resource_type == "StorageAccount":
            config['encryption_enabled'] = input("Enable encryption? (y/n): ").strip().lower() == 'y'
            config['max_size_gb'] = int(input("Enter max size (GB): ").strip())
        elif resource_type == "CacheDB":
            config['ttl_seconds'] = int(input("Enter TTL (seconds): ").strip())
            config['capacity_mb'] = int(input("Enter capacity (MB): ").strip())
            config['eviction_policy'] = input("Enter eviction policy (LRU/FIFO): ").strip().upper()
        
        enable_logging = input("Enable logging for this resource? (y/n): ").strip().lower() == 'y'
        
        resource_id = self.manager.create_resource(resource_type, config, enable_logging)
        if resource_id:
            print(f"\nResource created successfully with ID: {resource_id}")
    
    def list_resources(self):
        """List all resources."""
        resources = self.manager.list_resources()
        
        if not resources:
            print("\nNo resources available.")
            return
        
        print("\nResources:")
        for rid, resource in resources.items():
            print(f"  [{rid}] {resource.name} - State: {resource.get_state()}")
    
    def start_resource(self):
        """Start a resource."""
        rid = input("Enter resource ID: ").strip()
        self.manager.start_resource(rid)
    
    def stop_resource(self):
        """Stop a resource."""
        rid = input("Enter resource ID: ").strip()
        self.manager.stop_resource(rid)
    
    def delete_resource(self):
        """Delete a resource."""
        rid = input("Enter resource ID: ").strip()
        self.manager.delete_resource(rid)
    
    def view_details(self):
        """View resource details."""
        rid = input("Enter resource ID: ").strip()
        details = self.manager.get_resource_details(rid)
        if details:
            print("\n" + details)


if __name__ == "__main__":
    from src.services.user_repository import User
    app = CloudResourceManagerApp()
    app.run()
