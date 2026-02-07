from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Conversar com IA", callback_data="menu_chat")],
        [InlineKeyboardButton("Analisar imagem", callback_data="menu_image")],
        [InlineKeyboardButton("Lembretes", callback_data="menu_reminders")],
        [
            InlineKeyboardButton("Configuracoes", callback_data="menu_settings"),
            InlineKeyboardButton("Ajuda", callback_data="menu_help"),
        ],
    ])


def settings_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Trocar modelo IA", callback_data="settings_model")],
        [InlineKeyboardButton("Alterar prompt do sistema", callback_data="settings_prompt")],
        [InlineKeyboardButton("Limpar historico", callback_data="settings_clear")],
        [InlineKeyboardButton("Voltar", callback_data="menu_main")],
    ])


def model_selection_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Gemini 2.0 Flash (rapido)", callback_data="model_gemini-2.0-flash")],
        [InlineKeyboardButton("Gemini 2.5 Flash (mais recente)", callback_data="model_gemini-2.5-flash-preview-04-17")],
        [InlineKeyboardButton("Voltar", callback_data="menu_settings")],
    ])


def confirm_keyboard(action: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Sim", callback_data=f"confirm_{action}"),
            InlineKeyboardButton("Nao", callback_data=f"cancel_{action}"),
        ]
    ])


def persistent_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [["Menu", "Limpar historico", "Ajuda"]],
        resize_keyboard=True,
        is_persistent=True,
    )
