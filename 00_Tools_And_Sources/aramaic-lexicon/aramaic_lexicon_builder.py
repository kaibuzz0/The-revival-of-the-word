#!/usr/bin/env python3
"""
Aramaic Lexicon Builder
Builds an Aramaic-English dictionary for Biblical and Galilean Aramaic
"""
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

# Core Aramaic vocabulary
# Biblical Aramaic (Daniel/Ezra) + Galilean Aramaic (Jesus' language)

ARAMAIC_CORE_VOCABULARY = {
    # Articles and Pronouns
    "הַ": {"def": "the (definite article)", "pos": "article", "translit": "ha", "root": "h"},
    "דִּ": {"def": "which, who, that (relative)", "pos": "pronoun", "translit": "di", "root": "d"},
    "מַן": {"def": "who, what", "pos": "pronoun", "translit": "man", "root": "m-n"},
    "מָה": {"def": "what", "pos": "pronoun", "translit": "māh", "root": "m-h"},
    "אֲנָה": {"def": "I", "pos": "pronoun", "translit": "ʾănāh", "root": "ʾ-n-h"},
    "אַתָּה": {"def": "you (masculine singular)", "pos": "pronoun", "translit": "ʾattāh", "root": "ʾ-t-h"},
    "אַתִּי": {"def": "you (feminine singular)", "pos": "pronoun", "translit": "ʾattî", "root": "ʾ-t"},
    "הוּא": {"def": "he, it", "pos": "pronoun", "translit": "hûʾ", "root": "h-w-ʾ"},
    "הִיא": {"def": "she, it", "pos": "pronoun", "translit": "hîʾ", "root": "h-y-ʾ"},
    "אֲנַחְנָא": {"def": "we", "pos": "pronoun", "translit": "ʾănaḥnāʾ", "root": "ʾ-n-ḥ"},
    "אִנּוּן": {"def": "they (masculine)", "pos": "pronoun", "translit": "ʾinnûn", "root": "ʾ-n"},
    "אִנִּין": {"def": "they (feminine)", "pos": "pronoun", "translit": "ʾinnîn", "root": "ʾ-n"},
    "הֲדָא": {"def": "this (masculine)", "pos": "demonstrative", "translit": "hăḏāʾ", "root": "h-ḏ-ʾ"},
    "הָדֵא": {"def": "this (feminine)", "pos": "demonstrative", "translit": "hāḏēʾ", "root": "h-ḏ-ʾ"},
    "אֵלֶּה": {"def": "these", "pos": "demonstrative", "translit": "ʾēlleh", "root": "ʾ-l-h"},
    
    # Divine Names
    "אֱלָהָא": {"def": "God", "pos": "noun", "translit": "ʾĕlāhāʾ", "root": "ʾ-l-h"},
    "אֱלָהֵהּ": {"def": "his God", "pos": "noun", "translit": "ʾĕlāhēh", "root": "ʾ-l-h"},
    "מָרֵא": {"def": "lord, master", "pos": "noun", "translit": "mārēʾ", "root": "m-r-ʾ"},
    "מַלְכוּתָא": {"def": "kingdom", "pos": "noun", "translit": "malkûṯāʾ", "root": "m-l-k"},
    "מֶלֶךְ": {"def": "king", "pos": "noun", "translit": "meleḵ", "root": "m-l-k"},
    "מַלְאֲכָא": {"def": "angel, messenger", "pos": "noun", "translit": "malʾăḵāʾ", "root": "m-l-ʾ"},
    "בְּרִי": {"def": "son", "pos": "noun", "translit": "bərî", "root": "b-r"},
    "אַבָּא": {"def": "father (emphatic)", "pos": "noun", "translit": "ʾabbāʾ", "root": "ʾ-b"},
    "רוּחַ": {"def": "spirit, wind", "pos": "noun", "translit": "rûaḥ", "root": "r-w-ḥ"},
    "קְדָם": {"def": "before, ancient", "pos": "preposition/adjective", "translit": "qəḏām", "root": "q-d-m"},
    "שְׁמַיָּא": {"def": "heavens", "pos": "noun", "translit": "šəmayyāʾ", "root": "š-m-y"},
    "אַרְעָא": {"def": "earth, land", "pos": "noun", "translit": "ʾarʿāʾ", "root": "ʾ-r-ʿ"},
    
    # Common Nouns
    "אֱנָשָׁא": {"def": "man, human", "pos": "noun", "translit": "ʾĕnāšāʾ", "root": "ʾ-n-š"},
    "גְּבַר": {"def": "man, male", "pos": "noun", "translit": "gəḇar", "root": "g-b-r"},
    "אַנְתָּה": {"def": "you (emphatic)", "pos": "pronoun", "translit": "ʾanṯāh", "root": "ʾ-n-ṯ"},
    "בַּיִת": {"def": "house", "pos": "noun", "translit": "bayiṯ", "root": "b-y-ṯ"},
    "דּוּכְרָן": {"def": "memory, mention", "pos": "noun", "translit": "dûḵrān", "root": "d-k-r"},
    "מִלְּתָא": {"def": "word, matter", "pos": "noun", "translit": "milləṯāʾ", "root": "m-l-ʾ"},
    "פֶּה": {"def": "mouth", "pos": "noun", "translit": "peh", "root": "p-h"},
    "עַיִן": {"def": "eye", "pos": "noun", "translit": "ʿayin", "root": "ʿ-y-n"},
    "אָזְנָא": {"def": "ear", "pos": "noun", "translit": "ʾoznāʾ", "root": "ʾ-z-n"},
    "יַד": {"def": "hand", "pos": "noun", "translit": "yaḏ", "root": "y-d"},
    "רֵאשׁ": {"def": "head", "pos": "noun", "translit": "rēš", "root": "r-ʾ-š"},
    "לֵב": {"def": "heart", "pos": "noun", "translit": "lēḇ", "root": "l-ḇ-ḇ"},
    "דָּם": {"def": "blood", "pos": "noun", "translit": "dām", "root": "d-m"},
    "בְּשַׂר": {"def": "flesh", "pos": "noun", "translit": "bəśar", "root": "b-ś-r"},
    "גְּשַׁם": {"def": "rain", "pos": "noun", "translit": "gəšam", "root": "g-š-m"},
    "מַיִן": {"def": "water", "pos": "noun", "translit": "mayin", "root": "m-y-n"},
    "נוּרָא": {"def": "fire", "pos": "noun", "translit": "nûrāʾ", "root": "n-w-r"},
    "אִילָן": {"def": "tree", "pos": "noun", "translit": "ʾîlān", "root": "ʾ-y-l"},
    "דְּרָךְ": {"def": "way, road", "pos": "noun", "translit": "dərāḵ", "root": "d-r-k"},
    "קְבֵל": {"def": "presence, before", "pos": "noun", "translit": "qəḇēl", "root": "q-ḇ-l"},
    "דָּת": {"def": "law, decree", "pos": "noun", "translit": "dāṯ", "root": "d-ṯ"},
    "טְעֵם": {"def": "taste, judgment", "pos": "noun", "translit": "ṭəʿēm", "root": "ṭ-ʿ-m"},
    "צְלֵם": {"def": "image, likeness", "pos": "noun", "translit": "ṣəlēm", "root": "ṣ-l-m"},
    "כְּתָב": {"def": "writing, inscription", "pos": "noun", "translit": "kəṯāḇ", "root": "k-ṯ-ḇ"},
    "סְפַר": {"def": "book, scroll", "pos": "noun", "translit": "səfar", "root": "s-f-r"},
    
    # Verbs
    "אֲמַר": {"def": "to say", "pos": "verb", "translit": "ʾămar", "root": "ʾ-m-r"},
    "הֲוָה": {"def": "to be, become", "pos": "verb", "translit": "hăwāh", "root": "h-w-h"},
    "עֲבַד": {"def": "to do, make, serve", "pos": "verb", "translit": "ʿăḇaḏ", "root": "ʿ-ḇ-ḏ"},
    "יְדַע": {"def": "to know", "pos": "verb", "translit": "yəḏaʿ", "root": "y-d-ʿ"},
    "חֲזָה": {"def": "to see", "pos": "verb", "translit": "ḥăzāh", "root": "ḥ-z-h"},
    "שְׁמַע": {"def": "to hear", "pos": "verb", "translit": "šəmaʿ", "root": "š-m-ʿ"},
    "יְהַב": {"def": "to give", "pos": "verb", "translit": "yəhaḇ", "root": "y-h-ḇ"},
    "נְסַב": {"def": "to take, receive", "pos": "verb", "translit": "nəsaḇ", "root": "n-s-ḇ"},
    "אֲתָה": {"def": "to come", "pos": "verb", "translit": "ʾăṯāh", "root": "ʾ-ṯ-h"},
    "אֲזַל": {"def": "to go", "pos": "verb", "translit": "ʾăzal", "root": "ʾ-z-l"},
    "נְפַל": {"def": "to fall", "pos": "verb", "translit": "nəfal", "root": "n-f-l"},
    "קוּם": {"def": "to rise, stand", "pos": "verb", "translit": "qûm", "root": "q-w-m"},
    "עֲלָה": {"def": "to go up", "pos": "verb", "translit": "ʿălāh", "root": "ʿ-l-h"},
    "נְחֵת": {"def": "to go down", "pos": "verb", "translit": "nəḥēṯ", "root": "n-ḥ-ṯ"},
    "חַיַי": {"def": "to live", "pos": "verb", "translit": "ḥayay", "root": "ḥ-y-y"},
    "מַיַת": {"def": "to die", "pos": "verb", "translit": "mayaṯ", "root": "m-w-ṯ"},
    "גְּנַז": {"def": "to hide, treasure", "pos": "verb", "translit": "gənaz", "root": "g-n-z"},
    "חֲסַד": {"def": "to be merciful", "pos": "verb", "translit": "ḥăsaḏ", "root": "ḥ-s-d"},
    "טְעַן": {"def": "to load, carry", "pos": "verb", "translit": "ṭəʿan", "root": "ṭ-ʿ-n"},
    "פְּתַח": {"def": "to open", "pos": "verb", "translit": "pəṯaḥ", "root": "p-ṯ-ḥ"},
    "סְגַר": {"def": "to shut, close", "pos": "verb", "translit": "səgar", "root": "s-g-r"},
    "שְׁכַב": {"def": "to lie down", "pos": "verb", "translit": "šəḵaḇ", "root": "š-ḵ-ḇ"},
    "חֲזַק": {"def": "to be strong", "pos": "verb", "translit": "ḥăzaq", "root": "ḥ-z-q"},
    "בְּנָה": {"def": "to build", "pos": "verb", "translit": "bənāh", "root": "b-n-h"},
    "קְטַל": {"def": "to kill", "pos": "verb", "translit": "qəṭal", "root": "q-ṭ-l"},
    
    # Prepositions
    "בְּ": {"def": "in, with, by", "pos": "preposition", "translit": "bə", "root": "b"},
    "לְ": {"def": "to, for, of", "pos": "preposition", "translit": "lə", "root": "l"},
    "מִן": {"def": "from, out of", "pos": "preposition", "translit": "min", "root": "m-n"},
    "עַל": {"def": "upon, over, against", "pos": "preposition", "translit": "ʿal", "root": "ʿ-l"},
    "תְּחוֹת": {"def": "under, beneath", "pos": "preposition", "translit": "təḥôṯ", "root": "ṯ-ḥ-ṯ"},
    "לְקֳבֵל": {"def": "before, in front of", "pos": "preposition", "translit": "ləqŏḇēl", "root": "q-ḇ-l"},
    "בָּתוֹךְ": {"def": "in the midst of", "pos": "preposition", "translit": "bāṯôḵ", "root": "b-ṯ-ḵ"},
    "כְּ": {"def": "like, as", "pos": "preposition", "translit": "kə", "root": "k"},
    "עַד": {"def": "until, as far as", "pos": "preposition", "translit": "ʿaḏ", "root": "ʿ-ḏ"},
    "בֵּין": {"def": "between", "pos": "preposition", "translit": "bēn", "root": "b-y-n"},
    
    # Conjunctions
    "וְ": {"def": "and", "pos": "conjunction", "translit": "wə", "root": "w"},
    "אֲלָא": {"def": "but, however", "pos": "conjunction", "translit": "ʾălāʾ", "root": "ʾ-l"},
    "דִּי": {"def": "that, because, which", "pos": "conjunction", "translit": "dî", "root": "d"},
    "כָּל־קְבֵל": {"def": "therefore", "pos": "conjunction", "translit": "kāl-qəḇēl", "root": "k-l; q-ḇ-l"},
    "אִם": {"def": "if", "pos": "conjunction", "translit": "ʾim", "root": "ʾ-m"},
    "אוֹ": {"def": "or", "pos": "conjunction", "translit": "ʾô", "root": "ʾ"},
    
    # Negatives
    "לָא": {"def": "no, not", "pos": "negative", "translit": "lāʾ", "root": "l-ʾ"},
    "אֱלָא": {"def": "except, but", "pos": "negative", "translit": "ʾĕlāʾ", "root": "ʾ-l"},
    
    # Adjectives
    "טָב": {"def": "good", "pos": "adjective", "translit": "ṭāḇ", "root": "ṭ-ḇ"},
    "רַב": {"def": "great, many", "pos": "adjective", "translit": "raḇ", "root": "r-ḇ"},
    "זְעֵיר": {"def": "small, little", "pos": "adjective", "translit": "zəʿēr", "root": "z-ʿ-r"},
    "קַדִּישׁ": {"def": "holy", "pos": "adjective", "translit": "qadiš", "root": "q-d-š"},
    "יַקִּיר": {"def": "precious, heavy", "pos": "adjective", "translit": "yaqqîr", "root": "y-q-r"},
    "חֲשִׁיב": {"def": "important, worthy", "pos": "adjective", "translit": "ḥăšîḇ", "root": "ḥ-š-ḇ"},
    "כֵּן": {"def": "true, right", "pos": "adjective", "translit": "kēn", "root": "k-n"},
    "מְהַחֲזֵה": {"def": "visible, conspicuous", "pos": "adjective", "translit": "məhaḥăzēh", "root": "ḥ-z-h"},
    
    # Numbers
    "חַד": {"def": "one", "pos": "numeral", "translit": "ḥaḏ", "root": "ḥ-d"},
    "תְּרֵין": {"def": "two", "pos": "numeral", "translit": "tərēn", "root": "t-r-n"},
    "תְּלָתָא": {"def": "three", "pos": "numeral", "translit": "təlāṯāʾ", "root": "t-l-ṯ"},
    "אַרְבַּע": {"def": "four", "pos": "numeral", "translit": "ʾarbaʿ", "root": "ʾ-r-b-ʿ"},
    "חֲמִשָּׁא": {"def": "five", "pos": "numeral", "translit": "ḥămiššāʾ", "root": "ḥ-m-š"},
    
    # Particles
    "הֵיךְ": {"def": "how?", "pos": "particle", "translit": "hêḵ", "root": "h-y-ḵ"},
    "לְמָא": {"def": "why?", "pos": "particle", "translit": "ləmāʾ", "root": "l-m"},
    "אֱדַיִן": {"def": "then", "pos": "particle", "translit": "ʾĕḏayin", "root": "ʾ-ḏ-y"},
    "כְּעֶת": {"def": "now", "pos": "particle", "translit": "kəʿeṯ", "root": "k-ʿ-ṯ"},
    "בַּאדַיִן": {"def": "then, afterwards", "pos": "particle", "translit": "baʾḏayin", "root": "ʾ-ḏ-y"},
}

