import time
import sys
from PyQt5.QtWidgets import QApplication
from src.core.triggers.idle_trigger import IdleTrigger
from src.core.triggers.window_trigger import WindowTrigger
from src.core.triggers.time_trigger import TimeTrigger
from src.ui.pet_window import PetWindow

def main():
    app = QApplication(sys.argv)

    pet_window = PetWindow(r"D:\Dreami\assets\expressions\MikuQ.jpg")
    pet_window.show()

    sys.exit(app.exec_())
    
    # 1. 创建三个小侦探
    t_trigger = TimeTrigger()
    w_trigger = WindowTrigger()
    i_trigger = IdleTrigger(idle_time=5)  # 为了方便测试，先设5秒不动就挂机

    print("Dreami 启动！(Ctrl+C 退出，试试5秒不动键盘鼠标)")

    # 2. 主循环
    while True:
        # 每隔1秒问一遍
        msg = t_trigger.check()
        if msg:
            print("[时间]", msg)

        msg = w_trigger.check()
        if msg:
            print("[窗口]", msg)

        msg = i_trigger.check()
        if msg:
            print("[空闲]", msg)

        time.sleep(1)

if __name__ == "__main__":
    main()