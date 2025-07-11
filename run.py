#!/usr/bin/env python3
"""
Run script for Translation Service
Starts the FastAPI server
"""

import os
import sys
import uvicorn
from dotenv import load_dotenv

def main():
    """Start the translation service."""
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    print("🚀 Starting Translation Service...")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🔄 Reload: {reload}")
    print("\n🌐 Service will be available at:")
    print(f"   - Main API: http://{host}:{port}")
    print(f"   - Health Check: http://{host}:{port}/health")
    print(f"   - Swagger UI: http://{host}:{port}/docs")
    print(f"   - ReDoc: http://{host}:{port}/redoc")
    print("\n⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 