#!/usr/bin/env python3
"""
Coptic Lexicon Builder
Builds a Coptic-English dictionary from available sources
"""
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

# Core Coptic vocabulary - foundational words from Nag Hammadi and biblical texts
# This is a seed lexicon that can be expanded
COPTIC_CORE_VOCABULARY = {
    # Articles
    "ⲡ": {"def": "the (masculine singular article)", "pos": "article", "translit": "p", "origin": "pi"},
    "ⲧ": {"def": "the (feminine singular article)", "pos": "article", "translit": "t", "origin": "tau"},
    "ⲛ": {"def": "the (plural article)", "pos": "article", "translit": "n", "origin": "nu"},
    "ⲟⲩ": {"def": "a, an (indefinite article)", "pos": "article", "translit": "ou", "origin": "Greek: οὐ"},
    "ⲡⲉⲓ": {"def": "this (masculine)", "pos": "demonstrative", "translit": "pei", "origin": "pi + ei"},
    "ⲧⲉⲓ": {"def": "this (feminine)", "pos": "demonstrative", "translit": "tei", "origin": "tau + ei"},
    "ⲛⲉⲓ": {"def": "these (plural)", "pos": "demonstrative", "translit": "nei", "origin": "nu + ei"},
    
    # Personal pronouns
    "ⲁⲛⲟⲕ": {"def": "I, me", "pos": "pronoun", "translit": "anok", "origin": "Egyptian"},
    "ⲛⲧⲟⲕ": {"def": "you (masculine singular)", "pos": "pronoun", "translit": "ntok", "origin": "Egyptian"},
    "ⲛⲧⲟ": {"def": "you (feminine singular)", "pos": "pronoun", "translit": "nto", "origin": "Egyptian"},
    "ⲛⲧⲟⲩ": {"def": "you (plural)", "pos": "pronoun", "translit": "ntou", "origin": "Egyptian"},
    "ⲛⲧⲟϥ": {"def": "he, him", "pos": "pronoun", "translit": "ntof", "origin": "Egyptian"},
    "ⲛⲧⲟⲥ": {"def": "she, her", "pos": "pronoun", "translit": "ntos", "origin": "Egyptian"},
    "ⲛⲧⲟⲟⲩ": {"def": "they, them", "pos": "pronoun", "translit": "ntoou", "origin": "Egyptian"},
    
    # Common nouns
    "ⲣⲱⲙⲉ": {"def": "man, person", "pos": "noun", "translit": "rōme", "origin": "Egyptian rmṯ"},
    "ⲥϩⲓⲙⲉ": {"def": "woman", "pos": "noun", "translit": "shime", "origin": "Egyptian ẖmt"},
    "ϣⲏⲣⲉ": {"def": "son, child", "pos": "noun", "translit": "shēre", "origin": "Egyptian šr"},
    "ⲥⲟⲛ": {"def": "brother", "pos": "noun", "translit": "son", "origin": "Greek: ἀδελφός"},
    "ⲥⲱⲛⲉ": {"def": "sister", "pos": "noun", "translit": "sōne", "origin": "Greek: ἀδελφή"},
    "ⲉⲓⲱⲧ": {"def": "father", "pos": "noun", "translit": "eitōt", "origin": "Egyptian it"},
    "ⲙⲁⲁⲩ": {"def": "mother", "pos": "noun", "translit": "maau", "origin": "Egyptian mw.t"},
    "ϩⲏⲧ": {"def": "heart", "pos": "noun", "translit": "hēt", "origin": "Egyptian ḥꜣt"},
    "ⲣⲁϣⲉ": {"def": "joy, gladness", "pos": "noun", "translit": "rashe", "origin": "Egyptian ršw"},
    "ⲙⲟⲩⲛ": {"def": "water", "pos": "noun", "translit": "moun", "origin": "Egyptian mw"},
    "ⲣⲏ": {"def": "sun", "pos": "noun", "translit": "rē", "origin": "Egyptian rꜥ"},
    "ⲡⲉ": {"def": "heaven, sky", "pos": "noun", "translit": "pe", "origin": "Egyptian pt"},
    "ⲕⲁϩ": {"def": "earth, land", "pos": "noun", "translit": "kah", "origin": "Egyptian tꜣ"},
    "ϩⲱⲃ": {"def": "thing, matter", "pos": "noun", "translit": "hōb", "origin": "Egyptian ḫt"},
    "ϩⲟⲓⲛⲉ": {"def": "road, way", "pos": "noun", "translit": "hoine", "origin": "Egyptian wꜣt"},
    "ⲙⲛⲧ": {"def": "nature, condition, -ness", "pos": "noun", "translit": "mnt", "origin": "Egyptian mnt"},
    "ⲡⲛⲉⲩⲙⲁ": {"def": "spirit, breath, wind", "pos": "noun", "translit": "pneuma", "origin": "Greek: πνεῦμα"},
    "ⲯⲩⲭⲏ": {"def": "soul", "pos": "noun", "translit": "psychē", "origin": "Greek: ψυχή"},
    "ⲥⲁⲣⲝ": {"def": "flesh", "pos": "noun", "translit": "sarx", "origin": "Greek: σάρξ"},
    "ⲥⲱⲙⲁ": {"def": "body", "pos": "noun", "translit": "sōma", "origin": "Greek: σῶμα"},
    
    # Verbs
    "ⲉⲓ": {"def": "to come", "pos": "verb", "translit": "ei", "origin": "Egyptian ii"},
    "ⲃⲱⲕ": {"def": "to go, walk", "pos": "verb", "translit": "bōk", "origin": "Egyptian bk"},
    "ϩⲱⲥ": {"def": "to speak, say", "pos": "verb", "translit": "hōs", "origin": "Egyptian ḏd"},
    "ϯ": {"def": "to give", "pos": "verb", "translit": "ti", "origin": "Egyptian di"},
    "ϫⲓ": {"def": "to take, receive", "pos": "verb", "translit": "ji", "origin": "Egyptian ḫi"},
    "ⲙⲟⲩⲧⲉ": {"def": "to call", "pos": "verb", "translit": "moute", "origin": "Egyptian mwt"},
    "ⲛⲁⲩ": {"def": "to see", "pos": "verb", "translit": "nau", "origin": "Egyptian mꜣꜣ"},
    "ⲥⲱⲧⲙ": {"def": "to hear", "pos": "verb", "translit": "sōtm", "origin": "Egyptian sḏm"},
    "ⲙⲟⲟⲩⲧⲉ": {"def": "to kill", "pos": "verb", "translit": "mooute", "origin": "Egyptian mwt"},
    "ⲱⲛϩ": {"def": "to live", "pos": "verb", "translit": "ōnh", "origin": "Egyptian ꜥnḫ"},
    "ⲙⲟⲩ": {"def": "to die", "pos": "verb", "translit": "mou", "origin": "Egyptian mwt"},
    "ϣⲱⲡⲉ": {"def": "to become, be", "pos": "verb", "translit": "shōpe", "origin": "Egyptian ḫpr"},
    "ⲉⲓⲣⲉ": {"def": "to do, make", "pos": "verb", "translit": "eire", "origin": "Egyptian ir"},
    "ⲙⲉ": {"def": "to love", "pos": "verb", "translit": "me", "origin": "Egyptian mr"},
    "ⲥⲟⲟⲩⲛ": {"def": "to know", "pos": "verb", "translit": "sooun", "origin": "Egyptian rh"},
    "ϩⲓ": {"def": "to throw, cast", "pos": "verb", "translit": "hi", "origin": "Egyptian hi"},
    
    # Prepositions
    "ϩⲛ": {"def": "in, at, by (prefix)", "pos": "preposition", "translit": "hn", "origin": "Egyptian m"},
    "ⲉ": {"def": "to, toward, for", "pos": "preposition", "translit": "e", "origin": "Egyptian r"},
    "ⲛ": {"def": "of, by (genitive)", "pos": "preposition", "translit": "n", "origin": "Egyptian n"},
    "ϩⲓ": {"def": "under, through, by", "pos": "preposition", "translit": "hi", "origin": "Egyptian ḥr"},
    "ⲙⲛ": {"def": "with, and", "pos": "preposition", "translit": "mn", "origin": "Egyptian ḥnꜥ"},
    "ϩⲁ": {"def": "with, by, near", "pos": "preposition", "translit": "ha", "origin": "Egyptian ḥꜣ"},
    "ϩⲓⲧⲛ": {"def": "through, by means of", "pos": "preposition", "translit": "hitn", "origin": "Greek"},
    "ⲕⲁⲧⲁ": {"def": "according to", "pos": "preposition", "translit": "kata", "origin": "Greek: κατά"},
    
    # Conjunctions
    "ⲁⲩⲱ": {"def": "and", "pos": "conjunction", "translit": "auō", "origin": "Greek: αὐτός"},
    "ⲇⲉ": {"def": "but, and, now", "pos": "conjunction", "translit": "de", "origin": "Greek: δέ"},
    "ϫⲉ": {"def": "that, for, because", "pos": "conjunction", "translit": "je", "origin": "Egyptian ntt"},
    "ϩⲱⲥ": {"def": "until, when", "pos": "conjunction", "translit": "hōs", "origin": "Greek: ἕως"},
    "ⲉⲧⲃⲉ": {"def": "because, since", "pos": "conjunction", "translit": "etbe", "origin": "Egyptian"},
    "ⲏ": {"def": "or", "pos": "conjunction", "translit": "ē", "origin": "Greek: ἤ"},
    "ⲉⲓⲧⲉ": {"def": "if", "pos": "conjunction", "translit": "eite", "origin": "Greek: εἴτε"},
    
    # Negatives
    "ⲛ": {"def": "not (present)", "pos": "negative", "translit": "n", "origin": "Egyptian nn"},
    "ⲙⲡⲉ": {"def": "not (past)", "pos": "negative", "translit": "mpe", "origin": "Egyptian n-m-ir"},
    
    # Numbers
    "ⲟⲩⲁ": {"def": "one", "pos": "numeral", "translit": "oua", "origin": "Egyptian waꜥ"},
    "ⲥⲛⲁⲩ": {"def": "two", "pos": "numeral", "translit": "snau", "origin": "Egyptian snwj"},
    "ϣⲟⲙⲛ̄ⲧ": {"def": "three", "pos": "numeral", "translit": "shomnt", "origin": "Egyptian ḫmt"},
    "ϥⲧⲟⲟⲩ": {"def": "four", "pos": "numeral", "translit": "ftoou", "origin": "Egyptian jfdw"},
    "ⲧⲓⲟⲩ": {"def": "five", "pos": "numeral", "translit": "tiou", "origin": "Egyptian djwf"},
    
    # Divine names
    "ⲛⲟⲩⲧⲉ": {"def": "God", "pos": "noun", "translit": "noute", "origin": "Egyptian nṯr"},
    "ⲓⲥ": {"def": "Jesus", "pos": "proper noun", "translit": "is", "origin": "Greek: Ἰησοῦς"},
    "ⲭⲣⲓⲥⲧⲟⲥ": {"def": "Christ", "pos": "proper noun", "translit": "christos", "origin": "Greek: Χριστός"},
    "ⲡⲛⲟⲩⲧⲉ": {"def": "the God", "pos": "proper noun", "translit": "pnoute", "origin": "ⲡ + ⲛⲟⲩⲧⲉ"},
    "ⲙⲁⲣⲓⲁ": {"def": "Mary", "pos": "proper noun", "translit": "maria", "origin": "Greek: Μαρία"},
    "ⲡⲁⲩⲗⲟⲥ": {"def": "Paul", "pos": "proper noun", "translit": "paulos", "origin": "Greek: Παῦλος"},
    "ⲡⲉⲧⲣⲟⲥ": {"def": "Peter", "pos": "proper noun", "translit": "petros", "origin": "Greek: Πέτρος"},
    
    # Common adjectives
    "ⲛⲟⲃⲉ": {"def": "bad, evil", "pos": "adjective", "translit": "nobe", "origin": "Egyptian bin"},
    "ⲛⲁⲛⲟⲩⲃ": {"def": "good, beautiful", "pos": "adjective", "translit": "nanoub", "origin": "Egyptian nfr"},
    "ⲛⲓⲙ": {"def": "small, little", "pos": "adjective", "translit": "nim", "origin": "Egyptian nḏs"},
    "ⲟⲩⲟⲓ": {"def": "great, big", "pos": "adjective", "translit": "ouoi", "origin": "Greek: πολύς"},
    "ⲕⲟⲩⲓ": {"def": "small, young", "pos": "adjective", "translit": "koui", "origin": "Greek: μικρός"},
    "ⲥⲟⲩ": {"def": "first", "pos": "adjective", "translit": "sou", "origin": "Egyptian tp"},
    "ⲥⲛⲟⲟⲩⲥ": {"def": "last", "pos": "adjective", "translit": "snoous", "origin": "Egyptian ḥr"},
    "ϩⲁⲑ": {"def": "exalted", "pos": "adjective", "translit": "hath", "origin": "Egyptian šꜣi"},
    "ⲟⲩⲁⲁⲃ": {"def": "holy", "pos": "adjective", "translit": "ouaab", "origin": "Egyptian wꜥb"},
    
    # Gospel of Thomas specific
    "ϫⲉ": {"def": "saying, word", "pos": "noun", "translit": "je", "origin": "Coptic"},
    "ⲥⲁϩⲛⲉ": {"def": "truth", "pos": "noun", "translit": "sahne", "origin": "Egyptian mꜣꜣt"},
    "ⲥⲟⲫⲓⲁ": {"def": "wisdom", "pos": "noun", "translit": "sophia", "origin": "Greek: σοφία"},
    "ⲅⲛⲱⲥⲓⲥ": {"def": "knowledge", "pos": "noun", "translit": "gnōsis", "origin": "Greek: γνῶσις"},
    "ⲣⲁϩⲧ": {"def": "kingdom, reign", "pos": "noun", "translit": "raht", "origin": "Egyptian nsyt"},
    
    # Gospel of Mary specific  
    "ⲛⲟϭ": {"def": "thing, matter", "pos": "noun", "translit": "noj", "origin": "Greek?"},
    "ⲁⲗⲗⲁ": {"def": "if", "pos": "conjunction", "translit": "alla", "origin": "Greek: ἀλλά"},
}

