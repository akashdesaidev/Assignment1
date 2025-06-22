import json
import re
from typing import Dict, List, Tuple, Optional

class HallucinationValidator:
    def __init__(self, kb_path: str = "kb.json"):
        """Initialize validator with knowledge base"""
        with open(kb_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.kb = {item['question'].lower().strip(): item['answer'].lower().strip() 
                  for item in data['knowledge_base']}
        
    def normalize_text(self, text: str) -> str:
        """Normalize text for comparison"""
        # Remove extra whitespace, punctuation, and convert to lowercase
        text = re.sub(r'[^\w\s]', '', text.lower().strip())
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def calculate_similarity(self, answer1: str, answer2: str) -> float:
        """Calculate similarity between two answers using simple string matching"""
        norm1 = self.normalize_text(answer1)
        norm2 = self.normalize_text(answer2)
        
        # Exact match
        if norm1 == norm2:
            return 1.0
            
        # Check if one is contained in the other
        if norm1 in norm2 or norm2 in norm1:
            return 0.8
            
        # Check word overlap
        words1 = set(norm1.split())
        words2 = set(norm2.split())
        if words1 and words2:
            overlap = len(words1.intersection(words2))
            total = len(words1.union(words2))
            return overlap / total if total > 0 else 0.0
        
        return 0.0
    
    def validate_answer(self, question: str, model_answer: str, threshold: float = 0.7) -> Tuple[str, str]:
        """
        Validate model answer against knowledge base
        Returns: (status, reason)
        """
        question_norm = question.lower().strip()
        
        # Check if question exists in KB
        kb_answer = None
        for kb_q, kb_a in self.kb.items():
            if self.calculate_similarity(question_norm, kb_q) > 0.9:
                kb_answer = kb_a
                break
        
        if kb_answer is None:
            return "RETRY", "out-of-domain"
        
        # Compare model answer with KB answer
        similarity = self.calculate_similarity(model_answer, kb_answer)
        
        if similarity >= threshold:
            return "PASS", f"matches KB (similarity: {similarity:.2f})"
        else:
            return "RETRY", "answer differs from KB"
    
    def get_kb_answer(self, question: str) -> Optional[str]:
        """Get the correct answer from KB for a question"""
        question_norm = question.lower().strip()
        for kb_q, kb_a in self.kb.items():
            if self.calculate_similarity(question_norm, kb_q) > 0.9:
                return kb_a
        return None

# Test the validator
if __name__ == "__main__":
    validator = HallucinationValidator()
    
    # Test cases
    test_cases = [
        ("What is the capital of France?", "Paris"),
        ("What is the capital of France?", "London"),
        ("What is the capital of Mars?", "Mars City"),
    ]
    
    for question, answer in test_cases:
        status, reason = validator.validate_answer(question, answer)
        print(f"Q: {question}")
        print(f"A: {answer}")
        print(f"Status: {status} - {reason}")
        print("-" * 50) 