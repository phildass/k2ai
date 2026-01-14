import json
import os
from typing import Optional, Dict, List
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class FAQService:
    """
    Service to load and match predetermined FAQ answers.
    Provides case-insensitive keyword matching for user queries.
    """
    
    def __init__(self, faq_file_path: Optional[str] = None):
        """
        Initialize FAQ service and load FAQ data.
        
        Args:
            faq_file_path: Path to the FAQ JSON file. Defaults to backend/private_faq/faqs.json
        """
        if faq_file_path is None:
            # Default to private_faq/faqs.json in backend directory
            backend_dir = Path(__file__).parent.parent
            faq_file_path = backend_dir / "private_faq" / "faqs.json"
        
        self.faq_file_path = Path(faq_file_path)
        self.faqs: Dict[str, Dict] = {}
        self.load_faqs()
    
    def load_faqs(self) -> None:
        """
        Load FAQs from the JSON file into memory.
        Called on initialization and can be called again to reload.
        """
        try:
            if not self.faq_file_path.exists():
                logger.warning(f"FAQ file not found at {self.faq_file_path}. FAQ matching will be disabled.")
                self.faqs = {}
                return
            
            with open(self.faq_file_path, 'r', encoding='utf-8') as f:
                self.faqs = json.load(f)
            
            logger.info(f"Loaded {len(self.faqs)} FAQ entries from {self.faq_file_path}")
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing FAQ JSON file: {e}")
            self.faqs = {}
        except Exception as e:
            logger.error(f"Error loading FAQ file: {e}")
            self.faqs = {}
    
    def reload_faqs(self) -> None:
        """
        Reload FAQs from the file.
        Useful for hot-reloading when the FAQ file is updated.
        """
        logger.info("Reloading FAQs...")
        self.load_faqs()
    
    def find_matching_faq(self, user_message: str) -> Optional[Dict[str, str]]:
        """
        Search for a matching FAQ based on user message.
        Performs case-insensitive keyword matching.
        
        Args:
            user_message: The user's question/message
            
        Returns:
            Dictionary with 'topic' and 'answer' if match found, None otherwise
        """
        if not self.faqs:
            return None
        
        # Normalize user message to lowercase for matching
        normalized_message = user_message.lower()
        
        # Check each FAQ entry
        for topic, faq_data in self.faqs.items():
            keywords = faq_data.get("keywords", [])
            
            # Check if any keyword matches in the user message
            for keyword in keywords:
                if keyword.lower() in normalized_message:
                    return {
                        "topic": topic,
                        "answer": faq_data.get("answer", "")
                    }
        
        return None
    
    def get_all_topics(self) -> List[str]:
        """
        Get a list of all available FAQ topics.
        
        Returns:
            List of topic names
        """
        return list(self.faqs.keys())
    
    def get_faq_by_topic(self, topic: str) -> Optional[Dict]:
        """
        Get FAQ data for a specific topic.
        
        Args:
            topic: The topic name
            
        Returns:
            FAQ data dictionary or None if not found
        """
        return self.faqs.get(topic)
