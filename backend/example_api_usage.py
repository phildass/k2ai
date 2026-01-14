#!/usr/bin/env python3
"""
Example script demonstrating the K2 Communications chatbot API usage.
Shows both predefined Q&A and LLM fallback scenarios.
"""

import requests
import json
import sys

API_URL = "http://localhost:8000/api/chat/"

def send_message(message: str, conversation_id: str = "example-001") -> dict:
    """Send a message to the chatbot and return the response."""
    payload = {
        "message": message,
        "conversation_id": conversation_id,
        "language": "en"
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        sys.exit(1)

def print_response(response: dict):
    """Pretty print the chatbot response."""
    print("\n" + "="*70)
    print("🤖 CHATBOT RESPONSE")
    print("="*70)
    print(f"\n{response['message']}\n")
    
    metadata = response.get('metadata', {})
    source = metadata.get('source', 'unknown')
    
    print("-"*70)
    print(f"📊 METADATA")
    print(f"   Source: {source.upper()}")
    
    if source == 'predefined':
        print(f"   Matched Question: {metadata.get('matched_question')}")
        print(f"   Confidence: {metadata.get('confidence'):.2f}")
    elif source == 'llm':
        print(f"   Model: {metadata.get('model')}")
    
    suggestions = response.get('suggestions', [])
    if suggestions:
        print(f"\n💡 SUGGESTIONS:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"   {i}. {suggestion}")
    
    print("="*70 + "\n")

def main():
    """Run example queries to demonstrate the chatbot."""
    
    print("\n🎯 K2 Communications Chatbot API - Example Usage\n")
    
    # Example 1: Predefined Q&A (exact match)
    print("\n📝 Example 1: Exact Question Match (Predefined Q&A)")
    print("Question: 'What services do you offer?'")
    response1 = send_message("What services do you offer?")
    print_response(response1)
    
    # Example 2: Predefined Q&A (keyword match)
    print("\n📝 Example 2: Keyword Match (Predefined Q&A)")
    print("Question: 'Tell me about your pricing'")
    response2 = send_message("Tell me about your pricing")
    print_response(response2)
    
    # Example 3: Predefined Q&A (fuzzy match)
    print("\n📝 Example 3: Fuzzy Match (Predefined Q&A)")
    print("Question: 'How can I contact you?'")
    response3 = send_message("How can I contact you?")
    print_response(response3)
    
    # Example 4: LLM fallback (or error if no API key)
    print("\n📝 Example 4: Non-Predefined Question (LLM Fallback)")
    print("Question: 'What makes a good press release?'")
    response4 = send_message("What makes a good press release?")
    print_response(response4)
    
    print("\n✅ Examples complete!")
    print("\nNote: If Example 4 shows an error, make sure OPENAI_API_KEY is configured.")
    print("      Predefined Q&A (Examples 1-3) work without an API key.\n")

if __name__ == "__main__":
    # Check if server is running
    try:
        requests.get("http://localhost:8000/health", timeout=2)
    except requests.exceptions.RequestException:
        print("\n❌ Error: Backend server is not running!")
        print("Please start the server first:")
        print("  cd backend")
        print("  python -m uvicorn main:app --reload --port 8000\n")
        sys.exit(1)
    
    main()
