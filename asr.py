import whisper
import numpy as np


WHISPER_SAMPLE_RATE = 16000  # Whisper 固定采样率

class WhisperASR:
    """
    Whisper ASR 封装
    """
    def __init__(self, model_name="tiny"):
        print(f"🎧 加载 Whisper {model_name} 模型...")
        self.model = whisper.load_model(model_name)
        print("✅ Whisper 模型加载完成")

    def transcribe(self, audio: np.ndarray) -> str:
        """
        将音频数组转文字
        """
        # 保证音频长度至少为 16k
        audio = np.pad(audio, (0, max(0, WHISPER_SAMPLE_RATE - len(audio))))
        audio = whisper.pad_or_trim(audio)
        result = self.model.transcribe(audio, fp16=False)
        return result["text"].strip() or "(未识别到内容)"