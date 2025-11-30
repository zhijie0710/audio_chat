import pyttsx3
import threading

class TTS:
    """
    pyttsx3 TTS 封装，支持打断
    """
    def __init__(self, rate=150):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.lock = threading.Lock()
        self.stop_speaking = True

    def speak(self, text: str):
        """
        异步播放文字
        """
        def run():
            with self.lock:
                self.stop_speaking = False
                self.engine.say(text)
                self.engine.runAndWait()
                self.stop_speaking = True
        threading.Thread(target=run, daemon=True).start()

    def stop(self):
        """
        打断正在播放的语音
        """
        with self.lock:
            if not self.stop_speaking:
                self.engine.stop()
                self.stop_speaking = True