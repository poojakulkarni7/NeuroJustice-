from datetime import datetime

def now_string():
    return datetime.now().strftime("%d-%m-%Y %I:%M %p")