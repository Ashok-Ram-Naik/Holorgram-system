import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import time
import os

WORDS = ['next', 'previous', 'rotate', 'stop', 'background']
RATE = 22050
DURATION = 1.5 # seconds
SAMPLES_PER_WORD = 10
DATA_DIR = 'voice_data'

os.makedirs(DATA_DIR, exist_ok=True)
for word in WORDS:
    os.makedirs(os.path.join(DATA_DIR, word), exist_ok=True)

print("Voice Data Collector")
print("====================")
print(f"We will record {SAMPLES_PER_WORD} samples for each word.")
print(f"Each recording is {DURATION} seconds long.")
print("Wait for the 'RECORDING...' prompt, speak the word clearly, then wait.")

for word in WORDS:
    print(f"\n--- Get ready to record '{word.upper()}' ---")
    input("Press Enter to begin this word...")
    
    for i in range(SAMPLES_PER_WORD):
        print(f"[{i+1}/{SAMPLES_PER_WORD}] Recording in 1 second...")
        time.sleep(1)
        print(">> RECORDING...")
        audio_data = sd.rec(int(DURATION * RATE), samplerate=RATE, channels=1, dtype='int16')
        sd.wait()
        print("Saved.")
        
        filepath = os.path.join(DATA_DIR, word, f"{word}_{i}.wav")
        wav.write(filepath, RATE, audio_data)
        time.sleep(0.5)

print("\nAll data collected successfully!")
