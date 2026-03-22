from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)

from config import TOKEN, DISCUSSION_GROUP_ID
from handlers.start import start
from handlers.refs import my_refs
from handlers.menu import materials_menu, check_and_send, check_subscription, show_main_menu
from handlers.admin import (
    admin_panel,
    stats,
    ask_broadcast_text,
    do_broadcast,
    WAITING_BROADCAST,
)
from handlers.game_review import (
    open_game_review,
    receive_game_review,
    WAITING_GAME_REVIEW,
)
from handlers.leaderboard import show_leaderboard
from handlers.comment_points import handle_comment_points


def build_app():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(ask_broadcast_text, pattern="^do_broadcast$"),
            CallbackQueryHandler(open_game_review, pattern="^game_review$"),
        ],
        states={
            WAITING_BROADCAST: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, do_broadcast)
            ],
            WAITING_GAME_REVIEW: [
                MessageHandler(
                    (filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL)
                    & ~filters.COMMAND,
                    receive_game_review,
                )
            ],
        },
        fallbacks=[],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    app.add_handler(CallbackQueryHandler(materials_menu, pattern="^materials_menu$"))
    app.add_handler(CallbackQueryHandler(my_refs, pattern="^my_refs$"))
    app.add_handler(CallbackQueryHandler(admin_panel, pattern="^admin_panel$"))
    app.add_handler(CallbackQueryHandler(stats, pattern="^stats$"))
    app.add_handler(CallbackQueryHandler(check_subscription, pattern="^check_subscription$"))
    app.add_handler(CallbackQueryHandler(check_and_send, pattern="^(link_|secret_)"))
    app.add_handler(CallbackQueryHandler(show_main_menu, pattern="^back_to_menu$"))
    app.add_handler(CallbackQueryHandler(show_leaderboard, pattern="^leaderboard$"))

    if DISCUSSION_GROUP_ID:
        app.add_handler(
            MessageHandler(
                filters.Chat(chat_id=DISCUSSION_GROUP_ID)
                & ~filters.StatusUpdate.ALL
                & ~filters.COMMAND,
                handle_comment_points,
            )
        )

    return app


if __name__ == "__main__":
    app = build_app()
    app.run_polling()
