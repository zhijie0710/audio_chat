import torch
from pathlib import Path
import numpy as np

class SileroVAD:
    """封装 Silero VAD"""
    def __init__(self, model_path="vad.pt", sample_rate=16000):
        self.sample_rate = sample_rate
        vad_model_path = Path(model_path)
        if not vad_model_path.exists():
            raise FileNotFoundError(f"{model_path} 未找到，请先下载")
        self.model = torch.jit.load(vad_model_path)
        self.model.eval()
        # Silero VAD 要求固定长度
        self.chunk_size = 512 if sample_rate == 16000 else 256

    def is_speech(self, audio_chunk: np.ndarray) -> bool:
        """判断音频块是否有人说话"""
        if len(audio_chunk) < self.chunk_size:
            audio_chunk = np.pad(audio_chunk, (0, self.chunk_size - len(audio_chunk)))
        else:
            audio_chunk = audio_chunk[:self.chunk_size]
        audio_tensor = torch.from_numpy(audio_chunk.flatten()).float()
        with torch.no_grad():
            return self.model(audio_tensor, self.sample_rate).item() > 0.5