# Extended vocabulary from common Coptic texts
COPTIC_EXTENDED_VOCABULARY = {
    # More body parts
    "ϩⲟ": {"def": "face", "pos": "noun", "translit": "ho", "origin": "Egyptian ḥr"},
    "ⲧⲟⲩ": {"def": "head", "pos": "noun", "translit": "tou", "origin": "Egyptian ḏd"},
    "ϩⲟⲩⲓⲧ": {"def": "hand", "pos": "noun", "translit": "houit", "origin": "Egyptian ḏrt"},
    "ⲣⲁϩ": {"def": "foot", "pos": "noun", "translit": "rah", "origin": "Egyptian rd"},
    "ⲙⲁⲁϫⲉ": {"def": "eye", "pos": "noun", "translit": "maaje", "origin": "Egyptian jrt"},
    "ⲙⲉϩ": {"def": "thigh, side", "pos": "noun", "translit": "meh", "origin": "Egyptian mḥ"},
    "ϩⲛⲟⲩ": {"def": "voice", "pos": "noun", "translit": "hnou", "origin": "Egyptian ḥnw"},
    
    # More nature words
    "ϣⲁϣ": {"def": "tree, wood", "pos": "noun", "translit": "shash", "origin": "Egyptian št"},
    "ϩⲓⲟⲙ": {"def": "sea, lake", "pos": "noun", "translit": "hiom", "origin": "Greek: ἡ θάλασσα"},
    "ϩⲁⲉ": {"def": "field", "pos": "noun", "translit": "hae", "origin": "Egyptian sḥt"},
    "ⲣⲱ": {"def": "river", "pos": "noun", "translit": "rō", "origin": "Greek: ῥεῖν"},
    "ⲕⲏⲡⲉ": {"def": "garden", "pos": "noun", "translit": "kēpe", "origin": "Greek: κῆπος"},
    "ⲛⲟⲩⲛⲉ": {"def": "fountain, well", "pos": "noun", "translit": "noune", "origin": "Greek: πηγή"},
    
    # Time
    "ϩⲟⲟⲩ": {"def": "day", "pos": "noun", "translit": "hoou", "origin": "Egyptian hrw"},
    "ⲧⲉⲃⲛⲏ": {"def": "evening", "pos": "noun", "translit": "tebnē", "origin": "Greek: ἑσπέρα"},
    "ϩⲧⲟ": {"def": "morning", "pos": "noun", "translit": "hto", "origin": "Greek: ἑωθινός"},
    "ⲣⲟⲩϩⲉ": {"def": "day, time", "pos": "noun", "translit": "rouhe", "origin": "Egyptian tr"},
    "ⲥⲟⲟⲩ": {"def": "time, hour", "pos": "noun", "translit": "soou", "origin": "Greek: ὥρα"},
    
    # Abstract concepts
    "ⲙⲉ": {"def": "truth", "pos": "noun", "translit": "me", "origin": "Egyptian mꜣꜣt"},
    "ⲙⲛⲧⲣⲉ": {"def": "joy", "pos": "noun", "translit": "mntre", "origin": "Egyptian"},
    "ϩⲓⲥⲉ": {"def": "wound, mark", "pos": "noun", "translit": "hise", "origin": "Greek: ἕλκος"},
    "ⲥⲙⲟⲧ": {"def": "blessing", "pos": "noun", "translit": "smot", "origin": "Egyptian sḥtp"},
    "ϩⲓⲣⲏⲛⲏ": {"def": "peace", "pos": "noun", "translit": "hirēnē", "origin": "Greek: εἰρήνη"},
    "ⲁⲅⲁⲡⲏ": {"def": "love", "pos": "noun", "translit": "agapē", "origin": "Greek: ἀγάπη"},
    "ⲡⲓⲥⲧⲓⲥ": {"def": "faith", "pos": "noun", "translit": "pistis", "origin": "Greek: πίστις"},
    "ⲉⲗⲡⲓⲥ": {"def": "hope", "pos": "noun", "translit": "elpis", "origin": "Greek: ἐλπίς"},
    "ⲇⲓⲕⲁⲓⲟⲥⲩⲛⲏ": {"def": "righteousness", "pos": "noun", "translit": "dikaiosynē", "origin": "Greek: δικαιοσύνη"},
    
    # Actions
    "ⲱϣ": {"def": "to wash", "pos": "verb", "translit": "ōsh", "origin": "Egyptian wꜥb"},
    "ⲉⲓⲛⲉ": {"def": "to bring", "pos": "verb", "translit": "eine", "origin": "Egyptian jnj"},
    "ⲥⲱⲣ": {"def": "to write", "pos": "verb", "translit": "sōr", "origin": "Egyptian sšꜣ"},
    "ϣⲱⲣ": {"def": "to spread", "pos": "verb", "translit": "shōr", "origin": "Egyptian pꜣḏ"},
    "ϯϩⲏ": {"def": "to command", "pos": "verb", "translit": "tihē", "origin": "Egyptian wd"},
    "ⲥⲓⲛⲉ": {"def": "to kiss", "pos": "verb", "translit": "sine", "origin": "Greek: κυνέω"},
    "ⲣⲟϩ": {"def": "to open", "pos": "verb", "translit": "roh", "origin": "Egyptian wn"},
    "ϭⲱ": {"def": "to remain, stay", "pos": "verb", "translit": "chō", "origin": "Greek: μένω"},
    "ϣⲱⲱⲧ": {"def": "to seek", "pos": "verb", "translit": "shōwt", "origin": "Greek: ζητεῖν"},
    "ⲙⲟⲟⲩⲧ": {"def": "to touch", "pos": "verb", "translit": "moout", "origin": "Greek: ἅπτεσθαι"},
    
    # Materials
    "ϩⲁⲙ": {"def": "reed, papyrus", "pos": "noun", "translit": "ham", "origin": "Egyptian ꜥm"},
    "ⲥⲟ": {"def": "rock, stone", "pos": "noun", "translit": "so", "origin": "Greek: πέτρα"},
    "ϩⲟⲩⲛⲧ": {"def": "clothing", "pos": "noun", "translit": "hount", "origin": "Egyptian mnḫt"},
    "ⲥⲟⲃⲧ": {"def": "sword", "pos": "noun", "translit": "sobt", "origin": "Greek: σπάθη"},
    "ⲟⲩⲱⲛϩ": {"def": "light", "pos": "noun", "translit": "ouōnh", "origin": "Egyptian ꜣḫt"},
    "ⲥⲕⲟⲧⲟⲥ": {"def": "darkness", "pos": "noun", "translit": "skotos", "origin": "Greek: σκότος"},
    "ⲡⲩⲣ": {"def": "fire", "pos": "noun", "translit": "pyr", "origin": "Greek: πῦρ"},
    
    # More divine/names
    "ⲓⲟⲩⲇⲁⲥ": {"def": "Judas", "pos": "proper noun", "translit": "ioudas", "origin": "Greek: Ἰούδας"},
    "ⲓⲁⲕⲱⲃⲟⲥ": {"def": "James", "pos": "proper noun", "translit": "iakōbos", "origin": "Greek: Ἰάκωβος"},
    "ⲓⲱⲁⲛⲛⲏⲥ": {"def": "John", "pos": "proper noun", "translit": "iōannēs", "origin": "Greek: Ἰωάννης"},
    "ⲁⲛⲇⲣⲉⲁⲥ": {"def": "Andrew", "pos": "proper noun", "translit": "andreas", "origin": "Greek: Ἀνδρέας"},
    "ⲡⲓⲗⲁⲧⲟⲥ": {"def": "Pilate", "pos": "proper noun", "translit": "pilatos", "origin": "Greek: Πιλᾶτος"},
    "ϩⲣⲟⲇⲏ": {"def": "Herod", "pos": "proper noun", "translit": "hrōdē", "origin": "Greek: Ἡρῴδης"},
    "ⲁⲡⲟⲥⲧⲟⲗⲟⲥ": {"def": "apostle", "pos": "noun", "translit": "apostolos", "origin": "Greek: ἀπόστολος"},
    "ⲇⲓⲁⲕⲟⲛⲟⲥ": {"def": "deacon", "pos": "noun", "translit": "diakonos", "origin": "Greek: διάκονος"},
    "ⲉⲡⲓⲥⲕⲟⲡⲟⲥ": {"def": "bishop, overseer", "pos": "noun", "translit": "episkopos", "origin": "Greek: ἐπίσκοπος"},
    "ⲡⲣⲉⲥⲃⲩⲧⲉⲣⲟⲥ": {"def": "elder, priest", "pos": "noun", "translit": "presbyteros", "origin": "Greek: πρεσβύτερος"},
    "ⲉⲩⲁⲅⲅⲉⲗⲓⲟⲛ": {"def": "gospel", "pos": "noun", "translit": "euaggelion", "origin": "Greek: εὐαγγέλιον"},
    "ⲕⲱⲛ": {"def": "village", "pos": "noun", "translit": "kōn", "origin": "Greek: κώμη"},
    "ⲡⲟⲗⲓⲥ": {"def": "city", "pos": "noun", "translit": "polis", "origin": "Greek: πόλις"},
    "ⲟⲓⲕⲓⲁ": {"def": "house", "pos": "noun", "translit": "oikia", "origin": "Greek: οἰκία"},
    "ⲉⲕⲕⲗⲏⲥⲓⲁ": {"def": "church, assembly", "pos": "noun", "translit": "ekklēsia", "origin": "Greek: ἐκκλησία"},
}

