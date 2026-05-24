"""
Dreami 桌面宠物主程序

功能：
1. 集成时间触发和空闲触发模块
2. 显示宠物角色和对话气泡
3. 使用 QTimer 实现定期状态检查
"""
# 上面是文件的说明（文档字符串），不会影响程序运行，只是给人看的。

# ===================== 1. 导入库 =====================
import os                       # 用于处理文件路径和切换工作目录
import sys                      # 用于退出程序（比如导入失败时直接结束）         

# ---------- 尝试导入 PyQt5 和我们自己写的各个模块 ----------
    # PyQt5 是制作窗口界面的工具库
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QTimer, Qt          # QTimer 是定时器，Qt 包含一些常量
from src.ui.bubble import Bubble             # 对话气泡组件（显示文字的泡泡）
from src.core.triggers.time_checker import TimeTrigger      # 时间触发器（比如早上、中午）
from src.core.triggers.idle_checker import IdleTrigger      # 空闲触发器（检测键盘鼠标多久没动）
from src.core.triggers.window_checker import WindowTrigger  # 窗口触发器（检测当前是什么软件）
from src.core.triggers.smart_reply import SmartReplyManager # 智能回复管理器（综合 AI 和对话库）
from src.ui.pet_window import PetWindow                     # 宠物窗口基类（透明无边框窗口）
from PyQt5.QtGui import QPixmap              # 用于处理图片


# ===================== 2. 定义主窗口类 DreamiWindow =====================
class DreamiWindow(PetWindow):
    """
    这是宠物窗口的“增强版”，继承了 PetWindow 的透明背景、置顶等基础功能，
    然后加上了对话气泡、各种触发器和定时检查逻辑。
    """
    def __init__(self):
        # 先调用父类（PetWindow）的初始化，并传入角色图片的路径
        super().__init__("assets/expressions/MikuQ.jpg")

        # ----- 初始化气泡 -----
        # Bubble 是一个能显示文字的泡泡小组件，需要指定父窗口（self 就是 DreamiWindow）
        self.bubble = Bubble(self)
        # 把气泡移动到窗口右上角的位置（相对宠物窗口的坐标）
        self.bubble.move(self.width() - self.bubble.width() - 20, 20)

        # ----- 初始化触发器（三个检测来源）-----
        self.time_trigger = TimeTrigger()    # 检测时间，返回如 "morning", "afternoon" 等
        self.idle_trigger = IdleTrigger()    # 检测用户多久没动，返回如 "idle_10min"
        self.window_trigger = WindowTrigger() # 检测当前窗口标题，返回如 "coding", "anime"

        # ----- 初始化智能回复管理器（支持 AI 生成回复）-----
        from src.utils.llm_client import LLMClient                   # AI 客户端（连接 DeepSeek）  

        # 创建 AI 客户端，指定模型和性格
        self.llm_client = LLMClient(model="deepseek-chat")

        self.smart_reply_manager = SmartReplyManager(self.llm_client) # 智能回复管理器，负责根据触发器状态决定说什么话
    
        # ----- 设置定时器，定期检查触发器状态 -----
        self.timer = QTimer(self)                     # 创建一个定时器
        self.timer.timeout.connect(self.check_triggers) # 每次定时器到时间，就调用 check_triggers 方法
        self.timer.start(10000)                        # 启动定时器，每隔 10000 毫秒（10秒）触发一次

    def check_triggers(self):
        """
        这个方法每秒执行一次，它会：
        拿到了回复，就让气泡显示出来
        """
        llm_text = self.smart_reply_manager.get_reply("default")  # 使用智能回复管理器生成回复
        print(f"[Dreami]: {llm_text}")
        self.bubble.show_message(llm_text)  # 显示 AI 生成的回复




# ===================== 3. 程序入口 main 函数 =====================
def main():
    # 创建一个 QApplication 对象，这是 PyQt5 程序的基础，所有窗口都要依附它
    app = QApplication(sys.argv)

    # 把当前工作目录切换到 main.py 所在的文件夹（项目根目录），确保后续路径正确
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 创建我们的宠物窗口对象
    window = DreamiWindow()
    window.resize(200, 200)  # 设置窗口大小为宽200高200像素
    window.show()            # 让窗口显示出来

    window.check_triggers

    window.raise_()  # 把窗口提升到所有窗口的最上层（确保能看到）

    # 进入 PyQt5 的事件循环，程序会一直运行直到用户关闭窗口或退出
    sys.exit(app.exec_())

    
# 如果当前文件是被直接运行的（而不是被导入到其他地方），就执行 main()
if __name__ == "__main__":
    main()