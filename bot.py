from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)
from config import TOKEN
from handlers.start import start
from handlers.refs import my_refs
from handlers.menu import check_and_send, materials_menu
from handlers.admin import (
    admin_panel,
    stats,
    ask_broadcast_text,
    do_broadcast,
    WAITING_BROADCAST,
)


app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(ask_broadcast_text, pattern="^do_broadcast$")],
    states={
        WAITING_BROADCAST: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, do_broadcast)
        ]
    },
    fallbacks=[],
)

app.add_handler(CommandHandler("start", start))
app.add_handler(conv_handler)

app.add_handler(CallbackQueryHandler(materials_menu, pattern="^materials_menu$"))
app.add_handler(CallbackQueryHandler(my_refs, pattern="^my_refs$"))
app.add_handler(CallbackQueryHandler(admin_panel, pattern="^admin_panel$"))
app.add_handler(CallbackQueryHandler(stats, pattern="^stats$"))
app.add_handler(CallbackQueryHandler(check_and_send, pattern="^link_"))

app.run_polling()
