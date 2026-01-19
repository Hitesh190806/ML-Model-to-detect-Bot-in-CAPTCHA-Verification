from flask import Flask, request, jsonify
from flask_cors import CORS
from tracker import BehaviorTracker
from model import BotDetector
from captcha import AdvancedCaptchaSystem
import uuid
import time

app = Flask(__name__)
CORS(app)  # Allow websites to use this API

# Load the trained model
print("🚀 Starting Advanced Intelligent CAPTCHA API...")
print("📂 Loading trained model...")
detector = BotDetector()
detector.load('bot_detector.pkl')

# Create advanced CAPTCHA system with quizzes
captcha_system = AdvancedCaptchaSystem(detector)
print("✅ System ready with quiz-based challenges!\n")

# Store active user sessions
sessions = {}
# Store active CAPTCHAs for verification
active_captchas = {}

# Clean up old sessions (older than 10 minutes)
def cleanup_old_sessions():
    current_time = time.time()
    sessions_to_remove = []
    
    for session_id, tracker in sessions.items():
        # If session is older than 10 minutes (600 seconds)
        if current_time - tracker.start_time > 600:
            sessions_to_remove.append(session_id)
    
    for session_id in sessions_to_remove:
        del sessions[session_id]
        if session_id in active_captchas:
            del active_captchas[session_id]
    
    if sessions_to_remove:
        print(f"🧹 Cleaned up {len(sessions_to_remove)} old sessions")

