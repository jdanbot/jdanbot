import itertools

from aiogram import types
from ..config import dp
from .. import handlers


def generate_word_variants_with_uppercase(word: str, combinations: list = None):
    if combinations is None:
        combinations = get_word_variants_based_on_word_len(word)

    a = list(map(itertools.permutations, combinations))

    uppercase_map = set([x for a in list(a) for x in a])
    variants = []

    for m in uppercase_map:
        variants.append("".join([
            letter.upper()
            if int(m[i]) == 1 
            else letter
            for i, letter in enumerate(word)
        ]))

    return variants


def get_word_variants_based_on_word_len(word: str):
    variants = [
        [1],
        [10, 11],
        [100, 110, 111],
        [1000, 1100, 1110, 1111],
    ]

    if len(word) > len(variants):
        return []

    return map(lambda x: list(str(x)), variants[len(word) - 1])


### http://steen.free.fr/cyrpol/index.html
POLISH_TRANSLITERATION_SCHEMAS = ",".join("""
ia: я, ja: я, ie: э, je: э, i:и, io: ё, jo: ё
ió: ю, jó: ю, iu: ю, ju: ю, ą: а, ę: е, y: ы, e: э
ó: у, u: у, a: а, о: о
szcz:щ, cz: ч, sz: ш, ż: ж, rz: ж, r: р
m: м, l: ль, ł: л, j: й, n: н, f: ф, w: в
g: г, ch: х, h: х, k: к, t: т, ć: чь, b: б
dź: д, d: д, s: с, ś: сь, z: з, ź: зь, ń: нь, p: п, v: в, c: ц
ьо: ё, ьа: я
""".replace(" ", "").split()).split(",")

a = generate_word_variants_with_uppercase(
    "szcz"
)

BIG_POLIST_SCHEMAS = []

for schema in POLISH_TRANSLITERATION_SCHEMAS:
    pol, rus = schema.split(":")

    variants = generate_word_variants_with_uppercase(pol)

    BIG_POLIST_SCHEMAS \
        .extend(list(map(lambda x: f"{x}:{rus.upper()}", variants)))

# POLISH_TRANSLITERATION_SCHEMAS.extend(BIG_POLIST_SCHEMAS)
BIG_POLIST_SCHEMAS.extend(POLISH_TRANSLITERATION_SCHEMAS)
POLISH_TRANSLITERATION_SCHEMAS = BIG_POLIST_SCHEMAS

@dp.message_handler(commands=["cyr"])
@handlers.get_text
async def cyr(message: types.Message, text: str):
    result = text

    for schema in POLISH_TRANSLITERATION_SCHEMAS:
        result = result.replace(*schema.split(":"))

    await message.reply(result)