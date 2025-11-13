"""Main CLI application for cloud resource management."""
from src.patterns.resource_factory import ResourceFactory
from src.patterns.resource_decorator import LoggingDecorator


class CloudResourceManager:
    """Main application for managing cloud resources."""
    
    def __init__(self):
        self.factory = ResourceFactory()
        self.resources = {}
        self.next_id = 1
    
    def run(self):
        """Run the main menu loop."""
        while True:
            print("\n" + "="*50)
            print("Cloud Resource Management System")
            print("="*50)
            print("1. Create Resource")
            print("2. List Resources")
            print("3. Start Resource")
            print("4. Stop Resource")
            print("5. Delete Resource")
            print("6. View Resource Details")
            print("7. Exit")
            
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
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                print(f"Error: {str(e)}")
    
    def create_resource(self):
        """Create a new resource."""
        print("\nAvailable resource types:")
        types = self.factory.list_available_types()
        for i, rtype in enumerate(types, 1):
            print(f"{i}. {rtype}")
        
        type_choice = input("Select resource type: ").strip()
        try:
            resource_type = types[int(type_choice) - 1]
        except (ValueError, IndexError):
            print("Invalid selection")
            return
        
        name = input("Enter resource name: ").strip()
        
        config = {'id': str(self.next_id), 'name': name}
        
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
        
        resource = self.factory.create_resource(resource_type, config)
        
        # Wrap with logging decorator
        enable_logging = input("Enable logging for this resource? (y/n): ").strip().lower() == 'y'
        if enable_logging:
            resource = LoggingDecorator(resource)
        
        self.resources[str(self.next_id)] = resource
        self.next_id += 1
        print(f"\nResource created successfully with ID: {config['id']}")
    
    def list_resources(self):
        """List all resources."""
        if not self.resources:
            print("\nNo resources available.")
            return
        
        print("\nResources:")
        for rid, resource in self.resources.items():
            print(f"  [{rid}] {resource.name} - State: {resource.get_state()}")
    
    def start_resource(self):
        """Start a resource."""
        rid = input("Enter resource ID: ").strip()
        if rid in self.resources:
            self.resources[rid].start()
        else:
            print("Resource not found")
    
    def stop_resource(self):
        """Stop a resource."""
        rid = input("Enter resource ID: ").strip()
        if rid in self.resources:
            self.resources[rid].stop()
        else:
            print("Resource not found")
    
    def delete_resource(self):
        """Delete a resource."""
        rid = input("Enter resource ID: ").strip()
        if rid in self.resources:
            self.resources[rid].delete()
        else:
            print("Resource not found")
    
    def view_details(self):
        """View resource details."""
        rid = input("Enter resource ID: ").strip()
        if rid in self.resources:
            print("\n" + self.resources[rid].get_details())
        else:
            print("Resource not found")


if __name__ == "__main__":
    manager = CloudResourceManager()
    manager.run()
