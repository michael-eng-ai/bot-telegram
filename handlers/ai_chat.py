from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

import database
import gemini_client
import keyboards


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = update.message.text

    # Atalhos do teclado persistente
    if text == "Menu":
        await update.message.reply_text(
            "Menu principal:",
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return
    if text == "Limpar historico":
        await database.clear_history(user.id)
        await update.message.reply_text("Historico limpo!")
        return
    if text == "Ajuda":
        from handlers.commands import help_command
        await help_command(update, context)
        return

    # Modo aguardando novo system prompt
    if context.user_data.get("awaiting_prompt"):
        context.user_data["awaiting_prompt"] = False
        await database.update_user_settings(user.id, system_prompt=text)
        await update.message.reply_text(
            f"Prompt do sistema atualizado para:\n\n{text}",
            reply_markup=keyboards.settings_keyboard(),
        )
        return

    # Conversa com IA
    await database.upsert_user(user.id, user.username, user.first_name, user.language_code)
    settings = await database.get_user_settings(user.id)
    history = await database.get_history(user.id, limit=20)

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    try:
        response_text = await gemini_client.ask_gemini(
            prompt=text,
            history=history,
            system_prompt=settings["system_prompt"],
            model=settings["ai_model"],
        )
    except Exception as e:
        await update.message.reply_text(f"Erro ao consultar IA: {e}")
        return

    await database.save_message(user.id, "user", text, "text")
    await database.save_message(user.id, "model", response_text, "text")

    # Telegram limita mensagens a 4096 caracteres
    if len(response_text) > 4000:
        for i in range(0, len(response_text), 4000):
            await update.message.reply_text(response_text[i : i + 4000])
    else:
        await update.message.reply_text(response_text)
