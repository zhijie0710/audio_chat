# main.py
import sounddevice as sd
import numpy as np
import queue
from utils import load_hf_token
from llm import HuggingFaceLLM
from tts import TTS
from vad import SileroVAD
from asr import WhisperASR

# -----------------------------
# 1️⃣ 加载 HF_TOKEN
# -----------------------------
hf_token = load_hf_token("/Users/zhijietang/Desktop/audio_chat/hf.env")

# -----------------------------
# 2️⃣ 初始化模块
# -----------------------------
llm = HuggingFaceLLM(model_name="openai/gpt-oss-120b", temperature=0)
tts = TTS(rate=150)
vad = SileroVAD("vad.pt", sample_rate=16000)
asr = WhisperASR("tiny")

# -----------------------------
# 3️⃣ 音频队列 & 参数
# -----------------------------
SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_SIZE = 512  # 对应 VAD.chunk_size
audio_queue = queue.Queue()

def audio_callback(indata, frames, time_info, status):
    """麦克风音频回调，把数据放入队列"""
    audio_queue.put(indata.copy())

# -----------------------------
# 4️⃣ 主循环
# -----------------------------
def main():
    buffer = np.zeros(0, dtype=np.float32)
    in_speech = False

    print("🎙️ 实时语音助手启动，请讲话... (说 '退出' 或 '再见' 退出)")


    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS,
                        blocksize=BLOCK_SIZE, callback=audio_callback):
        try:
            while True:
                try:
                    chunk = audio_queue.get(timeout=1)
                except queue.Empty:
                    continue

                chunk = chunk.flatten()
                buffer = np.concatenate((buffer, chunk))
                speech_flag = vad.is_speech(chunk)

                if speech_flag:
                    if not in_speech:
                        print("🗣️ 检测到说话")
                        tts.stop()  # 打断 TTS
                        in_speech = True
                else:
                    if in_speech:
                        print("⏹️ 说话结束，识别中...")
                        text = asr.transcribe(buffer.copy())
                        print("💬 识别:", text)

                        # 检查退出指令
                        if "退出" in text or "再见" in text:
                            print("👋 语音助手已退出")
                            break

                        reply = llm.generate(text)
                        print("🤖 回复:", reply)
                        tts.speak(reply)

                        buffer = np.zeros(0, dtype=np.float32)
                        in_speech = False
        except KeyboardInterrupt:
            print("\n👋 语音助手已通过 Ctrl+C 退出")

if __name__ == "__main__":
    main()