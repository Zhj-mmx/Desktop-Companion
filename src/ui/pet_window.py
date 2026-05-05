import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QAction, QMenu
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap
from .bubble import Bubble

class PetWindow(QWidget):
    """
    桌面宠物窗口：透明背景、置顶、无边框，显示角色图片。
    """
    def __init__(self, image_path: str, width: int = 200, height: int = 200):
        super().__init__()

        # ---------- 1. 窗口基本设置 ----------
        self.setWindowTitle("Dreami")               # 标题（虽然看不到）
        self.setFixedSize(width, height)            # 固定窗口大小

        # ---------- 2. 透明背景与无边框 ----------
        self.setAttribute(Qt.WA_TranslucentBackground)  # 背景全透明
        self.setWindowFlags(
            Qt.FramelessWindowHint           # 无边框
            | Qt.WindowStaysOnTopHint        # 置顶（始终在最前）
            | Qt.Tool                        # 不显示在任务栏上（可选）
        )

        # ---------- 3. 角色图片显示 ----------
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, width, height)   # 图片铺满整个窗口
        self.pixmap = QPixmap(r"assets\expressions\MikuQ.jpg")
        self.label.setPixmap(self.pixmap.scaled(
            width, height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))
        self.label.setStyleSheet("background: transparent;")  # 标签也透明

        # ---------- 4. 定位到桌面右下角 ----------
        self.move_to_bottom_right()

        # ---------- 5.加一个右键菜单 ----------
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        # ---------- 6. 其他可能用到的变量 ----------
        self.dragging = False       # 鼠标拖拽移动（第一步可不做）
        self.offset = QPoint()
        self.bubble = None          # 对话气泡实例

        

    def move_to_bottom_right(self):
        """将窗口移动到主屏幕右下角（留一点边距）"""
        screen = QApplication.primaryScreen().availableGeometry()
        # availableGeometry 考虑了任务栏高度，不会挡住任务栏
        x = screen.width() - self.width() - 20    # 右边距 20 像素
        y = screen.height() - self.height() - 20  # 底边距 20 像素
        self.move(x, y)

    def show_context_menu(self, pos):
        """右键菜单"""
        menu = QMenu(self)
        exit_action = QAction("退出 Dreami", self)
        exit_action.triggered.connect(QApplication.quit)
        menu.addAction(exit_action)
        menu.exec_(self.mapToGlobal(pos))

    def show_bubble(self, text, duration=3000):
        """显示对话气泡"""
        if not self.bubble:
            self.bubble = Bubble(QLabel(self))  # 父组件是宠物窗口
            self.bubble.move(self.width() - self.bubble.width() - 10, -self.bubble.height() - 10)
        self.bubble.show_message(text, duration)


# 下面几行只在直接运行本文件时做测试用，平时由 main.py 调用
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PetWindow(r"D:\Dreami\assets\expressions\MikuQ.jpg")
    window.show()
    sys.exit(app.exec_())