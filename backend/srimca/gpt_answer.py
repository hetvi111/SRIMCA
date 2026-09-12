from .fallback import get_fallback_answer
import os

_openai_client = None

def get_client():
    global _openai_client
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return None
    if _openai_client is None:
        try:
            from openai import OpenAI
            _openai_client = OpenAI(api_key=api_key)
        except Exception as e:
            print(f"⚠️ OpenAI init error: {e}")
            return None
    return _openai_client


def get_gpt_answer(question):
    """Answer generator using OpenAI GPT if configured, or fallback engine."""
    client = get_client()
    if client:
        try:
            system_instruction = (
                "You are SRIMCA AI Assistant, the official AI guide for Shrimad Rajchandra Institute of Management and Computer Application (SRIMCA).\n"
                "1. If the user greets (hi, hello, hyy, namaste, કેમ છો, etc.), greet them warmly and state what SRIMCA questions you can help with.\n"
                "2. If the user asks about SRIMCA, courses (BCA, MCA, MBA), admissions, timetables, facilities, campus, placements, or contact info, answer clearly and accurately.\n"
                "3. If the user asks a question completely unrelated to SRIMCA college or campus life, politely inform them that you can only answer SRIMCA college-related questions.\n"
                "4. MULTILINGUAL REQUIREMENT: Automatically detect the user's language and respond in the SAME language (Supports English, Gujarati, and Hindi).\n"
                "   - If the query is in Gujarati (ગુજરાતી), reply in clear Gujarati script.\n"
                "   - If the query is in Hindi (हिंदी), reply in clear Hindi script.\n"
                "   - If the query is in English, reply in English."
            )
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": question}
                ],
                timeout=8,
                temperature=0.3,
                max_tokens=250
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[OpenAI Error]: {e}")

    try:
        answer = get_fallback_answer(question)
        if answer and answer.strip():
            return answer
    except Exception as e:
        print(f"Fallback Error: {e}")

    return "SRIMCA AI is currently unable to answer your query."
