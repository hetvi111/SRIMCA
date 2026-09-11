from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime, timedelta
from srimca.app import ask
from database import get_collection, Collections
from models import AIQueryModel

from srimca.recommendations import generate_recommendations

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')


def process_ai_request(save_query=True):
    data = request.get_json() or {}

    question = data.get('question', '').strip()
    user_id = data.get('user_id', '').strip()
    user_role = data.get('role', data.get('user_role', 'student')).strip()
    user_course = data.get('course', '').strip()
    user_semester = data.get('semester', '').strip()

    if not question:
        return jsonify({
            'status': 'error',
            'message': 'Question required'
        }), 400

    try:
        answer = ask(question)

        if not answer:
            answer = "I couldn't generate a response."

        rec = generate_recommendations(
            question=question,
            answer=answer,
            user_role=user_role,
            course=user_course,
            semester=user_semester
        )

        if save_query and user_id:
            ai_queries = get_collection(Collections.AI_QUERIES)

            query_doc = AIQueryModel.create_query(
                user_id=user_id,
                query=question,
                response=answer
            )

            ai_queries.insert_one(query_doc)

        return jsonify({
            'status': 'success',
            'success': True,
            'answer': answer,
            'follow_up_questions': rec['follow_up_questions'],
            'suggestions': rec['follow_up_questions'],
            'personalized_guidance': rec['personalized_guidance']
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'success': False,
            'message': str(e)
        }), 500


# Existing endpoint
@ai_bp.route('/chat', methods=['POST'])
def chat():
    return process_ai_request(save_query=True)


# Student endpoint
@ai_bp.route('/ask', methods=['POST'])
def ask_ai():
    return process_ai_request(save_query=True)


# Visitor endpoint
@ai_bp.route('/ask-guest', methods=['POST'])
def ask_guest():
    return process_ai_request(save_query=False)
