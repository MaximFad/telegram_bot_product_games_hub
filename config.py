import os
import json


def get_env(name: str, default=None, required: bool = True):
    value = os.environ.get(name, default)
    if required and (value is None or value == ""):
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


TOKEN = get_env("TOKEN")
CHANNEL_ID = int(get_env("CHANNEL_ID"))
ADMIN_ID = int(get_env("ADMIN_ID"))
SHEET_ID = get_env("GOOGLE_SHEET_ID")

REFERRALS_FOR_BONUS_1 = int(get_env("REFERRALS_FOR_BONUS_1", 2, required=False))
REFERRALS_FOR_BONUS_2 = int(get_env("REFERRALS_FOR_BONUS_2", 5, required=False))

LINKS = {
    "link_1": (get_env("LINK_1"), "📊 Инструменты для анализа игр"),
    "link_2": (get_env("LINK_2"), "📄 Пример карточки проекта"),
    "link_3": (get_env("LINK_3"), "🎓 Пример отличного туториала"),
    "link_4": (get_env("LINK_4"), "📝 Статьи на Teletype"),
    "link_5": (get_env("LINK_5"), "🎭 Ролевая модель игры"),
}

BONUS_LINKS = {
    1: get_env("BONUS_LINK"),
    2: get_env("BONUS_LINK_2"),
}

try:
    GOOGLE_CREDENTIALS = json.loads(get_env("GOOGLE_CREDENTIALS"))
except json.JSONDecodeError as e:
    raise RuntimeError(f"GOOGLE_CREDENTIALS invalid JSON: {e}")

DISCUSSION_GROUP_ID = int(get_env("DISCUSSION_GROUP_ID", 0, required=False))