# Extended vocabulary - New Testament Aramaisms and Peshitta
ARAMAIC_EXTENDED_VOCABULARY = {
    # NT Aramaic terms (Jesus' words)
    "אֲבָא": {"def": "father (Jesus' Aramaic)", "pos": "noun", "translit": "ʾăḇāʾ", "root": "ʾ-b", "note": "Mark 14:36, Abba Father"},
    "טַלִיתָא": {"def": "little girl", "pos": "noun", "translit": "ṭalîṯāʾ", "root": "ṭ-l-ṯ", "note": "Mark 5:41, Talitha cumi"},
    "קוּמִי": {"def": "rise!", "pos": "verb", "translit": "qûmî", "root": "q-w-m", "note": "Mark 5:41"},
    "אֶפְפַתַח": {"def": "be opened!", "pos": "verb", "translit": "ʾep̱paṯaḥ", "root": "p-ṯ-ḥ", "note": "Mark 7:34, Ephphatha"},
    "מַמְּדָא": {"def": "measure", "pos": "noun", "translit": "mammədāʾ", "root": "m-d-d", "note": "Matthew 23:32"},
    "גְּבוּרְתָּא": {"def": "power, might", "pos": "noun", "translit": "gəḇûrəṯāʾ", "root": "g-b-r", "note": "Matthew 6:13"},
    "חֵילָא": {"def": "wealth, strength", "pos": "noun", "translit": "ḥêlāʾ", "root": "ḥ-y-l", "note": "Matthew 6:13, power"},
    "מַלְכוּתָךְ": {"def": "your kingdom", "pos": "noun", "translit": "malkûṯāḵ", "root": "m-l-k", "note": "Lord's Prayer"},
    "תֵּאתֵא": {"def": "let come", "pos": "verb", "translit": "têʾṯēʾ", "root": "ʾ-ṯ-h", "note": "Lord's Prayer, thy kingdom come"},
    
    # Daniel/Ezra specific
    "פְּשַׁר": {"def": "interpretation", "pos": "noun", "translit": "pəšar", "root": "p-š-r"},
    "חֶלְמָא": {"def": "dream", "pos": "noun", "translit": "ḥelmāʾ", "root": "ḥ-l-m"},
    "חָזוּ": {"def": "vision", "pos": "noun", "translit": "ḥāzû", "root": "ḥ-z-h"},
    "סוֹף": {"def": "end", "pos": "noun", "translit": "sôp̱", "root": "s-w-p̱"},
    "זְמָן": {"def": "time", "pos": "noun", "translit": "zəmān", "root": "z-m-n"},
    "עִדָּן": {"def": "time, season", "pos": "noun", "translit": "ʿiddān", "root": "ʿ-d-n"},
    "דָּא": {"def": "this (demonstrative)", "pos": "demonstrative", "translit": "dāʾ", "root": "d"},
    "לָקֳבֵל": {"def": "according to", "pos": "preposition", "translit": "lāqŏḇēl", "root": "q-ḇ-l"},
    "וּמְדָן": {"def": "and judgment", "pos": "noun", "translit": "ûməḏān", "root": "d-y-n"},
    "צְדָקָה": {"def": "righteousness", "pos": "noun", "translit": "ṣəḏāqāh", "root": "ṣ-d-q"},
    
    # More common words
    "חֲכִים": {"def": "wise", "pos": "adjective", "translit": "ḥăḵîm", "root": "ḥ-ḵ-m"},
    "גְּבַרְתָּא": {"def": "mistress, lady", "pos": "noun", "translit": "gəḇarṯāʾ", "root": "g-b-r"},
    "אַנְתּוּן": {"def": "you (plural)", "pos": "pronoun", "translit": "ʾantûn", "root": "ʾ-n-ṯ"},
    "בְּנָא": {"def": "built (passive participle)", "pos": "adjective", "translit": "bənāʾ", "root": "b-n-h"},
    "גְּדַבַר": {"def": "to speak", "pos": "verb", "translit": "gəḏaḇar", "root": "d-ḇ-r"},
    "הוּדַע": {"def": "to inform", "pos": "verb", "translit": "hûḏaʿ", "root": "y-d-ʿ"},
    "מֵישְׁר": {"def": "uprightness", "pos": "noun", "translit": "mêšar", "root": "y-š-r"},
    "רְמָא": {"def": "to throw", "pos": "verb", "translit": "rəmāʾ", "root": "r-m-ʾ"},
    "תְּרוּם": {"def": "to rise", "pos": "verb", "translit": "tərûm", "root": "r-w-m"},
    "נְבַעַת": {"def": "to burst forth", "pos": "verb", "translit": "nəbaʿaṯ", "root": "n-b-ʿ"},
    "אֲחַשְׁדַּרְפְּנַיָּא": {"def": "satraps", "pos": "noun", "translit": "ʾăḥašdarpənnayyāʾ", "root": "Persian loan"},
    "עֵט": {"def": "counsel", "pos": "noun", "translit": "ʿēṭ", "root": "ʿ-y-ṭ"},
    "נְזִיד": {"def": "pulse, food", "pos": "noun", "translit": "nəzîḏ", "root": "n-z-d"},
    "טָל": {"def": "dew", "pos": "noun", "translit": "ṭāl", "root": "ṭ-l"},
    "רְעוּת": {"def": "will, desire", "pos": "noun", "translit": "rəʿûṯ", "root": "r-ʿ-h"},
    "כְּנֵמָא": {"def": "thus", "pos": "adverb", "translit": "kənēmāʾ", "root": "k-n-m"},
    "עַל־יְדֵי": {"def": "by the hand of", "pos": "preposition", "translit": "ʿal-yəḏê", "root": "ʿ-l; y-d"},
}

