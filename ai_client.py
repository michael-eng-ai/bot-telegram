from openai import AsyncOpenAI

from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEFAULT_MODEL, MAX_RESPONSE_TOKENS

_client = None


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        if not DEEPSEEK_API_KEY:
            raise RuntimeError("DEEPSEEK_API_KEY nao configurado.")
        _client = AsyncOpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
    return _client


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

    response = await _get_client().chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=MAX_RESPONSE_TOKENS,
        temperature=0.7,
    )
    return response.choices[0].message.content


async def ask_ai_vision(
    prompt: str,
    image_bytes: bytes,
    mime_type: str = "image/jpeg",
    system_prompt: str | None = None,
    model: str = DEFAULT_MODEL,
) -> str:
    import base64

    b64 = base64.b64encode(image_bytes).decode("utf-8")
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{b64}"}},
        ],
    })

    response = await _get_client().chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=MAX_RESPONSE_TOKENS,
    )
    return response.choices[0].message.content
