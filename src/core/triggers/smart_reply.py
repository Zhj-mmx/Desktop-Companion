# ===================== 1. 导入工具库 =====================
from datetime import datetime, timedelta   # 用来处理时间，比如记录“上次说话是几点”和“间隔了多久”
from typing import Optional, Dict          # 类型标注，让代码更清晰
from src.utils.llm_client import LLMClient # 导入我们自己写的“AI 大脑”模块
from src.utils.dialogue_manager import DialogueManager # 导入“对话库管理器”（备用话语）
from config import settings                # 导入项目设置（本章实际没用到，但留着方便以后扩展）
import random                              # 用来摇色子，随机生成冷却时间

class SmartReplyManager:
    """
    Dreami 的“说话策略师”。
    它来决定：现在能不能说话？说什么话？（是请求 AI，还是从本地对话库里抽一句？）
    """

    def __init__(self, llm_client: LLMClient, dialogue_manager: DialogueManager):
        """
        初始化方法，传入两个必须的工具：
        - llm_client: 那个能跟 DeepSeek 聊天的大脑
        - dialogue_manager: 本地备用话语库（当网络差或冷却期时救急用）
        """
        self.llm_client = llm_client           # 存下 AI 对话客户端
        self.dialogue_manager = dialogue_manager  # 存下本地对话库管理器

        # 冷却字典：记录每种标签上次成功调用 AI 的时间
        # 比如 self.cooldown_dict["morning"] = 2024-05-11 09:00:00
        self.cooldown_dict: Dict[str, datetime] = {}

        # 随机生成一个冷却秒数（120~180秒之间），避免老是固定间隔
        # 这样 Dreami 说话就像真人，有时候话密有时候话稀
        self.cooldown_seconds = random.randint(120, 180)

    def get_reply(self, tag: str, is_focus_mode: bool, context: Optional[Dict] = None) -> Optional[str]:
        """
        获取一条回复的核心方法。
        参数：
            tag: 触发标签，比如 "morning", "coding", "anime"
            is_focus_mode: 专注模式开关（True 表示不能说话）
            context: 可选的环境信息（暂时没用上）
        返回：
            如果应该说话，返回一个字符串句子；如果该闭嘴，返回 None。
        """

        # ---------- 第一关：专注模式 ----------
        if is_focus_mode:
            # 如果主人正在专注工作，Dreami 什么都不说，安静得像只小布偶
            return None

        # ---------- 第二关：AI 冷却检查 ----------
        last_call_time = self.cooldown_dict.get(tag)
        # 如果之前这个标签调用过 AI，并且距离现在还没过冷却时间
        if last_call_time and datetime.now() - last_call_time < timedelta(seconds=self.cooldown_seconds):
            # 冷却还没结束，不能频繁打扰 AI，从本地对话库里随便拿一句类似的话
            return self.dialogue_manager.get_random(tag)

        # ---------- 第三关：尝试调用 AI ----------
        reply = self.llm_client.generate(tag, context)
        if reply:
            # AI 成功返回了一句漂亮话
            # 更新冷却时间：记录下当下时间，等下次再想用同一个标签，就要等足冷却秒数
            self.cooldown_dict[tag] = datetime.now()
            return reply

        # ---------- 第四关：AI 失败或超时 ----------
        # 如果 AI 请求失败（比如网络断了），退回安全方案，从本地对话库拿话
        return self.dialogue_manager.get_random(tag)