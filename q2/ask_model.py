import json
import random
import time
from datetime import datetime
from validator import HallucinationValidator

class SimpleQuestionAnswerer:
    """Simulates a language model that can sometimes hallucinate"""
    
    def __init__(self):
        # Correct answers for KB questions
        self.kb_answers = {
            "what is the capital of france?": "Paris",
            "how many continents are there?": "7", 
            "what is the largest planet in our solar system?": "Jupiter",
            "who wrote romeo and juliet?": "William Shakespeare",
            "what is the chemical symbol for gold?": "Au",
            "in what year did world war ii end?": "1945",
            "what is the smallest prime number?": "2",
            "how many sides does a hexagon have?": "6",
            "what is the speed of light in vacuum?": "299,792,458 meters per second",
            "who painted the mona lisa?": "Leonardo da Vinci"
        }
        
        # Sometimes provide wrong answers to simulate hallucination
        self.wrong_answers = {
            "what is the capital of france?": ["London", "Berlin", "Madrid"],
            "how many continents are there?": ["5", "8", "6"],
            "what is the largest planet in our solar system?": ["Saturn", "Earth", "Neptune"],
            "who wrote romeo and juliet?": ["Charles Dickens", "Mark Twain", "Jane Austen"],
        }
    
    def answer_question(self, question: str, attempt: int = 1) -> str:
        """Simulate model answering a question"""
        question_lower = question.lower().strip()
        
        # Simulate thinking time
        time.sleep(0.1)
        
        # For KB questions, sometimes give wrong answers (30% chance on first try)
        if question_lower in self.kb_answers:
            if attempt == 1 and random.random() < 0.3 and question_lower in self.wrong_answers:
                return random.choice(self.wrong_answers[question_lower])
            return self.kb_answers[question_lower]
        
        # For out-of-domain questions, make up answers
        out_of_domain_responses = [
            "I believe the answer is 42",
            "According to my knowledge, it's definitely true", 
            "The correct response would be approximately 15.7",
            "Based on recent studies, the answer is yes",
            "I'm confident it's related to quantum mechanics"
        ]
        return random.choice(out_of_domain_responses)

def log_interaction(log_file, timestamp, question, answer, attempt, status, reason):
    """Log the interaction to file"""
    log_entry = f"[{timestamp}] Attempt {attempt}\n"
    log_entry += f"Q: {question}\n"
    log_entry += f"A: {answer}\n" 
    log_entry += f"Status: {status} - {reason}\n"
    log_entry += "-" * 80 + "\n"
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def main():
    # Initialize components
    model = SimpleQuestionAnswerer()
    validator = HallucinationValidator()
    
    # Load KB questions
    with open('kb.json', 'r', encoding='utf-8') as f:
        kb_data = json.load(f)
    kb_questions = [item['question'] for item in kb_data['knowledge_base']]
    
    # Add 5 edge case / out-of-domain questions
    edge_questions = [
        "What is the capital of Atlantis?",
        "How many moons does the planet Zorbex have?", 
        "Who invented the quantum spoon?",
        "What is the molecular weight of happiness?",
        "In which year will robots take over the world?"
    ]
    
    all_questions = kb_questions + edge_questions
    
    # Initialize log file
    log_file = "run.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"Hallucination Detection Run - {timestamp}\n")
        f.write("=" * 80 + "\n\n")
    
    results = {
        'total_questions': len(all_questions),
        'passes': 0,
        'retries': 0,
        'final_failures': 0,
        'kb_questions': len(kb_questions),
        'edge_questions': len(edge_questions),
        'details': []
    }
    
    print(f"Starting Hallucination Detection Test")
    print(f"Testing {len(all_questions)} questions ({len(kb_questions)} KB + {len(edge_questions)} edge cases)")
    print("-" * 60)
    
    for i, question in enumerate(all_questions, 1):
        print(f"\n[{i}/{len(all_questions)}] {question}")
        
        # First attempt
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        answer1 = model.answer_question(question, attempt=1)
        status1, reason1 = validator.validate_answer(question, answer1)
        
        log_interaction(log_file, timestamp, question, answer1, 1, status1, reason1)
        
        question_result = {
            'question': question,
            'is_kb_question': question in kb_questions,
            'attempt1': {'answer': answer1, 'status': status1, 'reason': reason1},
            'final_status': status1
        }
        
        if status1 == "PASS":
            print(f"PASS: {answer1}")
            results['passes'] += 1
        else:
            print(f"RETRY ({reason1}): {answer1}")
            results['retries'] += 1
            
            # Second attempt
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            answer2 = model.answer_question(question, attempt=2)
            status2, reason2 = validator.validate_answer(question, answer2)
            
            log_interaction(log_file, timestamp, question, answer2, 2, status2, reason2)
            
            question_result['attempt2'] = {'answer': answer2, 'status': status2, 'reason': reason2}
            question_result['final_status'] = status2
            
            if status2 == "PASS":
                print(f"PASS (retry): {answer2}")
                results['passes'] += 1
            else:
                print(f"FINAL FAIL: {answer2}")
                results['final_failures'] += 1
        
        results['details'].append(question_result)
    
    # Save results summary
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nFinal Results:")
    print(f"Total Questions: {results['total_questions']}")
    print(f"Passes: {results['passes']}")
    print(f"Retries: {results['retries']}")
    print(f"Final Failures: {results['final_failures']}")
    print(f"Success Rate: {results['passes']/results['total_questions']*100:.1f}%")

if __name__ == "__main__":
    main()
