"""
AI Recommendations Engine for SRIMCA AI
Generates contextual follow-up questions and personalized guidance based on user role and query.
"""

def generate_recommendations(
    question: str, 
    answer: str, 
    user_role: str = 'student', 
    course: str = None, 
    semester: str = None
) -> dict:
    """
    Generate follow-up questions and personalized guidance based on the user's query, answer, and profile.
    
    Parameters:
    - question: The user's input question
    - answer: The AI generated answer
    - user_role: Role ('student', 'faculty', 'visitor', 'admin')
    - course: Optional student course (e.g. BCA, MCA)
    - semester: Optional student semester (e.g. 2nd, 4th)
    
    Returns:
    - Dict with 'follow_up_questions' list and 'personalized_guidance' string
    """
    q_lower = (question or "").lower()
    ans_lower = (answer or "").lower()
    role_lower = (user_role or "student").lower()

    # Topic matching for follow-up questions
    if any(k in q_lower or k in ans_lower for k in ['timetable', 'class', 'schedule', 'time', 'lecture', 'lab']):
        follow_up_questions = [
            "What are the computer lab timings?",
            "When will the mid-term exams start?",
            "Who is the class coordinator for my semester?"
        ]
    elif any(k in q_lower or k in ans_lower for k in ['exam', 'test', 'mid-term', 'schedule', 'result', 'marks']):
        follow_up_questions = [
            "What is the passing criteria for mid-term exams?",
            "How do I view internal evaluation marks?",
            "Where can I find syllabus & study materials?"
        ]
    elif any(k in q_lower or k in ans_lower for k in ['course', 'admission', 'bca', 'mca', 'mba', 'eligibility', 'intake', 'fee']):
        follow_up_questions = [
            "What is the complete fee structure for BCA/MCA?",
            "What are the placement opportunities after MCA?",
            "How can I apply for admission at UTU?"
        ]
    elif any(k in q_lower or k in ans_lower for k in ['placement', 'job', 'salary', 'package', 'company', 'recruiters']):
        follow_up_questions = [
            "Which top companies recruit from SRIMCA?",
            "What placement preparation training is provided?",
            "What was the highest package offered last year?"
        ]
    elif any(k in q_lower or k in ans_lower for k in ['facility', 'library', 'hostel', 'canteen', 'sports', 'bus', 'transport']):
        follow_up_questions = [
            "What are the central library opening hours?",
            "What bus routes cover Surat and Navsari?",
            "How do I register for campus hostel?"
        ]
    elif any(k in q_lower or k in ans_lower for k in ['assignment', 'material', 'notes', 'submission']):
        follow_up_questions = [
            "How do I submit assignments online?",
            "Where can I access past exam papers?",
            "What is the late assignment submission policy?"
        ]
    else:
        follow_up_questions = [
            "What courses are offered at SRIMCA?",
            "What are the campus facilities and computer labs?",
            "How can I contact the college principal or HOD?"
        ]

    # Personalized Guidance based on role and details
    if role_lower in ['visitor', 'guest']:
        guidance = " **Visitor Guidance:** Welcome to SRIMCA! You can explore our courses, schedule a campus visit, or inquire about BCA/MCA admissions."
    elif role_lower == 'faculty':
        guidance = " **Faculty Guidance:** You can post class notices, upload lecture materials, and create student assignments via your dashboard."
    elif role_lower == 'admin':
        guidance = " **Admin Guidance:** Use the admin console to send FCM push notifications, manage notices, and review system analytics."
    else:  # student
        course_str = f" for {course}" if course else ""
        sem_str = f" ({semester})" if semester else ""
        guidance = f" **Student Guidance:** Stay updated with your class timetable and notice board{course_str}{sem_str} to never miss an exam or assignment deadline."

    return {
        "follow_up_questions": follow_up_questions,
        "personalized_guidance": guidance
    }
