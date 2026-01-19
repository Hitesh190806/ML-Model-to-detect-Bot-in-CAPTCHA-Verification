from model import BotDetector
import random
import time

class AdvancedCaptchaSystem:
    """
    Advanced CAPTCHA system with multiple challenge types including quizzes
    """
    
    def __init__(self, bot_detector):
        self.detector = bot_detector
        
        # Define risk thresholds
        self.LOW_RISK = 0.3      # Below 30% = probably human
        self.MEDIUM_RISK = 0.6   # 30-60% = suspicious
        self.HIGH_RISK = 0.85    # Above 60% = likely bot
        
        # Quiz database
        self.quiz_questions = self._load_quiz_database()
    
    def _load_quiz_database(self):
        """Load different types of quiz questions"""
        return {
            'logic': [
                {
                    'question': 'If all roses are flowers and some flowers fade quickly, can we conclude all roses fade quickly?',
                    'options': ['Yes', 'No', 'Maybe', 'Cannot determine'],
                    'correct': 'No',
                    'explanation': 'This is a logical fallacy. We cannot conclude all roses fade quickly.'
                },
                {
                    'question': 'What comes next in the sequence: 2, 4, 8, 16, ?',
                    'options': ['24', '32', '20', '18'],
                    'correct': '32',
                    'explanation': 'Each number is doubled: 2×2=4, 4×2=8, 8×2=16, 16×2=32'
                },
                {
                    'question': 'Which word does not belong: Car, Bus, Train, Table, Bicycle',
                    'options': ['Car', 'Table', 'Train', 'Bicycle'],
                    'correct': 'Table',
                    'explanation': 'Table is not a vehicle.'
                },
                {
                    'question': 'If 5 cats can catch 5 mice in 5 minutes, how many cats are needed to catch 100 mice in 100 minutes?',
                    'options': ['100 cats', '20 cats', '5 cats', '10 cats'],
                    'correct': '5 cats',
                    'explanation': 'The rate remains constant. 5 cats can catch 5 mice in 5 minutes, so they can catch 100 mice in 100 minutes.'
                }
            ],
            'common_sense': [
                {
                    'question': 'What do you use to cut paper?',
                    'options': ['Hammer', 'Scissors', 'Spoon', 'Keyboard'],
                    'correct': 'Scissors',
                    'explanation': 'Scissors are the common tool for cutting paper.'
                },
                {
                    'question': 'Where do fish live?',
                    'options': ['Desert', 'Water', 'Mountains', 'Clouds'],
                    'correct': 'Water',
                    'explanation': 'Fish are aquatic animals and live in water.'
                },
                {
                    'question': 'What season comes after winter?',
                    'options': ['Summer', 'Fall', 'Spring', 'Monsoon'],
                    'correct': 'Spring',
                    'explanation': 'The seasonal cycle is Winter → Spring → Summer → Fall.'
                },
                {
                    'question': 'Which is heavier: a kilogram of feathers or a kilogram of iron?',
                    'options': ['Feathers', 'Iron', 'Both are equal', 'Cannot determine'],
                    'correct': 'Both are equal',
                    'explanation': 'Both weigh exactly 1 kilogram, regardless of material.'
                },
                {
                    'question': 'How many days are in a week?',
                    'options': ['5', '6', '7', '8'],
                    'correct': '7',
                    'explanation': 'A week has 7 days.'
                }
            ],
            'math': [
                {
                    'question': 'What is 15 + 27?',
                    'options': ['42', '41', '43', '40'],
                    'correct': '42',
                    'explanation': '15 + 27 = 42'
                },
                {
                    'question': 'What is 12 × 8?',
                    'options': ['84', '96', '88', '92'],
                    'correct': '96',
                    'explanation': '12 × 8 = 96'
                },
                {
                    'question': 'What is 100 - 37?',
                    'options': ['63', '73', '67', '57'],
                    'correct': '63',
                    'explanation': '100 - 37 = 63'
                },
                {
                    'question': 'What is 50% of 80?',
                    'options': ['30', '40', '45', '35'],
                    'correct': '40',
                    'explanation': '50% of 80 = 80 ÷ 2 = 40'
                },
                {
                    'question': 'How many minutes are in 2.5 hours?',
                    'options': ['120', '150', '180', '130'],
                    'correct': '150',
                    'explanation': '2.5 hours × 60 minutes = 150 minutes'
                }
            ],
            'visual': [
                {
                    'question': 'How many letters are in the word "CAPTCHA"?',
                    'options': ['6', '7', '8', '5'],
                    'correct': '7',
                    'explanation': 'C-A-P-T-C-H-A = 7 letters'
                },
                {
                    'question': 'What color do you get when you mix blue and yellow?',
                    'options': ['Purple', 'Green', 'Orange', 'Red'],
                    'correct': 'Green',
                    'explanation': 'Blue + Yellow = Green'
                },
                {
                    'question': 'How many sides does a triangle have?',
                    'options': ['2', '3', '4', '5'],
                    'correct': '3',
                    'explanation': 'A triangle has 3 sides by definition.'
                },
                {
                    'question': 'What shape is a stop sign?',
                    'options': ['Circle', 'Square', 'Octagon', 'Triangle'],
                    'correct': 'Octagon',
                    'explanation': 'Stop signs are octagonal (8-sided).'
                }
            ],
            'pattern': [
                {
                    'question': 'Complete the pattern: A, C, E, G, ?',
                    'options': ['H', 'I', 'J', 'K'],
                    'correct': 'I',
                    'explanation': 'Skip one letter each time: A, (B), C, (D), E, (F), G, (H), I'
                },
                {
                    'question': 'What comes next: 🌙, ⭐, 🌙, ⭐, ?',
                    'options': ['🌙', '⭐', '☀️', '🌍'],
                    'correct': '🌙',
                    'explanation': 'The pattern alternates between moon and star.'
                },
                {
                    'question': 'Complete: 1, 1, 2, 3, 5, 8, ?',
                    'options': ['11', '12', '13', '14'],
                    'correct': '13',
                    'explanation': 'Fibonacci sequence: each number is the sum of previous two (5+8=13).'
                }
            ]
        }
    
    def check_user(self, features):
        """
        Analyze user behavior and decide what to do
        """
        # Get bot probability from ML model
        bot_prob = self.detector.predict(features)
        
        # Decide action based on probability
        if bot_prob < self.LOW_RISK:
            return {
                'action': 'allow',
                'probability': float(bot_prob),
                'message': 'Behavior looks human. Access granted! ✅',
                'risk_level': 'low'
            }
        
        elif bot_prob < self.MEDIUM_RISK:
            return {
                'action': 'simple_quiz',
                'probability': float(bot_prob),
                'message': 'Slightly suspicious. Please answer this simple question. 🤔',
                'captcha_type': 'simple_quiz',
                'risk_level': 'medium'
            }
        
        elif bot_prob < self.HIGH_RISK:
            return {
                'action': 'medium_quiz',
                'probability': float(bot_prob),
                'message': 'Suspicious activity detected. Complete this challenge. ⚠️',
                'captcha_type': 'medium_quiz',
                'risk_level': 'high'
            }
        
        else:
            return {
                'action': 'hard_quiz',
                'probability': float(bot_prob),
                'message': 'High risk detected. Complete multiple challenges. 🚨',
                'captcha_type': 'hard_quiz',
                'risk_level': 'critical'
            }
    
    def generate_captcha(self, captcha_type):
        """
        Generate CAPTCHA challenge based on type
        """
        if captcha_type == 'simple_quiz':
            # Simple checkbox with timing
            return {
                'type': 'checkbox',
                'instruction': 'Click the checkbox to verify you are human',
                'difficulty': 'easy',
                'time_limit': 30,
                'requires_timing_analysis': True
            }
        
        elif captcha_type == 'medium_quiz':
            # Single quiz question
            category = random.choice(['common_sense', 'math', 'visual'])
            question = random.choice(self.quiz_questions[category])
            
            return {
                'type': 'quiz',
                'difficulty': 'medium',
                'category': category,
                'question': question['question'],
                'options': question['options'],
                'correct_answer': question['correct'],
                'explanation': question['explanation'],
                'time_limit': 45,
                'question_id': f"{category}_{random.randint(1000, 9999)}"
            }
        
        elif captcha_type == 'hard_quiz':
            # Multiple quiz questions
            questions = []
            
            # Mix different categories
            categories = random.sample(['logic', 'common_sense', 'math', 'pattern'], 3)
            
            for category in categories:
                question = random.choice(self.quiz_questions[category])
                questions.append({
                    'category': category,
                    'question': question['question'],
                    'options': question['options'],
                    'correct_answer': question['correct'],
                    'explanation': question['explanation']
                })
            
            return {
                'type': 'multi_quiz',
                'difficulty': 'hard',
                'questions': questions,
                'total_questions': len(questions),
                'passing_score': 2,  # Must get at least 2/3 correct
                'time_limit': 90,
                'quiz_id': f"multi_{random.randint(1000, 9999)}"
            }
        
        else:
            # Fallback to simple checkbox
            return self.generate_captcha('simple_quiz')
    
    def verify_captcha_response(self, captcha, user_response):
        """
        Check if user's CAPTCHA response is correct
        """
        if captcha['type'] == 'checkbox':
            # Check if they clicked and timing is human-like
            clicked = user_response.get('clicked', False)
            response_time = user_response.get('response_time', 0)
            
            # Too fast = bot (less than 0.5 seconds)
            # Too slow = suspicious (more than 30 seconds)
            if response_time < 0.5:
                return {
                    'verified': False,
                    'reason': 'Response too fast - suspicious behavior'
                }
            
            return {
                'verified': clicked and response_time < 30,
                'reason': 'Checkbox verified' if clicked else 'Checkbox not clicked'
            }
        
        elif captcha['type'] == 'quiz':
            # Check single quiz answer
            user_answer = user_response.get('answer')
            correct_answer = captcha['correct_answer']
            response_time = user_response.get('response_time', 0)
            
            is_correct = user_answer == correct_answer
            
            # Too fast for a quiz = suspicious
            if is_correct and response_time < 2:
                return {
                    'verified': False,
                    'reason': 'Answer too fast - suspicious behavior',
                    'correct_answer': correct_answer
                }
            
            return {
                'verified': is_correct,
                'reason': 'Correct answer!' if is_correct else 'Incorrect answer',
                'correct_answer': correct_answer if not is_correct else None,
                'explanation': captcha['explanation']
            }
        
        elif captcha['type'] == 'multi_quiz':
            # Check multiple quiz answers
            user_answers = user_response.get('answers', [])
            questions = captcha['questions']
            passing_score = captcha['passing_score']
            
            correct_count = 0
            results = []
            
            for i, question in enumerate(questions):
                user_answer = user_answers[i] if i < len(user_answers) else None
                is_correct = user_answer == question['correct_answer']
                
                if is_correct:
                    correct_count += 1
                
                results.append({
                    'question': question['question'],
                    'user_answer': user_answer,
                    'correct_answer': question['correct_answer'],
                    'is_correct': is_correct,
                    'explanation': question['explanation']
                })
            
            passed = correct_count >= passing_score
            
            return {
                'verified': passed,
                'reason': f'Passed {correct_count}/{len(questions)} questions',
                'score': correct_count,
                'total': len(questions),
                'passing_score': passing_score,
                'results': results
            }
        
        return {
            'verified': False,
            'reason': 'Unknown CAPTCHA type'
        }
    
    def get_statistics(self):
        """Get system statistics"""
        total_questions = sum(len(questions) for questions in self.quiz_questions.values())
        
        return {
            'thresholds': {
                'low_risk': self.LOW_RISK,
                'medium_risk': self.MEDIUM_RISK,
                'high_risk': self.HIGH_RISK
            },
            'model_trained': self.detector.is_trained,
            'quiz_database': {
                'total_categories': len(self.quiz_questions),
                'total_questions': total_questions,
                'categories': list(self.quiz_questions.keys())
            }
        }

