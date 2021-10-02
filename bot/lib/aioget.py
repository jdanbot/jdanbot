import httpx


async def aioget(url, params={}, timeout=10, headers=None):
    headers = headers if headers is not None else {
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0" # noqa
    }

    if not url.startswith("https://") and not url.startswith("http://"):
        url = f"http://{url}"

    async with httpx.AsyncClient() as client:
        return await client.get(
            url, params=params, timeout=timeout, headers=headers)
