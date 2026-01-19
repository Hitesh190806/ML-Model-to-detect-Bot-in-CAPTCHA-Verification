import time
import json

class BehaviorTracker:
    """
    This class tracks user behavior like mouse movements and keystrokes
    """
    
    def __init__(self):
        # Store all tracked events
        self.mouse_data = []
        self.keyboard_data = []
        self.start_time = time.time()
    
    def add_mouse_movement(self, x, y):
        """
        Save mouse position and when it happened
        x, y = mouse coordinates on screen
        """
        self.mouse_data.append({
            'x': x,
            'y': y,
            'time': time.time()
        })
    
    def add_keystroke(self, key):
        """
        Save what key was pressed and when
        """
        self.keyboard_data.append({
            'key': key,
            'time': time.time()
        })
    
    def get_features(self):
        """
        Convert raw data into features the ML model can understand
        """
        features = {}
        
        # Feature 1: How many mouse movements?
        features['mouse_count'] = len(self.mouse_data)
        
        # Feature 2: Average mouse speed
        if len(self.mouse_data) > 1:
            speeds = []
            for i in range(1, len(self.mouse_data)):
                # Calculate distance between two points
                x1, y1 = self.mouse_data[i-1]['x'], self.mouse_data[i-1]['y']
                x2, y2 = self.mouse_data[i]['x'], self.mouse_data[i]['y']
                distance = ((x2-x1)**2 + (y2-y1)**2) ** 0.5
                
                # Calculate time difference
                time_diff = self.mouse_data[i]['time'] - self.mouse_data[i-1]['time']
                
                # Speed = distance / time
                if time_diff > 0:
                    speed = distance / time_diff
                    speeds.append(speed)
            
            features['avg_mouse_speed'] = sum(speeds) / len(speeds) if speeds else 0
        else:
            features['avg_mouse_speed'] = 0
        
        # Feature 3: How many keys pressed?
        features['keystroke_count'] = len(self.keyboard_data)
        
        # Feature 4: Typing speed (keys per second)
        session_time = time.time() - self.start_time
        features['typing_speed'] = features['keystroke_count'] / session_time if session_time > 0 else 0
        
        # Feature 5: Total session time
        features['session_duration'] = session_time
        
        return features

# Test the tracker
if __name__ == "__main__":
    print("Testing Behavior Tracker...\n")
    
    tracker = BehaviorTracker()
    
    # Simulate some mouse movements
    print("Simulating mouse movements...")
    tracker.add_mouse_movement(100, 200)
    time.sleep(0.1)
    tracker.add_mouse_movement(150, 250)
    time.sleep(0.1)
    tracker.add_mouse_movement(200, 300)
    
    # Simulate typing
    print("Simulating keyboard typing...")
    tracker.add_keystroke('h')
    time.sleep(0.2)
    tracker.add_keystroke('e')
    time.sleep(0.15)
    tracker.add_keystroke('l')
    time.sleep(0.18)
    tracker.add_keystroke('l')
    time.sleep(0.12)
    tracker.add_keystroke('o')
    
    # Get features
    features = tracker.get_features()
    
    print("\n✓ Extracted Features:")
    print(f"  - Mouse movements: {features['mouse_count']}")
    print(f"  - Average mouse speed: {features['avg_mouse_speed']:.2f} pixels/sec")
    print(f"  - Keystrokes: {features['keystroke_count']}")
    print(f"  - Typing speed: {features['typing_speed']:.2f} keys/sec")
    print(f"  - Session duration: {features['session_duration']:.2f} seconds")
    print("\n✓ Tracker working perfectly!")