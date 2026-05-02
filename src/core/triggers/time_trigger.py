import datetime

class TimeTrigger:
    def __init__(self):
        self.last_period = None

    def _get_period(self):
        """根据当前小时，返回属于哪个时段"""
        hour = datetime.datetime.now().hour
        if 6 <= hour < 9:
            return '早上'
        elif 9 <= hour < 12:
            return '上午'
        elif 12 <= hour < 14:
            return '中午'
        elif 14 <= hour < 18:
            return '下午'
        elif 18 <= hour < 22:
            return '晚上'
        else:
            return '深夜'
        
    def check(self):
        """返回当前时段应说的话，时段没变化就返回 None"""
        period = self._get_period()
        if period != self.last_period:
            self.last_period = period
            # 不同时段的问候语
            greetings = {
                '早上': '主人早安～今天也是元气满满的一天！',
                '上午': '上午好呀，记得喝水哦。',
                '中午': '该吃午饭啦，Dreami 也想吃一口~',
                '下午': '下午好，再加把劲就下班啦！',
                '晚上': '晚上好，今天辛苦了～',
                '深夜': '这么晚了还不睡，Dreami 要陪你熬夜吗？'
            }
            return greetings.get(period, '')
        return None  # 时段没变，不说话