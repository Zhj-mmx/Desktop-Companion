# 导入类型提示工具，让代码能标注变量的类型（比如字典、列表），不写也能运行，但写了更容易理解
from typing import Dict, List, Optional
import random  # 随机模块，用来从对话列表里随机抽一句

class DialogueManager:
    """
    对话管理器：存放所有备选对话，并根据标签随机返回一句。
    就像一个小句子仓库，你给一个标签（比如 "morning"），它从对应的货架上随便拿一句给你。
    """

    def __init__(self):
        """
        初始化方法：创建对象时自动执行。
        准备一个空的大仓库 self.dialogues，它是一个字典：
            - 键（key）是标签，比如 "morning", "coding", "rain"
            - 值（value）是对应的句子列表，比如 ["早上好！", "新的一天开始了！"]
        一开始仓库是空的，需要用 add_dialogue 往里面加句子。
        """
        self.dialogues: Dict[str, List[str]] = {}  # 字典：{ 标签: [句子1, 句子2, ...] }

    def add_dialogue(self, tag: str, dialogue: str):
        """
        往仓库里添加一句对话。
        参数：
            tag: 标签，比如 "morning"，表示这句对话属于哪种场景
            dialogue: 具体的句子，比如 "今天也要元气满满哦！"

        用法举例：
            manager.add_dialogue("morning", "早啊！")
            manager.add_dialogue("morning", "又是阳光灿烂的一天~")
        这样 "morning" 这个标签下就有两句备选了。
        """
        # 如果标签不存在，就先创建一个空列表来放句子
        if tag not in self.dialogues:
            self.dialogues[tag] = []
        # 把新句子添加到对应标签的列表末尾
        self.dialogues[tag].append(dialogue)

    def get_random(self, tag: str) -> Optional[str]:
        """
        根据标签随机抽取一句对话。
        参数：
            tag: 标签，比如 "morning"
        返回值：
            如果该标签下有句子，随机返回一句（字符串）；
            如果该标签不存在或列表为空，返回 None（表示没有可用的对话）。

        内部原理：
            使用 random.choice() 从列表中随机选一个元素，就像从袋子里抽纸条。
        """
        # 如果仓库里没有这个标签，或者标签对应的列表是空的，返回 None
        if tag not in self.dialogues or not self.dialogues[tag]:
            return None
        # 否则，从该标签的句子列表中随机挑一个返回
        return random.choice(self.dialogues[tag])