# Predefined Q&A with LLM Fallback - Implementation Guide

## Overview

The K2 Communications chatbot now supports **predefined Q&A pairs** with automatic **LLM fallback**. This hybrid approach provides:
- ✅ **Fast, consistent answers** for common questions
- ✅ **No API costs** for predefined answers
- ✅ **LLM flexibility** for complex or unique questions
- ✅ **Easy maintenance** via JSON configuration

## How It Works

When a user sends a message to `/api/chat/`:

1. **Predefined Q&A Check**: The system first searches for matching predefined answers using fuzzy keyword matching
2. **LLM Fallback**: If no match is found (confidence < 0.3), the system calls the OpenAI API for a generated response
3. **Source Tracking**: The response includes metadata showing whether it came from predefined Q&A or the LLM

## Architecture

```
User Question
     ↓
┌─────────────────────┐
│  QA Service         │
│  (Keyword Matching) │
└─────────────────────┘
     ↓
  Match Found? ──No──→ ┌──────────────┐
     │                 │   LLM Call   │
     │                 │  (OpenAI)    │
     │                 └──────────────┘
     Yes                      ↓
     ↓                       ↓
┌─────────────────────────────────┐
│  Return Response with Metadata  │
│  source: "predefined" or "llm"  │
└─────────────────────────────────┘
```

## Files Added/Modified

### New Files

1. **`backend/data/predefined_qa.json`** - Contains Q&A pairs with keywords
2. **`backend/services/qa_service.py`** - Handles predefined Q&A matching

### Modified Files

1. **`backend/services/chatbot_service.py`** - Integrated QA service with LLM fallback
2. **`backend/models/schemas.py`** - Already had metadata field (no changes needed)

## Configuration

### Adding/Updating Predefined Q&A

Edit `backend/data/predefined_qa.json`:

```json
{
  "questions": [
    {
      "question": "Your predefined question here",
      "answer": "Your detailed answer here\n\nCan include:\n- Bullet points\n- **Bold text**\n- Multiple paragraphs",
      "keywords": ["keyword1", "keyword2", "multi word keyword"]
    }
  ]
}
```

**Best Practices for Keywords:**
- Include obvious keywords: "pricing", "cost", "services"
- Include phrases: "get in touch", "crisis management"
- Include synonyms: "contact", "reach", "get in touch"
- 4-8 keywords per question is ideal
- More specific keywords = better matches

### Matching Algorithm

The system uses a keyword-based fuzzy matching algorithm:

1. **Exact Match (Confidence = 1.0)**: Question text matches exactly
2. **Keyword Match (Confidence = 0.3 to 0.9)**: Keywords found in user message
   - Score = 0.3 + (matched_keywords / total_keywords) × 0.6
   - Threshold = 0.3 (minimum confidence required)

**Examples:**
- "What services do you offer?" → Exact match → Confidence 1.0
- "Tell me about your pricing" → Keyword "pricing" → Confidence ~0.375
- "How can I contact you?" → Keyword "contact" → Confidence ~0.375
- "What is AI?" → No match → Falls back to LLM

## API Response Format

### Predefined Answer Response

```json
{
  "message": "The predefined answer text...",
  "conversation_id": "abc-123",
  "suggestions": ["Related question 1", "Related question 2"],
  "metadata": {
    "source": "predefined",
    "matched_question": "Original question from JSON",
    "confidence": 0.85,
    "language": "en",
    "timestamp": "2026-01-14T08:00:00.000000"
  }
}
```

### LLM-Generated Response

```json
{
  "message": "AI-generated answer...",
  "conversation_id": "abc-123",
  "suggestions": ["Follow-up 1", "Follow-up 2"],
  "metadata": {
    "source": "llm",
    "language": "en",
    "model": "gpt-4-turbo-preview",
    "timestamp": "2026-01-14T08:00:00.000000"
  }
}
```

## Testing

### Test Predefined Q&A

```bash
curl -X POST "http://localhost:8000/api/chat/" \
  -H "Content-Type: application/json" \
  -d '{"message": "What services do you offer?", "conversation_id": "test-123"}'
```

Expected: `"source": "predefined"` in metadata

### Test LLM Fallback

```bash
curl -X POST "http://localhost:8000/api/chat/" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the future of PR in the metaverse?", "conversation_id": "test-456"}'
```

Expected: `"source": "llm"` in metadata (or `"source": "error"` if API key not configured)

### Test Keywords

```bash
# Should match "contact" question
curl -X POST "http://localhost:8000/api/chat/" \
  -H "Content-Type: application/json" \
  -d '{"message": "I need to get in touch", "conversation_id": "test-789"}'
```

## Environment Setup

### OpenAI API Key Configuration

**Option 1: Standard OpenAI**
```bash
export OPENAI_API_KEY="sk-your-actual-openai-key"
```

**Option 2: Azure OpenAI**
```bash
# Note: Azure OpenAI requires code modifications (not currently implemented)
export AZURE_OPENAI_API_KEY="your-azure-key"
export AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"
```

### Complete `.env` File

```env
# Required
OPENAI_API_KEY=sk-your-actual-openai-key

# Optional - LLM Configuration
LLM_MODEL=gpt-4-turbo-preview
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000

# Optional - CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

## Maintenance

### Reloading Q&A Data (Without Restart)

The QA service has a `reload_qa_data()` method:

```python
# In future: Add an admin endpoint
@router.post("/admin/reload-qa")
async def reload_qa():
    chatbot_service = get_chatbot_service()
    success = chatbot_service.qa_service.reload_qa_data()
    return {"success": success}
```

### Monitoring

Check the `source` field in responses:
- High `"predefined"` count = Good (fast, free)
- High `"llm"` count = Consider adding more predefined Q&A
- High `"error"` count = Check API key or connectivity

## Current Predefined Questions

1. "Who is your CEO?"
2. "What services do you offer?"
3. "How can I contact K2 Communications?"
4. "What are your office hours?"
5. "Do you provide crisis management?"
6. "What industries do you serve?"
7. "Do you offer multilingual services?"
8. "What is your pricing?"
9. "How do I get started?"
10. "What makes K2 Communications different?"

## Future Enhancements

- [ ] Add advanced fuzzy matching (Levenshtein distance, embeddings)
- [ ] Support for multi-turn Q&A flows
- [ ] Analytics dashboard for Q&A performance
- [ ] A/B testing different answer variations
- [ ] Admin UI for managing Q&A pairs
- [ ] Automatic Q&A suggestions from conversation logs
- [ ] Multi-language Q&A support

## Troubleshooting

### Predefined answers not matching

1. Check keywords in `backend/data/predefined_qa.json`
2. Lower the threshold in `qa_service.py` (current: 0.3)
3. Add more variations as keywords

### Always getting LLM responses

1. Check if `backend/data/predefined_qa.json` exists
2. Verify JSON format is valid
3. Check server logs for loading errors

### LLM not working

1. Verify `OPENAI_API_KEY` environment variable is set
2. Check API key is valid and has credits
3. Verify network connectivity to OpenAI API

## Example Use Cases

### Customer Service FAQ
- "What are your hours?"
- "How do I contact support?"
- "What services do you offer?"

### Product Information
- "Tell me about crisis management"
- "What industries do you serve?"
- "Do you offer multilingual services?"

### Sales & Pricing
- "What is your pricing?"
- "How do I get started?"
- "Schedule a consultation"

---

**For questions or issues, contact the development team or refer to the main README.md**
