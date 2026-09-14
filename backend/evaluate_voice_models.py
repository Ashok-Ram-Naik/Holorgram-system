import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2" # Suppress TF warnings
import numpy as np
import scipy.io.wavfile as wav
import tensorflow as tf

try:
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, confusion_matrix
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError:
    print("ERROR: Missing evaluation libraries. Please run:")
    print("pip install scikit-learn matplotlib seaborn pandas scipy")
    exit(1)

WORDS = ['next', 'previous', 'rotate', 'stop', 'background']
TARGET_LEN = 22050
AUGMENTATIONS_PER_SAMPLE = 50
DATA_DIR = 'voice_data'

def augment_audio(audio_data):
    noise_amp = 0.05 * np.random.uniform() * np.amax(audio_data)
    audio_data = audio_data.astype('float64') + noise_amp * np.random.normal(size=audio_data.shape[0])
    shift = np.random.randint(2000)
    if shift > 0:
        direction = np.random.choice(['left', 'right'])
        if direction == 'left':
            audio_data = np.pad(audio_data, (0, shift), mode='constant')[shift:]
        else:
            audio_data = np.pad(audio_data, (shift, 0), mode='constant')[:-shift]
    return audio_data

def build_dataset_from_real():
    X = []
    y = []
    
    if not os.path.exists(DATA_DIR):
         print(f"ERROR: '{DATA_DIR}' folder not found! Please run collect_voice_data.py first to record your voice.")
         exit(1)
         
    for label, word in enumerate(WORDS):
        word_dir = os.path.join(DATA_DIR, word)
        if not os.path.exists(word_dir):
            continue
            
        for file in os.listdir(word_dir):
            if not file.endswith('.wav'): continue
            
            file_path = os.path.join(word_dir, file)
            try:
                rate, data = wav.read(file_path)
                
                if len(data.shape) > 1:
                    data = data.mean(axis=1)
                if np.max(np.abs(data)) > 0:
                    data = data / np.max(np.abs(data))
                    
                if len(data) > TARGET_LEN:
                    start = (len(data) - TARGET_LEN) // 2
                    data = data[start:start+TARGET_LEN]
                else:
                    data = np.pad(data, (0, TARGET_LEN - len(data)), mode='constant')
                    
                X.append(data)
                y.append(label)
                
                # Apply data augmentation to massively expand dataset for CNN
                for _ in range(AUGMENTATIONS_PER_SAMPLE):
                    aug_data = augment_audio(data)
                    X.append(aug_data)
                    y.append(label)
            except Exception as e:
                pass
                
    return np.array(X), np.array(y)

if __name__ == "__main__":
    print("\n--- INITIALIZING VOICE MODEL EVALUATION ---")
    print("1. Loading Audio Waves and Applying Data Augmentation...")
    X, y = build_dataset_from_real()
    
    if len(X) == 0:
        print(f"Error: No valid .wav files found inside '{DATA_DIR}/' subdirectories.")
        exit(1)
        
    # Reshape for Conv1D (Samples, Timesteps, Channels)
    X = X.reshape(-1, TARGET_LEN, 1)
    print(f"Total augmented audio samples prepared: {len(X)}")

    print("\n2. Splitting into Train and Test sets (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training samples: {len(X_train)} | Testing samples: {len(X_test)}")

    print("\n3. Building and Training Conv1D Architecture...")
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=(TARGET_LEN, 1)),
        tf.keras.layers.Conv1D(16, 11, activation='relu', strides=4),
        tf.keras.layers.MaxPooling1D(4),
        tf.keras.layers.Conv1D(32, 11, activation='relu', strides=4),
        tf.keras.layers.MaxPooling1D(4),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(len(WORDS), activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    # Train silently
    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)

    print("\n4. Evaluating CNN on unseen Test Data...")
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"-> Test Accuracy: {test_acc*100:.2f}%")

    print("\n5. Generating Predictions...")
    y_pred_probs = model.predict(X_test, verbose=0)
    y_pred = np.argmax(y_pred_probs, axis=1)

    print("\n\n================ CLASSIFICATION REPORT ================")
    unique_labels = sorted(list(set(y)))
    target_names = [WORDS[i] for i in unique_labels]
    
    print(classification_report(y_test, y_pred, target_names=target_names))
    print("=======================================================\n")

    print("6. Generating Voice Confusion Matrix Image...")
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(10, 8))
    # Using an Orange colormap to visually distinguish it from the Gesture (Blue) one
    sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges', 
                xticklabels=target_names, yticklabels=target_names)
    plt.title('Voice Command Recognition Confusion Matrix', fontsize=16)
    plt.ylabel('Actual Command', fontsize=12)
    plt.xlabel('Predicted Command', fontsize=12)
    plt.xticks(rotation=45)

    output_img = "voice_confusion_matrix.png"
    plt.savefig(output_img, dpi=300, bbox_inches='tight')
    print(f"Success! Saved visual confusion matrix to {os.path.abspath(output_img)}")
    print("You can now include 'voice_confusion_matrix.png' in your project report.")
