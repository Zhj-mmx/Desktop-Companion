# ===================== 1. 导入工具库 =====================
from datetime import datetime, timedelta   # 用来处理时间，比如记录“上次说话是几点”和“间隔了多久”
from typing import Optional, Dict          # 类型标注，让代码更清晰
from src.utils.llm_client import LLMClient # 导入我们自己写的“AI 大脑”模块
from config import settings                # 导入项目设置（本章实际没用到，但留着方便以后扩展）
import random                              # 用来摇色子，随机生成冷却时间

class SmartReplyManager:
    """
    Dreami 的“说话策略师”。
    它来决定：现在能不能说话？说什么话？（是请求 AI，还是从本地对话库里抽一句？）
    """

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client           # 存下 AI 对话客户端
        # 冷却字典：记录每种标签上次成功调用 AI 的时间
        self.cooldown_dict: Dict[str, datetime] = {}
        # 随机生成一个冷却秒数（120~180秒之间），避免老是固定间隔
        self.cooldown_seconds = random.randint(15, 60)

    def get_reply(self, tag: str) -> Optional[str]:
        """
        获取一条回复的核心方法。
        返回：
            如果应该说话，返回一个字符串句子；如果该闭嘴，返回 None。
        """
        last_call_time = 0
        if last_call_time and datetime.now() - last_call_time < timedelta(seconds=self.cooldown_seconds):
            # 冷却还没结束，暂时不说话
            return None

        reply = self.llm_client.generate()
        if reply:
            last_call_time = datetime.now()
            return reply
        # 请求失败（比如网络断了），暂时不说话
        return None
