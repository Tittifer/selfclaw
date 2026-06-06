from selfclaw.skills import help_skill, run_skill, time_skill


def test_help_skill():
    reply = help_skill("help")

    assert reply == "可用技能：time / 时间"


def test_time_skill_with_english():
    reply = time_skill("time")

    assert reply is not None
    assert reply.startswith("当前时间是 ")


def test_time_skill_with_chinese():
    reply = time_skill("时间")

    assert reply is not None
    assert reply.startswith("当前时间是 ")


def test_run_skill_returns_none_for_unknown_input():
    reply = run_skill("hello")

    assert reply is None