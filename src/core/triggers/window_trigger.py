import pygetwindow as gw

class WindowTrigger:
    def __init__(self):
        self.last_title = ''  # 上一次的窗口标题

    def check(self):
        """检测当前窗口，如果和上次不同且包含关键词，就返回一句话"""
        try:
            win = gw.getActiveWindow()
            title = win.title if win else ''
        except:
            title = ''  # 如果获取失败，就当没窗口

        if not title or title == self.last_title:
            return None  # 窗口没变，不重复说话

        self.last_title = title

        # 关键词判断（顺序重要，长关键词优先）
        if any(k in title for k in ['Visual Studio Code', 'VS Code', 'PyCharm', 'IntelliJ']):
            return '主人在写代码呀，要不要来杯咖啡？'
        elif 'bilibili' in title or 'YouTube' in title:
            return '主人又在看视频啦，Dreami 也想看！'
        elif '微信' in title or 'WeChat' in title or 'QQ' in title:
            return '在和朋友聊天吗？帮 Dreami 也发个表情～'
        elif 'Word' in title or 'Excel' in title or 'WPS' in title:
            return '认真办公中…Dreami 乖乖不打扰。'
        else:
            # 其他窗口就不说话，也可以返回一句通用的话
            return None