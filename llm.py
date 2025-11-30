from huggingface_hub import InferenceClient

class HuggingFaceLLM:
    """
    调用 Hugging Face API 的 LLM
    """
    def __init__(self, model_name="openai/gpt-oss-120b", temperature=0):
        self.client = InferenceClient(model_name)
        self.temperature = temperature

    def generate(self, prompt: str) -> str:
        """
        根据输入文字生成回复
        """
        chat = self.client.chat  # 获取聊天接口
        response = chat.send_message(prompt)  # 发送用户输入
        return getattr(response, "generated_text", "(未生成内容)")