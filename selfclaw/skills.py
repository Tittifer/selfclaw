from datetime import datetime


def get_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def time_skill(user_text):
    if "time" in user_text or "时间" in user_text:
        return f"当前时间是 {get_time()}"

    return None


def help_skill(user_text):
    if user_text in ["help", "帮助"]:
        return "可用技能：time / 时间"

    return None


SKILLS = [
    help_skill,
    time_skill,
]


def run_skill(user_text):
    for skill in SKILLS:
        reply = skill(user_text)

        if reply is not None:
            return reply

    return None