import os
import json

TOKEN = os.environ["TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])
ADMIN_ID = int(os.environ["ADMIN_ID"])
SHEET_ID = os.environ["GOOGLE_SHEET_ID"]

REFERRALS_FOR_BONUS_1 = 2
REFERRALS_FOR_BONUS_2 = 5

LINKS = {
    "link_1": (os.environ["LINK_1"], "📊 Инструменты для анализа игр"),
    "link_2": (os.environ["LINK_2"], "Пример карточки проекта"),
    "link_3": (os.environ["LINK_3"], "Пример отличного туториала"),
    "link_4": (os.environ["LINK_4"], "Статьи на Teletype"),
}

BONUS_LINKS = {
    1: os.environ["BONUS_LINK"],
    2: os.environ["BONUS_LINK_2"],
}

GOOGLE_CREDENTIALS = json.loads(os.environ["GOOGLE_CREDENTIALS"])
