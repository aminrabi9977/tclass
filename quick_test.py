"""
Quick test to verify the file location fix.
Run this after the main.py hangs to see where files are actually created.
"""
import os

def check_file_locations():
    """Check where files are actually being created."""
    
    base_dir = "data/output/ai_filtered"
    temp_dir = "data/output/ai_filtered/temp"
    
    print("🔍 Checking file locations...")
    print("="*50)
    
    # Check main directory
    if os.path.exists(base_dir):
        main_files = [f for f in os.listdir(base_dir) if f.endswith('.xlsx')]
        print(f"📁 Main directory ({base_dir}):")
        if main_files:
            for f in main_files:
                print(f"   ✅ {f}")
        else:
            print("   ❌ No Excel files")
    else:
        print(f"❌ Main directory doesn't exist: {base_dir}")
    
    print()
    
    # Check temp directory
    if os.path.exists(temp_dir):
        temp_files = [f for f in os.listdir(temp_dir) if f.endswith('.xlsx')]
        print(f"📁 Temp directory ({temp_dir}):")
        if temp_files:
            for f in temp_files:
                file_path = os.path.join(temp_dir, f)
                print(f"   🔄 {f}")
                
                # Offer to move files
                if f.startswith("full_filtered_"):
                    main_path = os.path.join(base_dir, f)
                    if not os.path.exists(main_path):
                        import shutil
                        shutil.move(file_path, main_path)
                        print(f"   ➡️  Moved to main directory")
        else:
            print("   ❌ No Excel files")
    else:
        print(f"❌ Temp directory doesn't exist: {temp_dir}")
    
    print("="*50)
    print("🎯 After running this, try: python main.py again")

if __name__ == "__main__":
    check_file_locations()