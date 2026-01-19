import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import numpy as np

class BotDetector:
    """
    Machine Learning model to detect bots
    """
    
    def __init__(self):
        # Random Forest is good for this task
        self.model = RandomForestClassifier(
            n_estimators=100,  # Use 100 decision trees
            max_depth=10,
            random_state=42
        )
        self.is_trained = False
        self.feature_names = None
    
    def train(self, csv_file='training_data.csv'):
        """
        Train the model using our dataset
        """
        print("=" * 60)
        print("TRAINING BOT DETECTION MODEL")
        print("=" * 60)
        
        print("\n📂 Loading training data from", csv_file)
        df = pd.read_csv(csv_file)
        print(f"   ✓ Loaded {len(df)} samples")
        
        # Separate features (X) and labels (y)
        X = df.drop('is_bot', axis=1)  # Features
        y = df['is_bot']  # Labels (0=human, 1=bot)
        
        self.feature_names = X.columns.tolist()
        print(f"\n📊 Features used for training: {self.feature_names}")
        
        # Split into training (80%) and testing (20%)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\n📚 Training set: {len(X_train)} samples")
        print(f"🧪 Testing set: {len(X_test)} samples")
        print(f"   - Humans in training: {sum(y_train == 0)}")
        print(f"   - Bots in training: {sum(y_train == 1)}")
        
        # Train the model
        print("\n🔄 Training Random Forest model...")
        self.model.fit(X_train, y_train)
        print("   ✓ Training complete!")
        
        # Test accuracy
        print("\n📈 Evaluating model performance...")
        train_predictions = self.model.predict(X_train)
        test_predictions = self.model.predict(X_test)
        
        train_accuracy = accuracy_score(y_train, train_predictions)
        test_accuracy = accuracy_score(y_test, test_predictions)
        
        print(f"\n✅ RESULTS:")
        print(f"   Training Accuracy: {train_accuracy*100:.2f}%")
        print(f"   Testing Accuracy: {test_accuracy*100:.2f}%")
        
        # Confusion Matrix
        print("\n📊 Confusion Matrix (Test Set):")
        cm = confusion_matrix(y_test, test_predictions)
        print(f"   True Humans correctly identified: {cm[0][0]}")
        print(f"   Humans misclassified as Bots: {cm[0][1]}")
        print(f"   Bots misclassified as Humans: {cm[1][0]}")
        print(f"   True Bots correctly identified: {cm[1][1]}")
        
        # Detailed Report
        print("\n📋 Detailed Classification Report:")
        print(classification_report(y_test, test_predictions, 
                                   target_names=['Human', 'Bot']))
        
        # Feature Importance
        print("\n🎯 Feature Importance (what matters most):")
        importances = self.model.feature_importances_
        for name, importance in sorted(zip(self.feature_names, importances), 
                                      key=lambda x: x[1], reverse=True):
            print(f"   {name}: {importance*100:.2f}%")
        
        self.is_trained = True
        return self
    
    def predict(self, features):
        """
        Predict if given features are from a bot
        Returns: probability of being a bot (0 to 1)
        """
        if not self.is_trained:
            raise Exception("Model not trained yet! Run .train() first.")
        
        # Convert dict to DataFrame if needed
        if isinstance(features, dict):
            features = pd.DataFrame([features])
        
        # Ensure correct feature order
        features = features[self.feature_names]
        
        # Get probability of being a bot
        bot_probability = self.model.predict_proba(features)[0][1]
        
        return bot_probability
    
    def predict_with_details(self, features):
        """
        Get detailed prediction with explanation
        """
        bot_prob = self.predict(features)
        is_bot = bot_prob > 0.5
        
        return {
            'is_bot': is_bot,
            'bot_probability': bot_prob,
            'human_probability': 1 - bot_prob,
            'confidence': max(bot_prob, 1 - bot_prob),
            'prediction': 'BOT' if is_bot else 'HUMAN'
        }
    
    def save(self, filename='bot_detector.pkl'):
        """
        Save the trained model to a file
        """
        if not self.is_trained:
            print("⚠️  Warning: Model not trained yet!")
            return
        
        model_data = {
            'model': self.model,
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, filename)
        print(f"\n💾 Model saved to {filename}")
    
    def load(self, filename='bot_detector.pkl'):
        """
        Load a trained model from a file
        """
        print(f"📂 Loading model from {filename}...")
        model_data = joblib.load(filename)
        
        self.model = model_data['model']
        self.feature_names = model_data['feature_names']
        self.is_trained = model_data['is_trained']
        
        print(f"   ✓ Model loaded successfully!")

# Train and test the model
if __name__ == "__main__":
    # Create and train detector
    detector = BotDetector()
    detector.train('training_data.csv')
    
    # Save the model
    detector.save('bot_detector.pkl')
    
    # Test with example data
    print("\n" + "=" * 60)
    print("TESTING THE MODEL WITH EXAMPLES")
    print("=" * 60)
    
    # Example 1: Clear human behavior
    print("\n🧑 Test 1: Typical Human Behavior")
    human_features = {
        'mouse_count': 150,
        'avg_mouse_speed': 300,
        'keystroke_count': 80,
        'typing_speed': 5,
        'session_duration': 45
    }
    
    result = detector.predict_with_details(human_features)
    print(f"   Features: {human_features}")
    print(f"   Prediction: {result['prediction']}")
    print(f"   Bot Probability: {result['bot_probability']*100:.1f}%")
    print(f"   Confidence: {result['confidence']*100:.1f}%")
    
    # Example 2: Suspicious behavior
    print("\n🤔 Test 2: Suspicious Behavior")
    suspicious_features = {
        'mouse_count': 50,
        'avg_mouse_speed': 600,
        'keystroke_count': 150,
        'typing_speed': 12,
        'session_duration': 10
    }
    
    result = detector.predict_with_details(suspicious_features)
    print(f"   Features: {suspicious_features}")
    print(f"   Prediction: {result['prediction']}")
    print(f"   Bot Probability: {result['bot_probability']*100:.1f}%")
    print(f"   Confidence: {result['confidence']*100:.1f}%")
    
    # Example 3: Clear bot behavior
    print("\n🤖 Test 3: Clear Bot Behavior")
    bot_features = {
        'mouse_count': 5,
        'avg_mouse_speed': 1500,
        'keystroke_count': 300,
        'typing_speed': 25,
        'session_duration': 2
    }
    
    result = detector.predict_with_details(bot_features)
    print(f"   Features: {bot_features}")
    print(f"   Prediction: {result['prediction']}")
    print(f"   Bot Probability: {result['bot_probability']*100:.1f}%")
    print(f"   Confidence: {result['confidence']*100:.1f}%")
    
    # Example 4: Slow, careful human
    print("\n🐢 Test 4: Slow, Careful Human")
    slow_human = {
        'mouse_count': 80,
        'avg_mouse_speed': 150,
        'keystroke_count': 40,
        'typing_speed': 3,
        'session_duration': 90
    }
    
    result = detector.predict_with_details(slow_human)
    print(f"   Features: {slow_human}")
    print(f"   Prediction: {result['prediction']}")
    print(f"   Bot Probability: {result['bot_probability']*100:.1f}%")
    print(f"   Confidence: {result['confidence']*100:.1f}%")
    
    print("\n" + "=" * 60)
    print("✅ MODEL TRAINING AND TESTING COMPLETE!")
    print("=" * 60)
    print("\nNext step: Run 'python captcha.py' to build the CAPTCHA system")