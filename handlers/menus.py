from telegram import Update
from telegram.ext import ContextTypes

import database
import keyboards


HELP_TEXT = (
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


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu_main":
        await query.edit_message_text("Menu principal:", reply_markup=keyboards.main_menu_keyboard())

    elif data == "menu_chat":
        await query.edit_message_text(
            "Modo conversa ativado!\n"
            "Mande qualquer mensagem de texto e eu respondo com IA."
        )

    elif data == "menu_image":
        await query.edit_message_text(
            "Mande uma foto e eu analiso usando IA.\n"
            "Voce pode adicionar uma legenda com sua pergunta."
        )

    elif data == "menu_reminders":
        await query.edit_message_text(
            "Para criar um lembrete use:\n"
            "/remind <tempo> <mensagem>\n\n"
            "Formatos de tempo: 10m, 2h, 1d, ou HH:MM\n\n"
            "Exemplos:\n"
            "/remind 30m Fazer cafe\n"
            "/remind 14:30 Reuniao"
        )

    elif data == "menu_settings":
        await query.edit_message_text("Configuracoes:", reply_markup=keyboards.settings_keyboard())

    elif data == "menu_help":
        await query.edit_message_text(HELP_TEXT, reply_markup=keyboards.main_menu_keyboard())

    elif data == "settings_model":
        await query.edit_message_text(
            "Escolha o modelo de IA:",
            reply_markup=keyboards.model_selection_keyboard(),
        )

    elif data == "settings_prompt":
        context.user_data["awaiting_prompt"] = True
        await query.edit_message_text(
            "Envie a nova instrucao do sistema como mensagem de texto.\n"
            "Exemplo: 'Voce e um professor de ingles. Responda sempre em ingles.'"
        )

    elif data == "settings_clear":
        await query.edit_message_text(
            "Tem certeza que quer limpar todo o historico?",
            reply_markup=keyboards.confirm_keyboard("clear"),
        )

    elif data.startswith("model_"):
        model_name = data.replace("model_", "")
        await database.update_user_settings(query.from_user.id, ai_model=model_name)
        await query.edit_message_text(
            f"Modelo alterado para: {model_name}",
            reply_markup=keyboards.settings_keyboard(),
        )

    elif data == "confirm_clear":
        await database.clear_history(query.from_user.id)
        await query.edit_message_text("Historico limpo!", reply_markup=keyboards.main_menu_keyboard())

    elif data.startswith("cancel_"):
        await query.edit_message_text("Acao cancelada.", reply_markup=keyboards.main_menu_keyboard())
