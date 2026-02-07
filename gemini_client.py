from google import genai
from google.genai import types

from config import GEMINI_API_KEY, DEFAULT_MODEL, MAX_RESPONSE_TOKENS

client = genai.Client(api_key=GEMINI_API_KEY)


async def ask_gemini(
    prompt: str,
    history: list[dict] | None = None,
    system_prompt: str | None = None,
    model: str = DEFAULT_MODEL,
) -> str:
    contents = []
    if history:
        for msg in history:
            contents.append(
                types.Content(
                    role=msg["role"],
                    parts=[types.Part.from_text(text=msg["content"])],
                )
            )
    contents.append(
        types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
    )

    response = await client.aio.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=MAX_RESPONSE_TOKENS,
            temperature=0.7,
        ),
    )
    return response.text


async def ask_gemini_vision(
    prompt: str,
    image_bytes: bytes,
    mime_type: str = "image/jpeg",
    system_prompt: str | None = None,
    model: str = DEFAULT_MODEL,
) -> str:
    response = await client.aio.models.generate_content(
        model=model,
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


async def ask_gemini_audio(
    prompt: str,
    audio_bytes: bytes,
    mime_type: str = "audio/ogg",
    system_prompt: str | None = None,
    model: str = DEFAULT_MODEL,
) -> str:
    response = await client.aio.models.generate_content(
        model=model,
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
