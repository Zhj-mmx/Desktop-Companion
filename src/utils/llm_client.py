# ======================== 1. 导入工具 ========================
import logging
from typing import Optional, Dict, Union
from openai import OpenAI                     # 注意：现在只用 OpenAI 官方库，不需要 requests
from config import settings                   # 读取配置中的 API 密钥等
from src.utils.personality import PERSONALITY_PROMPTS
# ======================== 2. 创建 DeepSeek 客户端 ========================
# 这就好比给 Dreami 办了一张“AI 通讯卡”，以后发消息都通过这张卡。
client = OpenAI(
    api_key=settings.DEEPSEEK_API_KEY,        # 你的专属密码（API 密钥）
    base_url="https://api.deepseek.com"       # DeepSeek 的服务器地址
)

# ======================== 3. 定义 LLMClient 类 ========================
#LLMClient:
##generate:根据一个“情境标签”，生成一句 AI 回复。
##_build_prompt:根据标签生成给 AI 的“用户消息”。目前很简单，直接返回标签，未来可以混入天气、时间之类的额外信息。
##_process_response:从 OpenAI 库的返回对象里，把 AI 真正说的那句话提取出来，并清理首尾空白。

class LLMClient:
    """
    Dreami 的“语言中枢”。
    当你给它一个标签（比如 "morning"），它会去问 DeepSeek，
    然后带回来一句贴合 Dreami 性格的回复。
    """
    def __init__(self, model: str = "deepseek-chat", personality_prompt: Optional[Union[str, Dict]] = PERSONALITY_PROMPTS):
        """
        初始化——相当于给这个中枢装好“大脑版本”和“性格说明书”。
        参数:
            model: 要用哪个 DeepSeek 模型（默认为 deepseek-chat）。
            personality_prompt: 性格设定，告诉 AI 用什么样的语气说话。
        """
        self.model = model                     # 记住模型名称
        # 确保personality_prompt是字符串
        if isinstance(personality_prompt, dict):
            self.personality_prompt = personality_prompt.get("default", "")
        else:
            self.personality_prompt = personality_prompt or ""
        self.timeout = settings.LLM_TIMEOUT    # 最多等多长时间（秒）

    def generate(self, tag: str, context: Optional[Dict] = None) -> Optional[str]:
        """
        核心方法：根据一个“情境标签”，生成一句 AI 回复。
        例如:
            generate("morning") -> "早啊，窗帘拉开，阳光和你都醒了吗？"
        如果网络超时或其他原因失败，会安静地返回 None。
        """
        # 准备好要对 AI 说的话
        user_message = self._build_prompt(tag)   # 将标签转换成具体的问题内容

        try:
            # --- 这下面就是使用 OpenAI 库的“信封”寄信方式 ---
            response = client.chat.completions.create(
                model=self.model,                        # 使用之前记住的模型名称（不再是写死的）
                messages=[
                    {"role": "system", "content": self.personality_prompt},  # 设定 AI 的性格
                    {"role": "user",   "content": user_message}             # 真正要求它回复的内容
                ],
                max_tokens=30,                           # 限制回复长度，保持吐槽简短
                temperature=0.7,                         # 创意度：0.7 比较俏皮又不天马行空
                timeout=self.timeout,                    # 超时设定（OpenAI 库内置支持）
                stream=False                             # 不需要逐字蹦出，一次拿完整回复
            )

            # 从 AI 的回信里提取出文字内容
            return self._process_response(response)

        except Exception as e:
            # 任何意外（网络断了、超时、额度没了）都悄悄记下来，不搞崩程序
            logging.error(f"LLM请求失败: {e}")
            return None

    def _build_prompt(self, tag: str) -> str:
        """
        根据标签生成给 AI 的“用户消息”。
        目前很简单，直接返回标签，未来可以混入天气、时间之类的额外信息。
        """
        # 现在只是原样返回，但你可以在这里发挥想象力，比如：
        # return f"现在的情境是：{tag}，而且外面的天气是{context['weather']}"
        return f"现在的情境是：{tag}"

    def _process_response(self, response) -> str:
        """
        从 OpenAI 库的返回对象里，把 AI 真正说的那句话提取出来，并清理首尾空白。
        """
        # response.choices[0] 是 AI 给出的第一个（也是唯一一个）候选回答
        # .message.content 就是回答的文本，比如 "下午好，该起来活动活动啦~"
        return response.choices[0].message.content.strip()
    