# Test the advanced CAPTCHA system
if __name__ == "__main__":
    print("=" * 70)
    print("TESTING ADVANCED CAPTCHA SYSTEM WITH QUIZZES")
    print("=" * 70)
    
    # Load trained model
    print("\n📂 Loading trained bot detection model...")
    detector = BotDetector()
    detector.load('bot_detector.pkl')
    
    # Create advanced CAPTCHA system
    captcha_sys = AdvancedCaptchaSystem(detector)
    print("✓ Advanced CAPTCHA system initialized\n")
    
    # Show quiz database stats
    stats = captcha_sys.get_statistics()
    print(f"📚 Quiz Database:")
    print(f"   Categories: {stats['quiz_database']['total_categories']}")
    print(f"   Total Questions: {stats['quiz_database']['total_questions']}")
    print(f"   Available: {', '.join(stats['quiz_database']['categories'])}\n")
    
    # Test scenarios
    test_cases = [
        {
            'name': '🧑 Test 1: Clear Human Behavior',
            'features': {
                'mouse_count': 150,
                'avg_mouse_speed': 300,
                'keystroke_count': 80,
                'typing_speed': 5,
                'session_duration': 45
            }
        },
        {
            'name': '🤔 Test 2: Slightly Suspicious (Simple Quiz)',
            'features': {
                'mouse_count': 50,
                'avg_mouse_speed': 450,
                'keystroke_count': 100,
                'typing_speed': 9,
                'session_duration': 15
            }
        },
        {
            'name': '⚠️  Test 3: Very Suspicious (Medium Quiz)',
            'features': {
                'mouse_count': 30,
                'avg_mouse_speed': 800,
                'keystroke_count': 200,
                'typing_speed': 15,
                'session_duration': 8
            }
        },
        {
            'name': '🤖 Test 4: Clear Bot Behavior (Hard Multi-Quiz)',
            'features': {
                'mouse_count': 5,
                'avg_mouse_speed': 1500,
                'keystroke_count': 300,
                'typing_speed': 25,
                'session_duration': 2
            }
        }
    ]
    
    print("=" * 70)
    
    for test in test_cases:
        print(f"\n{test['name']}")
        print("-" * 70)
        
        # Check user
        result = captcha_sys.check_user(test['features'])
        
        # Display results
        print(f"📈 Analysis:")
        print(f"   Bot Probability: {result['probability']*100:.1f}%")
        print(f"   Risk Level: {result['risk_level'].upper()}")
        print(f"   Action: {result['action'].upper()}")
        print(f"   Message: {result['message']}")
        
        # Generate CAPTCHA if needed
        if result['action'] != 'allow':
            print(f"\n🔒 CAPTCHA Challenge Generated:")
            captcha = captcha_sys.generate_captcha(result['captcha_type'])
            print(f"   Type: {captcha['type']}")
            print(f"   Difficulty: {captcha['difficulty']}")
            print(f"   Time Limit: {captcha['time_limit']} seconds")
            
            if captcha['type'] == 'quiz':
                print(f"\n   📝 Question:")
                print(f"      Category: {captcha['category']}")
                print(f"      {captcha['question']}")
                print(f"      Options: {', '.join(captcha['options'])}")
                print(f"      ✓ Correct Answer: {captcha['correct_answer']}")
            
            elif captcha['type'] == 'multi_quiz':
                print(f"\n   📝 Multi-Question Quiz:")
                print(f"      Total Questions: {captcha['total_questions']}")
                print(f"      Passing Score: {captcha['passing_score']}/{captcha['total_questions']}")
                print(f"\n      Questions:")
                for i, q in enumerate(captcha['questions'], 1):
                    print(f"\n      {i}. [{q['category'].upper()}] {q['question']}")
                    print(f"         Options: {', '.join(q['options'])}")
                    print(f"         ✓ Answer: {q['correct_answer']}")
        else:
            print(f"\n✅ No CAPTCHA needed - Access granted!")
        
        print("=" * 70)
    
    # Test quiz verification
    print("\n\n" + "=" * 70)
    print("TESTING QUIZ VERIFICATION")
    print("=" * 70)
    
    # Test 1: Correct answer with good timing
    print("\n✅ Test 1: Correct Answer (Good Timing)")
    quiz = captcha_sys.generate_captcha('medium_quiz')
    print(f"Question: {quiz['question']}")
    print(f"Correct Answer: {quiz['correct_answer']}")
    
    verification = captcha_sys.verify_captcha_response(quiz, {
        'answer': quiz['correct_answer'],
        'response_time': 5.5
    })
    print(f"Result: {verification}")
    
    # Test 2: Wrong answer
    print("\n❌ Test 2: Wrong Answer")
    wrong_answer = [opt for opt in quiz['options'] if opt != quiz['correct_answer']][0]
    verification = captcha_sys.verify_captcha_response(quiz, {
        'answer': wrong_answer,
        'response_time': 4.0
    })
    print(f"Result: {verification}")
    
    # Test 3: Suspiciously fast correct answer (bot-like)
    print("\n🚨 Test 3: Suspiciously Fast Response")
    verification = captcha_sys.verify_captcha_response(quiz, {
        'answer': quiz['correct_answer'],
        'response_time': 0.3  # Too fast!
    })
    print(f"Result: {verification}")
    
    # Test 4: Multi-quiz
    print("\n📚 Test 4: Multi-Quiz Verification")
    multi_quiz = captcha_sys.generate_captcha('hard_quiz')
    correct_answers = [q['correct_answer'] for q in multi_quiz['questions']]
    
    # User gets 2 out of 3 correct
    user_answers = correct_answers.copy()
    user_answers[0] = 'Wrong Answer'  # Make first answer wrong
    
    verification = captcha_sys.verify_captcha_response(multi_quiz, {
        'answers': user_answers,
        'response_time': 30
    })
    print(f"Result: Verified={verification['verified']}, Score={verification['score']}/{verification['total']}")
    
    print("\n" + "=" * 70)
    print("✅ ADVANCED CAPTCHA SYSTEM TESTING COMPLETE!")
    print("=" * 70)
    print("\nNext step: Update the API and frontend to use quiz challenges!")