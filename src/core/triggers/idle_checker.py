import ctypes
from ctypes import wintypes

class IdleTrigger:
    def __init__(self, idle_time=5, speak_welcome=True):
        """
        idle_time: 多少秒无操作就算“挂机”
        speak_welcome: 挂机后再次操作是否说欢迎回来
        """
        self.idle_time = idle_time
        self.speak_welcome = speak_welcome
        self.was_idle = False  # 上一秒是否处于挂机状态

    def _get_idle_seconds(self):
        """调用 Windows API 获取空闲时间（秒）"""
        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [('cbSize', wintypes.UINT),
                        ('dwTime', wintypes.DWORD)]
        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
        if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
            millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
            return millis / 1000.0
        return 0

    def check(self):
        """返回挂机/回来相关的话"""
        idle_sec = self._get_idle_seconds()
        if idle_sec > self.idle_time:
            if not self.was_idle:
                self.was_idle = True
                return f'挂机时间:{idle_sec}'
        else:
            if self.was_idle and self.speak_welcome:
                self.was_idle = False
                return '挂机回来'
            self.was_idle = False
        return None