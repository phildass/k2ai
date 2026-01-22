import json
import os
from typing import Optional, Dict, List
from pathlib import Path
import logging
import re

logger = logging.getLogger(__name__)


class AdminQAService:
    """
    Service for managing admin-curated Q&A pairs.
    Provides CRUD operations and fuzzy matching for manually added Q&As.
    """
    
    def __init__(self, qa_file_path: Optional[str] = None):
        """
        Initialize the Admin Q&A service.
        
        Args:
            qa_file_path: Path to the JSON file containing admin Q&A pairs.
                         Defaults to backend/data/admin_qa.json
        """
        if qa_file_path is None:
            backend_dir = Path(__file__).parent.parent
            qa_file_path = backend_dir / "data" / "admin_qa.json"
        
        self.qa_file_path = Path(qa_file_path)
        self.qa_pairs: List[Dict] = []
        self._ensure_file_exists()
        self.load_qa_pairs()
    
    def _ensure_file_exists(self) -> None:
        """Ensure the admin Q&A file exists."""
        if not self.qa_file_path.exists():
            self.qa_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.qa_file_path, 'w', encoding='utf-8') as f:
                json.dump({"qa_pairs": []}, f, indent=2)
            logger.info(f"Created admin Q&A file at {self.qa_file_path}")
    
    def load_qa_pairs(self) -> None:
        """Load Q&A pairs from the JSON file."""
        try:
            with open(self.qa_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.qa_pairs = data.get('qa_pairs', [])
            logger.info(f"Loaded {len(self.qa_pairs)} admin Q&A pairs")
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing admin Q&A file: {e}")
            self.qa_pairs = []
        except Exception as e:
            logger.error(f"Error loading admin Q&A file: {e}")
            self.qa_pairs = []
    
    def save_qa_pairs(self) -> bool:
        """Save Q&A pairs to the JSON file."""
        try:
            with open(self.qa_file_path, 'w', encoding='utf-8') as f:
                json.dump({"qa_pairs": self.qa_pairs}, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.qa_pairs)} admin Q&A pairs")
            return True
        except Exception as e:
            logger.error(f"Error saving admin Q&A file: {e}")
            return False
    
    def add_qa_pair(self, question: str, answer: str) -> Dict:
        """
        Add a new Q&A pair.
        
        Args:
            question: The question or phrase
            answer: The admin response
            
        Returns:
            The created Q&A pair with ID
        """
        # Find the maximum existing ID and add 1, ensuring no collision even after deletions
        existing_ids = [qa.get('id', 0) for qa in self.qa_pairs]
        if existing_ids:
            qa_id = max(existing_ids) + 1
        else:
            qa_id = 1
        
        new_pair = {
            'id': qa_id,
            'question': question.strip(),
            'answer': answer.strip()
        }
        
        self.qa_pairs.append(new_pair)
        self.save_qa_pairs()
        logger.info(f"Added admin Q&A pair with ID {qa_id}")
        
        return new_pair
    
    def update_qa_pair(self, qa_id: int, question: str, answer: str) -> Optional[Dict]:
        """
        Update an existing Q&A pair.
        
        Args:
            qa_id: The ID of the Q&A pair to update
            question: The updated question
            answer: The updated answer
            
        Returns:
            The updated Q&A pair or None if not found
        """
        for qa in self.qa_pairs:
            if qa.get('id') == qa_id:
                qa['question'] = question.strip()
                qa['answer'] = answer.strip()
                self.save_qa_pairs()
                logger.info(f"Updated admin Q&A pair with ID {qa_id}")
                return qa
        
        logger.warning(f"Admin Q&A pair with ID {qa_id} not found")
        return None
    
    def delete_qa_pair(self, qa_id: int) -> bool:
        """
        Delete a Q&A pair.
        
        Args:
            qa_id: The ID of the Q&A pair to delete
            
        Returns:
            True if deleted, False if not found
        """
        initial_count = len(self.qa_pairs)
        self.qa_pairs = [qa for qa in self.qa_pairs if qa.get('id') != qa_id]
        
        if len(self.qa_pairs) < initial_count:
            self.save_qa_pairs()
            logger.info(f"Deleted admin Q&A pair with ID {qa_id}")
            return True
        
        logger.warning(f"Admin Q&A pair with ID {qa_id} not found")
        return False
    
    def get_all_qa_pairs(self) -> List[Dict]:
        """Get all Q&A pairs."""
        return self.qa_pairs
    
    def get_qa_pair(self, qa_id: int) -> Optional[Dict]:
        """Get a specific Q&A pair by ID."""
        for qa in self.qa_pairs:
            if qa.get('id') == qa_id:
                return qa
        return None
    
    def find_matching_qa(self, user_message: str) -> Optional[Dict]:
        """
        Find a matching admin Q&A pair using fuzzy matching.
        
        Args:
            user_message: The user's question
            
        Returns:
            Dictionary with matched Q&A pair or None
        """
        if not self.qa_pairs or not user_message:
            return None
        
        user_message_lower = user_message.lower().strip()
        
        # First, try exact match
        for qa in self.qa_pairs:
            question_lower = qa['question'].lower().strip()
            if user_message_lower == question_lower:
                return {
                    'id': qa['id'],
                    'question': qa['question'],
                    'answer': qa['answer'],
                    'match_type': 'exact'
                }
        
        # Then, try partial match (question contains user message or vice versa)
        for qa in self.qa_pairs:
            question_lower = qa['question'].lower().strip()
            # Check if user message contains the question or question contains user message
            if question_lower in user_message_lower or user_message_lower in question_lower:
                # Additional check: ensure at least 50% of words match
                user_words = set(re.findall(r'\w+', user_message_lower))
                question_words = set(re.findall(r'\w+', question_lower))
                
                if user_words and question_words:
                    common_words = user_words & question_words
                    similarity = len(common_words) / min(len(user_words), len(question_words))
                    
                    if similarity >= 0.5:
                        return {
                            'id': qa['id'],
                            'question': qa['question'],
                            'answer': qa['answer'],
                            'match_type': 'partial'
                        }
        
        # Finally, try keyword-based matching
        best_match = None
        best_score = 0
        
        for qa in self.qa_pairs:
            question_lower = qa['question'].lower().strip()
            user_words = set(re.findall(r'\w+', user_message_lower))
            question_words = set(re.findall(r'\w+', question_lower))
            
            if user_words and question_words:
                common_words = user_words & question_words
                # Calculate Jaccard similarity
                score = len(common_words) / len(user_words | question_words)
                
                if score > best_score and score >= 0.3:  # Minimum 30% similarity
                    best_score = score
                    best_match = {
                        'id': qa['id'],
                        'question': qa['question'],
                        'answer': qa['answer'],
                        'match_type': 'keyword'
                    }
        
        return best_match
    
    def reload(self) -> None:
        """Reload Q&A pairs from file."""
        self.load_qa_pairs()
