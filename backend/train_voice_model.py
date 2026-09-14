import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"
import numpy as np
import pyttsx3
import scipy.io.wavfile as wav
import tensorflow as tf
import time
import shutil

WORDS = ['next', 'previous', 'rotate', 'stop', 'background']
TARGET_LEN = 22050
SAMPLES_PER_WORD = 500

DATA_DIR = 'voice_data'
AUGMENTATIONS_PER_SAMPLE = 50

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
         print(f"ERROR: {DATA_DIR} not found! Please run collect_voice_data.py first.")
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
                    # take center
                    start = (len(data) - TARGET_LEN) // 2
                    data = data[start:start+TARGET_LEN]
                else:
                    data = np.pad(data, (0, TARGET_LEN - len(data)), mode='constant')
                    
                # Use original
                X.append(data)
                y.append(label)
                
                # Augment
                for _ in range(AUGMENTATIONS_PER_SAMPLE):
                    aug_data = augment_audio(data)
                    X.append(aug_data)
                    y.append(label)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                
    return np.array(X), np.array(y)

print("Building dataset from REAL voice recordings...")
X, y = build_dataset_from_real()
X = X.reshape(-1, TARGET_LEN, 1)

indices = np.arange(X.shape[0])
np.random.shuffle(indices)
X = X[indices]
y = y[indices]

# No temp_dir to delete anymore since we use real data.

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
model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2)

import sys
import types
import setuptools
sys.modules['distutils'] = setuptools._distutils
sys.modules['distutils.util'] = setuptools._distutils.util
if not hasattr(tf.compat.v1, 'estimator'):
    tf.compat.v1.estimator = types.ModuleType('estimator')
    tf.compat.v1.estimator.Exporter = object

import tensorflowjs as tfjs
out_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'models', 'voice_model')
os.makedirs(out_dir, exist_ok=True)
with open(os.path.join(out_dir, 'metadata.json'), 'w') as f:
    f.write(f'{{"sequence_length": {TARGET_LEN}, "words": {WORDS}}}')
tfjs.converters.save_keras_model(model, out_dir)
print(f"Voice model successfully saved to {out_dir}")
