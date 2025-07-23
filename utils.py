import datetime

def format_duration(time_diff):
    # return str(datetime.timedelta(seconds=time_diff))  # 精确的位数太多，不美观
    hours, rem = divmod(time_diff, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{seconds:05.2f}"

def get_choice(valid_options, txt):
    while True:
        choice = input(txt).strip().upper()
        if choice not in valid_options:
            print(f"Invalid input. Valid options: {', '.join(valid_options)}. Please re-enter.")
        else:
            return choice

