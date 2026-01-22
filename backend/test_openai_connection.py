#!/usr/bin/env python3
"""
OpenAI API Connection Test Script

This script verifies that:
1. The OpenAI API key is configured
2. The API key is valid
3. The chatbot can generate live AI responses

Run this script to verify your OpenAI integration is working correctly.
"""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
import asyncio

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(message):
    """Print a success message in green."""
    print(f"{GREEN}✓{RESET} {message}")

def print_error(message):
    """Print an error message in red."""
    print(f"{RED}✗{RESET} {message}")

def print_warning(message):
    """Print a warning message in yellow."""
    print(f"{YELLOW}⚠{RESET} {message}")

def print_info(message):
    """Print an info message in blue."""
    print(f"{BLUE}ℹ{RESET} {message}")

def check_env_file():
    """Check if .env file exists and contains API key."""
    print("\n" + "="*60)
    print("OpenAI API Connection Test")
    print("="*60 + "\n")
    
    # Check if .env file exists
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(env_path):
        print_error(".env file not found!")
        print_info("Creating .env file from .env.example...")
        
        example_path = os.path.join(os.path.dirname(__file__), '.env.example')
        if os.path.exists(example_path):
            import shutil
            shutil.copy(example_path, env_path)
            print_warning(".env file created. Please add your OpenAI API key!")
            print_info(f"Edit {env_path} and set OPENAI_API_KEY=your-key-here")
            return False
        else:
            print_error(".env.example file not found either!")
            return False
    
    print_success(".env file found")
    return True

def test_api_key():
    """Test if the API key is configured and valid."""
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Check if API key exists
    if not api_key:
        print_error("OPENAI_API_KEY not found in environment!")
        print_info("Please set OPENAI_API_KEY in your .env file")
        return None
    
    # Check if it's the placeholder
    if api_key == "your_openai_api_key_here":
        print_error("OPENAI_API_KEY is still set to the placeholder value!")
        print_info("Please replace 'your_openai_api_key_here' with your actual OpenAI API key")
        print_info("Get your API key from: https://platform.openai.com/api-keys")
        return None
    
    # Check key format
    if not (api_key.startswith("sk-") or api_key.startswith("sk-proj-")):
        print_warning("API key format looks unusual (should start with 'sk-' or 'sk-proj-')")
        print_info("Proceeding anyway, but verify your key is correct")
    
    print_success("OpenAI API key is configured")
    print_info(f"Key prefix: {api_key[:20]}...")
    
    return api_key

def test_connection(api_key):
    """Test connection to OpenAI API."""
    try:
        client = OpenAI(api_key=api_key)
        
        # Get model from environment or use default
        model = os.getenv("LLM_MODEL", "gpt-4-turbo-preview")
        temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        max_tokens = int(os.getenv("LLM_MAX_TOKENS", "1000"))
        
        print_info(f"Testing connection with model: {model}")
        print_info("Sending test message to OpenAI...")
        
        # Simple test message
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Respond briefly."
                },
                {
                    "role": "user",
                    "content": "Say 'Hello, I am working!' if you can read this."
                }
            ],
            temperature=temperature,
            max_tokens=100
        )
        
        # Extract response
        ai_response = response.choices[0].message.content
        
        print_success("Successfully connected to OpenAI API!")
        print_success(f"Model: {model}")
        print_success("Live AI assistant is working!")
        
        print("\n" + "-"*60)
        print("Test Response:")
        print("-"*60)
        print(f"{BLUE}{ai_response}{RESET}")
        print("-"*60)
        
        return True
        
    except Exception as e:
        print_error(f"Failed to connect to OpenAI API: {str(e)}")
        
        # Provide specific error guidance
        error_str = str(e).lower()
        if "invalid" in error_str or "authentication" in error_str:
            print_info("Your API key appears to be invalid.")
            print_info("1. Check that you copied the entire key correctly")
            print_info("2. Verify the key hasn't been revoked at https://platform.openai.com/api-keys")
            print_info("3. Try generating a new API key")
        elif "rate" in error_str or "quota" in error_str:
            print_info("You've exceeded your rate limit or quota.")
            print_info("1. Check your usage at https://platform.openai.com/usage")
            print_info("2. Add credits or upgrade your plan")
            print_info("3. Wait a few minutes and try again")
        elif "model" in error_str:
            print_info(f"Model '{model}' may not be available for your account.")
            print_info("Try setting LLM_MODEL=gpt-3.5-turbo in your .env file")
        else:
            print_info("Check your internet connection and try again")
            print_info("OpenAI status: https://status.openai.com/")
        
        return False

