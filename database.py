import aiosqlite

from config import DATABASE_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id       INTEGER PRIMARY KEY,
    username      TEXT,
    first_name    TEXT,
    language_code TEXT DEFAULT 'pt',
    ai_model      TEXT DEFAULT 'gemini-2.0-flash',
    system_prompt TEXT DEFAULT 'Voce e um assistente util e amigavel. Responda em portugues.',
    created_at    TEXT DEFAULT (datetime('now')),
    last_active   TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS messages (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    role       TEXT NOT NULL CHECK(role IN ('user', 'model')),
    content    TEXT NOT NULL,
    media_type TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS reminders (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    chat_id     INTEGER NOT NULL,
    text        TEXT NOT NULL,
    remind_at   TEXT NOT NULL,
    is_sent     INTEGER DEFAULT 0,
    created_at  TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX IF NOT EXISTS idx_messages_user ON messages(user_id, created_at);
CREATE INDEX IF NOT EXISTS idx_reminders_pending ON reminders(is_sent, remind_at);
"""


async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.executescript(SCHEMA)
        await db.commit()


async def upsert_user(user_id: int, username: str | None, first_name: str | None, language_code: str | None):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """INSERT INTO users (user_id, username, first_name, language_code)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(user_id) DO UPDATE SET
                   username = excluded.username,
                   first_name = excluded.first_name,
                   last_active = datetime('now')""",
            (user_id, username, first_name, language_code),
        )
        await db.commit()


async def get_user_settings(user_id: int) -> dict:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT ai_model, system_prompt FROM users WHERE user_id = ?",
            (user_id,),
        )
        row = await cursor.fetchone()
        if row:
            return {"ai_model": row["ai_model"], "system_prompt": row["system_prompt"]}
        return {"ai_model": "gemini-2.0-flash", "system_prompt": "Voce e um assistente util e amigavel. Responda em portugues."}


async def update_user_settings(user_id: int, **kwargs):
    allowed = {"ai_model", "system_prompt"}
    fields = {k: v for k, v in kwargs.items() if k in allowed}
    if not fields:
        return
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [user_id]
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(f"UPDATE users SET {set_clause} WHERE user_id = ?", values)
        await db.commit()


async def save_message(user_id: int, role: str, content: str, media_type: str = "text"):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO messages (user_id, role, content, media_type) VALUES (?, ?, ?, ?)",
            (user_id, role, content, media_type),
        )
        await db.commit()


async def get_history(user_id: int, limit: int = 20) -> list[dict]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT role, content FROM messages WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit),
        )
        rows = await cursor.fetchall()
        return [{"role": row["role"], "content": row["content"]} for row in reversed(rows)]


async def clear_history(user_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM messages WHERE user_id = ?", (user_id,))
        await db.commit()


async def create_reminder(user_id: int, chat_id: int, text: str, remind_at: str) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO reminders (user_id, chat_id, text, remind_at) VALUES (?, ?, ?, ?)",
            (user_id, chat_id, text, remind_at),
        )
        await db.commit()
        return cursor.lastrowid


async def get_pending_reminders() -> list[dict]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT id, user_id, chat_id, text, remind_at FROM reminders WHERE is_sent = 0"
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def mark_reminder_sent(reminder_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("UPDATE reminders SET is_sent = 1 WHERE id = ?", (reminder_id,))
        await db.commit()
