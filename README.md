🤖ML-Model-to-Detect-Bot-in-CAPTCHA-Verification

🚀A Machine Learning based system to intelligently detect whether a CAPTCHA interaction is performed by a 🧑Human or an 🤖Bot using behavioral patterns instead of traditional CAPTCHA solving.

🔍Project-Overview
This project enhances CAPTCHA security by analyzing user interaction behavior such as mouse movement, timing, and activity flow.Using ML classification,the system predicts whether the interaction is bot-driven or human-driven,helping reduce false positives and improve security.🛡️

📂Project-Structure
📄advanced_test_page.html→Advanced CAPTCHA test interface  
📄test_page.html→Basic CAPTCHA test page  
🐍api.py→Flask API to serve ML predictions  
🐍model.py→Model training and saving logic  
🐍generate_data.py→Training data generation  
🐍tracker.py→Tracks user interaction behavior  
🐍captcha.py→CAPTCHA interaction logic  
📦bot_detector.pkl→Trained ML model  
📊training_data.csv→Collected training dataset  

🧠How-It-Works
1️⃣User interactions are tracked in real time  
2️⃣Behavioral data is collected and stored  
3️⃣ML model is trained using labeled data  
4️⃣API predicts Human✅or Bot❌  

⚙️Installation
pip install numpy pandas scikit-learn flask

🏋️Train-the-Model
python generate_data.py
python model.py

▶️Run-the-API
python api.py

🌐Server runs at:http://localhost:5000

🧪Testing
Open advanced_test_page.html in your browser and interact with the CAPTCHA.The system will classify the behavior automatically.

📈Features
✅Behavior-based bot detection
✅Machine Learning classification
✅Flask API integration
✅Real-time CAPTCHA interaction analysis

🎯Use-Cases
🔐Secure web forms
📝Prevent fake registrations
🛡️Reduce automated abuse
🤖Advanced CAPTCHA systems

🤝Contributions
Pull requests are welcome!Enhance models,features,or UI to make detection more robust.💡
