import sys
import os

# Add the backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import init_db
from app.config import settings

if __name__ == "__main__":
    print(f"Initializing database: {settings.database_name}")
    try:
        init_db()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)
