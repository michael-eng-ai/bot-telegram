import re
from datetime import datetime, timedelta, timezone

from telegram import Update
from telegram.ext import Application, ContextTypes

import database


async def remind_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Uso: /remind <tempo> <mensagem>\n\n"
            "Exemplos:\n"
            "  /remind 30m Fazer cafe\n"
            "  /remind 2h Reuniao\n"
            "  /remind 14:30 Almoco\n\n"
            "Formatos: 10m, 2h, 1d, ou HH:MM"
        )
        return

    time_str = context.args[0]
    text = " ".join(context.args[1:])
    now = datetime.now(timezone.utc)

    # Tempo relativo: 10m, 2h, 1d
    match = re.match(r"^(\d+)(m|h|d)$", time_str)
    if match:
        amount, unit = int(match.group(1)), match.group(2)
        delta = {
            "m": timedelta(minutes=amount),
            "h": timedelta(hours=amount),
            "d": timedelta(days=amount),
        }[unit]
        remind_at = now + delta
    else:
        # Horario fixo: HH:MM
        try:
            hour, minute = map(int, time_str.split(":"))
            remind_at = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if remind_at <= now:
                remind_at += timedelta(days=1)
        except ValueError:
            await update.message.reply_text("Formato invalido. Use: 10m, 2h, 1d, ou HH:MM")
            return

    reminder_id = await database.create_reminder(
        user_id=update.effective_user.id,
        chat_id=update.effective_chat.id,
        text=text,
        remind_at=remind_at.isoformat(),
    )

    context.job_queue.run_once(
        send_reminder,
        when=(remind_at - now).total_seconds(),
        data={"reminder_id": reminder_id, "chat_id": update.effective_chat.id, "text": text},
        name=f"reminder_{reminder_id}",
    )

    await update.message.reply_text(
        f"Lembrete agendado para {remind_at.strftime('%d/%m %H:%M')} UTC:\n{text}"
    )


async def send_reminder(context: ContextTypes.DEFAULT_TYPE) -> None:
    data = context.job.data
    await context.bot.send_message(
        chat_id=data["chat_id"],
        text=f"Lembrete: {data['text']}",
    )
    await database.mark_reminder_sent(data["reminder_id"])


async def restore_reminders(app: Application) -> None:
    pending = await database.get_pending_reminders()
    now = datetime.now(timezone.utc)
    for r in pending:
        remind_at = datetime.fromisoformat(r["remind_at"])
        if remind_at.tzinfo is None:
            remind_at = remind_at.replace(tzinfo=timezone.utc)
        delay = max((remind_at - now).total_seconds(), 0)
        app.job_queue.run_once(
            send_reminder,
            when=delay,
            data={"reminder_id": r["id"], "chat_id": r["chat_id"], "text": r["text"]},
            name=f"reminder_{r['id']}",
        )
