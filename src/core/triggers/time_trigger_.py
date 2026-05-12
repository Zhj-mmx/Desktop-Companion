from datetime import datetime, timedelta

class TimeTrigger:
    def __init__(self):
        self.last_trigger_time = None

    def check(self):
        now = datetime.now()
        if self.last_trigger_time is None or (now - self.last_trigger_time) >= timedelta(minutes=2):
            self.last_trigger_time = now
            return "time_trigger"
        return None
