# import torch

# # 下载模型
# vad_model, utils = torch.hub.load('snakers4/silero-vad', 'silero_vad', force_reload=True)

# # 保存到本地文件
# torch.jit.save(vad_model, "vad.pt")
# print("✅ vad.pt 已保存到当前目录")

# import pyttsx3

# def test_tts():
#     engine = pyttsx3.init()  # 初始化 TTS 引擎
#     engine.setProperty('rate', 150)   # 语速，可调
#     engine.setProperty('volume', 1.0) # 音量 0.0~1.0

#     text = "你好，我是你的语音助手。"
#     print(f"💬 TTS 播报: {text}")
#     engine.say(text)  # 将文字加入播放队列
#     engine.runAndWait()  # 等待播放完成

# if __name__ == "__main__":
#     test_tts()



# import subprocess

# def speak(text: str):
#     """使用 macOS say 命令播放语音"""
#     subprocess.run(["say", text])

# if __name__ == "__main__":
#     speak("你好，我是你的语音助手。")

import pyttsx3

class TTS:
    def __init__(self):
        # 初始化 TTS 引擎，指定 macOS 驱动 'nsss'
        self.engine = pyttsx3.init(driverName='nsss')
        
        # 设置语速和音量
        self.engine.setProperty('rate', 150)    # 语速，100~200 之间
        self.engine.setProperty('volume', 1.0)  # 音量，0.0~1.0
        
        # 获取可用声音列表，选第一个可用声音（默认 macOS 英文语音）
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)

    def speak(self, text: str):
        """
        播放文字
        """
        if not text.strip():
            return  # 避免空字符串导致播放异常
        # say 加入播放队列
        self.engine.say(text)
        # 等待播放完成，确保不会无限循环
        self.engine.runAndWait()

# 测试
if __name__ == "__main__":
    tts = TTS()
    tts.speak("你好，我是你的语音助手。")

