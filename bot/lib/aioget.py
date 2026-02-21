from typing import Any, Union

import aiohttp


async def aioget(
    url: str,
    params: dict[str, Any] = {},
    timeout: int = 10,
    headers: dict[str, Any] | None = None,
    disable_text_loading: bool = False,
    **kwargs_params,
) -> Union[aiohttp.Response, str]:
    headers = headers or {
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0"
    }

    if not any(
        [
            url.startswith("https://"),
            url.startswith("http://"),
        ]
    ):
        url = f"https://{url}"

    async with aiohttp.ClientSession(
        headers=headers,
        timeout=aiohttp.ClientTimeout(timeout),
    ) as session:
        async with session.get(
            url, params=params | kwargs_params
        ) as res:
            if disable_text_loading:
                text = None
            else:
                text = await res.text()

            return res, text
