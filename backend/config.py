import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "srimca_ai")

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "d352729f824cc6f38bc774a3f70086c06c9dbe34107086a156c76acc4c406c77")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION = os.getenv("JWT_EXPIRATION", "24h")

# OpenAI Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyANFmDjDUfI3wZkkE0irxaB_3x_2VWyeXk")

# Server Configuration
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
