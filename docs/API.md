# API Reference

## Base URL

**Development**: `http://localhost:8000`
**Production**: TBD

## Authentication

Currently, the API is open. Authentication will be added in future versions.

## Chat API

### Send Message

Send a message to the AI chatbot.

**Endpoint**: `POST /api/chat/message`

**Request Body**:
```json
{
  "message": "Tell me about your PR services",
  "conversation_id": "optional-uuid",
  "language": "en",
  "context": {}
}
```

**Response**:
```json
{
  "message": "K2 Communications offers comprehensive PR consultancy...",
  "conversation_id": "generated-uuid",
  "suggestions": [
    "Tell me more about crisis management",
    "How much does it cost?",
    "Schedule a consultation"
  ],
  "metadata": {
    "language": "en",
    "model": "gpt-4-turbo-preview",
    "timestamp": "2024-01-14T12:00:00Z"
  }
}
```

**Language Codes**:
- `en` - English
- `hi` - Hindi
- `ta` - Tamil
- `te` - Telugu
- `ml` - Malayalam
- `kn` - Kannada

### Get Conversation History

Retrieve all messages from a conversation.

**Endpoint**: `GET /api/chat/conversation/{conversation_id}`

**Response**:
```json
{
  "conversation_id": "uuid",
  "messages": [
    {
      "role": "user",
      "content": "Hello",
      "timestamp": "2024-01-14T12:00:00Z"
    },
    {
      "role": "assistant",
      "content": "Hello! How can I help?",
      "timestamp": "2024-01-14T12:00:01Z"
    }
  ]
}
```

## Services API

### List All Services

Get all services offered by K2 Communications.

**Endpoint**: `GET /api/services/`

**Response**:
```json
[
  {
    "id": "pr-consultancy",
    "name": "PR Consultancy",
    "description": "Strategic public relations consultancy...",
    "key_features": [
      "Media relations and outreach",
      "Brand positioning and messaging"
    ],
    "use_cases": [
      "Brand launches",
      "Corporate communications"
    ]
  }
]
```

### Get Service Details

Get detailed information about a specific service.

**Endpoint**: `GET /api/services/{service_id}`

**Path Parameters**:
- `service_id`: Service identifier (e.g., "pr-consultancy")

**Response**: Same structure as individual service in list above

**Error Response** (404):
```json
{
  "detail": "Service not found"
}
```

## Feedback API

### Submit Feedback

Submit user feedback for a conversation.

**Endpoint**: `POST /api/feedback/submit`

**Request Body**:
```json
{
  "conversation_id": "uuid",
  "rating": 5,
  "comment": "Very helpful!",
  "sentiment": "positive"
}
```

**Response**:
```json
{
  "status": "success",
  "message": "Thank you for your feedback!",
  "conversation_id": "uuid"
}
```

### Capture Lead

Capture lead information from interested clients.

**Endpoint**: `POST /api/feedback/lead`

**Request Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+91 98765 43210",
  "company": "Example Corp",
  "service_interest": "pr-consultancy",
  "message": "I'm interested in learning more..."
}
```

**Response**:
```json
{
  "status": "success",
  "message": "Thank you! We'll get in touch with you soon.",
  "lead_id": "generated-lead-id"
}
```

## Health Check

### API Health

Check if the API is running.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy"
}
```

### Root

Get API information.

**Endpoint**: `GET /`

**Response**:
```json
{
  "message": "K2 Communications AI Chatbot API",
  "status": "active",
  "version": "1.0.0"
}
```

## Error Responses

All endpoints may return error responses:

**400 Bad Request**:
```json
{
  "detail": "Invalid request parameters"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Rate Limiting

Currently no rate limiting. Will be added in production.

## CORS

CORS is configured to allow requests from:
- `http://localhost:3000` (development)
- Additional origins can be configured via `CORS_ORIGINS` environment variable

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.

Visit `http://localhost:8000/redoc` for alternative API documentation powered by ReDoc.
