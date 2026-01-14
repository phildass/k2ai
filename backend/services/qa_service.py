import json
import os
from typing import Optional, Dict, List
from pathlib import Path


class QAService:
    """
    Service for handling predefined Q&A pairs.
    Provides fuzzy matching for user questions against a curated set of FAQs.
    """
    
    def __init__(self, qa_file_path: Optional[str] = None):
        """
        Initialize the QA service with predefined questions and answers.
        
        Args:
            qa_file_path: Path to the JSON file containing Q&A pairs.
                         Defaults to backend/data/predefined_qa.json
        """
        if qa_file_path is None:
            # Default path relative to the backend directory
            backend_dir = Path(__file__).parent.parent
            qa_file_path = backend_dir / "data" / "predefined_qa.json"
        
        self.qa_file_path = qa_file_path
        self.qa_data = self._load_qa_data()
    
    def _load_qa_data(self) -> List[Dict]:
        """
        Load Q&A data from JSON file.
        
        Returns:
            List of Q&A dictionaries
        """
        try:
            with open(self.qa_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('questions', [])
        except FileNotFoundError:
            print(f"Warning: Q&A file not found at {self.qa_file_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"Warning: Error parsing Q&A file: {e}")
            return []
    
    def _calculate_similarity_score(self, user_message: str, qa_entry: Dict) -> float:
        """
        Calculate a similarity score between user message and a Q&A entry.
        Uses keyword matching for simplicity and performance.
        
        Args:
            user_message: The user's question (normalized to lowercase)
            qa_entry: Dictionary containing question, answer, and keywords
        
        Returns:
            Similarity score (0.0 to 1.0)
        """
        user_message_lower = user_message.lower()
        score = 0.0
        
        # Check for exact question match (highest score)
        if qa_entry['question'].lower() in user_message_lower or \
           user_message_lower in qa_entry['question'].lower():
            score = 1.0
            return score
        
        # Check keyword matches
        keywords = qa_entry.get('keywords', [])
        matched_keywords = 0
        
        for keyword in keywords:
            if keyword.lower() in user_message_lower:
                matched_keywords += 1
        
        # Calculate score based on keyword matches
        if matched_keywords > 0 and len(keywords) > 0:
            score = min(0.9, 0.3 + (matched_keywords / len(keywords)) * 0.6)
        
        return score
    
    def find_answer(self, user_message: str, threshold: float = 0.3) -> Optional[Dict]:
        """
        Find a predefined answer for the user's question using fuzzy matching.
        
        Args:
            user_message: The user's question
            threshold: Minimum similarity score to consider a match (0.0 to 1.0)
                      Default is 0.3 to allow single keyword matches
        
        Returns:
            Dictionary with 'answer', 'question', and 'confidence' if match found,
            None otherwise
        """
        if not user_message or not self.qa_data:
            return None
        
        best_match = None
        best_score = 0.0
        
        for qa_entry in self.qa_data:
            score = self._calculate_similarity_score(user_message, qa_entry)
            
            if score > best_score:
                best_score = score
                best_match = qa_entry
        
        # Only return a match if it meets the threshold
        if best_score >= threshold:
            return {
                'answer': best_match['answer'],
                'question': best_match['question'],
                'confidence': best_score
            }
        
        return None
    
    def reload_qa_data(self) -> bool:
        """
        Reload Q&A data from the file.
        Useful for updating Q&A without restarting the server.
        
        Returns:
            True if reload was successful, False otherwise
        """
        try:
            self.qa_data = self._load_qa_data()
            return True
        except Exception as e:
            print(f"Error reloading Q&A data: {e}")
            return False
    
    def get_all_questions(self) -> List[str]:
        """
        Get all predefined questions.
        
        Returns:
            List of question strings
        """
        return [qa['question'] for qa in self.qa_data]
