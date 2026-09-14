import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2" # Suppress TF warnings
import numpy as np
import tensorflow as tf
import csv
import glob

try:
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, confusion_matrix
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError:
    print("ERROR: Missing evaluation libraries. Please run:")
    print("pip install scikit-learn matplotlib seaborn pandas")
    exit(1)

GESTURES = {
    0: "None",
    1: "Thumb Up",
    2: "Index Point",
    3: "Open Palm",
    4: "Closed Fist"
}

def load_real_data():
    X = []
    y = []
    # Try multiple common paths where data might have been collected
    csv_files = glob.glob("../frontend/gesture_*_data.csv") + \
                glob.glob("gesture_*_data.csv") + \
                glob.glob("Hand data/gesture_*_data.csv") + \
                glob.glob("Hand data/*.csv")
    
    if not csv_files:
        print("ERROR: No gesture data CSVs found!")
        exit(1)
        
    for file in csv_files:
        print(f"Loading {file}...")
        with open(file, mode='r') as f:
            reader = csv.reader(f)
            next(reader) # skip header
            for row in reader:
                if not row: continue
                try:
                    y.append(int(row[0]))
                    X.append([float(val) for val in row[1:]])
                except Exception:
                    pass
                
    return np.array(X), np.array(y)

if __name__ == "__main__":
    print("\n--- INITIALIZING EVALUATION ---")
    print("1. Loading Dataset...")
    X, y = load_real_data()
    print(f"Total samples loaded: {len(X)}")

    print("\n2. Splitting into Train and Test sets (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training samples: {len(X_train)} | Testing samples: {len(X_test)}")

    print("\n3. Building and Training Model...")
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=(63,)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(5, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    # Train silently to avoid clutter
    model.fit(X_train, y_train, epochs=15, batch_size=32, verbose=0)

    print("\n4. Evaluating Model on unseen Test Data...")
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"-> Test Accuracy: {test_acc*100:.2f}%")

    print("\n5. Generating Predictions...")
    y_pred_probs = model.predict(X_test, verbose=0)
    y_pred = np.argmax(y_pred_probs, axis=1)

    print("\n\n================ CLASSIFICATION REPORT ================")
    # Handle cases where some gestures weren't loaded in the CSV
    unique_labels = sorted(list(set(y)))
    target_names = [GESTURES.get(i, f"Class {i}") for i in unique_labels]
    
    print(classification_report(y_test, y_pred, target_names=target_names))
    print("=======================================================\n")

    print("6. Generating Confusion Matrix Image...")
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=target_names, yticklabels=target_names)
    plt.title('Gesture Recognition Confusion Matrix', fontsize=16)
    plt.ylabel('Actual Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.xticks(rotation=45)

    # Save the plot
    output_img = "confusion_matrix.png"
    plt.savefig(output_img, dpi=300, bbox_inches='tight')
    print(f"Success! Saved visual confusion matrix to {os.path.abspath(output_img)}")
    print("You can now include 'confusion_matrix.png' in your project report.")
