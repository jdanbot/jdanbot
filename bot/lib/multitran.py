#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004

# Copyright (C) 2021 LёNya <lenechka@national.shitposting.agency>

# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.

#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

#  0. You just DO WHAT THE FUCK YOU WANT TO.


import re
import json
import aiohttp


DEFAULT_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded"
}


class GoogleTranslator:
    BASE_URL = "https://translate.google.com"
    URL = f"{BASE_URL}/_/TranslateWebserverUi/data/batchexecute"
    GOOGLE_RPC = "MkEWBc"

    def __init__(self):
        self._session = aiohttp.ClientSession()

    async def translate(
        self,
        text: str,
        src_lang: str = "auto",
        tgt_lang: str = "auto"
    ) -> str:
        parameter = [[text.strip(), src_lang, tgt_lang, True], [None]]
        escaped_parameter = json.dumps(parameter, separators=(',', ':'))

        rpc = [[[self.GOOGLE_RPC, escaped_parameter, None, "generic"]]]
        escaped_rpc = json.dumps(rpc, separators=(',', ':'))
        params = {"f.req": escaped_rpc}

        async with self._session.post(self.URL, params=params) as r:
            resp = await r.text()

        parts = re.split("([0-9]+|\)\]\}\')\n", resp)
        for part in parts:
            if self.GOOGLE_RPC in part:
                _t = json.loads(part)[0][2]
                _translation = json.loads(_t)[1]

                source_lang = _translation[3]
                target_lang = _translation[1]
                source_text = _translation[4][0]

                translated = _translation[0][0]

                pronounce = translated[1]
                _parts = translated[5]

                translated_text = ""
                parts = list()

                for part in _parts:
                    translated_text += " " + part[0]

                break
        return translated_text

    async def close(self):
        await self._session.close()
