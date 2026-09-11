from .fallback import get_fallback_answer
import os

try:
    from openai import OpenAI
    api_key = os.getenv('OPENAI_API_KEY')
    openai_client = OpenAI(api_key=api_key) if api_key else None
except Exception:
    openai_client = None


def get_gpt_answer(question):
    """Answer generator using OpenAI GPT if configured, or fallback engine."""
    if openai_client:
        try:
            system_instruction = (
                "You are SRIMCA AI Assistant, the official AI guide for Shrimad Rajchandra Institute of Management and Computer Application (SRIMCA).\n"
                "1. If the user greets (hi, hello, hyy, etc.), greet them warmly and state what SRIMCA questions you can help with.\n"
                "2. If the user asks about SRIMCA, courses (BCA, MCA, MBA), admissions, timetables, facilities, campus, placements, or contact info, answer clearly and accurately.\n"
                "3. If the user asks a question completely unrelated to SRIMCA college or campus life, politely inform them that you can only answer SRIMCA college-related questions."
            )
            response = openai_client.chat.completions.create(
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
            print(f"⚠️ OpenAI error: {e}")

    try:
        answer = get_fallback_answer(question)
        if answer and answer.strip():
            return answer
    except Exception as e:
        print(f"Fallback Error: {e}")

    return "SRIMCA AI is currently unable to answer your query."
