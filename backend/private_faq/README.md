# Private FAQ Configuration

This directory contains predetermined answers for common questions. These answers are checked **before** calling the LLM, providing fast, consistent responses for frequently asked questions.

## File Structure

- `faqs.json` - Main FAQ configuration file

## FAQ Format

Each entry in `faqs.json` follows this structure:

```json
{
  "topic_name": {
    "keywords": ["keyword1", "keyword2", "phrase"],
    "answer": "The predetermined answer to return"
  }
}
```

### Fields:

- **topic_name**: A unique identifier for the FAQ topic (e.g., "fees", "ceo", "contact")
- **keywords**: Array of keywords/phrases to match (case-insensitive)
- **answer**: The exact text to return when a keyword matches

## How Matching Works

1. User sends a message to `/api/chat/`
2. The system converts the message to lowercase
3. It checks if ANY keyword from ANY FAQ entry appears as a complete word in the message (using word boundary matching)
4. If a match is found, the predetermined answer is returned immediately
5. If no match, the system falls back to the OpenAI/LLM for a dynamic response

**Note:** The system uses word boundary matching, so "fee" will match "What is the fee?" but won't match "coffee" or "feedback".

## Examples

### Example 1: Fees/Pricing
```json
"fees": {
  "keywords": ["fees", "fee", "cost", "price", "pricing", "charges"],
  "answer": "The fees are dependent on a variety of factors. To get a concise answer, connect with our offices. Call ... in Bangalore, ... in Mumbai, ... in Delhi NCR. Or write to us at enquiry@k2communications.in"
}
```

User questions that will match:
- "What are your fees?"
- "How much does it cost?"
- "Tell me about pricing"
- "What are the charges?"

### Example 2: Contact Information
```json
"contact": {
  "keywords": ["contact", "reach", "call", "phone", "email"],
  "answer": "You can reach us at enquiry@k2communications.in or call our offices..."
}
```

## How to Update FAQs (Admin Only)

### Adding a New FAQ

1. Open `faqs.json` in a text editor
2. Add a new entry with a unique topic name:

```json
{
  "existing_topic": { ... },
  "new_topic": {
    "keywords": ["keyword1", "keyword2"],
    "answer": "Your predetermined answer here"
  }
}
```

3. Save the file
4. Restart the server to load the changes

### Editing an Existing FAQ

1. Open `faqs.json`
2. Find the topic you want to edit
3. Update the keywords or answer
4. Save the file

### Deleting an FAQ

1. Open `faqs.json`
2. Remove the entire topic entry (including the topic name and its content)
3. Ensure the JSON remains valid (commas, braces, etc.)
4. Save the file

## Best Practices

### Keywords
- Use variations of the same concept (e.g., "fee", "fees", "cost", "costs")
- Include common misspellings if relevant
- Keep them lowercase (matching is case-insensitive anyway)
- Use specific phrases for precise matching (e.g., "get in touch", "speak to")

### Answers
- Be clear and concise
- Include contact information when appropriate
- Use `\n` for line breaks in JSON strings
- Maintain a professional, friendly tone
- Update contact numbers and email addresses regularly

## Security Notes

- This directory is **NOT** publicly accessible via the API
- Only server-side code can read these files
- Keep sensitive information out of FAQs (they're not encrypted)
- Only admin/authorized personnel should edit these files

## Reloading FAQs

The FAQ service loads FAQs on startup. To reload without restarting:

```python
# In future versions, you could add an admin endpoint:
# POST /api/admin/reload-faqs
```

Currently, restart the backend server to reload:
```bash
# Stop the server (Ctrl+C)
# Restart it
uvicorn main:app --reload
```

## Response Format

When a FAQ matches, the API response includes:

```json
{
  "message": "The predetermined answer...",
  "conversation_id": "...",
  "suggestions": [...],
  "metadata": {
    "faq_topic": "fees",
    "timestamp": "..."
  },
  "answer_source": "faq_match"  // Indicates FAQ was used
}
```

When no FAQ matches (LLM response):

```json
{
  "message": "AI-generated response...",
  "conversation_id": "...",
  "suggestions": [...],
  "metadata": {
    "model": "gpt-4-turbo-preview",
    "timestamp": "..."
  },
  "answer_source": "ai"  // Indicates LLM was used
}
```

## Troubleshooting

### FAQ not matching
- Check keyword spelling
- Ensure JSON is valid
- Verify the keyword appears in the user's question
- Check server logs for FAQ loading errors

### JSON validation
Use an online JSON validator or:
```bash
python -m json.tool faqs.json
```

### Testing
Send test messages via the API:
```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What are your fees?"}'
```

Check the `answer_source` field in the response to confirm FAQ matching.
