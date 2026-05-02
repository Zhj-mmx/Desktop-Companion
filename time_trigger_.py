from datetime import datetime, time

class TimerTrigger:
    def __init__(self):
        self.last_trigger = {
            "morning": None,
            "noon": None,
            "night": None
        }

    def check(self):
        now = datetime.now()
        current_time = now.time()

        if time(6, 0) <= current_time <= time(9, 0):
            if self.last_trigger["morning"] != now.date():
                self.last_trigger["morning"] = now.date()
                return "time_morning" 
            
        if current_time >= time(23, 0) or current_time >= time(2, 0):
            if self.last_trigger["night"] != now.date():
                self.last_trigger["night"] = now.date()
                return "time_night"

            return None   