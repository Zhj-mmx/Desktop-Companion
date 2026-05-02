import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap


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
        self.pixmap = QPixmap("assets\expressions\MikuQ.jpg")
        self.label.setPixmap(self.pixmap.scaled(
            width, height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))
        self.label.setStyleSheet("background: transparent;")  # 标签也透明

        # ---------- 4. 定位到桌面右下角 ----------
        self.move_to_bottom_right()

        # ---------- 5. 其他可能用到的变量 ----------
        self.dragging = False       # 鼠标拖拽移动（第一步可不做）
        self.offset = QPoint()

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
        exit_action.triggered.connect(self.close)
        menu.addAction(exit_action)
        menu.exec_(self.mapToGlobal(pos))


# 下面几行只在直接运行本文件时做测试用，平时由 main.py 调用
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 请换成你自己的图片路径
    window = PetWindow("D:\Dreami\assets\expressions\MikuQ.jpg")
    window.show()
    sys.exit(app.exec_())