# Bot Telegram - Assistente com IA (Gemini)

Bot Telegram com inteligencia artificial usando Google Gemini, menus interativos, banco de dados e lembretes.

## Funcionalidades

- Conversa com IA (Google Gemini) com historico de contexto
- Analise de imagens (visao computacional)
- Transcricao e resposta de audios
- Analise de documentos (PDF, TXT, CSV, JSON)
- Menus interativos com botoes inline
- Sistema de lembretes agendados
- Configuracoes por usuario (modelo IA, prompt do sistema)

## Comandos

- `/start` - Iniciar o bot
- `/help` - Ver ajuda
- `/menu` - Abrir menu principal
- `/settings` - Configuracoes
- `/history` - Ver historico recente
- `/remind <tempo> <msg>` - Criar lembrete (ex: `/remind 30m Cafe`)

## Configurar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edite o `.env` com suas chaves:

```env
TELEGRAM_BOT_TOKEN=seu_token_do_botfather
GEMINI_API_KEY=sua_chave_do_google_ai
```

```bash
python bot.py
```

## Deploy (Railway)

1. Faca fork ou conecte este repo no [Railway](https://railway.app)
2. Adicione as variaveis de ambiente: `TELEGRAM_BOT_TOKEN` e `GEMINI_API_KEY`
3. Railway detecta o `Dockerfile` automaticamente e faz o deploy

## Deploy (Render)

1. Conecte o repo no [Render](https://render.com)
2. Crie um **Background Worker** (nao Web Service)
3. Build command: `pip install -r requirements.txt`
4. Start command: `python bot.py`
5. Adicione as variaveis de ambiente

## Tecnologias

- Python 3.13
- python-telegram-bot 21.10
- Google Gemini (google-genai)
- SQLite (aiosqlite)
