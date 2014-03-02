from datetime import datetime

def convert_date_string(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()
