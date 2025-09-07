# Connectinno Notes - Backend API - Case Study - Mehmet Kurt - Flutter  Dev.

FastAPI-based backend service providing RESTful API for the Flutter application.

## 🚀 Features

### 🔐 Authentication
- **Firebase JWT Verification**: Firebase ID token verification on every request
- **Secure Endpoints**: All endpoints require authentication
- **User Context**: User information automatically retrieved on every request

### 📝 Notes API
- **CRUD Operations**: Create, Read, Update, Delete operations
- **Owner-based Access**: Users can only access their own notes
- **Soft Delete**: Notes are securely deleted
- **Real-time Updates**: Real-time data synchronization with Firestore

### 🤖 AI Features
- **Note Summarization**: Note summarization with Google Gemini API
- **Todo Extraction**: Automatic todo extraction from notes
- **Smart Processing**: AI-powered content analysis

### 🔄 Data Management
- **Firestore Integration**: Google Cloud Firestore database
- **Data Validation**: Data validation with Pydantic
- **Error Handling**: Comprehensive error handling
- **Logging**: Detailed logging

## 🛠️ Tech Stack

- **FastAPI**: Modern Python web framework
- **Python**: 3.8+
- **Firebase Admin SDK**: Token verification and Firestore access
- **Google Cloud Firestore**: NoSQL database
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server
- **Google Gemini API**: AI features

## 📦 Installation

### Prerequisites
- Python 3.8+
- Firebase project
- Google Gemini API key
- Firestore database

### Environment Setup

1. **Create Virtual Environment**:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

3. **Environment Variables**:
Create `.env` file:
```env
FIREBASE_PROJECT_ID=your-project-id
GEMINI_API_KEY=your-gemini-api-key
FIREBASE_SERVICE_ACCOUNT_PATH=./serviceAccountKey.json
```

4. **Firebase Service Account**:
- Download service account key from Firebase Console
- Save as `serviceAccountKey.json`

### Running

```bash
# Development mode
uvicorn main:app --reload --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📚 API Endpoints

### Authentication
All endpoints require `Authorization: Bearer <firebase-id-token>` header.

### Notes Endpoints

#### `POST /api/notes`
Creates a new note.

**Request Body**:
```json
{
  "title": "Note Title",
  "content": "Note content",
  "id": "unique-id",
  "owner_uid": "user-uid",
  "created_at": "2025-01-07T10:00:00Z",
  "updated_at": "2025-01-07T10:00:00Z",
  "dirty": false,
  "deleted": false,
  "hasTodos": false,
  "todos": []
}
```

#### `GET /api/notes`
Gets all notes for the user.

#### `GET /api/notes/{note_id}`
Gets a specific note.

#### `PUT /api/notes/{note_id}`
Updates a note.

#### `DELETE /api/notes/{note_id}`
Deletes a note (soft delete).

#### `DELETE /api/notes/{note_id}/permanent`
Permanently deletes a note.

### AI Endpoints

#### `POST /api/ai/summarize`
Summarizes note content.

**Request Body**:
```json
{
  "content": "Note content to summarize"
}
```

#### `POST /api/ai/extract-todos`
Extracts todos from content.

**Request Body**:
```json
{
  "content": "Note content to extract todos from"
}
```

## 🔒 Security

### Authentication Flow
1. **Client**: Logs in with Firebase Auth
2. **Token**: Gets Firebase ID token
3. **Request**: Sends token in `Authorization` header
4. **Backend**: Verifies token with Firebase Admin SDK
5. **Access**: Endpoint access granted if verification successful

### Authorization
- **Owner-based Access**: Users can only access their own notes
- **UID Verification**: User UID is checked on every request
- **Data Isolation**: Data is isolated per user

## 🏗️ Architecture

### Project Structure
```
connectinno_backend/
├── main.py                 # FastAPI app and route definitions
├── auth.py                 # Firebase authentication
├── repository.py           # Firestore data access
├── schemas.py              # Pydantic models
├── ai_service.py           # AI features (Gemini API)
├── config.py               # Configuration
├── firebase_config.py      # Firebase setup
├── routes/
│   └── notes.py           # Notes endpoints
├── requirements.txt        # Python dependencies
└── serviceAccountKey.json  # Firebase service account
```

### Data Flow
1. **Request** → FastAPI endpoint
2. **Authentication** → Firebase token verification
3. **Validation** → Pydantic model validation
4. **Repository** → Firestore data access
5. **Response** → JSON response

## 🧪 Testing

### API Testing
```bash
# Run test script
python test_api.py

# Gemini API test
python test_gemini.py

# Todo extraction test
python test_todo_extraction.py
```

### Manual Testing
```bash
# API key check
python check_api_key.py
```

## 📊 Monitoring

### Logging
- **Request Logging**: All API requests are logged
- **Error Logging**: Error conditions are logged in detail
- **Performance Logging**: Response times are tracked

### Health Check
```bash
curl http://localhost:8000/health
```

## 🚀 Deployment

### Environment Variables
Set the following environment variables in production:
- `FIREBASE_PROJECT_ID`
- `GEMINI_API_KEY`
- `FIREBASE_SERVICE_ACCOUNT_PATH`

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔧 Configuration

### Firebase Setup
1. Create project in Firebase Console
2. Enable Authentication
3. Create Firestore database
4. Download service account key

### Gemini API Setup
1. Get API key from Google AI Studio
2. Set as environment variable

## 📝 API Documentation

FastAPI automatically generates API documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📚 Detailed Documentation

For more detailed information, see the [docs/](./docs/) folder:
- [API Endpoints](./docs/api-endpoints.md)
- [Authentication](./docs/authentication.md)
- [AI Features](./docs/ai-features.md)
- [Deployment](./docs/deployment.md)

