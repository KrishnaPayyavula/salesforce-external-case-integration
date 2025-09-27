#!/usr/bin/env python3
"""
Start script optimized for cloud deployment (Render, Railway, etc.)
This script ensures proper host binding for cloud platforms.
"""

import os
import uvicorn
from app.config import settings

def main():
    """Main function to start the application with cloud-optimized settings."""
    
    # Get port from environment (required by most cloud platforms)
    port = int(os.environ.get("PORT", 8000))
    
    # Force host to 0.0.0.0 for cloud deployment
    host = "0.0.0.0"
    
    # Disable reload in production
    reload = os.environ.get("DEBUG", "false").lower() == "true"
    
    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    print(f"🌐 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🔄 Reload: {reload}")
    print(f"📚 Documentation: http://{host}:{port}/docs")
    print(f"❤️  Health Check: http://{host}:{port}/health")
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
