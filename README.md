# SRIMCA AI - Smart College Assistant

A Flutter-based college assistant application with AI-powered chatbot for students, faculty, and visitors.

## Features

- **User Authentication**: Role-based login (Student, Faculty, Visitor)
- **AI Chatbot**: Get instant answers about college information
- **Notices**: View college notices and events
- **Profile Management**: User profile management

## Tech Stack

### Backend
- Python Flask
- MongoDB
- JWT Authentication
- OpenAI GPT

### Frontend
- Flutter
- Dart

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
# Add your OpenAI API key in .env
python app.py
```

### Frontend
```bash
cd frontend
flutter pub get
flutter run
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register` | POST | Register |
| `/api/auth/login` | POST | Login |
| `/api/ai/ask` | POST | Ask AI |
| `/api/ai/ask-guest` | POST | Ask AI (visitor) |
| `/health` | GET | Health check |

## Project Structure

```
srimca_ai/
├── backend/          # Flask API
├── frontend/         # Flutter app
├── TODO.md          # TODO list
└── README.md       # This file
```

## License

MIT
