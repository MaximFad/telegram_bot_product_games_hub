from config import REFERRALS_FOR_BONUS_1, REFERRALS_FOR_BONUS_2


class BotTexts:
    # =========================================================
    # НАЗВАНИЯ УРОВНЕЙ
    # Где используется:
    # - главное меню
    # - реферальная панель
    # - авто-сообщения о прогрессе
    # =========================================================
    LEVEL_1_NAME = "Джуниор разработчик"
    LEVEL_2_NAME = "Колдун магистр"
    LEVEL_3_NAME = "Легенда геймдева"

    # =========================================================
    # КНОПКИ
    # Где используется:
    # - inline кнопки в меню
    # - кнопки под материалами
    # - кнопки в админке
    # =========================================================
    BTN_MATERIALS = "📚 Таблицы и документы"
    BTN_MY_REFS = "🎁 Миссии, получить секретный бонус"
    BTN_ADMIN = "🛠 Админ панель"
    BTN_SUBSCRIBE = "Подписаться на канал"
    BTN_CHECK_SUBSCRIBE = "✅ Я подписался"
    BTN_SHARE = "🚀 Поделиться ссылкой"
    BTN_SHARE_WITH_FRIEND = "🎁 Отправить другу"
    BTN_BACK = "⬅️ Вернуться в меню"
    BTN_BROADCAST = "📢 Сделать рассылку"
    BTN_STATS = "📊 Статистика"

    # =========================================================
    # НАЗВАНИЯ БОНУСОВ В СПИСКЕ МАТЕРИАЛОВ
    # Где используется:
    # - экран выбора материалов
    # =========================================================
    BONUS_1_MENU_TITLE = "🎁 Секретный бонус"
    BONUS_2_MENU_TITLE = "💎 Главный приз"

    # =========================================================
    # ОБЩИЕ СЛУЖЕБНЫЕ ТЕКСТЫ
    # =========================================================
    TEXT_UNKNOWN_ACTION = "❌ Неизвестное действие."
    TEXT_MATERIAL_NOT_FOUND = "❌ Материал не найден."
    TEXT_CHECK_ERROR = "❌ Не удалось проверить подписку или открыть материал."

    # =========================================================
    # ГЛАВНОЕ МЕНЮ
    # Когда появляется:
    # - после /start
    # - после возврата в меню
    # =========================================================
    @classmethod
    def main_menu(cls, level_name: str, ref_link: str) -> str:
        return (
            "Привет! Это Product Games Hub.\n\n"
            f"🏅 Твой уровень: «{level_name}»\n"
            f"🎯 Миссия: дойти до «{cls.LEVEL_3_NAME}» и открыть все секретные материалы\n\n"
            "Выбери материал который хочешь получить:"
        )

    # =========================================================
    # ЭКРАН МАТЕРИАЛОВ
    # Когда появляется:
    # - после нажатия на кнопку материалов
    # =========================================================
    @classmethod
    def materials_menu(cls) -> str:
        return "Выбери документ, который хочешь получить:"

    # =========================================================
    # НЕ ПОДПИСАН НА КАНАЛ
    # Когда появляется:
    # - пользователь пытается открыть материал
    # - но не подписан на канал
    # =========================================================
    @classmethod
    def not_subscribed(cls, channel_username: str) -> str:
        return (
            f"❌ Сначала подпишись на канал @{channel_username}, чтобы получить материалы.\n"
            "После подписки вернись в бота и нажми кнопку ещё раз."
        )

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
            f"✅ Материал открыт: {material_name}:\n"
            f"{material_link}\n\n"
            "🎁 Теперь открой секретный бонус\n"
            f"🎯 Цель: пригласи {REFERRALS_FOR_BONUS_1} друзей по своей ссылке и открыть первый секретный бонус.\n"
            f"👥 Прогресс: {current_refs} из {REFERRALS_FOR_BONUS_1}\n\n"
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
            "👋 Это твоя реферальная панель.\n\n"
            f"🏅 Текущий уровень: «{current_level}»\n"
            f"👥 Твои приглашённые: {current_refs}\n\n"
            f"🔗 Твоя ссылка:\n{ref_link}\n\n"
        )

        if next_level_name and next_level_target:
            text += (
                f"🎯 Цель: дойти до уровня «{next_level_name}» и набрать {next_level_target} приглашённых.\n"
                "За уровни открываются секретные бонусы и материалы."
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
            f"❌ Этот бонус откроется после {need_refs} приглашённых.\n"
            f"Сейчас у тебя: {current_refs}."
        )

    # =========================================================
    # БОНУС 1 ОТКРЫТ
    # =========================================================
    @classmethod
    def bonus_1_opened(cls, link: str) -> str:
        return (
            "✅ Разблокирован первый секретный бонус:\n"
            f"{link}"
        )

    # =========================================================
    # БОНУС 2 ОТКРЫТ
    # =========================================================
    @classmethod
    def bonus_2_opened(cls, link: str) -> str:
        return (
            "✅ Разблокирован второй секретный бонус:\n"
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
            "🙌 Один друг уже с нами!\n\n"
            f"🏅 Текущий уровень: «{cls.LEVEL_1_NAME}»\n"
            f"👥 Приглашено друзей: {current_refs} из {REFERRALS_FOR_BONUS_1}\n\n"
            f"Ещё {left} — и откроется первый секретный материал.\n\n"
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
            f"🎉 Уровень «{cls.LEVEL_1_NAME}» завершён!\n\n"
            "Вот твой первый секретный материал:\n"
            f"🔗 {bonus_link}\n\n"
            f"🎯 Новый этап: уровень «{cls.LEVEL_2_NAME}»\n"
            f"Пригласи ещё {next_step_count} друзей и открой следующий бонус.\n\n"
            f"Текущий прогресс уровня «{cls.LEVEL_2_NAME}»: 0 из {next_step_count}\n\n"
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
            "🙌 Ещё один друг присоединился!\n\n"
            f"🏅 Текущий уровень: «{cls.LEVEL_2_NAME}»\n"
            f"👥 Прогресс: {progress_now} из {progress_total}\n"
            f"Осталось пригласить: {refs_left}\n\n"
            f"🔗 Твоя ссылка:\n{ref_link}"
        )

    # =========================================================
    # ПРОГРЕСС: ОТКРЫТ ФИНАЛЬНЫЙ БОНУС
    # =========================================================
    @classmethod
    def invite_progress_final(cls, bonus_link: str) -> str:
        return (
            f"🏆 Уровень «{cls.LEVEL_2_NAME}» завершён!\n\n"
            f"Ты пригласил {REFERRALS_FOR_BONUS_2} друзей и открыл все секретные материалы.\n\n"
            "Вот твой супер-секретный бонус:\n"
            f"🔗 {bonus_link}\n\n"
            "Спасибо, что помогаешь развивать канал."
        )

    # =========================================================
    # АДМИНКА
    # =========================================================
    @classmethod
    def admin_panel(cls) -> str:
        return "🔧 Админ-панель:"

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
            f"📊 Всего пользователей: {users_count}\n"
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
