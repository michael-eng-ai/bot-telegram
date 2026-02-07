import config
import database
from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)
from handlers import (
    start,
    help_command,
    menu_command,
    settings_command,
    history_command,
    handle_text,
    handle_photo,
    handle_voice,
    handle_document,
    handle_sticker,
    menu_callback,
    remind_command,
    restore_reminders,
)


async def post_init(app: Application) -> None:
    await database.init_db()
    await restore_reminders(app)


def main() -> None:
    if not config.TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN nao encontrado. Configure no .env.")
    if not config.DEEPSEEK_API_KEY:
        config.logger.warning("DS_API_KEY nao encontrado — chat de texto desabilitado.")

    app = (
        Application.builder()
        .token(config.TELEGRAM_BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CommandHandler("settings", settings_command))
    app.add_handler(CommandHandler("history", history_command))
    app.add_handler(CommandHandler("remind", remind_command))

    # Callbacks de botoes inline
    app.add_handler(CallbackQueryHandler(menu_callback))

    # Midia
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))

    # Texto (catch-all — deve ser o ultimo)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
