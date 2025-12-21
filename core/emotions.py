# emotions.py
from typing import Dict

EMOTION_LEXICON = {
    # 12: Joy / Sadness
    "joy":       (0.7,  ["blij", "happy", "vrolijk", "tevreden", "opgewekt"]),
    "sadness":   (-0.7, ["verdrietig", "bedroefd", "depressief", "somber", "down"]),

    # 13: Love / Hate
    "love":      (0.7,  ["liefde", "houden van", "ik hou van", "love", "lief"]),
    "hate":      (-0.7, ["haat", "haat hem", "haat haar", "ik verafschuw", "ik kan niet uitstaan"]),

    # 14: Hope / Despair
    "hope":      (0.6,  ["hoop", "hoopvol", "optimistisch", "ik geloof dat", "verwacht dat het goed komt"]),
    "despair":   (-0.7, ["wanhopig", "hopeloos", "geen hoop", "het heeft geen zin", "ik zie het niet meer zitten"]),

    # 15: Trust / Distrust
    "trust":     (0.6,  ["vertrouw", "vertrouwen", "ik geloof je", "betrouwbaar"]),
    "distrust":  (-0.6, ["wantrouw", "ik vertrouw het niet", "argwanend", "skeptisch tegenover jou"]),

    # 16: Peace / Anger
    "peace":     (0.6,  ["rust", "kalm", "peace", "ontspannen", "innerlijke rust"]),
    "anger":     (0.7,  ["boos", "woedend", "pissed", "geïrriteerd", "kwaad"]),

    # 17: Courage / Fear
    "courage":   (0.6,  ["moedig", "durf", "ik ga het toch doen", "dapper"]),
    "fear":      (-0.7, ["bang", "angstig", "bangig", "angst", "schrik"]),

    # 18: Gratitude / Resentment
    "gratitude": (0.8,  ["dankbaar", "dank je", "appreciatie", "thanks", "ik waardeer het"]),
    "resentment":(-0.7, ["wrok", "haatdragend", "ik neem het kwalijk", "verbitterd"]),

    # 19: Compassion / Cruelty
    "compassion":(0.7,  ["compassie", "medeleven", "empathie", "meeleven"]),
    "cruelty":   (-0.7, ["wreed", "hardvochtig", "genadeloos"]),

    # 20: Acceptance / Rejection
    "acceptance":(0.6,  ["acceptatie", "ik accepteer het", "het is oké zo", "ik kan ermee leven"]),
    "rejection": (-0.7, ["afwijzing", "ik wijs het af", "ongewenst", "niet goed genoeg"]),

    # 21: Curiosity / Apathy
    "curiosity": (0.7,  ["nieuwsgierig", "benieuwd", "ik wil weten", "interesse in"]),
    "apathy":    (-0.6, ["kan me niet schelen", "onverschillig", "maakt me niks uit", "apathisch"]),

    # 22: Pride / Shame
    "pride":     (0.7,  ["trots", "ben trots", "fiere", "stolz"]),
    "shame":     (-0.7, ["schaam", "gênant", "ik schaam me", "beschamend"]),

    # 23: Confidence / Doubt
    "confidence":(0.7,  ["zelfvertrouwen", "zeker van mezelf", "ik kan dit", "ik red dit wel"]),
    "doubt":     (-0.6, ["twijfel", "ik weet het niet", "ben niet zeker", "aarzeling"]),

    # 24: Freedom / Constraint
    "freedom":   (0.7,  ["vrijheid", "vrij voelen", "geen beperkingen", "onafhankelijk"]),
    "constraint":(-0.7, ["beperkt", "gevangen", "vastzitten", "geen ruimte"]),

    # 25: Connection / Isolation
    "connection":(0.7,  ["verbonden", "verbinding", "samen", "dichtbij mensen"]),
    "isolation": (-0.7, ["alleen", "eenzaam", "geïsoleerd", "niemand begrijpt me"]),

    # 26: Meaning / Emptiness
    "meaning":   (0.7,  ["zinvol", "betekenis", "purpose", "heeft nut"]),
    "emptiness": (-0.7, ["leeg", "zinloos", "heeft geen betekenis", "doelloos"]),

    # 27: Growth / Stagnation
    "growth":    (0.7,  ["groei", "ontwikkel", "leren", "vooruitgang"]),
    "stagnation":(-0.7, ["vastgelopen", "stagnatie", "kom geen stap verder", "in een sleur"]),

    # 28: Authenticity / Facade
    "authenticity":(0.7, ["authentiek", "echt mezelf", "oprecht", "zonder masker"]),
    "facade":    (-0.7, ["masker op", "doe alsof", "schijnvertoning", "nep"]),

    # 29: Presence / Absence
    "presence":  (0.6,  ["aanwezig", "hier en nu", "mindful", "gegrond"]),
    "absence":   (-0.6, ["afwezig", "er niet bij", "mentaal weg", "lost in thought"]),

    # 30: Harmony / Discord
    "harmony":   (0.7,  ["harmonie", "in balans", "alles klopt", "geen conflict"]),
    "discord":   (-0.7, ["onrust", "conflict", "ruzie", "frictie"]),

    # 31: Wonder / Cynicism
    "wonder":    (0.7,  ["verwonderd", "wow", "onder de indruk", "magisch"]),
    "cynicism":  (-0.7, ["cynisch", "sarcastisch", "gelooft nergens in", "bittersweet"]),

    # 32: Serenity / Anxiety
    "serenity":  (0.6,  ["sereniteit", "innerlijke rust", "kalme helderheid"]),
    "anxiety":   (-0.7, ["paniek", "anxious", "zenuwachtig", "overprikkeld", "ongerust"]),
}


def text_to_emotions(text: str) -> Dict[str, float]:
    text = text.lower()
    emotions: Dict[str, float] = {}
    for name, (value, keywords) in EMOTION_LEXICON.items():
        if any(k in text for k in keywords):
            emotions[name] = value
    return emotions
