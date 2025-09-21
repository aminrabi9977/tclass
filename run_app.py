"""
Performance-optimized launcher for the Tender Processing Web Application.
This script optimizes Streamlit for better performance.
"""

import streamlit as st
import os
import sys
from pathlib import Path

def setup_performance_optimizations():
    """Configure Streamlit for optimal performance."""
    
    # Set Streamlit configuration for performance
    st.set_page_config(
        page_title="Tender Processing System",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Performance configurations
    os.environ.setdefault('STREAMLIT_SERVER_MAX_UPLOAD_SIZE', '200')  # 200MB max upload
    os.environ.setdefault('STREAMLIT_SERVER_MAX_MESSAGE_SIZE', '200')  # 200MB max message
    os.environ.setdefault('STREAMLIT_BROWSER_GATHER_USAGE_STATS', 'false')  # Disable telemetry
    os.environ.setdefault('STREAMLIT_SERVER_ENABLE_CORS', 'false')  # Disable CORS for speed
    os.environ.setdefault('STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION', 'false')  # Disable XSRF for speed
    
    # Cache configurations
    os.environ.setdefault('STREAMLIT_SERVER_ENABLE_STATIC_SERVING', 'true')
    
def main():
    """Main launcher function."""
    
    # Set up performance optimizations
    setup_performance_optimizations()
    
    # Get the directory of this script
    app_dir = Path(__file__).parent
    
    # Path to the main app
    app_path = app_dir / "app.py"
    
    if not app_path.exists():
        print("❌ Error: app.py not found!")
        print(f"Looking for: {app_path}")
        return 1
    
    # Import and run the app
    try:
        import subprocess
        import sys
        
        # Run Streamlit with optimized settings
        cmd = [
            sys.executable, "-m", "streamlit", "run", str(app_path),
            "--server.maxUploadSize=200",
            "--server.maxMessageSize=200",
            "--browser.gatherUsageStats=false",
            "--server.enableCORS=false",
            "--server.enableXsrfProtection=false",
            "--theme.primaryColor=#667eea",
            "--theme.backgroundColor=#ffffff",
            "--theme.secondaryBackgroundColor=#f0f2f6"
        ]
        
        print("🚀 Starting Tender Processing System...")
        print("📊 Optimized for performance")
        print("🌐 Opening in your default browser...")
        
        # Run the command
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())