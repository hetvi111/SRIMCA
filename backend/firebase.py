"""
Firebase Admin SDK Integration
Handles Firebase authentication and token verification
"""

import os
import json
import firebase_admin
from firebase_admin import credentials, auth
from flask import jsonify, request, g
from functools import wraps
from config import get_config

# Firebase admin instance
_firebase_app = None


def _safe_print(msg: str):
    """Print message safely on platforms with restricted output encoding (e.g. Windows cp1252)"""
    try:
        print(msg)
    except UnicodeEncodeError:
        try:
            safe_msg = msg.encode('ascii', 'backslashreplace').decode('ascii')
            print(safe_msg)
        except Exception:
            pass


def initialize_firebase():
    """
    Initialize Firebase Admin SDK
    Uses the service account JSON file directly
    """
    global _firebase_app
    
    # Check if Firebase is already initialized
    if _firebase_app is not None:
        return _firebase_app
    
    try:
        # Try to load from JSON file
        json_path = os.path.join(os.path.dirname(__file__), 'srimcaai-firebase-adminsdk-fbsvc-e50090f727.json')
        
        if os.path.exists(json_path):
            cred = credentials.Certificate(json_path)
            _firebase_app = firebase_admin.initialize_app(cred)
            _safe_print(f"✅ Firebase Admin SDK initialized from JSON file")
            return _firebase_app
        else:
            # Fall back to environment variables
            config = get_config()
            if not config.FIREBASE_PRIVATE_KEY or not config.FIREBASE_CLIENT_EMAIL:
                _safe_print("⚠️ Firebase credentials not found. Firebase auth will be disabled.")
                return None
            
            # Handle newlines in private key
            private_key = config.FIREBASE_PRIVATE_KEY
            if '\\n' in private_key:
                private_key = private_key.replace('\\n', '\n')
            
            cred_dict = {
                "type": "service_account",
                "project_id": config.FIREBASE_PROJECT_ID,
                "private_key": private_key,
                "client_email": config.FIREBASE_CLIENT_EMAIL,
                "token_uri": "https://oauth2.googleapis.com/token",
            }
            
            cred = credentials.Certificate(cred_dict)
            _firebase_app = firebase_admin.initialize_app(cred)
            _safe_print(f"✅ Firebase Admin SDK initialized for project: {config.FIREBASE_PROJECT_ID}")
            return _firebase_app
        
    except Exception as e:
        _safe_print(f"❌ Failed to initialize Firebase: {e}")
        return None


def get_firebase_app():
    """Get the Firebase app instance"""
    global _firebase_app
    
    if _firebase_app is None:
        initialize_firebase()
    
    return _firebase_app


def verify_firebase_token(id_token: str):
    """
    Verify a Firebase ID token
    Returns the decoded token if valid, None otherwise
    """
    try:
        app = get_firebase_app()
        if app is None:
            return None
        
        decoded_token = auth.verify_id_token(id_token, app=app)
        return decoded_token
    
    except auth.InvalidIdTokenError:
        print("Invalid Firebase ID token")
        return None
    except auth.ExpiredIdTokenError:
        print("Expired Firebase ID token")
        return None
    except Exception as e:
        print(f"Firebase token verification error: {e}")
        return None


def get_firebase_user(uid: str):
    """
    Get Firebase user by UID
    Returns user record if found, None otherwise
    """
    try:
        app = get_firebase_app()
        if app is None:
            return None
        
        user = auth.get_user(uid, app=app)
        return user
    
    except auth.UserNotFoundError:
        return None
    except Exception as e:
        print(f"Error getting Firebase user: {e}")
        return None


def create_custom_token(uid: str, additional_claims: dict = None):
    """
    Create a custom Firebase token
    Can be used for custom authentication flow
    """
    try:
        app = get_firebase_app()
        if app is None:
            return None
        
        custom_token = auth.create_custom_token(uid, developer_claims=additional_claims, app=app)
        if isinstance(custom_token, bytes):
            return custom_token.decode('utf-8')
        return custom_token
    
    except Exception as e:
        print(f"Error creating custom token: {e}")
        return None


def require_firebase_auth(f):
    """
    Decorator to require Firebase authentication for Flask routes
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the ID token from the request header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'No authorization header provided'}), 401
        
        # Check if it's a Bearer token
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'error': 'Invalid authorization header format'}), 401
        
        id_token = parts[1]
        
        # Verify the token
        decoded_token = verify_firebase_token(id_token)
        
        if decoded_token is None:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Add the decoded token to Flask g and request context
        g.firebase_user = decoded_token
        g.firebase_uid = decoded_token.get('uid')
        setattr(request, 'firebase_user', decoded_token)
        setattr(request, 'firebase_uid', decoded_token.get('uid'))
        
        return f(*args, **kwargs)
    
    return decorated_function


def optional_firebase_auth(f):
    """
    Decorator for optional Firebase authentication
    If a valid token is provided, it will be available in request.firebase_user / g.firebase_user
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        user = None
        uid = None
        
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                id_token = parts[1]
                decoded_token = verify_firebase_token(id_token)
                if decoded_token:
                    user = decoded_token
                    uid = decoded_token.get('uid')
        
        g.firebase_user = user
        g.firebase_uid = uid
        setattr(request, 'firebase_user', user)
        setattr(request, 'firebase_uid', uid)
        
        return f(*args, **kwargs)
    
    return decorated_function


