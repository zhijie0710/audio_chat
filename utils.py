from dotenv import load_dotenv
import os

def load_hf_token(env_path: str):
    """加载 Hugging Face API Token"""
    load_dotenv(env_path, override=True)
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        raise ValueError("HF_TOKEN 未在 .env 文件中找到")
    return hf_token