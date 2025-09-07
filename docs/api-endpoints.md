# API Endpoints Documentation

## Overview

Bu dokümantasyon Connectinno Notes Backend API'sinin tüm endpoint'lerini detaylı olarak açıklar.

## Base URL

```
http://localhost:8000
```

## Authentication

Tüm endpoint'ler Firebase JWT token gerektirir:

```
Authorization: Bearer <firebase-id-token>
```

## Notes Endpoints

### Create Note

**POST** `/api/notes`

Yeni bir not oluşturur.

**Request Body:**
```json
{
  "title": "string",
  "content": "string",
  "id": "string",
  "owner_uid": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "dirty": boolean,
  "deleted": boolean,
  "hasTodos": boolean,
  "todos": ["string"]
}
```

**Response:**
```json
{
  "title": "string",
  "content": "string",
  "id": "string",
  "owner_uid": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "dirty": boolean,
  "deleted": boolean,
  "hasTodos": boolean,
  "todos": ["string"]
}
```

### Get All Notes

**GET** `/api/notes`

Kullanıcının tüm notlarını getirir.

**Response:**
```json
[
  {
    "title": "string",
    "content": "string",
    "id": "string",
    "owner_uid": "string",
    "created_at": "datetime",
    "updated_at": "datetime",
    "dirty": boolean,
    "deleted": boolean,
    "hasTodos": boolean,
    "todos": ["string"]
  }
]
```

### Get Single Note

**GET** `/api/notes/{note_id}`

Belirli bir notu getirir.

**Parameters:**
- `note_id` (string): Not ID'si

**Response:**
```json
{
  "title": "string",
  "content": "string",
  "id": "string",
  "owner_uid": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "dirty": boolean,
  "deleted": boolean,
  "hasTodos": boolean,
  "todos": ["string"]
}
```

### Update Note

**PUT** `/api/notes/{note_id}`

Notu günceller.

**Parameters:**
- `note_id` (string): Not ID'si

**Request Body:**
```json
{
  "title": "string",
  "content": "string",
  "id": "string",
  "owner_uid": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "dirty": boolean,
  "deleted": boolean,
  "hasTodos": boolean,
  "todos": ["string"]
}
```

### Delete Note (Soft Delete)

**DELETE** `/api/notes/{note_id}`

Notu siler (soft delete).

**Parameters:**
- `note_id` (string): Not ID'si

**Response:**
```json
{
  "message": "Note deleted successfully"
}
```

### Permanent Delete Note

**DELETE** `/api/notes/{note_id}/permanent`

Notu kalıcı olarak siler.

**Parameters:**
- `note_id` (string): Not ID'si

**Response:**
```json
{
  "message": "Note permanently deleted"
}
```

## AI Endpoints

### Summarize Note

**POST** `/api/ai/summarize`

Not içeriğini özetler.

**Request Body:**
```json
{
  "content": "string"
}
```

**Response:**
```json
{
  "summary": "string",
  "original_length": integer,
  "summary_length": integer
}
```

### Extract Todos

**POST** `/api/ai/extract-todos`

Not içeriğinden todo'ları çıkarır.

**Request Body:**
```json
{
  "content": "string"
}
```

**Response:**
```json
{
  "todos": ["string"],
  "count": integer
}
```

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Invalid or missing token"
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied"
}
```

### 404 Not Found
```json
{
  "detail": "Note not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["string"],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

API rate limiting uygulanmamaktadır, ancak production'da uygulanması önerilir.

## CORS

CORS tüm origin'lere açıktır. Production'da sadece gerekli origin'ler izin verilmelidir.
