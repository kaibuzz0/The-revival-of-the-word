#!/usr/bin/env python3
"""
Latin Lexicon Builder
Builds a Latin-English dictionary for Classical and Ecclesiastical Latin
"""
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

# Core Latin vocabulary - Classical and Ecclesiastical
LATIN_CORE_VOCABULARY = {
    # Articles/Pronouns (Latin has no articles, but has demonstratives)
    "hic": {"def": "this (masculine)", "pos": "demonstrative pronoun", "translit": "hic", "declension": "irregular", "case": "nominative"},
    "haec": {"def": "this (feminine)", "pos": "demonstrative pronoun", "translit": "haec", "declension": "irregular", "case": "nominative"},
    "hoc": {"def": "this (neuter)", "pos": "demonstrative pronoun", "translit": "hoc", "declension": "irregular", "case": "nominative"},
    "ille": {"def": "that (masculine)", "pos": "demonstrative pronoun", "translit": "ille", "declension": "irregular", "case": "nominative"},
    "illa": {"def": "that (feminine)", "pos": "demonstrative pronoun", "translit": "illa", "declension": "irregular", "case": "nominative"},
    "illud": {"def": "that (neuter)", "pos": "demonstrative pronoun", "translit": "illud", "declension": "irregular", "case": "nominative"},
    "is": {"def": "he, this", "pos": "personal pronoun", "translit": "is", "declension": "irregular", "case": "nominative"},
    "ea": {"def": "she, this", "pos": "personal pronoun", "translit": "ea", "declension": "irregular", "case": "nominative"},
    "id": {"def": "it, this", "pos": "personal pronoun", "translit": "id", "declension": "irregular", "case": "nominative"},
    "ego": {"def": "I", "pos": "personal pronoun", "translit": "ego", "declension": "irregular"},
    "tu": {"def": "you (singular)", "pos": "personal pronoun", "translit": "tu", "declension": "irregular"},
    "nos": {"def": "we", "pos": "personal pronoun", "translit": "nos", "declension": "irregular"},
    "vos": {"def": "you (plural)", "pos": "personal pronoun", "translit": "vos", "declension": "irregular"},
    "qui": {"def": "who, which (masculine)", "pos": "relative pronoun", "translit": "qui", "declension": "irregular", "case": "nominative"},
    "quae": {"def": "who, which (feminine)", "pos": "relative pronoun", "translit": "quae", "declension": "irregular", "case": "nominative"},
    "quod": {"def": "which (neuter)", "pos": "relative pronoun", "translit": "quod", "declension": "irregular", "case": "nominative"},
    
    # Divine Names
    "Deus": {"def": "God", "pos": "noun", "translit": "Deus", "declension": "2nd", "gender": "masculine"},
    "Dominus": {"def": "Lord, Master", "pos": "noun", "translit": "Dominus", "declension": "2nd", "gender": "masculine"},
    "Christus": {"def": "Christ, Anointed One", "pos": "noun", "translit": "Christus", "declension": "2nd", "gender": "masculine"},
    "Iesus": {"def": "Jesus", "pos": "proper noun", "translit": "Iesus", "declension": "irregular", "gender": "masculine"},
    "Spiritus": {"def": "Spirit, breath, wind", "pos": "noun", "translit": "Spiritus", "declension": "4th", "gender": "masculine"},
    "Sanctus": {"def": "Holy One, Saint", "pos": "noun/adjective", "translit": "Sanctus", "declension": "1st/2nd", "gender": "masculine"},
    "Pater": {"def": "Father", "pos": "noun", "translit": "Pater", "declension": "3rd", "gender": "masculine"},
    "Filius": {"def": "Son", "pos": "noun", "translit": "Filius", "declension": "2nd", "gender": "masculine"},
    "Mater": {"def": "Mother", "pos": "noun", "translit": "Mater", "declension": "3rd", "gender": "feminine"},
    "Maria": {"def": "Mary", "pos": "proper noun", "translit": "Maria", "declension": "1st", "gender": "feminine"},
    "Angelus": {"def": "Angel, messenger", "pos": "noun", "translit": "Angelus", "declension": "2nd", "gender": "masculine"},
    "caelum": {"def": "heaven, sky", "pos": "noun", "translit": "caelum", "declension": "2nd", "gender": "neuter"},
    "regnum": {"def": "kingdom, reign", "pos": "noun", "translit": "regnum", "declension": "2nd", "gender": "neuter"},
    "Rex": {"def": "King", "pos": "noun", "translit": "Rex", "declension": "3rd", "gender": "masculine"},
    
    # Common Nouns
    "homo": {"def": "man, human being", "pos": "noun", "translit": "homo", "declension": "3rd", "gender": "masculine"},
    "vir": {"def": "man, male", "pos": "noun", "translit": "vir", "declension": "3rd", "gender": "masculine"},
    "mulier": {"def": "woman", "pos": "noun", "translit": "mulier", "declension": "3rd", "gender": "feminine"},
    "femina": {"def": "woman", "pos": "noun", "translit": "femina", "declension": "1st", "gender": "feminine"},
    "puer": {"def": "boy, child", "pos": "noun", "translit": "puer", "declension": "2nd", "gender": "masculine"},
    "puella": {"def": "girl", "pos": "noun", "translit": "puella", "declension": "1st", "gender": "feminine"},
    "familia": {"def": "family, household", "pos": "noun", "translit": "familia", "declension": "1st", "gender": "feminine"},
    "domus": {"def": "house, home", "pos": "noun", "translit": "domus", "declension": "4th", "gender": "feminine"},
    "cor": {"def": "heart", "pos": "noun", "translit": "cor", "declension": "3rd", "gender": "neuter"},
    "anima": {"def": "soul, breath, life", "pos": "noun", "translit": "anima", "declension": "1st", "gender": "feminine"},
    "corpus": {"def": "body", "pos": "noun", "translit": "corpus", "declension": "3rd", "gender": "neuter"},
    "sanguis": {"def": "blood", "pos": "noun", "translit": "sanguis", "declension": "3rd", "gender": "masculine"},
    "caro": {"def": "flesh, meat", "pos": "noun", "translit": "caro", "declension": "3rd", "gender": "feminine"},
    "mens": {"def": "mind", "pos": "noun", "translit": "mens", "declension": "3rd", "gender": "feminine"},
    "oculus": {"def": "eye", "pos": "noun", "translit": "oculus", "declension": "2nd", "gender": "masculine"},
    "auris": {"def": "ear", "pos": "noun", "translit": "auris", "declension": "3rd", "gender": "feminine"},
    "manus": {"def": "hand", "pos": "noun", "translit": "manus", "declension": "4th", "gender": "feminine"},
    "caput": {"def": "head", "pos": "noun", "translit": "caput", "declension": "3rd", "gender": "neuter"},
    "pes": {"def": "foot", "pos": "noun", "translit": "pes", "declension": "3rd", "gender": "masculine"},
    "aqua": {"def": "water", "pos": "noun", "translit": "aqua", "declension": "1st", "gender": "feminine"},
    "ignis": {"def": "fire", "pos": "noun", "translit": "ignis", "declension": "3rd", "gender": "masculine"},
    "terra": {"def": "earth, land, ground", "pos": "noun", "translit": "terra", "declension": "1st", "gender": "feminine"},
    "mundus": {"def": "world, universe", "pos": "noun", "translit": "mundus", "declension": "2nd", "gender": "masculine"},
    "arbor": {"def": "tree", "pos": "noun", "translit": "arbor", "declension": "3rd", "gender": "feminine"},
    "sol": {"def": "sun", "pos": "noun", "translit": "sol", "declension": "3rd", "gender": "masculine"},
    "luna": {"def": "moon", "pos": "noun", "translit": "luna", "declension": "1st", "gender": "feminine"},
    "stella": {"def": "star", "pos": "noun", "translit": "stella", "declension": "1st", "gender": "feminine"},
    "via": {"def": "way, road, path", "pos": "noun", "translit": "via", "declension": "1st", "gender": "feminine"},
    "lux": {"def": "light", "pos": "noun", "translit": "lux", "declension": "3rd", "gender": "feminine"},
    "tenebrae": {"def": "darkness", "pos": "noun", "translit": "tenebrae", "declension": "1st", "gender": "feminine", "number": "plural"},
    "nox": {"def": "night", "pos": "noun", "translit": "nox", "declension": "3rd", "gender": "feminine"},
    "dies": {"def": "day", "pos": "noun", "translit": "dies", "declension": "5th", "gender": "masculine/feminine"},
    "aurum": {"def": "gold", "pos": "noun", "translit": "aurum", "declension": "2nd", "gender": "neuter"},
    "argentum": {"def": "silver", "pos": "noun", "translit": "argentum", "declension": "2nd", "gender": "neuter"},
    
    # Verbs
    "sum": {"def": "to be, exist", "pos": "verb", "translit": "sum", "conjugation": "irregular"},
    "est": {"def": "he/she/it is", "pos": "verb", "translit": "est", "conjugation": "irregular", "person": "3rd", "number": "singular"},
    "dico": {"def": "to say, speak", "pos": "verb", "translit": "dico", "conjugation": "3rd"},
    "facio": {"def": "to do, make", "pos": "verb", "translit": "facio", "conjugation": "3rd"},
    "habeo": {"def": "to have, hold", "pos": "verb", "translit": "habeo", "conjugation": "2nd"},
    "video": {"def": "to see", "pos": "verb", "translit": "video", "conjugation": "2nd"},
    "audio": {"def": "to hear", "pos": "verb", "translit": "audio", "conjugation": "4th"},
    "do": {"def": "to give", "pos": "verb", "translit": "do", "conjugation": "1st"},
    "capio": {"def": "to take, seize", "pos": "verb", "translit": "capio", "conjugation": "3rd"},
    "venio": {"def": "to come", "pos": "verb", "translit": "venio", "conjugation": "4th"},
    "vado": {"def": "to go", "pos": "verb", "translit": "vado", "conjugation": "1st"},
    "sto": {"def": "to stand", "pos": "verb", "translit": "sto", "conjugation": "1st"},
    "vivo": {"def": "to live", "pos": "verb", "translit": "vivo", "conjugation": "3rd"},
    "morior": {"def": "to die", "pos": "verb", "translit": "morior", "conjugation": "3rd", "deponent": "true"},
    "resurgo": {"def": "to rise again", "pos": "verb", "translit": "resurgo", "conjugation": "3rd"},
    "credo": {"def": "to believe, trust", "pos": "verb", "translit": "credo", "conjugation": "3rd"},
    "spero": {"def": "to hope", "pos": "verb", "translit": "spero", "conjugation": "1st"},
    "amo": {"def": "to love", "pos": "verb", "translit": "amo", "conjugation": "1st"},
    "scio": {"def": "to know", "pos": "verb", "translit": "scio", "conjugation": "4th"},
    "oportet": {"def": "it is necessary", "pos": "verb", "translit": "oportet", "impersonal": "true"},
    "oportet": {"def": "it is necessary", "pos": "verb", "translit": "oportet", "impersonal": "true"},
    "claudo": {"def": "to close, shut", "pos": "verb", "translit": "claudo", "conjugation": "3rd"},
    "aperio": {"def": "to open", "pos": "verb", "translit": "aperio", "conjugation": "4th"},
    "sedeo": {"def": "to sit", "pos": "verb", "translit": "sedeo", "conjugation": "2nd"},
    "iacio": {"def": "to throw, cast", "pos": "verb", "translit": "iacio", "conjugation": "3rd"},
    "mitto": {"def": "to send", "pos": "verb", "translit": "mitto", "conjugation": "3rd"},
    "facio": {"def": "to make, do", "pos": "verb", "translit": "facio", "conjugation": "3rd"},
    "accipio": {"def": "to receive, accept", "pos": "verb", "translit": "accipio", "conjugation": "3rd"},
    
    # Adjectives
    "bonus": {"def": "good", "pos": "adjective", "translit": "bonus", "declension": "1st/2nd", "gender": "masculine"},
    "malus": {"def": "bad, evil", "pos": "adjective", "translit": "malus", "declension": "1st/2nd", "gender": "masculine"},
    "magnus": {"def": "great, large", "pos": "adjective", "translit": "magnus", "declension": "1st/2nd", "gender": "masculine"},
    "parvus": {"def": "small, little", "pos": "adjective", "translit": "parvus", "declension": "1st/2nd", "gender": "masculine"},
    "sanctus": {"def": "holy, sacred", "pos": "adjective", "translit": "sanctus", "declension": "1st/2nd", "gender": "masculine"},
    "iustus": {"def": "just, righteous", "pos": "adjective", "translit": "iustus", "declension": "1st/2nd", "gender": "masculine"},
    "verus": {"def": "true, real", "pos": "adjective", "translit": "verus", "declension": "1st/2nd", "gender": "masculine"},
    "novus": {"def": "new", "pos": "adjective", "translit": "novus", "declension": "1st/2nd", "gender": "masculine"},
    "altus": {"def": "high, deep", "pos": "adjective", "translit": "altus", "declension": "1st/2nd", "gender": "masculine"},
    "longus": {"def": "long", "pos": "adjective", "translit": "longus", "declension": "1st/2nd", "gender": "masculine"},
    "propinquus": {"def": "near", "pos": "adjective", "translit": "propinquus", "declension": "1st/2nd", "gender": "masculine"},
    "dulcis": {"def": "sweet", "pos": "adjective", "translit": "dulcis", "declension": "3rd", "gender": "masculine/feminine"},
    "omnis": {"def": "all, every", "pos": "adjective", "translit": "omnis", "declension": "3rd", "gender": "masculine/feminine"},
    "totus": {"def": "whole, entire", "pos": "adjective", "translit": "totus", "declension": "irregular", "gender": "masculine"},
    "multus": {"def": "much, many", "pos": "adjective", "translit": "multus", "declension": "1st/2nd", "gender": "masculine"},
    "paucus": {"def": "few", "pos": "adjective", "translit": "paucus", "declension": "1st/2nd", "gender": "masculine"},
    "primus": {"def": "first", "pos": "adjective", "translit": "primus", "declension": "irregular", "gender": "masculine"},
    "ultimus": {"def": "last", "pos": "adjective", "translit": "ultimus", "declension": "1st/2nd", "gender": "masculine"},
    "aeternus": {"def": "eternal", "pos": "adjective", "translit": "aeternus", "declension": "1st/2nd", "gender": "masculine"},
    "immortalis": {"def": "immortal", "pos": "adjective", "translit": "immortalis", "declension": "3rd", "gender": "masculine/feminine"},
    
    # Prepositions
    "in": {"def": "in, into, on", "pos": "preposition", "translit": "in", "case": "ablative/accusative"},
    "ad": {"def": "to, toward", "pos": "preposition", "translit": "ad", "case": "accusative"},
    "ab": {"def": "from, away from", "pos": "preposition", "translit": "ab", "case": "ablative"},
    "cum": {"def": "with", "pos": "preposition", "translit": "cum", "case": "ablative"},
    "de": {"def": "down from, concerning", "pos": "preposition", "translit": "de", "case": "ablative"},
    "ex": {"def": "out of, from", "pos": "preposition", "translit": "ex", "case": "ablative"},
    "per": {"def": "through, by means of", "pos": "preposition", "translit": "per", "case": "accusative"},
    "pro": {"def": "before, for", "pos": "preposition", "translit": "pro", "case": "ablative"},
    "sine": {"def": "without", "pos": "preposition", "translit": "sine", "case": "ablative"},
    "sub": {"def": "under, up to", "pos": "preposition", "translit": "sub", "case": "ablative/accusative"},
    "super": {"def": "above, over, upon", "pos": "preposition", "translit": "super", "case": "ablative/accusative"},
    "trans": {"def": "across, beyond", "pos": "preposition", "translit": "trans", "case": "accusative"},
    "propter": {"def": "on account of", "pos": "preposition", "translit": "propter", "case": "accusative"},
    "inter": {"def": "between, among", "pos": "preposition", "translit": "inter", "case": "accusative"},
    "ante": {"def": "before (in time/place)", "pos": "preposition", "translit": "ante", "case": "accusative"},
    "post": {"def": "after", "pos": "preposition", "translit": "post", "case": "accusative"},
    "contra": {"def": "against", "pos": "preposition", "translit": "contra", "case": "accusative"},
    
    # Conjunctions
    "et": {"def": "and", "pos": "conjunction", "translit": "et"},
    "sed": {"def": "but", "pos": "conjunction", "translit": "sed"},
    "aut": {"def": "or", "pos": "conjunction", "translit": "aut"},
    "vel": {"def": "or (inclusive)", "pos": "conjunction", "translit": "vel"},
    "neque": {"def": "and not, nor", "pos": "conjunction", "translit": "neque"},
    "quia": {"def": "because", "pos": "conjunction", "translit": "quia"},
    "quoniam": {"def": "since, because", "pos": "conjunction", "translit": "quoniam"},
    "si": {"def": "if", "pos": "conjunction", "translit": "si"},
    "nisi": {"def": "unless, except", "pos": "conjunction", "translit": "nisi"},
    "ut": {"def": "so that, in order that", "pos": "conjunction", "translit": "ut"},
    "cum": {"def": "when, since", "pos": "conjunction", "translit": "cum"},
    "dum": {"def": "while", "pos": "conjunction", "translit": "dum"},
    "enim": {"def": "for", "pos": "conjunction", "translit": "enim"},
    "igitur": {"def": "therefore", "pos": "conjunction", "translit": "igitur"},
    "itaque": {"def": "and so, therefore", "pos": "conjunction", "translit": "itaque"},
    
    # Numbers
    "unus": {"def": "one", "pos": "numeral", "translit": "unus", "declension": "irregular"},
    "duo": {"def": "two", "pos": "numeral", "translit": "duo", "declension": "irregular"},
    "tres": {"def": "three", "pos": "numeral", "translit": "tres", "declension": "irregular"},
    "quattuor": {"def": "four", "pos": "numeral", "translit": "quattuor", "indeclinable": "true"},
    "quinque": {"def": "five", "pos": "numeral", "translit": "quinque", "indeclinable": "true"},
    "centum": {"def": "hundred", "pos": "numeral", "translit": "centum", "indeclinable": "true"},
    "mille": {"def": "thousand", "pos": "numeral", "translit": "mille", "declension": "irregular"},
    
    # Adverbs
    "non": {"def": "not", "pos": "adverb", "translit": "non"},
    "iam": {"def": "now, already", "pos": "adverb", "translit": "iam"},
    "semper": {"def": "always", "pos": "adverb", "translit": "semper"},
    "nunquam": {"def": "never", "pos": "adverb", "translit": "nunquam"},
    "hic": {"def": "here", "pos": "adverb", "translit": "hic"},
    "illic": {"def": "there", "pos": "adverb", "translit": "illic"},
    "bene": {"def": "well", "pos": "adverb", "translit": "bene"},
    "male": {"def": "badly, poorly", "pos": "adverb", "translit": "male"},
    "sic": {"def": "thus, so", "pos": "adverb", "translit": "sic"},
    "modo": {"def": "only, just now", "pos": "adverb", "translit": "modo"},
    "tamen": {"def": "however, nevertheless", "pos": "adverb", "translit": "tamen"},
    
    # Ecclesiastical/Theological Terms
    "ecclesia": {"def": "church, assembly", "pos": "noun", "translit": "ecclesia", "declension": "1st", "gender": "feminine"},
    "sacramentum": {"def": "sacrament, mystery", "pos": "noun", "translit": "sacramentum", "declension": "2nd", "gender": "neuter"},
    "peccatum": {"def": "sin", "pos": "noun", "translit": "peccatum", "declension": "2nd", "gender": "neuter"},
    "gratia": {"def": "grace, thanks", "pos": "noun", "translit": "gratia", "declension": "1st", "gender": "feminine"},
    "fides": {"def": "faith, trust", "pos": "noun", "translit": "fides", "declension": "3rd", "gender": "feminine"},
    "spes": {"def": "hope", "pos": "noun", "translit": "spes", "declension": "3rd", "gender": "feminine"},
    "caritas": {"def": "love, charity", "pos": "noun", "translit": "caritas", "declension": "3rd", "gender": "feminine"},
    "veritas": {"def": "truth", "pos": "noun", "translit": "veritas", "declension": "3rd", "gender": "feminine"},
    "iustitia": {"def": "justice, righteousness", "pos": "noun", "translit": "iustitia", "declension": "1st", "gender": "feminine"},
    "misericordia": {"def": "mercy", "pos": "noun", "translit": "misericordia", "declension": "1st", "gender": "feminine"},
    "virtus": {"def": "virtue, power", "pos": "noun", "translit": "virtus", "declension": "3rd", "gender": "feminine"},
    "sapientia": {"def": "wisdom", "pos": "noun", "translit": "sapientia", "declension": "1st", "gender": "feminine"},
    "scientia": {"def": "knowledge", "pos": "noun", "translit": "scientia", "declension": "1st", "gender": "feminine"},
    "creatio": {"def": "creation", "pos": "noun", "translit": "creatio", "declension": "3rd", "gender": "feminine"},
    "creatura": {"def": "creature", "pos": "noun", "translit": "creatura", "declension": "1st", "gender": "feminine"},
    "vita": {"def": "life", "pos": "noun", "translit": "vita", "declension": "1st", "gender": "feminine"},
    "mors": {"def": "death", "pos": "noun", "translit": "mors", "declension": "3rd", "gender": "feminine"},
    "resurrectio": {"def": "resurrection", "pos": "noun", "translit": "resurrectio", "declension": "3rd", "gender": "feminine"},
    "crux": {"def": "cross", "pos": "noun", "translit": "crux", "declension": "3rd", "gender": "feminine"},
    "baptisma": {"def": "baptism", "pos": "noun", "translit": "baptisma", "declension": "3rd", "gender": "neuter"},
    "apostolus": {"def": "apostle", "pos": "noun", "translit": "apostolus", "declension": "2nd", "gender": "masculine"},
    "evangelium": {"def": "gospel", "pos": "noun", "translit": "evangelium", "declension": "2nd", "gender": "neuter"},
    "testamentum": {"def": "testament, covenant", "pos": "noun", "translit": "testamentum", "declension": "2nd", "gender": "neuter"},
    "propheta": {"def": "prophet", "pos": "noun", "translit": "propheta", "declension": "1st", "gender": "masculine"},
    "sacerdos": {"def": "priest", "pos": "noun", "translit": "sacerdos", "declension": "3rd", "gender": "masculine"},
    "episcopus": {"def": "bishop, overseer", "pos": "noun", "translit": "episcopus", "declension": "2nd", "gender": "masculine"},
    "presbyter": {"def": "elder, priest", "pos": "noun", "translit": "presbyter", "declension": "2nd", "gender": "masculine"},
    "templum": {"def": "temple", "pos": "noun", "translit": "templum", "declension": "2nd", "gender": "neuter"},
    "altare": {"def": "altar", "pos": "noun", "translit": "altare", "declension": "3rd", "gender": "neuter"},
    "panis": {"def": "bread", "pos": "noun", "translit": "panis", "declension": "3rd", "gender": "masculine"},
    "vinum": {"def": "wine", "pos": "noun", "translit": "vinum", "declension": "2nd", "gender": "neuter"},
    "corpus": {"def": "body", "pos": "noun", "translit": "corpus", "declension": "3rd", "gender": "neuter"},
    "sanguis": {"def": "blood", "pos": "noun", "translit": "sanguis", "declension": "3rd", "gender": "masculine"},
    "paradisus": {"def": "paradise", "pos": "noun", "translit": "paradisus", "declension": "2nd", "gender": "masculine"},
    "infernus": {"def": "hell", "pos": "noun", "translit": "infernus", "declension": "2nd", "gender": "masculine"},
    "daemon": {"def": "demon", "pos": "noun", "translit": "daemon", "declension": "3rd", "gender": "masculine"},
    "diabolus": {"def": "devil", "pos": "noun", "translit": "diabolus", "declension": "2nd", "gender": "masculine"},
    "satanas": {"def": "satan", "pos": "noun", "translit": "satanas", "declension": "irregular", "gender": "masculine"},
    "oratio": {"def": "prayer", "pos": "noun", "translit": "oratio", "declension": "3rd", "gender": "feminine"},
    "hymnus": {"def": "hymn", "pos": "noun", "translit": "hymnus", "declension": "2nd", "gender": "masculine"},
    "gloria": {"def": "glory", "pos": "noun", "translit": "gloria", "declension": "1st", "gender": "feminine"},
    "laus": {"def": "praise", "pos": "noun", "translit": "laus", "declension": "3rd", "gender": "feminine"},
    "pax": {"def": "peace", "pos": "noun", "translit": "pax", "declension": "3rd", "gender": "feminine"},
    "unitas": {"def": "unity", "pos": "noun", "translit": "unitas", "declension": "3rd", "gender": "feminine"},
    "trinitas": {"def": "trinity", "pos": "noun", "translit": "trinitas", "declension": "3rd", "gender": "feminine"},
}