class AramaicLexicon:
    """Aramaic-English lexicon"""
    
    def __init__(self):
        self.entries = {}
        self.root_index = defaultdict(list)
        
    def build(self):
        """Build lexicon from vocabulary lists"""
        print("[*] Building Aramaic lexicon...")
        
        # Combine vocabularies
        all_vocab = {**ARAMAIC_CORE_VOCABULARY, **ARAMAIC_EXTENDED_VOCABULARY}
        
        for word, data in all_vocab.items():
            entry = {
                "word": word,
                "definition": data["def"],
                "part_of_speech": data["pos"],
                "transliteration": data["translit"],
                "root": data["root"]
            }
            
            # Add notes if present
            if "note" in data:
                entry["note"] = data["note"]
            
            self.entries[word] = entry
            
            # Index by root
            if data["root"]:
                for root_part in data["root"].split(";"):
                    self.root_index[root_part.strip()].append(word)
        
        print(f"    [+] Built {len(self.entries)} entries")
        
    def export_json(self, output_path: str):
        """Export to JSON"""
        print(f"[*] Exporting to {output_path}...")
        
        data = {
            "metadata": {
                "title": "Aramaic Lexicon",
                "language": "Aramaic (Biblical and Galilean)",
                "script": "Hebrew (square script)",
                "period": "Biblical (600-400 BCE), Galilean (Jesus' era, 30 CE)",
                "total_entries": len(self.entries),
                "format": "JSON",
                "notes": "Biblical Aramaic from Daniel/Ezra. Jesus spoke Galilean Aramaic. Includes NT Aramaic terms."
            },
            "entries": self.entries,
            "root_index": dict(self.root_index)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"    [+] Exported {len(self.entries)} entries")
    
    def export_markdown(self, output_path: str):
        """Export to Markdown"""
        print(f"[*] Exporting markdown to {output_path}...")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Aramaic Lexicon\n\n")
            f.write("**Aramaic-English Dictionary (Biblical and Galilean)**\n\n")
            f.write(f"Total Entries: {len(self.entries)}\n\n")
            f.write("---\n\n")
            
            # Sort by Aramaic word
            sorted_entries = sorted(self.entries.items(), key=lambda x: x[0])
            
            for word, entry in sorted_entries:
                f.write(f"## {word}\n\n")
                f.write(f"**Transliteration:** *{entry['transliteration']}*\n\n")
                f.write(f"**Part of Speech:** {entry['part_of_speech']}\n\n")
                f.write(f"**Definition:** {entry['definition']}\n\n")
                if entry['root']:
                    f.write(f"**Root:** {entry['root']}\n\n")
                if "note" in entry:
                    f.write(f"**Note:** {entry['note']}\n\n")
                f.write("---\n\n")
        
        print(f"    [+] Exported {len(self.entries)} entries")
    
    def export_websters_style(self, output_path: str):
        """Export in Webster's dictionary format"""
        print(f"[*] Exporting Webster's style to {output_path}...")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("ARAMAIC LEXICON\n")
            f.write("Biblical and Galilean Aramaic Dictionary\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("About Aramaic:\n")
            f.write("  - Semitic language (like Hebrew and Arabic)\n")
            f.write("  - Jesus' spoken language (Galilean dialect)\n")
            f.write("  - Biblical Aramaic in Daniel (ch. 2-7) and Ezra\n")
            f.write("  - Written in Hebrew script (square letters)\n")
            f.write("  - Triliteral root system\n\n")
            
            f.write("Pronunciation Guide:\n")
            f.write("  ʾ = glottal stop (like uh-oh)\n")
            f.write("  ḥ/ḫ = voiceless pharyngeal (like Scottish loch)\n")
            f.write("  ʿ = voiced pharyngeal\n")
            f.write("  ṣ/ṣ = emphatic s\n")
            f.write("  ṭ = emphatic t\n")
            f.write("  ā = long a, ē = long e, ō = long o\n\n")
            
            f.write("-" * 70 + "\n\n")
            
            sorted_entries = sorted(self.entries.items(), key=lambda x: x[0])
            
            for word, entry in sorted_entries:
                f.write(f"\n{word}")
                if entry['transliteration']:
                    f.write(f"  ({entry['transliteration']})")
                
                f.write(f"  [{entry['part_of_speech']}]")
                f.write("\n")
                
                # Definition
                f.write(f"    {entry['definition']}\n")
                
                # Root
                if entry['root']:
                    f.write(f"    Root: {entry['root']}\n")
                
                # Note
                if "note" in entry:
                    f.write(f"    Note: {entry['note']}\n")
                
                f.write("\n")
        
        print(f"    [+] Exported {len(self.entries)} entries")
    
    def search(self, query: str) -> list:
        """Search the lexicon"""
        results = []
        query_lower = query.lower()
        
        for word, entry in self.entries.items():
            match = False
            
            if query_lower in word.lower():
                match = True
            elif query_lower in entry['definition'].lower():
                match = True
            elif query_lower in entry['transliteration'].lower():
                match = True
            elif query_lower in entry['root'].lower():
                match = True
            
            if match:
                results.append((word, entry))
        
        return results


def main():
    lexicon = AramaicLexicon()
    
    # Build from vocabulary
    lexicon.build()
    
    # Create output directory
    out_dir = Path("/root/aramaic_lexicon_output")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Export all formats
    lexicon.export_json(out_dir / "aramaic_lexicon.json")
    lexicon.export_markdown(out_dir / "aramaic_lexicon.md")
    lexicon.export_websters_style(out_dir / "websters_aramaic.txt")
    
    # Sample entries
    print("\n" + "=" * 70)
    print("SAMPLE ENTRIES")
    print("=" * 70 + "\n")
    
    sample_words = ['אֱלָהָא', 'אֲבָא', 'יְשׁוּע', 'שְׁמַע', 'מַלְכוּתָא', 'שְׁלָם']
    for word in sample_words:
        if word in lexicon.entries:
            e = lexicon.entries[word]
            print(f"{word} ({e['transliteration']})")
            print(f"  {e['definition']}")
            print(f"  [{e['part_of_speech']}] Root: {e['root']}\n")
    
    print("=" * 70)
    print("ARAMAIC LEXICON COMPLETE")
    print("=" * 70)
    print(f"\nOutput files in {out_dir.absolute()}:")
    print(f"  - aramaic_lexicon.json (full)")
    print(f"  - aramaic_lexicon.md (human-readable)")
    print(f"  - websters_aramaic.txt (Webster's style)")
    print(f"\nTo search: python search_aramaic.py <word>")


if __name__ == "__main__":
    main()
