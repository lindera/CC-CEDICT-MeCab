import re

pattern = re.compile(r"^(.*?) (.*?) \[(.*?)\] /(.*?)$")

# The cost of every unknown word in unk.def. Keep the two in sync.
UNK_COST = 400

# Runs of the characters that char.def groups into one unknown word and that
# have entries of their own: Latin letters (ALPHA) and digits (NUMERIC).
latin = re.compile(r"[A-Za-zÀ-ÿĀ-ſƀ-ȶḀ-ỹＡ-Ｚａ-ｚ]+")
digits = re.compile(r"[0-9０-９⁰-₟⅐-↏]+")


def word_cost(surface, length):
    # An entry made only of Latin letters or only of digits costs one less
    # than the unknown word for the same run: it wins for exactly that run,
    # and never as part of a longer run (UNK_COST - 1 + UNK_COST > UNK_COST).
    if latin.fullmatch(surface) or digits.fullmatch(surface):
        return UNK_COST - 1
    # Any other entry costs less the longer it is, and less than the
    # entries it could be split into.
    return int(max(-36000, -400 * (length ** 1.5)))


# surface -> csv (surface, left id, right id, cost, pinyin, traditional, simplified, definition)
dict = {}

with open("cedict_ts.u8") as f:
    for line in f:
        line = line.strip()
        if line.startswith("#"):
            continue

        match = pattern.match(line)
        if match:
            traditional = match.group(1)
            simplified = match.group(2)
            pinyin = match.group(3)
            definition = match.group(4)

            length = len(traditional)
            dict[traditional] = f"{traditional},0,0,{word_cost(traditional, length)},*,*,*,*,{pinyin},{traditional},{simplified},{definition}"
            dict[simplified] = f"{simplified},0,0,{word_cost(simplified, length)},*,*,*,*,{pinyin},{traditional},{simplified},{definition}"

with open("cedict.csv", mode='w') as f:
    for value in dict.values():
        f.write(value + "\n")

