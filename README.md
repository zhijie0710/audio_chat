# Description
# 实时语音助手 (Audio Chat Assistant)

基于 **Silero VAD + Whisper ASR + Hugging Face LLM + pyttsx3 TTS** 的实时语音助手项目，可在本地终端运行，实现实时语音交互，并支持打断功能。

---

## 功能特点

- 🎙 **实时语音识别**：使用 Silero VAD 检测用户讲话，Whisper ASR 将语音转文字  
- 🤖 **智能对话生成**：调用 Hugging Face LLM API 生成自然语言回复  
- 🔊 **文字转语音**：pyttsx3 TTS 播报 LLM 回复  
- ✋ **打断功能**：在用户再次说话时自动停止正在播放的 TTS  
- 🌐 **全局可用**：支持在任意终端运行  
- 💡 **低延迟交互**：VAD + 队列 + Whisper tiny 模型实现快速响应  

---

## 目录结构
```python
audio_chat/
├─ main.py # 程序入口
├─ llm.py # Hugging Face LLM 封装
├─ tts.py # pyttsx3 TTS 封装
├─ vad.py # Silero VAD 封装
├─ asr.py # Whisper ASR 封装
├─ utils.py # 辅助函数，如 hf.env 加载
├─ hf_1.env # 存放 Hugging Face API Token
├─ vad.pt # Silero VAD 模型文件
```
---

## 架构流程

```
语音输入（麦克风）
       ↓
VAD (Silero) → 判断说话段
       ↓
ASR (Whisper) → 转文字
       ↓
LLM（HF API）→ 生成文本回复
       ↓
TTS (pyttsx3) → 播放语音
```

## 安装依赖

建议使用 **Python 虚拟环境**：

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS / Linux
# venv\Scripts\activate    # Windows

# 安装 Python 依赖
pip install sounddevice pyttsx3 torch numpy<2 openai-whisper python-dotenv huggingface-hub
```

## 系统依赖
# FFmpeg（Whisper 需要处理音频）

macOS 全局安装：
```python 
brew install ffmpeg
```
或者下载静态二进制，放到 /usr/local/bin 并确保可执行权限：
```python
chmod +x /usr/local/bin/ffmpeg
ffmpeg -version  # 测试是否可用
```
## 配置 Hugging Face Token

1.在 Hugging Face创建账户并获取 API Token

2.创建 hf.env 文件，内容如下：
```python
HF_TOKEN=你的 Hugging Face API Token
```
3.项目中会通过 utils.py 自动加载该 Token。

## 使用方法

1.启动项目：
```python
python main.py
```

2.程序启动后：

🎤 开始讲话，VAD 会检测语音

⏹️ 说话结束后，ASR 识别语音并显示文字

🤖 LLM 根据识别文字生成回复

🔊 TTS 自动播报回复

✋ 如果你在 TTS 播报过程中再次讲话，TTS 会自动停止

## 注意事项

需要保证麦克风和扬声器可用

Silero VAD 模型 vad.pt 必须放在项目目录

Whisper 模型默认使用 tiny 以保证 CPU 下响应速度快

LLM 生成回复依赖 Hugging Face API，需联网


## 扩展与优化

可以更换 ASR 模型（如 Whisper large 或本地 whisper.cpp）

可更换 LLM 模型或本地部署大模型

可增加多线程处理，实现边说边识别边生成回复

可将 TTS 替换为更自然的 TTS 引擎（如 Coqui TTS、Edge TTS 等）