# Extended vocabulary
LATIN_EXTENDED_VOCABULARY = {
    # More body parts
    "os": {"def": "mouth, face", "pos": "noun", "translit": "os", "declension": "3rd", "gender": "neuter"},
    "nasus": {"def": "nose", "pos": "noun", "translit": "nasus", "declension": "2nd", "gender": "masculine"},
    "dens": {"def": "tooth", "pos": "noun", "translit": "dens", "declension": "3rd", "gender": "masculine"},
    "lingua": {"def": "tongue, language", "pos": "noun", "translit": "lingua", "declension": "1st", "gender": "feminine"},
    "bracchium": {"def": "arm", "pos": "noun", "translit": "bracchium", "declension": "2nd", "gender": "neuter"},
    "crus": {"def": "leg", "pos": "noun", "translit": "crus", "declension": "3rd", "gender": "neuter"},
    "pes": {"def": "foot", "pos": "noun", "translit": "pes", "declension": "3rd", "gender": "masculine"},
    "digitus": {"def": "finger", "pos": "noun", "translit": "digitus", "declension": "2nd", "gender": "masculine"},
    "unguis": {"def": "nail, claw", "pos": "noun", "translit": "unguis", "declension": "3rd", "gender": "masculine"},
    "cutis": {"def": "skin", "pos": "noun", "translit": "cutis", "declension": "3rd", "gender": "feminine"},
    "capillus": {"def": "hair", "pos": "noun", "translit": "capillus", "declension": "2nd", "gender": "masculine"},
    "vertex": {"def": "top of head", "pos": "noun", "translit": "vertex", "declension": "3rd", "gender": "masculine"},
    "gena": {"def": "cheek", "pos": "noun", "translit": "gena", "declension": "1st", "gender": "feminine"},
    "collum": {"def": "neck", "pos": "noun", "translit": "collum", "declension": "2nd", "gender": "neuter"},
    "pectus": {"def": "chest, breast", "pos": "noun", "translit": "pectus", "declension": "3rd", "gender": "neuter"},
    "venter": {"def": "belly, stomach", "pos": "noun", "translit": "venter", "declension": "3rd", "gender": "masculine"},
    "tergum": {"def": "back", "pos": "noun", "translit": "tergum", "declension": "2nd", "gender": "neuter"},
    "sanguis": {"def": "blood", "pos": "noun", "translit": "sanguis", "declension": "3rd", "gender": "masculine"},
    "vena": {"def": "vein", "pos": "noun", "translit": "vena", "declension": "1st", "gender": "feminine"},
    
    # Nature
    "ventus": {"def": "wind", "pos": "noun", "translit": "ventus", "declension": "2nd", "gender": "masculine"},
    "tempestas": {"def": "storm", "pos": "noun", "translit": "tempestas", "declension": "3rd", "gender": "feminine"},
    "imber": {"def": "rain", "pos": "noun", "translit": "imber", "declension": "3rd", "gender": "masculine"},
    "nubes": {"def": "cloud", "pos": "noun", "translit": "nubes", "declension": "3rd", "gender": "feminine"},
    "fulmen": {"def": "lightning", "pos": "noun", "translit": "fulmen", "declension": "3rd", "gender": "neuter"},
    "tonitrus": {"def": "thunder", "pos": "noun", "translit": "tonitrus", "declension": "2nd", "gender": "masculine"},
    "flumen": {"def": "river", "pos": "noun", "translit": "flumen", "declension": "3rd", "gender": "neuter"},
    "lacus": {"def": "lake", "pos": "noun", "translit": "lacus", "declension": "4th", "gender": "masculine"},
    "mons": {"def": "mountain", "pos": "noun", "translit": "mons", "declension": "3rd", "gender": "masculine"},
    "vallis": {"def": "valley", "pos": "noun", "translit": "vallis", "declension": "3rd", "gender": "feminine"},
    "sylva": {"def": "forest, wood", "pos": "noun", "translit": "sylva", "declension": "1st", "gender": "feminine"},
    "flos": {"def": "flower", "pos": "noun", "translit": "flos", "declension": "3rd", "gender": "masculine"},
    "herba": {"def": "grass, herb", "pos": "noun", "translit": "herba", "declension": "1st", "gender": "feminine"},
    "fructus": {"def": "fruit", "pos": "noun", "translit": "fructus", "declension": "4th", "gender": "masculine"},
    "semen": {"def": "seed", "pos": "noun", "translit": "semen", "declension": "3rd", "gender": "neuter"},
    "radix": {"def": "root", "pos": "noun", "translit": "radix", "declension": "3rd", "gender": "feminine"},
    "folium": {"def": "leaf", "pos": "noun", "translit": "folium", "declension": "2nd", "gender": "neuter"},
    "ramus": {"def": "branch", "pos": "noun", "translit": "ramus", "declension": "2nd", "gender": "masculine"},
    "cortex": {"def": "bark, shell", "pos": "noun", "translit": "cortex", "declension": "3rd", "gender": "masculine"},
    "sucus": {"def": "sap, juice", "pos": "noun", "translit": "sucus", "declension": "2nd", "gender": "masculine"},
    "spina": {"def": "thorn", "pos": "noun", "translit": "spina", "declension": "1st", "gender": "feminine"},
    
    # Animals
    "animal": {"def": "animal", "pos": "noun", "translit": "animal", "declension": "3rd", "gender": "neuter"},
    "bestia": {"def": "beast, animal", "pos": "noun", "translit": "bestia", "declension": "1st", "gender": "feminine"},
    "avis": {"def": "bird", "pos": "noun", "translit": "avis", "declension": "3rd", "gender": "feminine"},
    "piscis": {"def": "fish", "pos": "noun", "translit": "piscis", "declension": "3rd", "gender": "masculine"},
    "serpens": {"def": "serpent, snake", "pos": "noun", "translit": "serpens", "declension": "3rd", "gender": "masculine/feminine"},
    "leo": {"def": "lion", "pos": "noun", "translit": "leo", "declension": "3rd", "gender": "masculine"},
    "lupus": {"def": "wolf", "pos": "noun", "translit": "lupus", "declension": "2nd", "gender": "masculine"},
    "ovis": {"def": "sheep", "pos": "noun", "translit": "ovis", "declension": "3rd", "gender": "feminine"},
    "capra": {"def": "goat", "pos": "noun", "translit": "capra", "declension": "1st", "gender": "feminine"},
    "bos": {"def": "ox, cow", "pos": "noun", "translit": "bos", "declension": "3rd", "gender": "masculine/feminine"},
    "porcus": {"def": "pig", "pos": "noun", "translit": "porcus", "declension": "2nd", "gender": "masculine"},
    "equus": {"def": "horse", "pos": "noun", "translit": "equus", "declension": "2nd", "gender": "masculine"},
    "asinus": {"def": "donkey, ass", "pos": "noun", "translit": "asinus", "declension": "2nd", "gender": "masculine"},
    "camelus": {"def": "camel", "pos": "noun", "translit": "camelus", "declension": "2nd", "gender": "masculine"},
    "elephans": {"def": "elephant", "pos": "noun", "translit": "elephans", "declension": "3rd", "gender": "masculine"},
    "ursus": {"def": "bear", "pos": "noun", "translit": "ursus", "declension": "2nd", "gender": "masculine"},
    "vulpes": {"def": "fox", "pos": "noun", "translit": "vulpes", "declension": "3rd", "gender": "feminine"},
    "lepus": {"def": "hare", "pos": "noun", "translit": "lepus", "declension": "3rd", "gender": "masculine"},
    "mus": {"def": "mouse", "pos": "noun", "translit": "mus", "declension": "3rd", "gender": "masculine/feminine"},
    "apis": {"def": "bee", "pos": "noun", "translit": "apis", "declension": "3rd", "gender": "feminine"},
    "formica": {"def": "ant", "pos": "noun", "translit": "formica", "declension": "1st", "gender": "feminine"},
    "papilio": {"def": "butterfly, moth", "pos": "noun", "translit": "papilio", "declension": "3rd", "gender": "masculine"},
    "vermis": {"def": "worm", "pos": "noun", "translit": "vermis", "declension": "3rd", "gender": "masculine"},
    
    # Time
    "hora": {"def": "hour", "pos": "noun", "translit": "hora", "declension": "1st", "gender": "feminine"},
    "momentum": {"def": "moment", "pos": "noun", "translit": "momentum", "declension": "2nd", "gender": "neuter"},
    "annus": {"def": "year", "pos": "noun", "translit": "annus", "declension": "2nd", "gender": "masculine"},
    "mensis": {"def": "month", "pos": "noun", "translit": "mensis", "declension": "3rd", "gender": "masculine"},
    "hebdomas": {"def": "week", "pos": "noun", "translit": "hebdomas", "declension": "3rd", "gender": "feminine"},
    "hodiernus": {"def": "today's, of today", "pos": "adjective", "translit": "hodiernus", "declension": "1st/2nd", "gender": "masculine"},
    "cras": {"def": "tomorrow", "pos": "adverb", "translit": "cras"},
    "heri": {"def": "yesterday", "pos": "adverb", "translit": "heri"},
    "mane": {"def": "morning", "pos": "noun", "translit": "mane", "declension": "irregular", "gender": "neuter"},
    "vesper": {"def": "evening", "pos": "noun", "translit": "vesper", "declension": "irregular", "gender": "masculine"},
    "meridies": {"def": "midday, noon", "pos": "noun", "translit": "meridies", "declension": "5th", "gender": "masculine"},
    "media nox": {"def": "midnight", "pos": "noun phrase", "translit": "media nox", "declension": "3rd", "gender": "feminine"},
    "aestas": {"def": "summer", "pos": "noun", "translit": "aestas", "declension": "3rd", "gender": "feminine"},
    "hiems": {"def": "winter", "pos": "noun", "translit": "hiems", "declension": "3rd", "gender": "feminine"},
    "ver": {"def": "spring", "pos": "noun", "translit": "ver", "declension": "irregular", "gender": "neuter"},
    "autumnus": {"def": "autumn, fall", "pos": "noun", "translit": "autumnus", "declension": "2nd", "gender": "masculine"},
    
    # Abstract
    "forma": {"def": "form, shape", "pos": "noun", "translit": "forma", "declension": "1st", "gender": "feminine"},
    "figura": {"def": "figure, shape", "pos": "noun", "translit": "figura", "declension": "1st", "gender": "feminine"},
    "materia": {"def": "matter, material", "pos": "noun", "translit": "materia", "declension": "1st", "gender": "feminine"},
    "causa": {"def": "cause, reason", "pos": "noun", "translit": "causa", "declension": "1st", "gender": "feminine"},
    "ratio": {"def": "reason, account", "pos": "noun", "translit": "ratio", "declension": "3rd", "gender": "feminine"},
    "mensura": {"def": "measure", "pos": "noun", "translit": "mensura", "declension": "1st", "gender": "feminine"},
    "numerus": {"def": "number", "pos": "noun", "translit": "numerus", "declension": "2nd", "gender": "masculine"},
    "ordo": {"def": "order, rank", "pos": "noun", "translit": "ordo", "declension": "3rd", "gender": "masculine"},
    "modus": {"def": "manner, measure", "pos": "noun", "translit": "modus", "declension": "2nd", "gender": "masculine"},
    "genus": {"def": "kind, race", "pos": "noun", "translit": "genus", "declension": "3rd", "gender": "neuter"},
    "nomen": {"def": "name", "pos": "noun", "translit": "nomen", "declension": "3rd", "gender": "neuter"},
    "res": {"def": "thing, matter, affair", "pos": "noun", "translit": "res", "declension": "5th", "gender": "feminine"},
    "opus": {"def": "work", "pos": "noun", "translit": "opus", "declension": "3rd", "gender": "neuter"},
    "ars": {"def": "art, skill", "pos": "noun", "translit": "ars", "declension": "3rd", "gender": "feminine"},
    "natura": {"def": "nature", "pos": "noun", "translit": "natura", "declension": "1st", "gender": "feminine"},
    "lex": {"def": "law", "pos": "noun", "translit": "lex", "declension": "3rd", "gender": "feminine"},
    "ius": {"def": "law, right, justice", "pos": "noun", "translit": "ius", "declension": "3rd", "gender": "neuter"},
    "potestas": {"def": "power", "pos": "noun", "translit": "potestas", "declension": "3rd", "gender": "feminine"},
    "vis": {"def": "force, power", "pos": "noun", "translit": "vis", "declension": "3rd", "gender": "feminine"},
    "voluntas": {"def": "will, wish", "pos": "noun", "translit": "voluntas", "declension": "3rd", "gender": "feminine"},
    "voluntas": {"def": "will, wish", "pos": "noun", "translit": "voluntas", "declension": "3rd", "gender": "feminine"},
    "voluntas": {"def": "will, wish", "pos": "noun", "translit": "voluntas", "declension": "3rd", "gender": "feminine"},
    
    # Social/Political
    "civitas": {"def": "city, state", "pos": "noun", "translit": "civitas", "declension": "3rd", "gender": "feminine"},
    "urbs": {"def": "city", "pos": "noun", "translit": "urbs", "declension": "3rd", "gender": "feminine"},
    "populus": {"def": "people, nation", "pos": "noun", "translit": "populus", "declension": "2nd", "gender": "masculine"},
    "gens": {"def": "race, people", "pos": "noun", "translit": "gens", "declension": "3rd", "gender": "feminine"},
    "natio": {"def": "nation, race", "pos": "noun", "translit": "natio", "declension": "3rd", "gender": "feminine"},
    "imperium": {"def": "empire, command", "pos": "noun", "translit": "imperium", "declension": "2nd", "gender": "neuter"},
    "provincia": {"def": "province", "pos": "noun", "translit": "provincia", "declension": "1st", "gender": "feminine"},
    "res publica": {"def": "republic, commonwealth", "pos": "noun phrase", "translit": "res publica", "declension": "5th/1st", "gender": "feminine"},
    "senatus": {"def": "senate", "pos": "noun", "translit": "senatus", "declension": "4th", "gender": "masculine"},
    "magistratus": {"def": "magistrate", "pos": "noun", "translit": "magistratus", "declension": "4th", "gender": "masculine"},
    "dux": {"def": "leader", "pos": "noun", "translit": "dux", "declension": "3rd", "gender": "masculine"},
    "princeps": {"def": "chief, first citizen", "pos": "noun", "translit": "princeps", "declension": "3rd", "gender": "masculine"},
    "imperator": {"def": "emperor, commander", "pos": "noun", "translit": "imperator", "declension": "3rd", "gender": "masculine"},
    "consul": {"def": "consul", "pos": "noun", "translit": "consul", "declension": "irregular", "gender": "masculine"},
    "praetor": {"def": "praetor", "pos": "noun", "translit": "praetor", "declension": "3rd", "gender": "masculine"},
    "quaestor": {"def": "quaestor", "pos": "noun", "translit": "quaestor", "declension": "3rd", "gender": "masculine"},
    "aedilis": {"def": "aedile", "pos": "noun", "translit": "aedilis", "declension": "3rd", "gender": "masculine"},
    "tribunus": {"def": "tribune", "pos": "noun", "translit": "tribunus", "declension": "2nd", "gender": "masculine"},
    "civis": {"def": "citizen", "pos": "noun", "translit": "civis", "declension": "3rd", "gender": "masculine/feminine"},
    "servus": {"def": "slave, servant", "pos": "noun", "translit": "servus", "declension": "2nd", "gender": "masculine"},
    "libertus": {"def": "freedman", "pos": "noun", "translit": "libertus", "declension": "2nd", "gender": "masculine"},
    "cliens": {"def": "client", "pos": "noun", "translit": "cliens", "declension": "3rd", "gender": "masculine"},
    "patronus": {"def": "patron", "pos": "noun", "translit": "patronus", "declension": "2nd", "gender": "masculine"},
    "amicus": {"def": "friend", "pos": "noun", "translit": "amicus", "declension": "2nd", "gender": "masculine"},
    "hostis": {"def": "enemy", "pos": "noun", "translit": "hostis", "declension": "3rd", "gender": "masculine"},
    "socius": {"def": "ally, companion", "pos": "noun", "translit": "socius", "declension": "2nd", "gender": "masculine"},
    "foedus": {"def": "treaty, league", "pos": "noun", "translit": "foedus", "declension": "3rd", "gender": "neuter"},
    "pax": {"def": "peace, treaty", "pos": "noun", "translit": "pax", "declension": "3rd", "gender": "feminine"},
    "bellum": {"def": "war", "pos": "noun", "translit": "bellum", "declension": "2nd", "gender": "neuter"},
    "victoria": {"def": "victory", "pos": "noun", "translit": "victoria", "declension": "1st", "gender": "feminine"},
    "triumphus": {"def": "triumph", "pos": "noun", "translit": "triumphus", "declension": "2nd", "gender": "masculine"},
    
    # Military
    "exercitus": {"def": "army", "pos": "noun", "translit": "exercitus", "declension": "4th", "gender": "masculine"},
    "legio": {"def": "legion", "pos": "noun", "translit": "legio", "declension": "3rd", "gender": "feminine"},
    "cohors": {"def": "cohort", "pos": "noun", "translit": "cohors", "declension": "3rd", "gender": "feminine"},
    "centuria": {"def": "century", "pos": "noun", "translit": "centuria", "declension": "1st", "gender": "feminine"},
    "manipulus": {"def": "maniple", "pos": "noun", "translit": "manipulus", "declension": "2nd", "gender": "masculine"},
    "acies": {"def": "battle line", "pos": "noun", "translit": "acies", "declension": "5th", "gender": "feminine"},
    "agmen": {"def": "column, army on the march", "pos": "noun", "translit": "agmen", "declension": "3rd", "gender": "neuter"},
    "castra": {"def": "camp", "pos": "noun", "translit": "castra", "declension": "2nd", "gender": "neuter", "number": "plural"},
    "proelium": {"def": "battle", "pos": "noun", "translit": "proelium", "declension": "2nd", "gender": "neuter"},
    "pugna": {"def": "fight", "pos": "noun", "translit": "pugna", "declension": "1st", "gender": "feminine"},
    "acies": {"def": "sharp edge, battle line", "pos": "noun", "translit": "acies", "declension": "5th", "gender": "feminine"},
    "gladius": {"def": "sword", "pos": "noun", "translit": "gladius", "declension": "2nd", "gender": "masculine"},
    "pilum": {"def": "javelin", "pos": "noun", "translit": "pilum", "declension": "2nd", "gender": "neuter"},
    "scutum": {"def": "shield", "pos": "noun", "translit": "scutum", "declension": "2nd", "gender": "neuter"},
    "lorica": {"def": "breastplate, corselet", "pos": "noun", "translit": "lorica", "declension": "1st", "gender": "feminine"},
    "galea": {"def": "helmet", "pos": "noun", "translit": "galea", "declension": "1st", "gender": "feminine"},
    "hasta": {"def": "spear", "pos": "noun", "translit": "hasta", "declension": "1st", "gender": "feminine"},
    "arcus": {"def": "bow", "pos": "noun", "translit": "arcus", "declension": "4th", "gender": "masculine"},
    "sagitta": {"def": "arrow", "pos": "noun", "translit": "sagitta", "declension": "1st", "gender": "feminine"},
    "machina": {"def": "machine, siege engine", "pos": "noun", "translit": "machina", "declension": "1st", "gender": "feminine"},
    "turris": {"def": "tower", "pos": "noun", "translit": "turris", "declension": "3rd", "gender": "feminine"},
    "murus": {"def": "wall", "pos": "noun", "translit": "murus", "declension": "2nd", "gender": "masculine"},
    "vallum": {"def": "rampart, palisade", "pos": "noun", "translit": "vallum", "declension": "2nd", "gender": "neuter"},
    "fossa": {"def": "ditch, trench", "pos": "noun", "translit": "fossa", "declension": "1st", "gender": "feminine"},
    "porta": {"def": "gate", "pos": "noun", "translit": "porta", "declension": "1st", "gender": "feminine"},
    "navis": {"def": "ship", "pos": "noun", "translit": "navis", "declension": "3rd", "gender": "feminine"},
    "classis": {"def": "fleet, class", "pos": "noun", "translit": "classis", "declension": "3rd", "gender": "feminine"},
    "eques": {"def": "horseman, knight", "pos": "noun", "translit": "eques", "declension": "3rd", "gender": "masculine"},
    "pedes": {"def": "foot-soldier", "pos": "noun", "translit": "pedes", "declension": "3rd", "gender": "masculine"},
    "miles": {"def": "soldier", "pos": "noun", "translit": "miles", "declension": "3rd", "gender": "masculine"},
    "signifer": {"def": "standard-bearer", "pos": "noun", "translit": "signifer", "declension": "irregular", "gender": "masculine"},
    "cornicen": {"def": "horn-blower", "pos": "noun", "translit": "cornicen", "declension": "3rd", "gender": "masculine"},
    "tubicen": {"def": "trumpeter", "pos": "noun", "translit": "tubicen", "declension": "3rd", "gender": "masculine"},
    "lictor": {"def": "lictor", "pos": "noun", "translit": "lictor", "declension": "3rd", "gender": "masculine"},
    
    # Economic
    "pecunia": {"def": "money", "pos": "noun", "translit": "pecunia", "declension": "1st", "gender": "feminine"},
    "res familiaris": {"def": "property, estate", "pos": "noun phrase", "translit": "res familiaris", "declension": "5th/3rd", "gender": "feminine"},
    "patrimonium": {"def": "inheritance", "pos": "noun", "translit": "patrimonium", "declension": "2nd", "gender": "neuter"},
    "peculium": {"def": "private property", "pos": "noun", "translit": "peculium", "declension": "2nd", "gender": "neuter"},
    "aes": {"def": "bronze, copper", "pos": "noun", "translit": "aes", "declension": "3rd", "gender": "neuter"},
    "ferrum": {"def": "iron", "pos": "noun", "translit": "ferrum", "declension": "2nd", "gender": "neuter"},
    "plumbum": {"def": "lead", "pos": "noun", "translit": "plumbum", "declension": "2nd", "gender": "neuter"},
    "aes alienum": {"def": "debt", "pos": "noun phrase", "translit": "aes alienum", "declension": "3rd/2nd", "gender": "neuter"},
    "fenus": {"def": "interest, profit", "pos": "noun", "translit": "fenus", "declension": "3rd", "gender": "neuter"},
    "merces": {"def": "wages, reward", "pos": "noun", "translit": "merces", "declension": "3rd", "gender": "feminine"},
    "stipendium": {"def": "stipend, pay", "pos": "noun", "translit": "stipendium", "declension": "2nd", "gender": "neuter"},
    "vectigal": {"def": "tax, revenue", "pos": "noun", "translit": "vectigal", "declension": "3rd", "gender": "neuter"},
    "tributum": {"def": "tribute, tax", "pos": "noun", "translit": "tributum", "declension": "2nd", "gender": "neuter"},
    "portorium": {"def": "customs duty", "pos": "noun", "translit": "portorium", "declension": "2nd", "gender": "neuter"},
    "decuma": {"def": "tithe", "pos": "noun", "translit": "decuma", "declension": "1st", "gender": "feminine"},
    "quattuorvir": {"def": "member of board of four", "pos": "noun", "translit": "quattuorvir", "declension": "irregular", "gender": "masculine"},
    "decemvir": {"def": "member of board of ten", "pos": "noun", "translit": "decemvir", "declension": "irregular", "gender": "masculine"},
    
    # Agriculture
    "ager": {"def": "field, land", "pos": "noun", "translit": "ager", "declension": "2nd", "gender": "masculine"},
    "arvum": {"def": "plowed land", "pos": "noun", "translit": "arvum", "declension": "2nd", "gender": "neuter"},
    "fundus": {"def": "farm, estate", "pos": "noun", "translit": "fundus", "declension": "2nd", "gender": "masculine"},
    "villa": {"def": "country house, farm", "pos": "noun", "translit": "villa", "declension": "1st", "gender": "feminine"},
    "rus": {"def": "country, countryside", "pos": "noun", "translit": "rus", "declension": "3rd", "gender": "neuter"},
    "seges": {"def": "crop, field of grain", "pos": "noun", "translit": "seges", "declension": "3rd", "gender": "feminine"},
    "messis": {"def": "harvest", "pos": "noun", "translit": "messis", "declension": "3rd", "gender": "feminine"},
    "triticum": {"def": "wheat", "pos": "noun", "translit": "triticum", "declension": "2nd", "gender": "neuter"},
    "hordeum": {"def": "barley", "pos": "noun", "translit": "hordeum", "declension": "2nd", "gender": "neuter"},
    "avena": {"def": "oats", "pos": "noun", "translit": "avena", "declension": "1st", "gender": "feminine"},
    "panis": {"def": "bread", "pos": "noun", "translit": "panis", "declension": "3rd", "gender": "masculine"},
    "vinum": {"def": "wine", "pos": "noun", "translit": "vinum", "declension": "2nd", "gender": "neuter"},
    "oleum": {"def": "oil", "pos": "noun", "translit": "oleum", "declension": "2nd", "gender": "neuter"},
    "lac": {"def": "milk", "pos": "noun", "translit": "lac", "declension": "3rd", "gender": "neuter"},
    "mel": {"def": "honey", "pos": "noun", "translit": "mel", "declension": "3rd", "gender": "neuter"},
    "caseus": {"def": "cheese", "pos": "noun", "translit": "caseus", "declension": "2nd", "gender": "masculine"},
    "caro": {"def": "meat, flesh", "pos": "noun", "translit": "caro", "declension": "3rd", "gender": "feminine"},
    "sal": {"def": "salt", "pos": "noun", "translit": "sal", "declension": "3rd", "gender": "masculine"},
    "arbor": {"def": "tree", "pos": "noun", "translit": "arbor", "declension": "3rd", "gender": "feminine"},
    "vitis": {"def": "vine", "pos": "noun", "translit": "vitis", "declension": "3rd", "gender": "feminine"},
    "uva": {"def": "grape", "pos": "noun", "translit": "uva", "declension": "1st", "gender": "feminine"},
    "malum": {"def": "apple", "pos": "noun", "translit": "malum", "declension": "2nd", "gender": "neuter"},
    "pomum": {"def": "fruit", "pos": "noun", "translit": "pomum", "declension": "2nd", "gender": "neuter"},
    "oliva": {"def": "olive", "pos": "noun", "translit": "oliva", "declension": "1st", "gender": "feminine"},
    "ficus": {"def": "fig", "pos": "noun", "translit": "ficus", "declension": "2nd/4th", "gender": "feminine"},
    "buxus": {"def": "box tree", "pos": "noun", "translit": "buxus", "declension": "2nd", "gender": "feminine"},
    "pinetum": {"def": "pine grove", "pos": "noun", "translit": "pinetum", "declension": "2nd", "gender": "neuter"},
    "querquetum": {"def": "oak grove", "pos": "noun", "translit": "querquetum", "declension": "2nd", "gender": "neuter"},
    
    # Tools/Implements
    "instrumentum": {"def": "tool, instrument", "pos": "noun", "translit": "instrumentum", "declension": "2nd", "gender": "neuter"},
    "machina": {"def": "machine", "pos": "noun", "translit": "machina", "declension": "1st", "gender": "feminine"},
    "fabrica": {"def": "workshop", "pos": "noun", "translit": "fabrica", "declension": "1st", "gender": "feminine"},
    "officina": {"def": "workshop, factory", "pos": "noun", "translit": "officina", "declension": "1st", "gender": "feminine"},
    "stibadium": {"def": "couch", "pos": "noun", "translit": "stibadium", "declension": "2nd", "gender": "neuter"},
    "lectus": {"def": "couch, bed", "pos": "noun", "translit": "lectus", "declension": "2nd", "gender": "masculine"},
    "mensa": {"def": "table", "pos": "noun", "translit": "mensa", "declension": "1st", "gender": "feminine"},
    "triclinium": {"def": "dining room", "pos": "noun", "translit": "triclinium", "declension": "2nd", "gender": "neuter"},
    "cubiculum": {"def": "bedroom", "pos": "noun", "translit": "cubiculum", "declension": "2nd", "gender": "neuter"},
    "atrium": {"def": "hall, court", "pos": "noun", "translit": "atrium", "declension": "2nd", "gender": "neuter"},
    "peristylium": {"def": "colonnade", "pos": "noun", "translit": "peristylium", "declension": "2nd", "gender": "neuter"},
    "impluvium": {"def": "rain basin", "pos": "noun", "translit": "impluvium", "declension": "2nd", "gender": "neuter"},
    "tablinum": {"def": "reception room", "pos": "noun", "translit": "tablinum", "declension": "2nd", "gender": "neuter"},
    "fauces": {"def": "throat, narrow passage", "pos": "noun", "translit": "fauces", "declension": "3rd", "gender": "feminine"},
    "ostium": {"def": "door, entrance", "pos": "noun", "translit": "ostium", "declension": "2nd", "gender": "neuter"},
    "ianua": {"def": "door", "pos": "noun", "translit": "ianua", "declension": "1st", "gender": "feminine"},
    "fenestra": {"def": "window", "pos": "noun", "translit": "fenestra", "declension": "1st", "gender": "feminine"},
    "camera": {"def": "vault, room", "pos": "noun", "translit": "camera", "declension": "1st", "gender": "feminine"},
    "solarium": {"def": "terrace", "pos": "noun", "translit": "solarium", "declension": "2nd", "gender": "neuter"},
    "balneum": {"def": "bath", "pos": "noun", "translit": "balneum", "declension": "2nd", "gender": "neuter"},
    "thermae": {"def": "warm baths", "pos": "noun", "translit": "thermae", "declension": "1st", "gender": "feminine"},
    
    # Clothing
    "vestis": {"def": "clothing", "pos": "noun", "translit": "vestis", "declension": "3rd", "gender": "feminine"},
    "vestimentum": {"def": "garment", "pos": "noun", "translit": "vestimentum", "declension": "2nd", "gender": "neuter"},
    "tunica": {"def": "tunic", "pos": "noun", "translit": "tunica", "declension": "1st", "gender": "feminine"},
    "toga": {"def": "toga", "pos": "noun", "translit": "toga", "declension": "1st", "gender": "feminine"},
    "stola": {"def": "robe, stola", "pos": "noun", "translit": "stola", "declension": "1st", "gender": "feminine"},
    "pallium": {"def": "cloak, mantle", "pos": "noun", "translit": "pallium", "declension": "2nd", "gender": "neuter"},
    "lacerna": {"def": "cape, cloak", "pos": "noun", "translit": "lacerna", "declension": "1st", "gender": "feminine"},
    "paenula": {"def": "thick cloak", "pos": "noun", "translit": "paenula", "declension": "1st", "gender": "feminine"},
    "amiculum": {"def": "wrap, mantle", "pos": "noun", "translit": "amiculum", "declension": "2nd", "gender": "neuter"},
    "sagum": {"def": "military cloak", "pos": "noun", "translit": "sagum", "declension": "2nd", "gender": "neuter"},
    "caliga": {"def": "military boot, sandal", "pos": "noun", "translit": "caliga", "declension": "1st", "gender": "feminine"},
    "solea": {"def": "sandal", "pos": "noun", "translit": "solea", "declension": "1st", "gender": "feminine"},
    "crepida": {"def": "sandal, shoe", "pos": "noun", "translit": "crepida", "declension": "1st", "gender": "feminine"},
    "perna": {"def": "ham", "pos": "noun", "translit": "perna", "declension": "1st", "gender": "feminine"},
    "pileus": {"def": "felt cap", "pos": "noun", "translit": "pileus", "declension": "2nd", "gender": "masculine"},
    "petasus": {"def": "broad-brimmed hat", "pos": "noun", "translit": "petasus", "declension": "2nd", "gender": "masculine"},
    "mitra": {"def": "headband, turban", "pos": "noun", "translit": "mitra", "declension": "1st", "gender": "feminine"},
    "cingulum": {"def": "girdle, belt", "pos": "noun", "translit": "cingulum", "declension": "2nd", "gender": "neuter"},
    "fibula": {"def": "brooch, clasp", "pos": "noun", "translit": "fibula", "declension": "1st", "gender": "feminine"},
    "acu": {"def": "needle", "pos": "noun", "translit": "acu", "declension": "4th", "gender": "feminine"},
    "tela": {"def": "web, loom", "pos": "noun", "translit": "tela", "declension": "1st", "gender": "feminine"},
    "lanaria": {"def": "wool merchant", "pos": "noun", "translit": "lanaria", "declension": "1st", "gender": "feminine"},
    "fullonica": {"def": "fuller's shop", "pos": "noun", "translit": "fullonica", "declension": "1st", "gender": "feminine"},
    "textor": {"def": "weaver", "pos": "noun", "translit": "textor", "declension": "3rd", "gender": "masculine"},
    "linteum": {"def": "linen, linen cloth", "pos": "noun", "translit": "linteum", "declension": "2nd", "gender": "neuter"},
    "byssus": {"def": "fine linen", "pos": "noun", "translit": "byssus", "declension": "2nd", "gender": "feminine"},
    "purpura": {"def": "purple dye, purple cloth", "pos": "noun", "translit": "purpura", "declension": "1st", "gender": "feminine"},
    "coccum": {"def": "scarlet", "pos": "noun", "translit": "coccum", "declension": "2nd", "gender": "neuter"},
    "purpureus": {"def": "purple", "pos": "adjective", "translit": "purpureus", "declension": "1st/2nd", "gender": "masculine"},
    "coccinus": {"def": "scarlet", "pos": "adjective", "translit": "coccinus", "declension": "1st/2nd", "gender": "masculine"},
    
    # Writing/Literature
    "littera": {"def": "letter, literature", "pos": "noun", "translit": "littera", "declension": "1st", "gender": "feminine"},
    "litterae": {"def": "epistle, literature", "pos": "noun", "translit": "litterae", "declension": "1st", "gender": "feminine"},
    "volumen": {"def": "volume, scroll", "pos": "noun", "translit": "volumen", "declension": "3rd", "gender": "neuter"},
    "codex": {"def": "book, codex", "pos": "noun", "translit": "codex", "declension": "3rd", "gender": "masculine"},
    "charta": {"def": "paper, papyrus", "pos": "noun", "translit": "charta", "declension": "1st", "gender": "feminine"},
    "membrana": {"def": "parchment", "pos": "noun", "translit": "membrana", "declension": "1st", "gender": "feminine"},
    "stylus": {"def": "stylus, pen", "pos": "noun", "translit": "stylus", "declension": "2nd", "gender": "masculine"},
    "calamus": {"def": "reed, pen", "pos": "noun", "translit": "calamus", "declension": "2nd", "gender": "masculine"},
    "atramentum": {"def": "ink", "pos": "noun", "translit": "atramentum", "declension": "2nd", "gender": "neuter"},
    "ceratum": {"def": "wax tablet", "pos": "noun", "translit": "ceratum", "declension": "2nd", "gender": "neuter"},
    "tabula": {"def": "tablet, writing tablet", "pos": "noun", "translit": "tabula", "declension": "1st", "gender": "feminine"},
    "scheda": {"def": "strip of papyrus, leaf", "pos": "noun", "translit": "scheda", "declension": "1st", "gender": "feminine"},
    "index": {"def": "index, list, informer", "pos": "noun", "translit": "index", "declension": "3rd", "gender": "masculine"},
    "titulus": {"def": "title, inscription", "pos": "noun", "translit": "titulus", "declension": "2nd", "gender": "masculine"},
    "subscriptio": {"def": "signature, subscription", "pos": "noun", "translit": "subscriptio", "declension": "3rd", "gender": "feminine"},
    "autographum": {"def": "autograph", "pos": "noun", "translit": "autographum", "declension": "2nd", "gender": "neuter"},
    "apographum": {"def": "copy", "pos": "noun", "translit": "apographum", "declension": "2nd", "gender": "neuter"},
    "liber": {"def": "book", "pos": "noun", "translit": "liber", "declension": "2nd", "gender": "masculine"},
    "bibliotheca": {"def": "library", "pos": "noun", "translit": "bibliotheca", "declension": "1st", "gender": "feminine"},
    "poeta": {"def": "poet", "pos": "noun", "translit": "poeta", "declension": "1st", "gender": "masculine"},
    "orator": {"def": "orator", "pos": "noun", "translit": "orator", "declension": "3rd", "gender": "masculine"},
    "historicus": {"def": "historian", "pos": "noun", "translit": "historicus", "declension": "2nd", "gender": "masculine"},
    "grammaticus": {"def": "grammarian, teacher", "pos": "noun", "translit": "grammaticus", "declension": "2nd", "gender": "masculine"},
    "rhetor": {"def": "rhetorician", "pos": "noun", "translit": "rhetor", "declension": "3rd", "gender": "masculine"},
    "philosophus": {"def": "philosopher", "pos": "noun", "translit": "philosophus", "declension": "2nd", "gender": "masculine"},
    "historia": {"def": "history, story", "pos": "noun", "translit": "historia", "declension": "1st", "gender": "feminine"},
    "fabula": {"def": "story, play", "pos": "noun", "translit": "fabula", "declension": "1st", "gender": "feminine"},
    "tragoedia": {"def": "tragedy", "pos": "noun", "translit": "tragoedia", "declension": "1st", "gender": "feminine"},
    "comoedia": {"def": "comedy", "pos": "noun", "translit": "comoedia", "declension": "1st", "gender": "feminine"},
    "ecloga": {"def": "eclogue, selection", "pos": "noun", "translit": "ecloga", "declension": "1st", "gender": "feminine"},
    "carmen": {"def": "song, poem", "pos": "noun", "translit": "carmen", "declension": "3rd", "gender": "neuter"},
    "versus": {"def": "verse, line", "pos": "noun", "translit": "versus", "declension": "4th", "gender": "masculine"},
    "sententia": {"def": "opinion, sentence", "pos": "noun", "translit": "sententia", "declension": "1st", "gender": "feminine"},
    "verbum": {"def": "word", "pos": "noun", "translit": "verbum", "declension": "2nd", "gender": "neuter"},
    "nomen": {"def": "name", "pos": "noun", "translit": "nomen", "declension": "3rd", "gender": "neuter"},
    "vocabulum": {"def": "word, term", "pos": "noun", "translit": "vocabulum", "declension": "2nd", "gender": "neuter"},
    "sermo": {"def": "speech, conversation", "pos": "noun", "translit": "sermo", "declension": "3rd", "gender": "masculine"},
    "oratio": {"def": "speech, prayer", "pos": "noun", "translit": "oratio", "declension": "3rd", "gender": "feminine"},
    "concio": {"def": "assembly, speech", "pos": "noun", "translit": "concio", "declension": "3rd", "gender": "feminine"},
    "declamatio": {"def": "declamation", "pos": "noun", "translit": "declamatio", "declension": "3rd", "gender": "feminine"},
    "recitatio": {"def": "reading aloud, recitation", "pos": "noun", "translit": "recitatio", "declension": "3rd", "gender": "feminine"},
    "lectio": {"def": "reading", "pos": "noun", "translit": "lectio", "declension": "3rd", "gender": "feminine"},
    "dictio": {"def": "expression, word", "pos": "noun", "translit": "dictio", "declension": "3rd", "gender": "feminine"},
    "elocutio": {"def": "style, expression", "pos": "noun", "translit": "elocutio", "declension": "3rd", "gender": "feminine"},
    "pronuntiatio": {"def": "delivery, pronunciation", "pos": "noun", "translit": "pronuntiatio", "declension": "3rd", "gender": "feminine"},
    "memoria": {"def": "memory", "pos": "noun", "translit": "memoria", "declension": "1st", "gender": "feminine"},
    "ars": {"def": "art, skill", "pos": "noun", "translit": "ars", "declension": "3rd", "gender": "feminine"},
    "ars poetica": {"def": "poetic art", "pos": "noun phrase", "translit": "ars poetica", "declension": "3rd/1st", "gender": "feminine"},
    "ars rhetorica": {"def": "rhetoric", "pos": "noun phrase", "translit": "ars rhetorica", "declension": "3rd/1st", "gender": "feminine"},
    "ars grammatica": {"def": "grammar", "pos": "noun phrase", "translit": "ars grammatica", "declension": "3rd/1st", "gender": "feminine"},
    "copia verborum": {"def": "abundance of words", "pos": "noun phrase", "translit": "copia verborum", "declension": "1st/2nd", "gender": "feminine/neuter"},
    "figura": {"def": "figure, form", "pos": "noun", "translit": "figura", "declension": "1st", "gender": "feminine"},
    "tropus": {"def": "trope", "pos": "noun", "translit": "tropus", "declension": "2nd", "gender": "masculine"},
    "schema": {"def": "scheme, figure", "pos": "noun", "translit": "schema", "declension": "3rd", "gender": "neuter"},
    "metrum": {"def": "meter", "pos": "noun", "translit": "metrum", "declension": "2nd", "gender": "neuter"},
    "versus": {"def": "verse", "pos": "noun", "translit": "versus", "declension": "4th", "gender": "masculine"},
    "hexameter": {"def": "hexameter", "pos": "noun", "translit": "hexameter", "declension": "3rd", "gender": "masculine"},
    "pentameter": {"def": "pentameter", "pos": "noun", "translit": "pentameter", "declension": "3rd", "gender": "masculine"},
    "elegia": {"def": "elegy, elegiac verse", "pos": "noun", "translit": "elegia", "declension": "1st", "gender": "feminine"},
    "epigramma": {"def": "epigram", "pos": "noun", "translit": "epigramma", "declension": "3rd", "gender": "neuter"},
    "epistula": {"def": "letter, epistle", "pos": "noun", "translit": "epistula", "declension": "1st", "gender": "feminine"},
    "satira": {"def": "satire", "pos": "noun", "translit": "satira", "declension": "1st", "gender": "feminine"},
    "ode": {"def": "ode", "pos": "noun", "translit": "ode", "declension": "3rd", "gender": "feminine"},
    "hymnus": {"def": "hymn", "pos": "noun", "translit": "hymnus", "declension": "2nd", "gender": "masculine"},
    "psalmus": {"def": "psalm", "pos": "noun", "translit": "psalmus", "declension": "2nd", "gender": "masculine"},
    "canticum": {"def": "song, canticle", "pos": "noun", "translit": "canticum", "declension": "2nd", "gender": "neuter"},
    "laudes": {"def": "praises", "pos": "noun", "translit": "laudes", "declension": "3rd", "gender": "feminine"},
    "gloria": {"def": "glory", "pos": "noun", "translit": "gloria", "declension": "1st", "gender": "feminine"},
    "honor": {"def": "honor", "pos": "noun", "translit": "honor", "declension": "3rd", "gender": "masculine"},
    "laus": {"def": "praise", "pos": "noun", "translit": "laus", "declension": "3rd", "gender": "feminine"},
    "decus": {"def": "honor, beauty", "pos": "noun", "translit": "decus", "declension": "3rd", "gender": "neuter"},
    "decorum": {"def": "propriety, decorum", "pos": "noun", "translit": "decorum", "declension": "2nd", "gender": "neuter"},
    
    # Law
    "ius": {"def": "law, right, justice", "pos": "noun", "translit": "ius", "declension": "3rd", "gender": "neuter"},
    "lex": {"def": "law", "pos": "noun", "translit": "lex", "declension": "3rd", "gender": "feminine"},
    "mos": {"def": "custom, habit", "pos": "noun", "translit": "mos", "declension": "3rd", "gender": "masculine"},
    "mores": {"def": "morals, customs", "pos": "noun", "translit": "mores", "declension": "3rd", "gender": "masculine"},
    "ius civile": {"def": "civil law", "pos": "noun phrase", "translit": "ius civile", "declension": "3rd/2nd", "gender": "neuter"},
    "ius gentium": {"def": "law of nations", "pos": "noun phrase", "translit": "ius gentium", "declension": "3rd/2nd", "gender": "neuter"},
    "ius naturale": {"def": "natural law", "pos": "noun phrase", "translit": "ius naturale", "declension": "3rd/2nd", "gender": "neuter"},
    "ius divinum": {"def": "divine law", "pos": "noun phrase", "translit": "ius divinum", "declension": "3rd/2nd", "gender": "neuter"},
    "ius publicum": {"def": "public law", "pos": "noun phrase", "translit": "ius publicum", "declension": "3rd/2nd", "gender": "neuter"},
    "ius privatum": {"def": "private law", "pos": "noun phrase", "translit": "ius privatum", "declension": "3rd/2nd", "gender": "neuter"},
    "ius honorarium": {"def": "praetorian law", "pos": "noun phrase", "translit": "ius honorarium", "declension": "3rd/2nd", "gender": "neuter"},
    "edictum": {"def": "edict", "pos": "noun", "translit": "edictum", "declension": "2nd", "gender": "neuter"},
    "senatus consultum": {"def": "senatorial decree", "pos": "noun phrase", "translit": "senatus consultum", "declension": "4th/2nd", "gender": "neuter"},
    "plebiscitum": {"def": "plebiscite", "pos": "noun", "translit": "plebiscitum", "declension": "2nd", "gender": "neuter"},
    "responsum": {"def": "legal opinion", "pos": "noun", "translit": "responsum", "declension": "2nd", "gender": "neuter"},
    "interdictum": {"def": "interdict, injunction", "pos": "noun", "translit": "interdictum", "declension": "2nd", "gender": "neuter"},
    "actio": {"def": "action, lawsuit", "pos": "noun", "translit": "actio", "declension": "3rd", "gender": "feminine"},
    "iudicium": {"def": "trial, judgment", "pos": "noun", "translit": "iudicium", "declension": "2nd", "gender": "neuter"},
    "litis": {"def": "dispute, lawsuit", "pos": "noun", "translit": "litis", "declension": "3rd", "gender": "feminine"},
    "lis": {"def": "lawsuit, quarrel", "pos": "noun", "translit": "lis", "declension": "3rd", "gender": "feminine"},
    "causa": {"def": "cause, case", "pos": "noun", "translit": "causa", "declension": "1st", "gender": "feminine"},
    "crimen": {"def": "accusation, crime", "pos": "noun", "translit": "crimen", "declension": "3rd", "gender": "neuter"},
    "delictum": {"def": "offense, delict", "pos": "noun", "translit": "delictum", "declension": "2nd", "gender": "neuter"},
    "facinus": {"def": "deed, crime", "pos": "noun", "translit": "facinus", "declension": "3rd", "gender": "neuter"},
    "maleficium": {"def": "wrongdoing, sorcery", "pos": "noun", "translit": "maleficium", "declension": "2nd", "gender": "neuter"},
    "poena": {"def": "punishment, penalty", "pos": "noun", "translit": "poena", "declension": "1st", "gender": "feminine"},
    "supplicium": {"def": "punishment, supplication", "pos": "noun", "translit": "supplicium", "declension": "2nd", "gender": "neuter"},
    "damnum": {"def": "damage, loss", "pos": "noun", "translit": "damnum", "declension": "2nd", "gender": "neuter"},
    " iniuria": {"def": "injustice, injury", "pos": "noun", "translit": " iniuria", "declension": "1st", "gender": "feminine"},
    " iniustitia": {"def": "injustice", "pos": "noun", "translit": " iniustitia", "declension": "1st", "gender": "feminine"},
    "culpa": {"def": "fault, blame", "pos": "noun", "translit": "culpa", "declension": "1st", "gender": "feminine"},
    "dolus": {"def": "fraud, deceit", "pos": "noun", "translit": "dolus", "declension": "2nd", "gender": "masculine"},
    "fraus": {"def": "fraud, deceit", "pos": "noun", "translit": "fraus", "declension": "3rd", "gender": "feminine"},
    "decemvir": {"def": "member of board of ten", "pos": "noun", "translit": "decemvir", "declension": "irregular", "gender": "masculine"},
    "tribunus plebis": {"def": "tribune of the plebs", "pos": "noun phrase", "translit": "tribunus plebis", "declension": "2nd/3rd", "gender": "masculine"},
    "aedilis": {"def": "aedile", "pos": "noun", "translit": "aedilis", "declension": "3rd", "gender": "masculine"},
    "praetor": {"def": "praetor", "pos": "noun", "translit": "praetor", "declension": "3rd", "gender": "masculine"},
    "quaestor": {"def": "quaestor", "pos": "noun", "translit": "quaestor", "declension": "3rd", "gender": "masculine"},
    "censor": {"def": "censor", "pos": "noun", "translit": "censor", "declension": "3rd", "gender": "masculine"},
    "consul": {"def": "consul", "pos": "noun", "translit": "consul", "declension": "irregular", "gender": "masculine"},
    "dictator": {"def": "dictator", "pos": "noun", "translit": "dictator", "declension": "3rd", "gender": "masculine"},
    "magister equitum": {"def": "master of horse", "pos": "noun phrase", "translit": "magister equitum", "declension": "2nd/2nd", "gender": "masculine"},
    "proconsul": {"def": "proconsul", "pos": "noun", "translit": "proconsul", "declension": "irregular", "gender": "masculine"},
    "propraetor": {"def": "propraetor", "pos": "noun", "translit": "propraetor", "declension": "irregular", "gender": "masculine"},
    "legatus": {"def": "legate, ambassador", "pos": "noun", "translit": "legatus", "declension": "2nd", "gender": "masculine"},
    "praefectus": {"def": "prefect", "pos": "noun", "translit": "praefectus", "declension": "2nd", "gender": "masculine"},
    "vigintisexvir": {"def": "member of board of twenty-six", "pos": "noun", "translit": "vigintisexvir", "declension": "irregular", "gender": "masculine"},
    
    # Religion
    "religio": {"def": "religion", "pos": "noun", "translit": "religio", "declension": "3rd", "gender": "feminine"},
    "cultus": {"def": "cult, worship", "pos": "noun", "translit": "cultus", "declension": "4th", "gender": "masculine"},
    "ritus": {"def": "rite", "pos": "noun", "translit": "ritus", "declension": "4th", "gender": "masculine"},
    "caerimonia": {"def": "religious ceremony", "pos": "noun", "translit": "caerimonia", "declension": "1st", "gender": "feminine"},
    "sacrum": {"def": "sacred rite", "pos": "noun", "translit": "sacrum", "declension": "2nd", "gender": "neuter"},
    "sacrificium": {"def": "sacrifice", "pos": "noun", "translit": "sacrificium", "declension": "2nd", "gender": "neuter"},
    "victima": {"def": "victim, sacrificial animal", "pos": "noun", "translit": "victima", "declension": "1st", "gender": "feminine"},
    "hostia": {"def": "sacrificial victim", "pos": "noun", "translit": "hostia", "declension": "1st", "gender": "feminine"},
    "libamen": {"def": "libation", "pos": "noun", "translit": "libamen", "declension": "3rd", "gender": "neuter"},
    "thura": {"def": "incense", "pos": "noun", "translit": "thura", "declension": "1st", "gender": "feminine"},
    "delubrum": {"def": "shrine, temple", "pos": "noun", "translit": "delubrum", "declension": "2nd", "gender": "neuter"},
    "fanum": {"def": "shrine, temple", "pos": "noun", "translit": "fanum", "declension": "2nd", "gender": "neuter"},
    "sacellum": {"def": "small shrine", "pos": "noun", "translit": "sacellum", "declension": "2nd", "gender": "neuter"},
    "sacristia": {"def": "sacristy", "pos": "noun", "translit": "sacristia", "declension": "1st", "gender": "feminine"},
    "aedes sacra": {"def": "sacred building", "pos": "noun phrase", "translit": "aedes sacra", "declension": "3rd/1st", "gender": "feminine"},
    "ara": {"def": "altar", "pos": "noun", "translit": "ara", "declension": "1st", "gender": "feminine"},
    "focus": {"def": "hearth, altar", "pos": "noun", "translit": "focus", "declension": "2nd", "gender": "masculine"},
    "lucus": {"def": "grove", "pos": "noun", "translit": "lucus", "declension": "2nd", "gender": "masculine"},
    "nemus": {"def": "grove, forest", "pos": "noun", "translit": "nemus", "declension": "3rd", "gender": "neuter"},
    "silva": {"def": "wood, forest", "pos": "noun", "translit": "silva", "declension": "1st", "gender": "feminine"},
    "precatio": {"def": "prayer", "pos": "noun", "translit": "precatio", "declension": "3rd", "gender": "feminine"},
    "invocatio": {"def": "invocation", "pos": "noun", "translit": "invocatio", "declension": "3rd", "gender": "feminine"},
    "votum": {"def": "vow", "pos": "noun", "translit": "votum", "declension": "2nd", "gender": "neuter"},
    "nuncupatio": {"def": "solemn declaration", "pos": "noun", "translit": "nuncupatio", "declension": "3rd", "gender": "feminine"},
    "dedicatio": {"def": "dedication", "pos": "noun", "translit": "dedicatio", "declension": "3rd", "gender": "feminine"},
    "consecratio": {"def": "consecration", "pos": "noun", "translit": "consecratio", "declension": "3rd", "gender": "feminine"},
    " inauguratio": {"def": "inauguration", "pos": "noun", "translit": " inauguratio", "declension": "3rd", "gender": "feminine"},
    "purificatio": {"def": "purification", "pos": "noun", "translit": "purificatio", "declension": "3rd", "gender": "feminine"},
    "piaculum": {"def": "expiatory sacrifice", "pos": "noun", "translit": "piaculum", "declension": "2nd", "gender": "neuter"},
    "piamentum": {"def": "means of expiation", "pos": "noun", "translit": "piamentum", "declension": "2nd", "gender": "neuter"},
    "sacerdos": {"def": "priest", "pos": "noun", "translit": "sacerdos", "declension": "3rd", "gender": "masculine"},
    "flamen": {"def": "priest", "pos": "noun", "translit": "flamen", "declension": "3rd", "gender": "masculine"},
    "pontifex": {"def": "pontiff, high priest", "pos": "noun", "translit": "pontifex", "declension": "3rd", "gender": "masculine"},
    "pontifex maximus": {"def": "high priest", "pos": "noun phrase", "translit": "pontifex maximus", "declension": "3rd/1st/2nd", "gender": "masculine"},
    "rex sacrorum": {"def": "king of sacred rites", "pos": "noun phrase", "translit": "rex sacrorum", "declension": "3rd/2nd", "gender": "masculine"},
    "augur": {"def": "augur, soothsayer", "pos": "noun", "translit": "augur", "declension": "3rd", "gender": "masculine"},
    "haruspex": {"def": "haruspex, diviner", "pos": "noun", "translit": "haruspex", "declension": "3rd", "gender": "masculine"},
    "decemvir sacris faciundis": {"def": "board of ten for sacred rites", "pos": "noun phrase", "translit": "decemvir sacris faciundis", "declension": "irregular/3rd", "gender": "masculine"},
    "septemvir epulonum": {"def": "board of seven for feasts", "pos": "noun phrase", "translit": "septemvir epulonum", "declension": "irregular/2nd", "gender": "masculine"},
    "quindecimvir sacris faciundis": {"def": "board of fifteen for sacred rites", "pos": "noun phrase", "translit": "quindecimvir sacris faciundis", "declension": "irregular/3rd", "gender": "masculine"},
    "salii": {"def": "leaping priests", "pos": "noun", "translit": "salii", "declension": "2nd", "gender": "masculine"},
    "luperci": {"def": "priests of Lupercus", "pos": "noun", "translit": "luperci", "declension": "2nd", "gender": "masculine"},
    "fetiales": {"def": "fetial priests", "pos": "noun", "translit": "fetiales", "declension": "3rd", "gender": "masculine"},
    "fratres arvales": {"def": "Arval brothers", "pos": "noun phrase", "translit": "fratres arvales", "declension": "3rd/3rd", "gender": "masculine"},
    "virgo vestalis": {"def": "Vestal virgin", "pos": "noun phrase", "translit": "virgo vestalis", "declension": "3rd/3rd", "gender": "feminine"},
    "sibylla": {"def": "sibyl", "pos": "noun", "translit": "sibylla", "declension": "1st", "gender": "feminine"},
    "vates": {"def": "prophet, poet", "pos": "noun", "translit": "vates", "declension": "3rd", "gender": "masculine/feminine"},
    "deus": {"def": "god", "pos": "noun", "translit": "deus", "declension": "2nd", "gender": "masculine"},
    "dea": {"def": "goddess", "pos": "noun", "translit": "dea", "declension": "1st", "gender": "feminine"},
    "divus": {"def": "deified", "pos": "adjective", "translit": "divus", "declension": "1st/2nd", "gender": "masculine"},
    "numen": {"def": "divine power, deity", "pos": "noun", "translit": "numen", "declension": "3rd", "gender": "neuter"},
    "genius": {"def": "guardian spirit", "pos": "noun", "translit": "genius", "declension": "2nd", "gender": "masculine"},
    "iuno": {"def": "Juno", "pos": "proper noun", "translit": "iuno", "declension": "3rd", "gender": "feminine"},
    "minerva": {"def": "Minerva", "pos": "proper noun", "translit": "minerva", "declension": "1st", "gender": "feminine"},
    "venus": {"def": "Venus", "pos": "proper noun", "translit": "venus", "declension": "3rd", "gender": "feminine"},
    "mars": {"def": "Mars", "pos": "proper noun", "translit": "mars", "declension": "3rd", "gender": "masculine"},
    "mercurius": {"def": "Mercury", "pos": "proper noun", "translit": "mercurius", "declension": "2nd", "gender": "masculine"},
    "iupiter": {"def": "Jupiter", "pos": "proper noun", "translit": "iupiter", "declension": "3rd", "gender": "masculine"},
    "iuno": {"def": "Juno", "pos": "proper noun", "translit": "iuno", "declension": "3rd", "gender": "feminine"},
    "neptunus": {"def": "Neptune", "pos": "proper noun", "translit": "neptunus", "declension": "2nd", "gender": "masculine"},
    "pluto": {"def": "Pluto", "pos": "proper noun", "translit": "pluto", "declension": "3rd", "gender": "masculine"},
    "apollo": {"def": "Apollo", "pos": "proper noun", "translit": "apollo", "declension": "3rd", "gender": "masculine"},
    "diana": {"def": "Diana", "pos": "proper noun", "translit": "diana", "declension": "1st", "gender": "feminine"},
    "vesta": {"def": "Vesta", "pos": "proper noun", "translit": "vesta", "declension": "1st", "gender": "feminine"},
    "ceres": {"def": "Ceres", "pos": "proper noun", "translit": "ceres", "declension": "3rd", "gender": "feminine"},
    "proserpina": {"def": "Proserpina", "pos": "proper noun", "translit": "proserpina", "declension": "1st", "gender": "feminine"},
    "bacchus": {"def": "Bacchus", "pos": "proper noun", "translit": "bacchus", "declension": "2nd", "gender": "masculine"},
    "liber": {"def": "Liber", "pos": "proper noun", "translit": "liber", "declension": "2nd", "gender": "masculine"},
    "libera": {"def": "Libera", "pos": "proper noun", "translit": "libera", "declension": "1st", "gender": "feminine"},
    "pan": {"def": "Pan", "pos": "proper noun", "translit": "pan", "declension": "3rd", "gender": "masculine"},
    "faunus": {"def": "Faunus", "pos": "proper noun", "translit": "faunus", "declension": "2nd", "gender": "masculine"},
    "silvanus": {"def": "Silvanus", "pos": "proper noun", "translit": "silvanus", "declension": "2nd", "gender": "masculine"},
    "terminus": {"def": "Terminus", "pos": "proper noun", "translit": "terminus", "declension": "2nd", "gender": "masculine"},
    "janus": {"def": "Janus", "pos": "proper noun", "translit": "janus", "declension": "2nd", "gender": "masculine"},
    "quirinus": {"def": "Quirinus", "pos": "proper noun", "translit": "quirinus", "declension": "2nd", "gender": "masculine"},
    "romulus": {"def": "Romulus", "pos": "proper noun", "translit": "romulus", "declension": "2nd", "gender": "masculine"},
    "remus": {"def": "Remus", "pos": "proper noun", "translit": "remus", "declension": "2nd", "gender": "masculine"},
    "aeneas": {"def": "Aeneas", "pos": "proper noun", "translit": "aeneas", "declension": "1st", "gender": "masculine"},
    "hercules": {"def": "Hercules", "pos": "proper noun", "translit": "hercules", "declension": "3rd", "gender": "masculine"},
    "castor": {"def": "Castor", "pos": "proper noun", "translit": "castor", "declension": "3rd", "gender": "masculine"},
    "pollux": {"def": "Pollux", "pos": "proper noun", "translit": "pollux", "declension": "3rd", "gender": "masculine"},
    "penates": {"def": "Penates", "pos": "noun", "translit": "penates", "declension": "3rd", "gender": "masculine"},
    "lares": {"def": "Lares", "pos": "noun", "translit": "lares", "declension": "3rd", "gender": "masculine"},
    "manes": {"def": "spirits of the dead", "pos": "noun", "translit": "manes", "declension": "3rd", "gender": "masculine"},
    "lemures": {"def": "ghosts", "pos": "noun", "translit": "lemures", "declension": "3rd", "gender": "masculine"},
    "larva": {"def": "mask, ghost", "pos": "noun", "translit": "larva", "declension": "1st", "gender": "feminine"},
    "spectrum": {"def": "apparition, ghost", "pos": "noun", "translit": "spectrum", "declension": "2nd", "gender": "neuter"},
    "umbra": {"def": "shade, ghost", "pos": "noun", "translit": "umbra", "declension": "1st", "gender": "feminine"},
    "simulacrum": {"def": "image, statue", "pos": "noun", "translit": "simulacrum", "declension": "2nd", "gender": "neuter"},
    "effigies": {"def": "effigy, image", "pos": "noun", "translit": "effigies", "declension": "5th", "gender": "feminine"},
    "imago": {"def": "image", "pos": "noun", "translit": "imago", "declension": "3rd", "gender": "feminine"},
    "forma": {"def": "form", "pos": "noun", "translit": "forma", "declension": "1st", "gender": "feminine"},
    "species": {"def": "appearance, kind", "pos": "noun", "translit": "species", "declension": "5th", "gender": "feminine"},
    "idolum": {"def": "idol, image", "pos": "noun", "translit": "idolum", "declension": "2nd", "gender": "neuter"},
    "daemon": {"def": "demon, spirit", "pos": "noun", "translit": "daemon", "declension": "3rd", "gender": "masculine"},
    "genius": {"def": "genius, guardian spirit", "pos": "noun", "translit": "genius", "declension": "2nd", "gender": "masculine"},
    "anima": {"def": "soul, breath", "pos": "noun", "translit": "anima", "declension": "1st", "gender": "feminine"},
    "animus": {"def": "mind, spirit", "pos": "noun", "translit": "animus", "declension": "2nd", "gender": "masculine"},
    "mens": {"def": "mind", "pos": "noun", "translit": "mens", "declension": "3rd", "gender": "feminine"},
    "spiritus": {"def": "spirit, breath", "pos": "noun", "translit": "spiritus", "declension": "4th", "gender": "masculine"},
    "corpus": {"def": "body", "pos": "noun", "translit": "corpus", "declension": "3rd", "gender": "neuter"},
    "sanguis": {"def": "blood", "pos": "noun", "translit": "sanguis", "declension": "3rd", "gender": "masculine"},
    "viscera": {"def": "internal organs, entrails", "pos": "noun", "translit": "viscera", "declension": "3rd", "gender": "neuter"},
    "exta": {"def": "entrails", "pos": "noun", "translit": "exta", "declension": "3rd", "gender": "neuter"},
    "litatio": {"def": "favorable sacrifice", "pos": "noun", "translit": "litatio", "declension": "3rd", "gender": "feminine"},
    "obtentio": {"def": "obtaining favorable omens", "pos": "noun", "translit": "obtentio", "declension": "3rd", "gender": "feminine"},
    "vitium": {"def": "fault, defect in omens", "pos": "noun", "translit": "vitium", "declension": "2nd", "gender": "neuter"},
    "procuratio": {"def": "expiation", "pos": "noun", "translit": "procuratio", "declension": "3rd", "gender": "feminine"},
    "evocatio": {"def": "evocation", "pos": "noun", "translit": "evocatio", "declension": "3rd", "gender": "feminine"},
    "devotio": {"def": "devotion", "pos": "noun", "translit": "devotio", "declension": "3rd", "gender": "feminine"},
    "evocatio deorum": {"def": "evocation of gods", "pos": "noun phrase", "translit": "evocatio deorum", "declension": "3rd/2nd", "gender": "feminine/masculine"},
    "devotio ducis": {"def": "devotion of the commander", "pos": "noun phrase", "translit": "devotio ducis", "declension": "3rd/3rd", "gender": "feminine/masculine"},
    "evocatio": {"def": "evocation", "pos": "noun", "translit": "evocatio", "declension": "3rd", "gender": "feminine"},
    "devotio": {"def": "devotion", "pos": "noun", "translit": "devotio", "declension": "3rd", "gender": "feminine"},
    "evocatio": {"def": "evocation", "pos": "noun", "translit": "evocatio", "declension": "3rd", "gender": "feminine"},
    "devotio": {"def": "devotion", "pos": "noun", "translit": "devotio", "declension": "3rd", "gender": "feminine"},
    "evocatio": {"def": "evocation", "pos": "noun", "translit": "evocatio", "declension": "3rd", "gender": "feminine"},
    "devotio": {"def": "devotion", "pos": "noun", "translit": "devotio", "declension": "3rd", "gender": "feminine"},
    "evocatio": {"def": "evocation", "pos": "noun", "translit": "evocatio", "declension": "3rd", "gender": "feminine"},
    "devotio": {"def": "devotion", "pos": "noun", "translit": "devotio", "declension": "3rd", "gender": "feminine"},
    "evocatio": {"def": "evocation", "pos": "noun", "translit": "evocatio", "declension": "3rd", "gender": "feminine"},
    "devotio": {"def": "devotion", "pos": "noun", "translit": "devotio", "declension": "3rd", "gender": "feminine"},
}

