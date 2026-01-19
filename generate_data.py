import pandas as pd
import random
import time

def generate_human_data(num_samples=100):
    """
    Simulate how humans interact with a website
    Humans: varied speed, irregular patterns, pauses
    """
    data = []
    
    for _ in range(num_samples):
        # Humans move mouse naturally (20-200 movements)
        mouse_count = random.randint(20, 200)
        
        # Humans have varied mouse speed (100-800 pixels/sec)
        avg_mouse_speed = random.uniform(100, 800)
        
        # Humans type at human speed (30-150 keys)
        keystroke_count = random.randint(30, 150)
        
        # Typing speed varies (2-8 keys per second)
        typing_speed = random.uniform(2, 8)
        
        # Humans spend time reading (10-120 seconds)
        session_duration = random.uniform(10, 120)
        
        data.append({
            'mouse_count': mouse_count,
            'avg_mouse_speed': avg_mouse_speed,
            'keystroke_count': keystroke_count,
            'typing_speed': typing_speed,
            'session_duration': session_duration,
            'is_bot': 0  # 0 = human
        })
    
    return data

def generate_bot_data(num_samples=100):
    """
    Simulate how bots interact
    Bots: consistent speed, perfect patterns, no pauses
    """
    data = []
    
    for _ in range(num_samples):
        # Bots make fewer, more direct movements (0-20)
        mouse_count = random.randint(0, 20)
        
        # Bots move at consistent, fast speed (500-2000 pixels/sec)
        avg_mouse_speed = random.uniform(500, 2000)
        
        # Bots type a lot or not at all (0-50 or 200-500)
        if random.random() < 0.5:
            keystroke_count = random.randint(0, 50)
        else:
            keystroke_count = random.randint(200, 500)
        
        # Bots type very fast or very slow (0-1 or 15-30 keys/sec)
        if random.random() < 0.5:
            typing_speed = random.uniform(0, 1)
        else:
            typing_speed = random.uniform(15, 30)
        
        # Bots are very fast (0-5 seconds)
        session_duration = random.uniform(0, 5)
        
        data.append({
            'mouse_count': mouse_count,
            'avg_mouse_speed': avg_mouse_speed,
            'keystroke_count': keystroke_count,
            'typing_speed': typing_speed,
            'session_duration': session_duration,
            'is_bot': 1  # 1 = bot
        })
    
    return data

if __name__ == "__main__":
    print("=" * 50)
    print("GENERATING TRAINING DATA")
    print("=" * 50)
    
    # Generate dataset
    print("\n📊 Generating human behavior samples...")
    human_data = generate_human_data(500)
    print(f"   ✓ Created {len(human_data)} human samples")
    
    print("\n🤖 Generating bot behavior samples...")
    bot_data = generate_bot_data(500)
    print(f"   ✓ Created {len(bot_data)} bot samples")
    
    # Combine and shuffle
    print("\n🔀 Combining and shuffling data...")
    all_data = human_data + bot_data
    random.shuffle(all_data)
    
    # Save to CSV file
    df = pd.DataFrame(all_data)
    df.to_csv('training_data.csv', index=False)
    
    print(f"\n✅ SUCCESS! Created training_data.csv with {len(all_data)} samples")
    print(f"   - Humans: {len(human_data)} samples")
    print(f"   - Bots: {len(bot_data)} samples")
    
    print("\n📋 First 5 rows of data:")
    print(df.head())
    
    print("\n📊 Data statistics:")
    print(df.describe())
    
    print("\n✅ Data generation complete!")
    print("   Next step: Run 'python model.py' to train the model")