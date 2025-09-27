#!/usr/bin/env python3
"""Simple script to run the Salesforce External Case Integration API."""

import os
import uvicorn
from app.config import settings

if __name__ == "__main__":
    # Override settings for cloud deployment
    host = os.environ.get("HOST", settings.host)
    port = int(os.environ.get("PORT", settings.port))
    debug = os.environ.get("DEBUG", str(settings.debug)).lower() == "true"
    
    print(f"Starting {settings.app_name} v{settings.app_version}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print(f"API Documentation: http://{host}:{port}/docs")
    print(f"Health Check: http://{host}:{port}/health")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
