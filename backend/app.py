from flask import Flask, jsonify
from flask_cors import CORS
from config import FLASK_DEBUG, FLASK_PORT
from database import db

# Import routes
from routes.auth_routes import auth_bp
from routes.ai_routes import ai_bp


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configure app
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['DEBUG'] = FLASK_DEBUG
    
    # Enable CORS for all routes (allows cross-origin requests from Flutter web)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints (routes)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    
    # Health check endpoint
    @app.route('/')
    def index():
        return jsonify({
            "success": True,
            "message": "SRIMCA AI API Server",
            "version": "1.0.0",
            "endpoints": {
                "auth": "/api/auth",
                "register": "POST /api/auth/register",
                "login": "POST /api/auth/login",
                "profile": "GET /api/auth/profile",
                "ai": "/api/ai"
            }
        })
    
    @app.route('/health')
    def health():
        return jsonify({
            "success": True,
            "status": "healthy",
            "database": "connected" if db.client else "disconnected"
        })

    # Helpful AI base endpoint to avoid generic 404 when client mistakenly hits /api/ai
    @app.route('/api/ai', methods=['GET'])
    def ai_base():
        return jsonify({
            "success": False,
            "message": "Use POST /api/ai/ask or POST /api/ai/ask-guest"
        }), 404

    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "message": "Endpoint not found"}), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"success": False, "message": "Internal server error"}), 500
    
    return app


# Create app instance
app = create_app()


if __name__ == '__main__':
    print(f"Starting SRIMCA AI API Server...")
    print(f"Server running at: http://localhost:{FLASK_PORT}")
    print(f"API Endpoints: http://localhost:{FLASK_PORT}/api/auth")
    app.run(host='0.0.0.0', port=FLASK_PORT, debug=FLASK_DEBUG)
