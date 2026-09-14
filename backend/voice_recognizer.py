import speech_recognition as sr
import threading
import time

class VoiceRecognizer:
    def __init__(self, callback=None):
        self.recognizer = sr.Recognizer()
        # Improve responsiveness
        self.recognizer.pause_threshold = 0.5 
        self.recognizer.non_speaking_duration = 0.3
        self.recognizer.dynamic_energy_threshold = True
        
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.callback = callback
        
        with self.microphone as source:
            print("Calibrating background noise... please wait.")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Calibration complete.")

    def start_listening(self):
        self.is_listening = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()

    def stop_listening(self):
        self.is_listening = False

    def _listen_loop(self):
        print("Voice Recognizer started listening...")
        while self.is_listening:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
                try:
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"Heard: '{text}'")
                    self._process_command(text)
                except sr.UnknownValueError:
                    # Ignore unintelligible speech silently
                    pass
                except sr.RequestError as e:
                    print(f"API Error (Google Speech): {e}")
                    
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                print(f"Voice recognition error: {e}")
                time.sleep(1)

    def _process_command(self, text):
        command = None
        if any(word in text for word in ["rotate", "spin", "turn", "start"]):
            command = "ROTATE"
        elif any(word in text for word in ["zoom", "closer", "bigger"]):
            command = "ZOOM"
        elif any(word in text for word in ["next", "change", "switch", "another"]):
            command = "NEXT_OBJECT"
        elif any(word in text for word in ["stop", "halt", "pause", "wait"]):
            command = "STOP"
            
        if command and self.callback:
            print(f"Executing Voice Command: {command}")
            self.callback({"type": "VOICE", "command": command, "raw_text": text})

if __name__ == "__main__":
    def on_voice(data):
        print(f"Callback received: {data}")
        
    vr = VoiceRecognizer(callback=on_voice)
    vr.start_listening()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        vr.stop_listening()
