"""Launcher script for Cloud Resource Management System."""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("Cloud Resource Management System")
    print("=" * 50)
    print("1. Run Simple CLI (no authentication)")
    print("2. Run Full CLI (with authentication)")
    print("3. Run Demo")
    print("4. Exit")
    
    choice = input("\nSelect option: ").strip()
    
    if choice == "1":
        from src.cli.main import CloudResourceManager
        app = CloudResourceManager()
        app.run()
    elif choice == "2":
        from src.cli.main_with_auth import CloudResourceManagerApp
        app = CloudResourceManagerApp()
        app.run()
    elif choice == "3":
        from src.cli import demo_resource_manager
        demo_resource_manager.demo_file_login()
        demo_resource_manager.demo_service_login()
        demo_resource_manager.demo_repository_operations()
    elif choice == "4":
        print("Goodbye!")
        sys.exit(0)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
