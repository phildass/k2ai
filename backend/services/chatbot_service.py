import os
from openai import AsyncOpenAI
from typing import Optional, Dict, List
from datetime import datetime
from .faq_service import FAQService
from services.qa_service import QAService
from services.admin_qa_service import AdminQAService

# Constants
PLACEHOLDER_API_KEY = "your_openai_api_key_here"

class ChatbotService:
    def __init__(self):
        # Check if API key is present
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key or self.api_key == PLACEHOLDER_API_KEY:
            self.api_key_missing = True
            self.client = None
        else:
            self.api_key_missing = False
            self.client = AsyncOpenAI(api_key=self.api_key)
        
        self.model = os.getenv("LLM_MODEL", "gpt-4-turbo-preview")
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", "1000"))
        
        # Initialize QA Service for predefined answers
        self.qa_service = QAService()
        
        # Initialize Admin QA Service for admin-curated answers
        self.admin_qa_service = AdminQAService()
        
        # In-memory conversation storage (replace with database in production)
        self.conversations: Dict[str, List[Dict]] = {}
        
        # Initialize FAQ service
        self.faq_service = FAQService()
        
    def get_system_prompt(self, language: str = "en") -> str:
        """
        Get the system prompt for the chatbot based on language.
        """
        base_prompt = """You are an expert, friendly AI assistant for K2 Communications, India's premier public relations and communications agency.

K2 Communications offers:
1. PR Consultancy - Strategic public relations and media relations
2. Reputation & Crisis Management - Proactive and reactive crisis handling
3. Digital & Social Media Marketing - Comprehensive digital strategies
4. Content Development - High-quality content creation
5. Market Research - In-depth market analysis
6. Translation Services - Multilingual campaign support

Key Values:
- Ethical practices and transparency
- Embracing new technologies including AI
- Multilingual, nationwide coverage across India
- Working with major Indian brands across multiple sectors

Your role as an expert, friendly K2 Communications assistant:
- Answer PR, services, and industry queries in a professional yet approachable way
- Explain services clearly and conversationally
- Help potential clients understand PR concepts and best practices
- Capture leads and answer inquiries with care
- Provide expert crisis management guidance
- Assist with content and media workflow questions
- Be professional yet warm and friendly in your tone
- Recommend appropriate services based on client needs
- Share industry insights when relevant

Always be helpful, knowledgeable, friendly, and represent K2 Communications' excellence in PR and communications."""

        if language == "hi":  # Hindi
            return base_prompt + "\n\nPlease respond in Hindi when appropriate."
        elif language in ["ta", "te", "ml", "kn"]:  # South Indian languages
            return base_prompt + f"\n\nPlease respond in the requested language ({language}) when appropriate."
        
        return base_prompt
    
    async def process_message(
        self,
        message: str,
        conversation_id: str,
        language: str = "en",
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Process a user message and generate a response.
        Priority order:
        1. Admin Q&A (highest priority)
        2. FAQ matches
        3. Predefined Q&A
        4. LLM fallback (lowest priority)
        """
        # Initialize conversation history if needed
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        # Add user message to history
        self.conversations[conversation_id].append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # STEP 1: Check for Admin Q&A match first (highest priority)
        admin_match = self.admin_qa_service.find_matching_qa(message)
        
        if admin_match:
            # Admin Q&A match found - return admin-curated answer
            answer = admin_match["answer"]
            
            # Add assistant response to history
            self.conversations[conversation_id].append({
                "role": "assistant",
                "content": answer,
                "timestamp": datetime.now().isoformat()
            })
            
            return {
                "message": answer,
                "suggestions": self._generate_suggestions(message, answer),
                "metadata": {
                    "source": "admin",
                    "matched_question": admin_match["question"],
                    "match_type": admin_match.get("match_type", "unknown"),
                    "language": language,
                    "timestamp": datetime.now().isoformat()
                },
                "answer_source": "admin"
            }
        
        # STEP 2: Check for FAQ match
        faq_match = self.faq_service.find_matching_faq(message)
        
        if faq_match:
            # FAQ match found - return predetermined answer
            answer = faq_match["answer"]
            
            # Add assistant response to history
            self.conversations[conversation_id].append({
                "role": "assistant",
                "content": answer,
                "timestamp": datetime.now().isoformat()
            })
            
            return {
                "message": answer,
                "suggestions": self._generate_suggestions(message, answer),
                "metadata": {
                    "language": language,
                    "faq_topic": faq_match["topic"],
                    "timestamp": datetime.now().isoformat()
                },
                "answer_source": "faq"
            }
        
        # STEP 3: Try predefined Q&A
        predefined_match = self.qa_service.find_answer(message)
        
        if predefined_match:
            # Found a predefined answer - use it
            assistant_message = predefined_match['answer']
            
            # Add assistant response to history
            self.conversations[conversation_id].append({
                "role": "assistant",
                "content": assistant_message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Generate suggestions based on the predefined answer
            suggestions = self._generate_suggestions(message, assistant_message)
            
            return {
                "message": assistant_message,
                "suggestions": suggestions,
                "metadata": {
                    "source": "predefined",
                    "matched_question": predefined_match['question'],
                    "confidence": predefined_match['confidence'],
                    "language": language,
                    "timestamp": datetime.now().isoformat()
                },
                "answer_source": "predefined"
            }
        
        # STEP 4: No predefined answer found - use LLM
        # Check if API key is missing
        if self.api_key_missing:
            missing_key_message = (
                "I apologize, but the chatbot is not fully configured yet. "
                "The OpenAI API key is missing. Please contact the administrator "
                "to set up the OPENAI_API_KEY in the environment configuration. "
                "In the meantime, you can reach out to K2 Communications directly "
                "at https://www.k2communications.in/ for assistance."
            )
            return {
                "message": missing_key_message,
                "suggestions": ["Visit K2 Communications website", "Contact support"],
                "metadata": {
                    "source": "error",
                    "error": "OPENAI_API_KEY not configured"
                },
                "answer_source": "ai"
            }
        
        # Prepare messages for OpenAI
        messages = [
            {"role": "system", "content": self.get_system_prompt(language)}
        ]
        
        # Add conversation history
        for msg in self.conversations[conversation_id]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        try:
            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversations[conversation_id].append({
                "role": "assistant",
                "content": assistant_message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Generate suggestions based on context
            suggestions = self._generate_suggestions(message, assistant_message)
            
            return {
                "message": assistant_message,
                "suggestions": suggestions,
                "metadata": {
                    "source": "llm",
                    "language": language,
                    "model": self.model,
                    "timestamp": datetime.now().isoformat()
                },
                "answer_source": "ai"
            }
        
        except Exception as e:
            # Fallback response
            return {
                "message": f"I apologize, but I'm experiencing technical difficulties. Please try again or contact us directly at K2 Communications. Error: {str(e)}",
                "suggestions": ["Try again", "Contact us", "View services"],
                "metadata": {
                    "source": "error",
                    "error": str(e)
                },
                "answer_source": "ai"
            }
    
    def _generate_suggestions(self, user_message: str, assistant_response: str) -> List[str]:
        """
        Generate follow-up suggestions based on the conversation.
        """
        suggestions = []
        
        # Default suggestions based on common topics
        if "service" in user_message.lower() or "service" in assistant_response.lower():
            suggestions.extend(["Tell me more about PR consultancy", "What is crisis management?"])
        
        if "price" in user_message.lower() or "cost" in user_message.lower():
            suggestions.append("Schedule a consultation")
        
        if "crisis" in user_message.lower():
            suggestions.extend(["How to handle a PR crisis?", "24/7 support options"])
        
        # Always include these options
        suggestions.extend(["View all services", "Speak to a consultant"])
        
        return suggestions[:4]  # Return top 4 suggestions
    
    async def get_conversation_history(self, conversation_id: str) -> List[Dict]:
        """
        Retrieve conversation history for a given conversation ID.
        """
        return self.conversations.get(conversation_id, [])
