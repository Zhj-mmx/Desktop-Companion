"""
Dreami 桌面宠物主程序

功能：
1. 集成时间触发和空闲触发模块
2. 显示宠物角色和对话气泡
3. 使用 QTimer 实现定期状态检查
"""
import os
import sys
try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
    from PyQt5.QtCore import QTimer, Qt
    from src.ui.bubble import Bubble
    from src.core.triggers.time_trigger import TimeTrigger
    from src.core.triggers.idle_trigger import IdleTrigger
    from src.core.triggers.window_trigger import WindowTrigger
    from src.ui.pet_window import PetWindow
    from PyQt5.QtGui import QPixmap
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保已安装 PyQt5 并检查模块路径")
    sys.exit(1)

class DreamiWindow(PetWindow):
    def __init__(self):
        super().__init__("assets/expressions/MikuQ.jpg")
        
        # 初始化气泡
        self.bubble = Bubble(self)
        self.bubble.move(self.width() - self.bubble.width() -20, 20)  # 修正Y坐标为正值
        
        # 初始化触发器
        self.time_trigger = TimeTrigger()
        self.idle_trigger = IdleTrigger()
        self.window_trigger = WindowTrigger()
        
        # 定时器设置 (每秒检查一次触发器)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_triggers)
        self.timer.start(1000)  # 1秒间隔
        
    def check_triggers(self):
        """检查所有触发器状态并更新对话"""
        # 检查时间触发
        time_text = self.time_trigger.check()
        if time_text:
            print(f"[DEBUG] 时间触发: {time_text}")  # 添加调试输出
            self.bubble.show_message(time_text)
            
        # 检查空闲触发
        idle_text = self.idle_trigger.check()
        if idle_text:
            print(f"[DEBUG] 空闲触发: {idle_text}")  # 添加调试输出
            self.bubble.show_message(idle_text)

        # 检查窗口触发
        window_text = self.window_trigger.check()
        if window_text:
            print(f"[DEBUG] 窗口触发: {window_text}")  # 添加调试输出
            self.bubble.show_message(window_text)

def main():
    app = QApplication(sys.argv)
    
    # 设置工作目录为项目根目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    window = DreamiWindow()
    window.resize(200, 200)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()