class CopticLexicon:
    """Coptic-English lexicon"""
    
    def __init__(self):
        self.entries = {}
        self.etymology_index = defaultdict(list)
        
    def build(self):
        """Build lexicon from vocabulary lists"""
        print("[*] Building Coptic lexicon...")
        
        # Combine core and extended vocabulary
        all_vocab = {**COPTIC_CORE_VOCABULARY, **COPTIC_EXTENDED_VOCABULARY}
        
        for word, data in all_vocab.items():
            entry = {
                "word": word,
                "definition": data["def"],
                "part_of_speech": data["pos"],
                "transliteration": data["translit"],
                "etymology": data["origin"]
            }
            
            self.entries[word] = entry
            
            # Index by etymology
            origin = data["origin"].split(":")[0].strip()
            self.etymology_index[origin].append(word)
        
        print(f"    [+] Built {len(self.entries)} entries")
        
    def export_json(self, output_path: str):
        """Export to JSON"""
        print(f"[*] Exporting to {output_path}...")
        
        data = {
            "metadata": {
                "title": "Coptic Lexicon",
                "language": "Coptic (Sahidic dialect)",
                "period": "Early Christian Period (100-800 CE)",
                "total_entries": len(self.entries),
                "format": "JSON",
                "notes": "This is a seed lexicon based on common Coptic texts including Nag Hammadi library. Full Crum dictionary contains 10,000+ entries."
            },
            "entries": self.entries,
            "etymology_breakdown": dict(self.etymology_index)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"    [+] Exported {len(self.entries)} entries")
    
    def export_markdown(self, output_path: str):
        """Export to Markdown"""
        print(f"[*] Exporting markdown to {output_path}...")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Coptic Lexicon\n\n")
            f.write("**Coptic-English Dictionary (Sahidic Dialect)**\n\n")
            f.write(f"Total Entries: {len(self.entries)}\n\n")
            f.write("---\n\n")
            
            # Sort by Coptic word
            sorted_entries = sorted(self.entries.items(), key=lambda x: x[0])
            
            for word, entry in sorted_entries:
                f.write(f"## {word}\n\n")
                f.write(f"**Transliteration:** *{entry['transliteration']}*\n\n")
                f.write(f"**Part of Speech:** {entry['part_of_speech']}\n\n")
                f.write(f"**Definition:** {entry['definition']}\n\n")
                f.write(f"**Origin:** {entry['etymology']}\n\n")
                f.write("---\n\n")
        
        print(f"    [+] Exported {len(self.entries)} entries")
    
    def export_websters_style(self, output_path: str):
        """Export in Webster's dictionary format"""
        print(f"[*] Exporting Webster's style to {output_path}...")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("COPTIC LEXICON\n")
            f.write("Coptic-English Dictionary (Sahidic Dialect)\n")
            f.write("Period: 100-800 CE (Early Christian Egypt)\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("About Coptic:\n")
            f.write("  - Written in modified Greek alphabet\n")
            f.write("  - Last stage of ancient Egyptian language\n")
            f.write("  - Dialects: Sahidic (Upper Egypt), Bohairic (Lower Egypt)\n")
            f.write("  - Used for early Christian texts (Nag Hammadi library)\n\n")
            
            f.write("Pronunciation Guide:\n")
            f.write("  ⲁ = a as in father    ⲉ = e as in pet\n")
            f.write("  ⲏ = ay as in say      ⲓ = i as in machine\n")
            f.write("  ⲟ = o as in note      ⲩ = u/y as in French tu\n")
            f.write("  ⲱ = o as in tone      ϩ = h (rough breathing)\n")
            f.write("  ϣ = sh                ϭ = ky/ch\n")
            f.write("  ϥ = f                 ⲑ = th as in thin\n\n")
            
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
                
                # Origin
                if entry['etymology']:
                    f.write(f"    Origin: {entry['etymology']}\n")
                
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
            elif query in entry['etymology'].lower():
                match = True
            
            if match:
                results.append((word, entry))
        
        return results


def main():
    lexicon = CopticLexicon()
    
    # Build from vocabulary
    lexicon.build()
    
    # Create output directory
    out_dir = Path("/root/coptic_lexicon_output")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Export all formats
    lexicon.export_json(out_dir / "coptic_lexicon.json")
    lexicon.export_markdown(out_dir / "coptic_lexicon.md")
    lexicon.export_websters_style(out_dir / "websters_coptic.txt")
    
    # Sample entries
    print("\n" + "=" * 70)
    print("SAMPLE ENTRIES")
    print("=" * 70 + "\n")
    
    sample_words = ['ⲛⲟⲩⲧⲉ', 'ⲓⲥ', 'ⲁⲅⲁⲡⲏ', 'ⲥⲁϩⲛⲉ', 'ⲡⲛⲉⲩⲙⲁ', 'ⲣⲱⲙⲉ', 'ⲉⲓ']
    for word in sample_words:
        if word in lexicon.entries:
            e = lexicon.entries[word]
            print(f"{word} ({e['transliteration']})")
            print(f"  {e['definition']}")
            print(f"  [{e['part_of_speech']}] Origin: {e['etymology']}\n")
    
    print("=" * 70)
    print("COPTIC LEXICON COMPLETE")
    print("=" * 70)
    print(f"\nOutput files in {out_dir.absolute()}:")
    print(f"  - coptic_lexicon.json (full)")
    print(f"  - coptic_lexicon.md (human-readable)")
    print(f"  - websters_coptic.txt (Webster's style)")
    print(f"\nTo search: python search_coptic.py <word>")
    print("\nNOTE: This is a seed lexicon. For complete coverage,")
    print("add Crum's Coptic Dictionary (10,000+ entries)")


if __name__ == "__main__":
    main()
