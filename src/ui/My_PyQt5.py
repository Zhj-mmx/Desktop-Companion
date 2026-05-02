import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QAction, QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

# 请将路径替换为你自己的 PNG 角色图路径（支持透明通道）
IMAGE_PATH = r"assets\expressions\MikuQ.jpg"

class PetWindow(QWidget):
    """桌面宠物主窗口"""
    def __init__(self):
        super().__init__()

        # 1. 设置无边框、置顶、工具窗口（不在任务栏显示）
        self.setWindowFlags(
            Qt.FramelessWindowHint        # 无边框
            | Qt.WindowStaysOnTopHint     # 窗口置顶
            | Qt.Tool                     # 不显示在任务栏
        )
        # 2. 设置窗口背景完全透明
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 3. 固定窗口大小
        self.setFixedSize(200, 200)

        # 4. 加载角色图片并显示在 QLabel 中
        self.label = QLabel(self)
        pixmap = QPixmap(IMAGE_PATH)
        if pixmap.isNull():
            # 如果图片加载失败，显示一个占位文字（实际开发中可替换为默认图）
            self.label.setText("🐱 图片未找到")
            self.label.setAlignment(Qt.AlignCenter)
            self.label.setStyleSheet("color: white; font-size: 20px;")
        else:
            # 缩放图片以适应窗口，保持平滑变换和透明通道
            pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(pixmap)
            self.label.setStyleSheet("background: transparent;")  # 标签背景透明
        self.label.setGeometry(0, 0, 200, 200)  # 铺满整个窗口

        # 5. 将窗口移动到屏幕右下角（不被任务栏遮挡）
        self.move_to_bottom_right()

        # 6. 添加右键菜单（退出功能）
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def move_to_bottom_right(self):
        """将窗口定位到屏幕可用区域的右下角"""
        # 获取主屏幕对象
        screen = QApplication.primaryScreen()
        # 获取可用桌面区域（排除任务栏等占用的空间）
        available_geometry = screen.availableGeometry()
        screen_width = available_geometry.width()
        screen_height = available_geometry.height()
        # 计算窗口左上角坐标
        x = screen_width - self.width()
        y = screen_height - self.height()
        self.move(x, y)

    def show_context_menu(self, pos):
        """右键菜单"""
        menu = QMenu(self)
        exit_action = QAction("退出 Dreami", self)
        exit_action.triggered.connect(self.close)
        menu.addAction(exit_action)
        menu.exec_(self.mapToGlobal(pos))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 不显示主窗口的默认任务栏图标（因为我们已经用了 Qt.Tool）
    app.setQuitOnLastWindowClosed(True)
    pet = PetWindow()
    pet.show()
    sys.exit(app.exec_())