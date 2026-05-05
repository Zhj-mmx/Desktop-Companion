"""
对话气泡组件
继承自 QLabel，实现文字提示框功能：
1. 可在宠物窗口上方显示
2. 3秒后自动淡出消失
"""
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen, QFont

class Bubble(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 气泡样式
        self.setStyleSheet("""
            background-color: rgba(255, 255, 255, 200);
            border-radius: 10px;
            padding: 8px;
            color: black;
        """)
        
        # 字体设置
        font = QFont()
        font.setPixelSize(16)
        self.setFont(font)
        
        # 初始化动画
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(500)  # 淡出时间500ms
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.finished.connect(self.hide)
        
    def show_message(self, text, duration=3000):
        """
        显示消息气泡
        :param text: 要显示的文字
        :param duration: 显示持续时间（毫秒）
        """
        self.setText(text)
        self.adjustSize()  # 自动调整大小
        self.show()
        
        # 设置淡出定时器
        QTimer.singleShot(duration, self.start_fade_out)
        
    def start_fade_out(self):
        """启动淡出动画"""
        self.fade_animation.start()