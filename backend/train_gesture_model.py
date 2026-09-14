import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"
import numpy as np
import tensorflow as tf
import os

# Classes:
# 0: None
# 1: Thumb_Up (NEXT)
# 2: Index_Point (PREV)
# 3: Open_Palm (ROTATE)
# 4: Closed_Fist (STOP)

NUM_SAMPLES_PER_CLASS = 2000

import csv

CSV_FILE = "gesture_data.csv"

import glob

def load_real_data():
    X = []
    y = []
    
    csv_files = glob.glob("../frontend/gesture_*_data.csv") + \
                glob.glob("gesture_*_data.csv") + \
                glob.glob("gesture_data.csv") + \
                glob.glob("Hand data/gesture_*_data.csv") + \
                glob.glob("Hand data/*.csv")
    if not csv_files:
        print("ERROR: No gesture data CSVs found! Please open frontend/collect_data.html and record some data first.")
        exit(1)
        
    for file in csv_files:
        print(f"Loading {file}...")
        with open(file, mode='r') as f:
            reader = csv.reader(f)
            next(reader) # skip header
            for row in reader:
                if not row: continue
                y.append(int(row[0]))
                X.append([float(val) for val in row[1:]])
                
    return np.array(X), np.array(y)

print("Loading REAL gesture dataset from CSV...")
X, y = load_real_data()

indices = np.arange(X.shape[0])
np.random.shuffle(indices)
X = X[indices]
y = y[indices]

model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(63,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(5, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

print("Training model...")
model.fit(X, y, epochs=15, batch_size=32, validation_split=0.2)

import sys
import types
import setuptools
sys.modules['distutils'] = setuptools._distutils
sys.modules['distutils.util'] = setuptools._distutils.util
if not hasattr(tf.compat.v1, 'estimator'):
    tf.compat.v1.estimator = types.ModuleType('estimator')
    tf.compat.v1.estimator.Exporter = object

import tensorflowjs as tfjs

out_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'models', 'gesture_model')
os.makedirs(out_dir, exist_ok=True)
tfjs.converters.save_keras_model(model, out_dir)
print(f"Model successfully saved to {out_dir}")
