import os
from dotenv import load_dotenv

load_dotenv()  # 自动寻找项目根目录下的 .env 文件

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
LLM_TIMEOUT = 25
LLM_COOLDOWN_SECONDS = 150  # 修改为150秒（2.5分钟）
LLM_MODEL = "deepseek-v4-pro"