from config import REFERRALS_FOR_BONUS_1, REFERRALS_FOR_BONUS_2


# =========================================================
# ТЕКСТ ПЕРВОГО ПОКАЗА ДЛЯ НЕПОДПИСАННОГО ПОЛЬЗОВАТЕЛЯ
# Когда появляется:
# - пользователь впервые заходит в бота через /start
# - бот проверяет подписку и видит, что подписки нет
# =========================================================
FIRST_NOT_SUBSCRIBED_TEXT = (
    "Привет! Это Product Games Hub.\n"
    "Чтобы открыть доступ к материалам, подпишись на канал:"
)

# =========================================================
# ТЕКСТ ПОВТОРНОГО ПОКАЗА ДЛЯ НЕПОДПИСАННОГО ПОЛЬЗОВАТЕЛЯ
# Когда появляется:
# - пользователь нажал кнопку проверки подписки
# - но всё ещё не подписался
# - либо пытается открыть материалы/миссии без подписки
# =========================================================
REPEAT_NOT_SUBSCRIBED_TEXT = (
    "❌ Сначала подпишись на канал @{channel_username}, чтобы получить материалы.\n"
    "После подписки вернись в бота и нажми кнопку ещё раз."
)


class BotTexts:
    # =========================================================
    # НАЗВАНИЯ УРОВНЕЙ
    # Где используется:
    # - главное меню
    # - реферальная панель
    # - авто-сообщения о прогрессе
    # =========================================================
    LEVEL_1_NAME = "Джуниор разработчик"
    LEVEL_2_NAME = "Мастер геймдева"
    LEVEL_3_NAME = "Легенда геймдева"

    # =========================================================
    # КНОПКИ
    # Где используется:
    # - inline кнопки в меню
    # - кнопки под материалами
    # - кнопки в админке
    # =========================================================
    BTN_MATERIALS = "🗂 Открыть материалы"
    BTN_MY_REFS = "🎯 Миссии и бонусы"
    BTN_ADMIN = "🛠 Админ панель"
    BTN_SUBSCRIBE = "📡 Подписаться на канал"
    BTN_CHECK_SUBSCRIBE = "✅ Я подписался"
    BTN_SHARE = "🚀 Поделиться ссылкой"
    BTN_SHARE_WITH_FRIEND = "🎁 Отправить другу"
    BTN_BACK = "⬅️ Назад в меню"
    BTN_BROADCAST = "📣 Сделать рассылку"
    BTN_STATS = "🏆 Статистика"

    # =========================================================
    # НАЗВАНИЯ БОНУСОВ В СПИСКЕ МАТЕРИАЛОВ
    # Где используется:
    # - экран выбора материалов
    # =========================================================
    BONUS_1_MENU_TITLE = "🎁 Секретный бонус"
    BONUS_2_MENU_TITLE = "💎 Главный бонус"

    # =========================================================
    # ОБЩИЕ СЛУЖЕБНЫЕ ТЕКСТЫ
    # =========================================================
    TEXT_UNKNOWN_ACTION = "❌ Неизвестное действие."
    TEXT_MATERIAL_NOT_FOUND = "❌ Материал не найден."
    TEXT_CHECK_ERROR = "❌ Не удалось проверить подписку или открыть материал."

    # =========================================================
    # ГЛАВНОЕ МЕНЮ
    # Когда появляется:
    # - после /start, если пользователь подписан
    # - после кнопки "Я подписался", если подписка подтверждена
    # - после возврата в меню
    # =========================================================
    @classmethod
    def main_menu(cls, level_name: str, ref_link: str) -> str:
        return (
            "Привет! Это Product Games Hub.\n\n"
            f"🏅 Твой уровень: «{level_name}»\n"
            f"🎯 Миссия: дойти до «{cls.LEVEL_3_NAME}» и открыть все секретные материалы\n\n"
            f"🔗 Твоя ссылка:\n{ref_link}\n\n"
            "Выбери, с чего начать:"
        )

    # =========================================================
    # ЭКРАН МАТЕРИАЛОВ
    # Когда появляется:
    # - после нажатия на кнопку материалов
    # =========================================================
    @classmethod
    def materials_menu(cls) -> str:
        return "🗂 Материалы — выбери, что открыть:"

    # =========================================================
    # ОБЫЧНЫЙ МАТЕРИАЛ ОТКРЫТ
    # Когда появляется:
    # - пользователь подписан
    # - открыл обычный материал
    # =========================================================
    @classmethod
    def material_opened(
        cls,
        material_name: str,
        material_link: str,
        current_level: str,
        current_refs: int,
        ref_link: str,
    ) -> str:
        return (
            f"🗂 Материал открыт: {material_name}\n"
            f"{material_link}\n\n"
            "💎 Следующая цель — секретный бонус\n"
            f"👥 Пригласи {REFERRALS_FOR_BONUS_1} друзей по своей ссылке.\n"
            f"📈 Прогресс: {current_refs} из {REFERRALS_FOR_BONUS_1}\n\n"
            f"🔗 Твоя ссылка:\n{ref_link}"
        )

    # =========================================================
    # РЕФЕРАЛЬНАЯ ПАНЕЛЬ
    # Когда появляется:
    # - пользователь нажал "Мои реферальные ссылки"
    # =========================================================
    @classmethod
    def refs_panel(
        cls,
        current_level: str,
        current_refs: int,
        ref_link: str,
        next_level_name: str | None,
        next_level_target: int | None,
    ) -> str:
        text = (
            "🎯 Твой прогресс по приглашениям\n\n"
            f"🏅 Текущий уровень: {current_level}\n"
            f"👥 Приглашено друзей: {current_refs}\n\n"
            f"🔗 Твоя ссылка:\n{ref_link}\n\n"
        )

        if next_level_name and next_level_target:
            refs_left = max(next_level_target - current_refs, 0)
            text += (
                f"🎁 Следующая цель — уровень «{next_level_name}»\n"
                f"Пригласи ещё {refs_left} друзей, чтобы открыть новый бонус."
            )
        else:
            text += (
                f"🏆 Ты уже на максимальном уровне «{cls.LEVEL_3_NAME}».\n"
                "Ты открыл все основные бонусы."
            )

        return text

    # =========================================================
    # БОНУС ЗАКРЫТ
    # Когда появляется:
    # - нажали на бонус
    # - но не хватает приглашённых
    # =========================================================
    @classmethod
    def bonus_locked(cls, need_refs: int, current_refs: int) -> str:
        return (
            f"🔒 Бонус откроется после {need_refs} приглашённых.\n"
            f"Сейчас у тебя: {current_refs}."
        )

    # =========================================================
    # БОНУС 1 ОТКРЫТ
    # =========================================================
    @classmethod
    def bonus_1_opened(cls, link: str) -> str:
        return (
            "🎁 Секретный бонус открыт:\n"
            f"{link}"
        )

    # =========================================================
    # БОНУС 2 ОТКРЫТ
    # =========================================================
    @classmethod
    def bonus_2_opened(cls, link: str) -> str:
        return (
            "💎 Главный бонус открыт:\n"
            f"{link}"
        )

    # =========================================================
    # ПРОГРЕСС: ПОЛУЧЕН ПЕРВЫЙ РЕФЕРАЛ
    # Когда появляется:
    # - inviter получил первого приглашённого
    # =========================================================
    @classmethod
    def invite_progress_first(cls, ref_link: str, current_refs: int) -> str:
        left = max(REFERRALS_FOR_BONUS_1 - current_refs, 0)
        return (
            "🎉 Первый друг уже с тобой!\n\n"
            f"🏅 Текущий уровень: «{cls.LEVEL_1_NAME}»\n"
            f"👥 Приглашено друзей: {current_refs} из {REFERRALS_FOR_BONUS_1}\n\n"
            f"Осталось ещё {left}, чтобы открыть первый бонус.\n\n"
            f"🔗 Твоя ссылка:\n{ref_link}"
        )

    # =========================================================
    # ПРОГРЕСС: ОТКРЫТ ПЕРВЫЙ БОНУС
    # Когда появляется:
    # - inviter дошёл до первого порога
    # =========================================================
    @classmethod
    def invite_progress_bonus_1_unlocked(cls, ref_link: str, bonus_link: str) -> str:
        next_step_count = REFERRALS_FOR_BONUS_2 - REFERRALS_FOR_BONUS_1
        return (
            f"🎉 Уровень «{cls.LEVEL_1_NAME}» пройден!\n\n"
            "Вот твой первый бонус:\n"
            f"🎁 {bonus_link}\n\n"
            f"Следующая цель — «{cls.LEVEL_2_NAME}»\n"
            f"Пригласи ещё {next_step_count} друзей, чтобы открыть главный бонус.\n\n"
            f"🔗 Твоя ссылка:\n{ref_link}"
        )

    # =========================================================
    # ПРОГРЕСС: МЕЖДУ БОНУСОМ 1 И БОНУСОМ 2
    # =========================================================
    @classmethod
    def invite_progress_middle(
        cls,
        ref_link: str,
        progress_now: int,
        progress_total: int,
        refs_left: int,
    ) -> str:
        return (
            "🚀 Ещё один друг присоединился!\n\n"
            f"🏅 Текущий уровень: «{cls.LEVEL_2_NAME}»\n"
            f"📈 Прогресс: {progress_now} из {progress_total}\n"
            f"👥 Осталось пригласить: {refs_left}\n\n"
            f"🔗 Твоя ссылка:\n{ref_link}"
        )

    # =========================================================
    # ПРОГРЕСС: ОТКРЫТ ФИНАЛЬНЫЙ БОНУС
    # =========================================================
    @classmethod
    def invite_progress_final(cls, bonus_link: str) -> str:
        return (
            f"🏆 Уровень «{cls.LEVEL_2_NAME}» завершён!\n\n"
            f"Ты пригласил {REFERRALS_FOR_BONUS_2} друзей и открыл все материалы.\n\n"
            "Вот твой главный бонус:\n"
            f"💎 {bonus_link}"
        )

    # =========================================================
    # АДМИНКА
    # =========================================================
    @classmethod
    def admin_panel(cls) -> str:
        return "🛠 Админ-панель:"

    @classmethod
    def no_admin_panel_access(cls) -> str:
        return "❌ У тебя нет доступа к админ-панели."

    @classmethod
    def no_stats_access(cls) -> str:
        return "❌ У тебя нет доступа к статистике."

    @classmethod
    def no_broadcast_access(cls) -> str:
        return "❌ У тебя нет доступа к рассылке."

    @classmethod
    def admin_stats(cls, users_count: int, refs_count: int) -> str:
        return (
            f"🏆 Всего пользователей: {users_count}\n"
            f"🔗 Всего рефералов: {refs_count}"
        )

    @classmethod
    def ask_broadcast_text(cls) -> str:
        return "✏️ Напиши текст рассылки:"

    @classmethod
    def broadcast_done(cls, success_count: int, total_count: int) -> str:
        return f"✅ Отправлено {success_count}/{total_count}"


class BotLogic:
    # =========================================================
    # ЛОГИКА УРОВНЕЙ
    # Тут обычно геймдизу можно не лазить,
    # но если меняются названия уровней — всё подтянется автоматически
    # =========================================================
    @classmethod
    def get_level_name(cls, count: int) -> str:
        if count < REFERRALS_FOR_BONUS_1:
            return BotTexts.LEVEL_1_NAME
        if count < REFERRALS_FOR_BONUS_2:
            return BotTexts.LEVEL_2_NAME
        return BotTexts.LEVEL_3_NAME

    @classmethod
    def get_next_level_target(cls, count: int):
        if count < REFERRALS_FOR_BONUS_1:
            return BotTexts.LEVEL_2_NAME, REFERRALS_FOR_BONUS_1
        if count < REFERRALS_FOR_BONUS_2:
            return BotTexts.LEVEL_3_NAME, REFERRALS_FOR_BONUS_2
        return None, None