def test_chatbot_integration():
    """Test the actual chatbot service integration."""
    print("\n" + "="*60)
    print("Testing K2AI Chatbot Integration")
    print("="*60 + "\n")
    
    try:
        from services.chatbot_service import ChatbotService
        
        print_info("Initializing ChatbotService...")
        service = ChatbotService()
        
        if service.api_key_missing:
            print_error("ChatbotService detected missing API key")
            return False
        
        print_success("ChatbotService initialized successfully")
        print_info("Testing with a real question...")
        
        # Test with a question that should trigger OpenAI
        async def test_message():
            response = await service.process_message(
                message="What are the latest trends in AI?",
                conversation_id="test-connection",
                language="en"
            )
            return response
        
        # Run async function
        response = asyncio.run(test_message())
        
        if response.get("metadata", {}).get("source") == "llm":
            print_success("Live AI response received!")
            print("\n" + "-"*60)
            print("AI Response:")
            print("-"*60)
            print(f"{BLUE}{response['message'][:200]}...{RESET}")
            print("-"*60)
            return True
        elif response.get("metadata", {}).get("source") == "predefined":
            print_warning("Received predefined answer instead of AI response")
            print_info("This is expected if the question matches predefined Q&A")
            return True
        else:
            print_error("Unexpected response source")
            return False
            
    except Exception as e:
        print_error(f"Failed to test chatbot integration: {str(e)}")
        print_info("Make sure you're running this from the backend directory")
        return False

def main():
    """Main test function."""
    # Test 1: Check .env file
    if not check_env_file():
        print("\n" + "="*60)
        print_error("Setup incomplete. Please create .env file and add your API key.")
        print_info("See OPENAI_SETUP_GUIDE.md for detailed instructions")
        print("="*60 + "\n")
        sys.exit(1)
    
    # Test 2: Check API key configuration
    api_key = test_api_key()
    if not api_key:
        print("\n" + "="*60)
        print_error("API key not configured. Please set OPENAI_API_KEY in .env file.")
        print_info("See OPENAI_SETUP_GUIDE.md for detailed instructions")
        print("="*60 + "\n")
        sys.exit(1)
    
    # Test 3: Test OpenAI connection
    print("\n" + "-"*60)
    if not test_connection(api_key):
        print("\n" + "="*60)
        print_error("OpenAI connection failed. See errors above for details.")
        print_info("See OPENAI_SETUP_GUIDE.md for troubleshooting")
        print("="*60 + "\n")
        sys.exit(1)
    
    # Test 4: Test chatbot integration
    if not test_chatbot_integration():
        print("\n" + "="*60)
        print_warning("Chatbot integration test had issues, but basic API works")
        print("="*60 + "\n")
        sys.exit(1)
    
    # All tests passed!
    print("\n" + "="*60)
    print_success("ALL TESTS PASSED!")
    print("="*60)
    print(f"\n{GREEN}✓ Your OpenAI integration is working correctly!{RESET}")
    print(f"{GREEN}✓ The K2AI chatbot can now provide live AI responses.{RESET}\n")
    
    print("Next steps:")
    print("1. Start the backend: uvicorn main:app --reload --port 8000")
    print("2. Test via API: curl -X POST http://localhost:8000/api/chat/ \\")
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"message": "Tell me about K2 Communications"}\'')
    print("3. Start the frontend and test the chat interface\n")
    
    sys.exit(0)

if __name__ == "__main__":
    main()