class LatinLexicon:
    """Latin-English lexicon"""
    
    def __init__(self):
        self.entries = {}
        self.root_index = defaultdict(list)
        
    def build(self):
        """Build lexicon from vocabulary lists"""
        print("[*] Building Latin lexicon...")
        
        # Combine vocabularies
        all_vocab = {**LATIN_CORE_VOCABULARY, **LATIN_EXTENDED_VOCABULARY}
        
        for word, data in all_vocab.items():
            entry = {
                "word": word,
                "definition": data["def"],
                "part_of_speech": data["pos"],
                "transliteration": data["translit"],
            }
            
            # Add optional fields
            if "root" in data:
                entry["root"] = data["root"]
            if "declension" in data:
                entry["declension"] = data["declension"]
            if "conjugation" in data:
                entry["conjugation"] = data["conjugation"]
            if "gender" in data:
                entry["gender"] = data["gender"]
            if "case" in data:
                entry["case"] = data["case"]
            if "person" in data:
                entry["person"] = data["person"]
            if "number" in data:
                entry["number"] = data["number"]
            if "deponent" in data:
                entry["deponent"] = data["deponent"]
            if "impersonal" in data:
                entry["impersonal"] = data["impersonal"]
            if "indeclinable" in data:
                entry["indeclinable"] = data["indeclinable"]
            
            self.entries[word] = entry
            
            # Index by root
            if "root" in data and data["root"]:
                for root_part in data["root"].split(";"):
                    self.root_index[root_part.strip()].append(word)
        
        print(f"    [+] Built {len(self.entries)} entries")
        
    def export_json(self, output_path: str):
        """Export to JSON"""
        print(f"[*] Exporting to {output_path}...")
        
        data = {
            "metadata": {
                "title": "Latin Lexicon",
                "language": "Latin (Classical and Ecclesiastical)",
                "period": "Classical (100 BCE-200 CE), Ecclesiastical (to present)",
                "total_entries": len(self.entries),
                "format": "JSON",
                "notes": "Includes Classical Latin and Ecclesiastical/Church Latin. Vulgate Bible uses Ecclesiastical Latin."
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
            f.write("# Latin Lexicon\n\n")
            f.write("**Latin-English Dictionary (Classical and Ecclesiastical)**\n\n")
            f.write(f"Total Entries: {len(self.entries)}\n\n")
            f.write("---\n\n")
            
            # Sort by Latin word
            sorted_entries = sorted(self.entries.items(), key=lambda x: x[0])
            
            for word, entry in sorted_entries:
                f.write(f"## {word}\n\n")
                f.write(f"**Transliteration:** *{entry['transliteration']}*\n\n")
                f.write(f"**Part of Speech:** {entry['part_of_speech']}\n\n")
                f.write(f"**Definition:** {entry['definition']}\n\n")
                
                if "declension" in entry:
                    f.write(f"**Declension:** {entry['declension']}\n\n")
                if "conjugation" in entry:
                    f.write(f"**Conjugation:** {entry['conjugation']}\n\n")
                if "gender" in entry:
                    f.write(f"**Gender:** {entry['gender']}\n\n")
                if "root" in entry:
                    f.write(f"**Root:** {entry['root']}\n\n")
                    
                f.write("---\n\n")
        
        print(f"    [+] Exported {len(self.entries)} entries")
    
    def export_websters_style(self, output_path: str):
        """Export in Webster's dictionary format"""
        print(f"[*] Exporting Webster's style to {output_path}...")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("LATIN LEXICON\n")
            f.write("Classical and Ecclesiastical Latin Dictionary\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("About Latin:\n")
            f.write("  - Language of ancient Rome and the Roman Empire\n")
            f.write("  - Classical Latin: 100 BCE - 200 CE\n")
            f.write("  - Ecclesiastical Latin: Church and Vulgate Bible (400 CE-present)\n")
            f.write("  - Extensive case system (nominative, genitive, dative, accusative, ablative, vocative)\n")
            f.write("  - Five declensions, four conjugations\n\n")
            
            f.write("Pronunciation Guide:\n")
            f.write("  ā = long a (father)    ă = short a (cat)\n")
            f.write("  ē = long e (say)       ĕ = short e (pet)\n")
            f.write("  ī = long i (machine)   ĭ = short i (pin)\n")
            f.write("  ō = long o (tone)      ŏ = short o (hot)\n")
            f.write("  ū = long u (rule)      ŭ = short u (put)\n")
            f.write("  c = always hard k (cat)   g = always hard g (go)\n")
            f.write("  v = w or v               j = y (as in yes)\n\n")
            
            f.write("-" * 70 + "\n\n")
            
            sorted_entries = sorted(self.entries.items(), key=lambda x: x[0])
            
            for word, entry in sorted_entries:
                f.write(f"\n{word}")
                if entry['transliteration'] != word.lower():
                    f.write(f"  ({entry['transliteration']})")
                
                f.write(f"  [{entry['part_of_speech']}]")
                
                # Add grammar info
                grammar = []
                if "declension" in entry:
                    grammar.append(f"{entry['declension']} decl.")
                if "conjugation" in entry:
                    grammar.append(f"{entry['conjugation']} conj.")
                if "gender" in entry:
                    grammar.append(entry['gender'])
                    
                if grammar:
                    f.write(f" ({', '.join(grammar)})")
                
                f.write("\n")
                
                # Definition
                f.write(f"    {entry['definition']}\n")
                
                # Root
                if "root" in entry:
                    f.write(f"    Root: {entry['root']}\n")
                
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
            elif 'root' in entry and query_lower in entry['root'].lower():
                match = True
            
            if match:
                results.append((word, entry))
        
        return results


def main():
    lexicon = LatinLexicon()
    
    # Build from vocabulary
    lexicon.build()
    
    # Create output directory
    out_dir = Path("/root/latin_lexicon_output")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Export all formats
    lexicon.export_json(out_dir / "latin_lexicon.json")
    lexicon.export_markdown(out_dir / "latin_lexicon.md")
    lexicon.export_websters_style(out_dir / "websters_latin.txt")
    
    # Sample entries
    print("\n" + "=" * 70)
    print("SAMPLE ENTRIES")
    print("=" * 70 + "\n")
    
    sample_words = ['Deus', 'Dominus', 'Iesus', 'caritas', 'veritas', 'pax']
    for word in sample_words:
        if word in lexicon.entries:
            e = lexicon.entries[word]
            print(f"{word} ({e['transliteration']})")
            print(f"  {e['definition']}")
            print(f"  [{e['part_of_speech']}]\n")
    
    print("=" * 70)
    print("LATIN LEXICON COMPLETE")
    print("=" * 70)
    print(f"\nOutput files in {out_dir.absolute()}:")
    print(f"  - latin_lexicon.json (full)")
    print(f"  - latin_lexicon.md (human-readable)")
    print(f"  - websters_latin.txt (Webster's style)")
    print(f"\nTo search: python search_latin.py <word>")


if __name__ == "__main__":
    main()
