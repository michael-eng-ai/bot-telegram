from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

import database
import ai_client


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    photo = update.message.photo[-1]
    caption = update.message.caption or "Descreva esta imagem em detalhes."

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    file = await context.bot.get_file(photo.file_id)
    image_bytes = await file.download_as_bytearray()

    await database.upsert_user(user.id, user.username, user.first_name, user.language_code)
    settings = await database.get_user_settings(user.id)

    try:
        response_text = await ai_client.ask_ai_vision(
            prompt=caption,
            image_bytes=bytes(image_bytes),
            mime_type="image/jpeg",
            system_prompt=settings["system_prompt"],
            model=settings["ai_model"],
        )
    except Exception as e:
        await update.message.reply_text(f"Erro ao analisar imagem: {e}")
        return

    await database.save_message(user.id, "user", f"[Imagem] {caption}", "image")
    await database.save_message(user.id, "model", response_text, "text")
    await update.message.reply_text(response_text)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    voice = update.message.voice or update.message.audio

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    file = await context.bot.get_file(voice.file_id)
    audio_bytes = await file.download_as_bytearray()

    await database.upsert_user(user.id, user.username, user.first_name, user.language_code)
    settings = await database.get_user_settings(user.id)

    # DeepSeek nao suporta audio nativo, transcrever nao e possivel
    await update.message.reply_text(
        "Desculpe, no momento nao consigo processar mensagens de audio. "
        "Por favor, envie sua mensagem como texto."
    )


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    doc = update.message.document

    if doc.file_size and doc.file_size > 10 * 1024 * 1024:
        await update.message.reply_text("Arquivo muito grande (max 10MB).")
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    file = await context.bot.get_file(doc.file_id)
    file_bytes = await file.download_as_bytearray()
    mime_type = doc.mime_type or "application/octet-stream"
    caption = update.message.caption or f"Analise este arquivo ({doc.file_name})."

    await database.upsert_user(user.id, user.username, user.first_name, user.language_code)
    settings = await database.get_user_settings(user.id)

    text_mimes = {"text/plain", "text/csv", "text/html", "application/json", "application/pdf"}

    try:
        if mime_type in text_mimes:
            text_content = bytes(file_bytes).decode("utf-8", errors="replace")[:10000]
            response_text = await ai_client.ask_ai(
                prompt=f"{caption}\n\nConteudo do arquivo:\n{text_content}",
                system_prompt=settings["system_prompt"],
                model=settings["ai_model"],
            )
        else:
            response_text = await ai_client.ask_ai(
                prompt=f"{caption}\n\n(Arquivo binario: {doc.file_name}, tipo: {mime_type}, tamanho: {doc.file_size} bytes)",
                system_prompt=settings["system_prompt"],
                model=settings["ai_model"],
            )
    except Exception as e:
        await update.message.reply_text(f"Erro ao analisar documento: {e}")
        return

    await database.save_message(user.id, "user", f"[Documento: {doc.file_name}] {caption}", "document")
    await database.save_message(user.id, "model", response_text, "text")
    await update.message.reply_text(response_text)


async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    emoji = update.message.sticker.emoji or "?"
    await update.message.reply_text(f"Legal o sticker! {emoji}")