@app.route('/')
def home():
    """
    API documentation page with statistics
    """
    cleanup_old_sessions()
    stats = captcha_system.get_statistics()
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Advanced Intelligent CAPTCHA API</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }}
            h1 {{
                color: #2c3e50;
                margin-bottom: 10px;
                font-size: 32px;
            }}
            .badge {{
                display: inline-block;
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
                padding: 6px 15px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
                margin-left: 10px;
                text-transform: uppercase;
            }}
            .subtitle {{
                color: #7f8c8d;
                margin-bottom: 30px;
                font-size: 16px;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            .stat-card {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
                transition: transform 0.3s;
            }}
            .stat-card:hover {{
                transform: translateY(-5px);
            }}
            .stat-value {{
                font-size: 36px;
                font-weight: bold;
                margin-bottom: 8px;
            }}
            .stat-label {{
                font-size: 14px;
                opacity: 0.95;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            .feature-list {{
                background: linear-gradient(135deg, #e8f4f8 0%, #f0f8ff 100%);
                padding: 25px;
                border-radius: 15px;
                margin: 25px 0;
                border-left: 5px solid #667eea;
            }}
            .feature-list h3 {{
                color: #2c3e50;
                margin-bottom: 15px;
                font-size: 20px;
            }}
            .feature-list ul {{
                list-style: none;
                padding: 0;
            }}
            .feature-list li {{
                padding: 10px 0;
                color: #34495e;
                font-size: 15px;
                border-bottom: 1px solid rgba(102, 126, 234, 0.1);
            }}
            .feature-list li:last-child {{
                border-bottom: none;
            }}
            .feature-list li:before {{
                content: "✓ ";
                color: #28a745;
                font-weight: bold;
                margin-right: 10px;
                font-size: 18px;
            }}
            .endpoint-section {{
                margin: 30px 0;
            }}
            .endpoint-section h3 {{
                color: #2c3e50;
                margin-bottom: 20px;
                font-size: 24px;
            }}
            .endpoint {{
                background: #f8f9fa;
                padding: 20px;
                margin: 15px 0;
                border-radius: 10px;
                border-left: 5px solid #667eea;
                transition: all 0.3s;
            }}
            .endpoint:hover {{
                background: #e9ecef;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            }}
            .method {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 5px 12px;
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
                margin-right: 10px;
                display: inline-block;
            }}
            .method.get {{
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            }}
            code {{
                background: #2c3e50;
                color: #ecf0f1;
                padding: 4px 10px;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
            }}
            .endpoint-desc {{
                color: #6c757d;
                margin-top: 8px;
                font-size: 14px;
                line-height: 1.6;
            }}
            .info-box {{
                background: linear-gradient(135deg, #fff3cd 0%, #fff9e6 100%);
                padding: 20px;
                border-radius: 10px;
                border-left: 5px solid #ffc107;
                margin: 25px 0;
            }}
            .info-box h4 {{
                color: #856404;
                margin-bottom: 10px;
                font-size: 18px;
            }}
            .info-box p {{
                color: #856404;
                line-height: 1.8;
                margin: 5px 0;
            }}
            .cta-button {{
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 30px;
                border-radius: 10px;
                text-decoration: none;
                font-weight: bold;
                margin-top: 20px;
                transition: transform 0.3s, box-shadow 0.3s;
            }}
            .cta-button:hover {{
                transform: translateY(-3px);
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Advanced Intelligent CAPTCHA API <span class="badge">With Quizzes</span></h1>
            <p class="subtitle">ML-Powered Bot Detection with Interactive Quiz Challenges</p>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">{len(sessions)}</div>
                    <div class="stat-label">Active Sessions</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(active_captchas)}</div>
                    <div class="stat-label">Active CAPTCHAs</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['quiz_database']['total_categories']}</div>
                    <div class="stat-label">Quiz Categories</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['quiz_database']['total_questions']}</div>
                    <div class="stat-label">Quiz Questions</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{'✅' if stats['model_trained'] else '❌'}</div>
                    <div class="stat-label">Model Status</div>
                </div>
            </div>
            
            <div class="feature-list">
                <h3>🎯 System Features</h3>
                <ul>
                    <li>Machine Learning Bot Detection (Random Forest Classifier)</li>
                    <li>Behavioral Analysis (Mouse, Keyboard, Timing)</li>
                    <li>Quiz-Based CAPTCHA Challenges</li>
                    <li>Multiple Difficulty Levels (Simple/Medium/Hard)</li>
                    <li>Quiz Categories: Logic, Math, Common Sense, Patterns, Visual</li>
                    <li>Adaptive Risk Assessment</li>
                    <li>Response Time Analysis (Detect Too-Fast Responses)</li>
                    <li>Multi-Question Challenges for High-Risk Cases</li>
                    <li>Real-time Session Management</li>
                </ul>
            </div>
            
            <div class="endpoint-section">
                <h3>📡 API Endpoints</h3>
                
                <div class="endpoint">
                    <span class="method">POST</span> <code>/api/session/start</code>
                    <div class="endpoint-desc">
                        Start a new tracking session. Returns a unique session ID.
                        <br><strong>Response:</strong> <code>{{"session_id": "...", "success": true}}</code>
                    </div>
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> <code>/api/track</code>
                    <div class="endpoint-desc">
                        Track user behavior (mouse movements, keystrokes).
                        <br><strong>Body:</strong> <code>{{"session_id": "...", "type": "mouse", "x": 100, "y": 200}}</code>
                        <br><strong>Types:</strong> "mouse" or "keyboard"
                    </div>
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> <code>/api/verify</code>
                    <div class="endpoint-desc">
                        Analyze user behavior and determine if CAPTCHA/quiz is needed.
                        <br><strong>Body:</strong> <code>{{"session_id": "..."}}</code>
                        <br><strong>Returns:</strong> Risk assessment + quiz challenge if bot detected
                    </div>
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> <code>/api/verify/quiz</code>
                    <div class="endpoint-desc">
                        Submit quiz answer for verification.
                        <br><strong>Body:</strong> <code>{{"session_id": "...", "response": {{"answer": "...", "response_time": 5.5}}}}</code>
                        <br><strong>Returns:</strong> Verification result with explanation
                    </div>
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/api/stats</code>
                    <div class="endpoint-desc">
                        Get system statistics and configuration.
                        <br><strong>Returns:</strong> Active sessions, quiz database info, thresholds
                    </div>
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/api/health</code>
                    <div class="endpoint-desc">
                        Health check endpoint.
                        <br><strong>Returns:</strong> System status and timestamp
                    </div>
                </div>
            </div>
            
            <div class="info-box">
                <h4>💡 How It Works</h4>
                <p>1️⃣ System tracks user behavior (mouse, keyboard, timing)</p>
                <p>2️⃣ ML model analyzes patterns and calculates bot probability</p>
                <p>3️⃣ Based on risk level:</p>
                <p>&nbsp;&nbsp;&nbsp;&nbsp;• <strong>Low Risk (0-30%):</strong> Access granted immediately ✅</p>
                <p>&nbsp;&nbsp;&nbsp;&nbsp;• <strong>Medium Risk (30-60%):</strong> Simple checkbox or easy quiz 🤔</p>
                <p>&nbsp;&nbsp;&nbsp;&nbsp;• <strong>High Risk (60-85%):</strong> Single quiz question ⚠️</p>
                <p>&nbsp;&nbsp;&nbsp;&nbsp;• <strong>Critical Risk (85-100%):</strong> Multiple quiz questions 🚨</p>
                <p>4️⃣ User solves quiz to prove they're human</p>
                <p>5️⃣ System verifies answer and response time</p>
            </div>
            
            <div style="text-align: center; margin-top: 40px;">
                <h3 style="color: #2c3e50; margin-bottom: 15px;">🧪 Ready to Test?</h3>
                <p style="color: #6c757d; margin-bottom: 20px;">Open the test page to see quiz challenges in action!</p>
                <a href="#" class="cta-button" onclick="alert('Open advanced_test_page.html in your browser'); return false;">
                    🚀 Try It Now
                </a>
            </div>
            
            <div style="margin-top: 40px; padding: 20px; background: #f8f9fa; border-radius: 10px; text-align: center;">
                <p style="color: #6c757d; font-size: 14px;">
                    <strong>Quiz Categories Available:</strong><br>
                    {', '.join(stats['quiz_database']['categories']).title()}
                </p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/api/session/start', methods=['POST'])
def start_session():
    """
    Start a new tracking session for a user
    """
    cleanup_old_sessions()
    
    session_id = str(uuid.uuid4())  # Generate unique ID
    sessions[session_id] = BehaviorTracker()
    
    print(f"🆕 New session started: {session_id[:8]}...")
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'message': 'Session started. Behavior tracking enabled with quiz-based verification.'
    })

@app.route('/api/track', methods=['POST'])
def track_behavior():
    """
    Record user behavior (mouse movements, keystrokes)
    """
    data = request.json
    session_id = data.get('session_id')
    
    if not session_id or session_id not in sessions:
        return jsonify({'error': 'Invalid session ID'}), 400
    
    tracker = sessions[session_id]
    
    # Track based on event type
    if data.get('type') == 'mouse':
        tracker.add_mouse_movement(data['x'], data['y'])
    elif data.get('type') == 'keyboard':
        tracker.add_keystroke(data.get('key', ''))
    
    return jsonify({'success': True})

@app.route('/api/verify', methods=['POST'])
def verify_user():
    """
    Analyze behavior and decide if CAPTCHA/quiz is needed
    """
    data = request.json
    session_id = data.get('session_id')
    
    if not session_id or session_id not in sessions:
        return jsonify({'error': 'Invalid session ID'}), 400
    
    # Get tracked behavior
    tracker = sessions[session_id]
    features = tracker.get_features()
    
    print(f"\n📊 Verifying session {session_id[:8]}...")
    print(f"   Features: {features}")
    
    # Check with CAPTCHA system
    result = captcha_system.check_user(features)
    
    print(f"   Bot Probability: {result['probability']*100:.1f}%")
    print(f"   Risk Level: {result['risk_level']}")
    print(f"   Action: {result['action']}")
    
    # Add CAPTCHA/Quiz if needed
    if result['action'] != 'allow':
        captcha = captcha_system.generate_captcha(result.get('captcha_type'))
        result['captcha'] = captcha
        
        # Store CAPTCHA for later verification
        active_captchas[session_id] = {
            'captcha': captcha,
            'generated_at': time.time()
        }
        
        print(f"   CAPTCHA Type: {captcha['type']}")
        if captcha['type'] == 'quiz':
            print(f"   Quiz Category: {captcha['category']}")
        elif captcha['type'] == 'multi_quiz':
            print(f"   Total Questions: {captcha['total_questions']}")
    else:
        print(f"   ✅ Access granted - No CAPTCHA needed")
    
    return jsonify(result)

@app.route('/api/verify/quiz', methods=['POST'])
def verify_quiz():
    """
    Verify user's quiz answer submission
    """
    data = request.json
    session_id = data.get('session_id')
    user_response = data.get('response')
    
    if not session_id or session_id not in sessions:
        return jsonify({'error': 'Invalid session ID'}), 400
    
    if session_id not in active_captchas:
        return jsonify({'error': 'No active CAPTCHA for this session'}), 400
    
    captcha_data = active_captchas[session_id]
    captcha = captcha_data['captcha']
    
    # Calculate response time if not provided
    if 'response_time' not in user_response:
        user_response['response_time'] = time.time() - captcha_data['generated_at']
    
    # Verify the response
    verification = captcha_system.verify_captcha_response(captcha, user_response)
    
    print(f"\n✅ Quiz verification for {session_id[:8]}...")
    print(f"   Type: {captcha['type']}")
    print(f"   Verified: {verification['verified']}")
    print(f"   Reason: {verification['reason']}")
    
    if captcha['type'] == 'multi_quiz' and 'score' in verification:
        print(f"   Score: {verification['score']}/{verification['total']}")
    
    # Clear CAPTCHA if verified successfully
    if verification['verified']:
        del active_captchas[session_id]
        verification['message'] = 'Quiz solved correctly! Access granted. ✅'
        verification['access_granted'] = True
    else:
        verification['message'] = 'Quiz failed. Please try again. ❌'
        verification['access_granted'] = False
    
    return jsonify(verification)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get system statistics
    """
    cleanup_old_sessions()
    stats = captcha_system.get_statistics()
    
    return jsonify({
        'active_sessions': len(sessions),
        'active_captchas': len(active_captchas),
        'model_trained': detector.is_trained,
        'quiz_database': stats['quiz_database'],
        'thresholds': stats['thresholds']
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'system': 'Advanced Intelligent CAPTCHA API',
        'version': '2.0',
        'features': ['ML Detection', 'Quiz Challenges', 'Adaptive Risk']
    })

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🚀 ADVANCED INTELLIGENT CAPTCHA API SERVER")
    print("=" * 70)
    print("\n📍 Server running at: http://localhost:5000")
    print("📖 Open browser to see API documentation")
    print("🎯 Features: Quiz-Based Bot Detection")
    
    # Get quiz stats
    quiz_stats = captcha_system.get_statistics()
    print(f"📚 Quiz Categories: {', '.join(quiz_stats['quiz_database']['categories'])}")
    print(f"📝 Total Questions: {quiz_stats['quiz_database']['total_questions']}")
    
    print("\n🧪 Test with: advanced_test_page.html")
    print("\n💡 Press Ctrl+C to stop the server\n")
    print("=" * 70 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')