from telegram import Update
from telegram.ext import ContextTypes

import database
import keyboards


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await database.upsert_user(user.id, user.username, user.first_name, user.language_code)
    await update.message.reply_text(
        f"Ola {user.first_name}! Sou seu assistente com IA.\n"
        "Mande qualquer mensagem para conversar, ou use o menu abaixo.",
        reply_markup=keyboards.main_menu_keyboard(),
    )
    await update.message.reply_text(
        "Use os botoes abaixo para acesso rapido:",
        reply_markup=keyboards.persistent_reply_keyboard(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Comandos disponiveis:\n\n"
        "/start - Iniciar o bot\n"
        "/help - Ver esta ajuda\n"
        "/menu - Abrir menu principal\n"
        "/settings - Configuracoes\n"
        "/history - Ver historico recente\n"
        "/clear - Limpar historico\n"
        "/remind <tempo> <msg> - Criar lembrete\n\n"
        "Voce tambem pode:\n"
        "- Enviar texto para conversar com IA\n"
        "- Enviar fotos para analise visual\n"
        "- Enviar audio para transcricao\n"
        "- Enviar documentos para analise"
    )
    await update.message.reply_text(text)


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Menu principal:",
        reply_markup=keyboards.main_menu_keyboard(),
    )


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Configuracoes:",
        reply_markup=keyboards.settings_keyboard(),
    )


async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    history = await database.get_history(user.id, limit=5)
    if not history:
        await update.message.reply_text("Nenhum historico encontrado.")
        return

    lines = []
    for msg in history:
        role = "Voce" if msg["role"] == "user" else "Bot"
        content = msg["content"][:100]
        if len(msg["content"]) > 100:
            content += "..."
        lines.append(f"{role}: {content}")

    await update.message.reply_text("Historico recente:\n\n" + "\n\n".join(lines))
