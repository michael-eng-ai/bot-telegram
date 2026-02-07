from openai import AsyncOpenAI

from config import (
    DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEFAULT_MODEL, MAX_RESPONSE_TOKENS,
    GEMINI_API_KEY, GEMINI_MODEL,
)

# --- DeepSeek (texto) ---

_deepseek_client = None


def _get_deepseek() -> AsyncOpenAI:
    global _deepseek_client
    if _deepseek_client is None:
        if not DEEPSEEK_API_KEY:
            raise RuntimeError("DEEPSEEK_API_KEY nao configurado.")
        _deepseek_client = AsyncOpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
    return _deepseek_client


async def ask_ai(
    prompt: str,
    history: list[dict] | None = None,
    system_prompt: str | None = None,
    model: str = DEFAULT_MODEL,
) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if history:
        for msg in history:
            role = msg["role"] if msg["role"] == "user" else "assistant"
            messages.append({"role": role, "content": msg["content"]})
    messages.append({"role": "user", "content": prompt})

    response = await _get_deepseek().chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=MAX_RESPONSE_TOKENS,
        temperature=0.7,
    )
    return response.choices[0].message.content


# --- Gemini (imagem + audio) ---

_gemini_client = None


def _get_gemini():
    global _gemini_client
    if _gemini_client is None:
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY nao configurado.")
        from google import genai
        _gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    return _gemini_client


async def ask_vision(
    prompt: str,
    image_bytes: bytes,
    mime_type: str = "image/jpeg",
    system_prompt: str | None = None,
) -> str:
    from google.genai import types

    response = await _get_gemini().aio.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt),
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                ],
            )
        ],
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=MAX_RESPONSE_TOKENS,
        ),
    )
    return response.text


async def ask_audio(
    prompt: str,
    audio_bytes: bytes,
    mime_type: str = "audio/ogg",
    system_prompt: str | None = None,
) -> str:
    from google.genai import types

    response = await _get_gemini().aio.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt),
                    types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
                ],
            )
        ],
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=MAX_RESPONSE_TOKENS,
        ),
    )
    return response.text
