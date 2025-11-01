from typing import Any

import httpx


async def aioget(
    url: str,
    params: dict[str, Any] = {},
    timeout: int = 10,
    headers: dict[str, Any] | None = None,
) -> httpx.Response:
    headers = headers or {
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0"
    }

    if not any([url.startswith("https://"), url.startswith("http://")]):
        url = f"https://{url}"

    async with httpx.AsyncClient() as client:
        return await client.get(url, params=params, timeout=timeout, headers=headers)
