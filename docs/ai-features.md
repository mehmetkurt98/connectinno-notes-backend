# AI Features Documentation

## Overview

Connectinno Notes Backend API, Google Gemini API kullanarak AI destekli özellikler sunar.

## Available AI Features

### 1. Note Summarization
- Uzun notları özetler
- Ana noktaları çıkarır
- Kelime sayısını azaltır

### 2. Todo Extraction
- Not içeriğinden todo'ları çıkarır
- Yapılacak işleri listeler
- Otomatik todo oluşturma

## Google Gemini API Integration

### Configuration
```env
GEMINI_API_KEY=your-gemini-api-key
```

### API Setup
1. Google AI Studio'da API key alın
2. Environment variable olarak ayarlayın
3. API key'i güvenli şekilde saklayın

## API Endpoints

### Summarize Note

**POST** `/api/ai/summarize`

Not içeriğini özetler.

**Request Body:**
```json
{
  "content": "Uzun not içeriği buraya yazılır..."
}
```

**Response:**
```json
{
  "summary": "Özetlenmiş içerik",
  "original_length": 150,
  "summary_length": 50
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/ai/summarize" \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{
       "content": "Bu çok uzun bir not içeriği. İçinde birçok bilgi var. Ana konular şunlar: teknoloji, iş, kişisel gelişim. Her konu hakkında detaylı bilgiler mevcut."
     }'
```

### Extract Todos

**POST** `/api/ai/extract-todos`

Not içeriğinden todo'ları çıkarır.

**Request Body:**
```json
{
  "content": "Yapılacak işler: market alışverişi, doktor randevusu, proje raporu"
}
```

**Response:**
```json
{
  "todos": [
    "Market alışverişi",
    "Doktor randevusu",
    "Proje raporu"
  ],
  "count": 3
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/ai/extract-todos" \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{
       "content": "Bugün yapılacaklar: sabah kalk, elma ye, okula git, ödev yap, akşam yemek hazırla"
     }'
```

## Implementation Details

### AI Service Class
```python
class AIService:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
    
    def summarize_content(self, content: str) -> dict:
        # Summarization logic
        pass
    
    def extract_todos(self, content: str) -> dict:
        # Todo extraction logic
        pass
```

### Error Handling
- API key validation
- Rate limiting
- Content length limits
- Fallback responses

## Usage Examples

### Flutter Integration
```dart
// Summarize note
final response = await dio.post('/api/ai/summarize', data: {
  'content': noteContent,
});

// Extract todos
final response = await dio.post('/api/ai/extract-todos', data: {
  'content': noteContent,
});
```

### JavaScript Integration
```javascript
// Summarize note
const response = await fetch('/api/ai/summarize', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    content: noteContent
  })
});
```

## Performance Considerations

### 1. Response Time
- AI API calls can take 2-5 seconds
- Implement loading states in UI
- Consider caching for repeated requests

### 2. Rate Limiting
- Google Gemini API has rate limits
- Implement client-side rate limiting
- Handle rate limit errors gracefully

### 3. Content Length
- Very long content may timeout
- Implement content length limits
- Split large content into chunks

## Error Handling

### Common Errors

#### 1. API Key Issues
```json
{
  "detail": "Invalid API key"
}
```

#### 2. Rate Limiting
```json
{
  "detail": "Rate limit exceeded"
}
```

#### 3. Content Too Long
```json
{
  "detail": "Content too long for processing"
}
```

#### 4. AI Service Unavailable
```json
{
  "detail": "AI service temporarily unavailable"
}
```

## Testing

### Unit Tests
```python
def test_summarize_content():
    ai_service = AIService("test-api-key")
    result = ai_service.summarize_content("Test content")
    assert "summary" in result

def test_extract_todos():
    ai_service = AIService("test-api-key")
    result = ai_service.extract_todos("Do this, do that")
    assert "todos" in result
```

### Integration Tests
```python
def test_summarize_endpoint():
    response = client.post("/api/ai/summarize", json={
        "content": "Test content"
    })
    assert response.status_code == 200
    assert "summary" in response.json()
```

## Security Considerations

### 1. API Key Protection
- Never expose API key in client code
- Use environment variables
- Rotate keys regularly

### 2. Content Privacy
- Content is sent to Google Gemini API
- Ensure compliance with privacy policies
- Consider data encryption

### 3. Input Validation
- Validate input content
- Sanitize user input
- Prevent injection attacks

## Future Enhancements

### 1. Additional AI Features
- Content categorization
- Sentiment analysis
- Language translation
- Content generation

### 2. Performance Improvements
- Response caching
- Batch processing
- Async processing

### 3. Advanced Features
- Custom AI models
- User-specific training
- Advanced analytics
