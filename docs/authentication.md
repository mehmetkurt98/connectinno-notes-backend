# Authentication Documentation

## Overview

Connectinno Notes Backend API, Firebase Authentication kullanarak güvenli erişim sağlar.

## Authentication Flow

### 1. Client Authentication
- Kullanıcı Flutter uygulamasında Firebase Auth ile giriş yapar
- Firebase ID token alır
- Token'ı her API isteğinde `Authorization` header'ında gönderir

### 2. Server Verification
- Backend Firebase Admin SDK kullanarak token'ı doğrular
- Token geçerliyse kullanıcı bilgilerini alır
- Endpoint'e erişim sağlanır

## Token Format

```
Authorization: Bearer <firebase-id-token>
```

## Firebase Configuration

### Service Account Setup
1. Firebase Console'da proje oluşturun
2. Service Account key indirin
3. `serviceAccountKey.json` olarak kaydedin
4. Environment variable olarak ayarlayın

### Environment Variables
```env
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_SERVICE_ACCOUNT_PATH=./serviceAccountKey.json
```

## Token Verification Process

### 1. Token Extraction
```python
def get_current_user(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split(" ")
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=401, detail="Invalid token format")
        return token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
```

### 2. Firebase Verification
```python
def verify_firebase_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
```

## User Context

Her istekte kullanıcı bilgileri otomatik olarak alınır:

```python
{
    "uid": "user-uid",
    "email": "user@example.com",
    "email_verified": boolean,
    "firebase": {
        "identities": {
            "email": ["user@example.com"]
        },
        "sign_in_provider": "password"
    }
}
```

## Authorization

### Owner-based Access
- Kullanıcılar sadece kendi notlarına erişebilir
- Her istekte `owner_uid` kontrol edilir
- Veriler kullanıcı bazında izole edilir

### Example Implementation
```python
def check_ownership(note: dict, user_uid: str):
    if note.get("owner_uid") != user_uid:
        raise HTTPException(status_code=403, detail="Access denied")
```

## Error Handling

### 401 Unauthorized
- Invalid token
- Expired token
- Missing token
- Malformed token

### 403 Forbidden
- Valid token but insufficient permissions
- Access to other user's data

## Security Best Practices

### 1. Token Validation
- Her istekte token doğrulanır
- Expired token'lar reddedilir
- Invalid token'lar reddedilir

### 2. Data Isolation
- Kullanıcılar sadece kendi verilerine erişebilir
- Owner UID kontrolü yapılır
- Cross-user data access engellenir

### 3. Error Messages
- Güvenlik açığı yaratmayacak error mesajları
- Detaylı hata bilgisi verilmez
- Generic error responses

## Testing Authentication

### Valid Token Test
```bash
curl -H "Authorization: Bearer <valid-token>" \
     http://localhost:8000/api/notes
```

### Invalid Token Test
```bash
curl -H "Authorization: Bearer invalid-token" \
     http://localhost:8000/api/notes
```

### Missing Token Test
```bash
curl http://localhost:8000/api/notes
```

## Production Considerations

### 1. Token Refresh
- Client tarafında token refresh implementasyonu
- Expired token handling
- Automatic re-authentication

### 2. Rate Limiting
- API rate limiting uygulanması
- Brute force attack koruması
- DDoS protection

### 3. Monitoring
- Authentication failure monitoring
- Suspicious activity detection
- Log analysis

## Troubleshooting

### Common Issues

#### 1. "Invalid token" Error
- Token'ın expire olup olmadığını kontrol edin
- Token format'ının doğru olduğundan emin olun
- Firebase project ID'sinin doğru olduğunu kontrol edin

#### 2. "Access denied" Error
- Kullanıcının not sahibi olduğundan emin olun
- Owner UID'sinin doğru olduğunu kontrol edin

#### 3. "Service account" Error
- Service account key dosyasının doğru konumda olduğundan emin olun
- Environment variable'ların doğru ayarlandığını kontrol edin
