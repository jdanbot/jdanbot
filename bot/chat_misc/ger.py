from pathlib import Path

from msgspec import toml

TEXT = """
Die Postmoderne (von lateinisch post ‚hinter‘, ‚nach‘) ist im allgemeinen Sinn der Zustand der abendländischen Gesellschaft, Kultur und Kunst „nach“ der bis in die Gegenwart andauernden Moderne.

Im engeren Sinn ist die Postmoderne eine umstrittene politisch-wissenschaftlich-künstlerische Richtung, die sich gegen bestimmte Institutionen, Methoden, Begriffe und Grundannahmen der Moderne wendet und diese aufzulösen und zu überwinden versucht, dann auch Postmodernismus genannt.
Die Vertreter des Postmodernismus kritisieren das Innovationsstreben der Moderne als lediglich habituell und automatisiert (Sozialkonstruktivismus). Sie bescheinigen der Moderne ein illegitimes Vorherrschen eines totalitären Prinzips, das auf gesellschaftlicher Ebene Züge von Despotismus in sich trage und das bekämpft werden müsse. Maßgebende Ansätze der Moderne seien eindimensional und gescheitert (Nihilismus). Dem wird die Möglichkeit einer Vielfalt gleichberechtigt nebeneinander bestehender Perspektiven gegenübergestellt (Relativismus). Mit der Forderung nach einer prinzipiellen Offenheit von Kunst wird auch kritisch auf die Ästhetik der Moderne Bezug genommen.

Die Diskussion über die zeitliche und inhaltliche Bestimmung dessen, was genau postmodern bzw. postmodernistisch sei, wird etwa seit Anfang der 1980er Jahre geführt. Postmodernes Denken will nicht als bloße Zeitdiagnose verstanden werden, sondern als kritische Denkbewegung, die sich gegen Grundannahmen der Moderne wende und Alternativen aufzeige.
"""

german = toml.decode(
    Path("bot/chat_misc/lib/german.toml").read_bytes()
).items()


def german_to_cyr(
    text: str, variant: dict[str, str] = german
):
    for a, b in variant:
        text = text.replace(a, b)
        text = text.replace(a.upper(), b.upper())

    return text