def get_user_by_email(email: str):
    """
    Get Firebase user by email
    Returns user record if found, None otherwise
    """
    try:
        app = get_firebase_app()
        if app is None:
            return None
        
        user = auth.get_user_by_email(email, app=app)
        return user
    
    except auth.UserNotFoundError:
        return None
    except Exception as e:
        print(f"Error getting user by email: {e}")
        return None


def is_firebase_enabled():
    """Check if Firebase is properly initialized"""
    return get_firebase_app() is not None


# ================= FCM PUSH NOTIFICATIONS =================

def _get_android_config(priority: str = 'medium'):
    """Generate Android-specific configuration with priority mapping"""
    try:
        from firebase_admin import messaging
        priority_map = {
            'emergency': 'high',
            'high': 'high',
            'medium': 'normal',
            'low': 'normal'
        }
        fcm_priority = priority_map.get(priority.lower(), 'normal')
        return messaging.AndroidConfig(
            priority=fcm_priority,
            notification=messaging.AndroidNotification(
                channel_id='srimca_high_priority' if fcm_priority == 'high' else 'srimca_default'
            )
        )
    except Exception:
        return None


def send_push_notification(
    title: str,
    body: str,
    target_role: str = 'all',
    target_topics: list = None,
    priority: str = 'medium',
    data: dict = None
):
    """
    Send push notification to users based on role, target topics, and priority.
    
    Parameters:
    - title: Notification title
    - body: Notification body
    - target_role: 'all', 'student', 'faculty', 'admin'
    - target_topics: List of topic names (e.g. ['mca', 'mca_sem3'])
    - priority: 'emergency', 'high', 'medium', 'low'
    - data: Optional data payload (e.g. {'route': 'notice', 'notice_id': '123'})
    """
    app = get_firebase_app()
    if app is None:
        _safe_print("⚠️ Firebase not initialized. Skipping push notification.")
        return False

    try:
        from firebase_admin import messaging

        data_payload = {str(k): str(v) for k, v in (data or {}).items()}
        data_payload['priority'] = priority
        if 'route' not in data_payload and 'type' in data_payload:
            data_payload['route'] = data_payload['type']

        android_config = _get_android_config(priority)

        # Build list of topics to send to
        topics_to_send = set()
        
        if target_role:
            role_topic = target_role if target_role in ['student', 'faculty', 'admin'] else 'all'
            topics_to_send.add(role_topic)
            
        if target_topics:
            for top in target_topics:
                clean_top = str(top).strip().lower().replace(' ', '_')
                if clean_top:
                    topics_to_send.add(clean_top)

        # 1. Send push to each target topic
        for topic_name in topics_to_send:
            try:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=title,
                        body=body,
                    ),
                    data=data_payload,
                    topic=topic_name,
                    android=android_config,
                )
                response = messaging.send(message, app=app)
                _safe_print(f'✅ FCM push notification sent to topic "{topic_name}": {response}')
            except Exception as topic_err:
                _safe_print(f'⚠️ Error sending to topic "{topic_name}": {topic_err}')

        # 2. If notification type is exam, notice, or event, also dispatch to type topic
        notif_type = data_payload.get('type')
        if notif_type in ['exam', 'notice', 'event'] and notif_type not in topics_to_send:
            try:
                cat_message = messaging.Message(
                    notification=messaging.Notification(
                        title=title,
                        body=body,
                    ),
                    data=data_payload,
                    topic=notif_type,
                    android=android_config,
                )
                cat_response = messaging.send(cat_message, app=app)
                _safe_print(f'✅ FCM push notification sent to category topic "{notif_type}": {cat_response}')
            except Exception as cat_err:
                _safe_print(f'⚠️ Error sending to category topic: {cat_err}')

        # 3. Send direct push to saved device FCM tokens in database
        try:
            from database import get_collection, Collections
            users_col = get_collection(Collections.USERS)
            query = {'fcm_token': {'$exists': True, '$ne': None, '$ne': ''}}
            if target_role in ['student', 'faculty', 'admin']:
                query['role'] = target_role
                
            user_docs = list(users_col.find(query, {'fcm_token': 1}))
            tokens = [u['fcm_token'] for u in user_docs if u.get('fcm_token')]
            
            if tokens:
                for token in tokens:
                    try:
                        send_notification_to_user(token, title, body, data_payload, priority=priority)
                    except Exception:
                        pass
        except Exception as db_err:
            _safe_print(f'⚠️ Error fetching device FCM tokens from DB: {db_err}')

        return True
        
    except Exception as e:
        _safe_print(f'❌ Error sending push notification: {e}')
        return False


def send_notification_to_user(
    token: str,
    title: str,
    body: str,
    data: dict = None,
    priority: str = 'medium'
):
    """
    Send push notification to a specific device token
    
    Parameters:
    - token: FCM device token
    - title: Notification title
    - body: Notification body
    - data: Optional data payload
    - priority: Notification priority tag
    """
    app = get_firebase_app()
    if app is None:
        _safe_print("⚠️ Firebase not initialized. Skipping push notification to device.")
        return False

    try:
        from firebase_admin import messaging

        data_payload = {str(k): str(v) for k, v in (data or {}).items()}
        data_payload['priority'] = priority
        android_config = _get_android_config(priority)

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data_payload,
            token=token,
            android=android_config,
        )
        
        response = messaging.send(message, app=app)
        _safe_print(f'✅ FCM push notification sent to device token: {response}')
        return True
        
    except Exception as e:
        _safe_print(f'❌ Error sending push notification to device: {e}')
        return False
