#!/usr/bin/env python3
"""
Syriac Lexicon Builder
Builds a Syriac-English dictionary for the Peshitta and classical Syriac
"""
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

# Core Syriac vocabulary
# Peshitta Syriac (Syriac Bible) and classical Syriac literature

SYRIAC_CORE_VOCABULARY = {
    # Articles and Pronouns
    "ܗܘ": {"def": "he, that (masculine)", "pos": "demonstrative pronoun", "translit": "hû", "root": "h-w"},
    "ܗܝ": {"def": "she, that (feminine)", "pos": "demonstrative pronoun", "translit": "hî", "root": "h-y"},
    "ܗܢܘܢ": {"def": "they (masculine)", "pos": "demonstrative pronoun", "translit": "hennûn", "root": "h-n"},
    "ܗܢܝܢ": {"def": "they (feminine)", "pos": "demonstrative pronoun", "translit": "hennên", "root": "h-n"},
    "ܐܢܐ": {"def": "I", "pos": "personal pronoun", "translit": "ʾanâ", "root": "ʾ-n"},
    "ܐܢܬ": {"def": "you (masculine singular)", "pos": "personal pronoun", "translit": "ʾant", "root": "ʾ-n-t"},
    "ܐܢܬܝ": {"def": "you (feminine singular)", "pos": "personal pronoun", "translit": "ʾantî", "root": "ʾ-n-t"},
    "ܚܢܢ": {"def": "we", "pos": "personal pronoun", "translit": "ḥnan", "root": "ḥ-n-n"},
    "ܕ": {"def": "which, who, that, of", "pos": "relative pronoun/particle", "translit": "d-", "root": "d"},
    "ܡܢ": {"def": "who, what, from", "pos": "interrogative/preposition", "translit": "man", "root": "m-n"},
    "ܡܐ": {"def": "what", "pos": "interrogative pronoun", "translit": "mâ", "root": "m-ʾ"},
    "ܟܠ": {"def": "all, every", "pos": "adjective", "translit": "koll", "root": "k-l"},
    "ܗܢܐ": {"def": "this (masculine)", "pos": "demonstrative", "translit": "hânêʾ", "root": "h-n-ʾ"},
    "ܗܕܐ": {"def": "this (feminine)", "pos": "demonstrative", "translit": "hâḏêʾ", "root": "h-ḏ-ʾ"},
    
    # Divine Names
    "ܐܠܗܐ": {"def": "God", "pos": "noun", "translit": "ʾalâhâʾ", "root": "ʾ-l-h", "note": "The standard word for God in Syriac"},
    "ܡܪܝܐ": {"def": "the Lord", "pos": "proper noun", "translit": "mâryâʾ", "root": "m-r-ʾ", "note": "Used for YHWH in Peshitta"},
    "ܡܪܢ": {"def": "our Lord", "pos": "proper noun", "translit": "mâran", "root": "m-r", "note": "Common liturgical term"},
    "ܝܫܘܥ": {"def": "Jesus", "pos": "proper noun", "translit": "yešûʿ", "root": "y-š-ʿ", "note": "Jesus' name in Syriac"},
    "ܡܫܝܚܐ": {"def": "Christ, the Anointed", "pos": "proper noun", "translit": "mešîḥâʾ", "root": "m-š-ḥ", "note": "Messiah/Christ"},
    "ܪܘܚܐ": {"def": "spirit, wind, breath", "pos": "noun", "translit": "rûḥâʾ", "root": "r-w-ḥ"},
    "ܪܘܚܐ ܕܩܘܕܫܐ": {"def": "Holy Spirit", "pos": "proper noun", "translit": "rûḥâʾ d-qûḏšâʾ", "root": "r-w-ḥ; q-d-š"},
    "ܐܒܐ": {"def": "father", "pos": "noun", "translit": "ʾabbâʾ", "root": "ʾ-b"},
    "ܒܪܐ": {"def": "son", "pos": "noun", "translit": "brâʾ", "root": "b-r"},
    "ܡܠܟܐ": {"def": "king", "pos": "noun", "translit": "malkâʾ", "root": "m-l-k"},
    "ܡܠܟܘܬܐ": {"def": "kingdom", "pos": "noun", "translit": "malkûṯâʾ", "root": "m-l-k"},
    "ܡܪܝܡ": {"def": "Mary", "pos": "proper noun", "translit": "Maryam", "root": "m-r-y"},
    "ܦܛܪܘܣ": {"def": "Peter", "pos": "proper noun", "translit": "Peṭrôs", "root": "p-ṭ-r"},
    "ܦܘܠܘܣ": {"def": "Paul", "pos": "proper noun", "translit": "Pawlôs", "root": "p-w-l"},
    "ܝܘܚܢܢ": {"def": "John", "pos": "proper noun", "translit": "Yôḥannân", "root": "y-ḥ-n-n"},
    "ܡܪܝܡ": {"def": "Mary", "pos": "proper noun", "translit": "Maryam", "root": "m-r-y"},
    
    # Common Nouns
    "ܒܪܢܫܐ": {"def": "human being, person", "pos": "noun", "translit": "brĕnāšâʾ", "root": "b-r; n-ʾ-š", "note": "Literally 'son of man'"},
    "ܓܒܪܐ": {"def": "man, male", "pos": "noun", "translit": "gaḇrâʾ", "root": "g-b-r"},
    "ܐܢܬܬܐ": {"def": "woman", "pos": "noun", "translit": "ʾantattâʾ", "root": "ʾ-n-š"},
    "ܛܠܝܐ": {"def": "boy, child", "pos": "noun", "translit": "ṭalyâʾ", "root": "ṭ-l-y"},
    "ܒܝܬܐ": {"def": "house", "pos": "noun", "translit": "baytâʾ", "root": "b-y-t"},
    "ܠܒܐ": {"def": "heart", "pos": "noun", "translit": "lḇâʾ", "root": "l-b"},
    "ܢܦܫܐ": {"def": "soul, self, life", "pos": "noun", "translit": "nap̄šâʾ", "root": "n-p-š"},
    "ܦܓܪܐ": {"def": "body", "pos": "noun", "translit": "pagrâʾ", "root": "p-g-r"},
    "ܕܡܐ": {"def": "blood", "pos": "noun", "translit": "ḏemâʾ", "root": "ḏ-m-ʾ"},
    "ܒܣܪܐ": {"def": "flesh", "pos": "noun", "translit": "besrâʾ", "root": "b-s-r"},
    "ܥܝܢܐ": {"def": "eye", "pos": "noun", "translit": "ʿaynâʾ", "root": "ʿ-y-n"},
    "ܐܕܢܐ": {"def": "ear", "pos": "noun", "translit": "ʾaḏnâʾ", "root": "ʾ-ḏ-n"},
    "ܐܝܕܐ": {"def": "hand", "pos": "noun", "translit": "ʾîḏâʾ", "root": "y-d"},
    "ܪܝܫܐ": {"def": "head, beginning", "pos": "noun", "translit": "rîšâʾ", "root": "r-ʾ-š"},
    "ܐܦܐ": {"def": "face, nose", "pos": "noun", "translit": "ʾappâʾ", "root": "ʾ-p"},
    "ܦܘܡܐ": {"def": "mouth", "pos": "noun", "translit": "pûmâʾ", "root": "p-m"},
    "ܐܝܠܝܢ": {"def": "tree, wood", "pos": "noun", "translit": "ʾîlân", "root": "ʾ-y-l"},
    "ܡܝܐ": {"def": "water", "pos": "noun", "translit": "mayyâʾ", "root": "m-y"},
    "ܢܘܪܐ": {"def": "fire", "pos": "noun", "translit": "nûrâʾ", "root": "n-w-r"},
    "ܐܪܥܐ": {"def": "earth, land, ground", "pos": "noun", "translit": "ʾarʿâʾ", "root": "ʾ-r-ʿ"},
    "ܫܡܝܐ": {"def": "heaven, sky", "pos": "noun", "translit": "šmayyâʾ", "root": "š-m-y"},
    "ܕܪܐ": {"def": "dwelling, abode", "pos": "noun", "translit": "ḏar", "root": "ḏ-r"},
    "ܐܘܪܚܐ": {"def": "way, path, road", "pos": "noun", "translit": "ʾûrḥâʾ", "root": "ʾ-r-ḥ"},
    "ܢܘܗܪܐ": {"def": "light", "pos": "noun", "translit": "nûhrâʾ", "root": "n-w-h-r"},
    "ܚܫܘܟܐ": {"def": "darkness", "pos": "noun", "translit": "ḥeškâʾ", "root": "ḥ-š-k"},
    "ܝܘܡܐ": {"def": "day", "pos": "noun", "translit": "yômâʾ", "root": "y-w-m"},
    "ܠܠܝܐ": {"def": "night", "pos": "noun", "translit": "lelyâʾ", "root": "l-l-y"},
    "ܫܡܫܐ": {"def": "sun", "pos": "noun", "translit": "šemšâʾ", "root": "š-m-š"},
    "ܣܗܪܐ": {"def": "moon", "pos": "noun", "translit": "sāhrâʾ", "root": "s-h-r"},
    "ܟܘܟܒܐ": {"def": "star", "pos": "noun", "translit": "kôḵeḇâʾ", "root": "k-w-ḵ-ḇ"},
    
    # Verbs
    "ܐܡܪ": {"def": "to say", "pos": "verb", "translit": "ʾemar", "root": "ʾ-m-r"},
    "ܗܘܐ": {"def": "to be, become", "pos": "verb", "translit": "hǝwâʾ", "root": "h-w-ʾ"},
    "ܥܒܕ": {"def": "to do, make, work", "pos": "verb", "translit": "ʿǝḇaḏ", "root": "ʿ-ḇ-ḏ"},
    "ܝܕܥ": {"def": "to know", "pos": "verb", "translit": "yǝdaʿ", "root": "y-d-ʿ"},
    "ܚܙܐ": {"def": "to see", "pos": "verb", "translit": "ḥǝzâʾ", "root": "ḥ-z-ʾ"},
    "ܫܡܥ": {"def": "to hear", "pos": "verb", "translit": "šǝmaʿ", "root": "š-m-ʿ"},
    "ܝܗܒ": {"def": "to give", "pos": "verb", "translit": "yǝhaḇ", "root": "y-h-ḇ"},
    "ܢܣܒ": {"def": "to take, receive", "pos": "verb", "translit": "nǝsaḇ", "root": "n-s-ḇ"},
    "ܐܬܐ": {"def": "to come", "pos": "verb", "translit": "ʾǝṯâʾ", "root": "ʾ-ṯ-ʾ"},
    "ܐܙܠ": {"def": "to go", "pos": "verb", "translit": "ʾǝzal", "root": "ʾ-z-l"},
    "ܢܦܠ": {"def": "to fall", "pos": "verb", "translit": "nǝp̄al", "root": "n-p̄-l"},
    "ܩܡ": {"def": "to rise, stand", "pos": "verb", "translit": "qam", "root": "q-w-m"},
    "ܣܠܩ": {"def": "to go up, ascend", "pos": "verb", "translit": "sǝlaq", "root": "s-l-q"},
    "ܢܚܬ": {"def": "to go down, descend", "pos": "verb", "translit": "nǝḥeṯ", "root": "n-ḥ-ṯ"},
    "ܚܝ": {"def": "to live", "pos": "verb", "translit": "ḥay", "root": "ḥ-y-y"},
    "ܡܝܬ": {"def": "to die", "pos": "verb", "translit": "mîṯ", "root": "m-w-ṯ"},
    "ܩܛܠ": {"def": "to kill", "pos": "verb", "translit": "qǝṭal", "root": "q-ṭ-l"},
    "ܟܬܒ": {"def": "to write", "pos": "verb", "translit": "kǝṯaḇ", "root": "k-ṯ-ḇ"},
    "ܩܪܐ": {"def": "to call, read", "pos": "verb", "translit": "qǝrâʾ", "root": "q-r-ʾ"},
    "ܦܬܚ": {"def": "to open", "pos": "verb", "translit": "pǝtaḥ", "root": "p-ṯ-ḥ"},
    "ܣܟܪ": {"def": "to close", "pos": "verb", "translit": "sǝkar", "root": "s-k-r"},
    "ܫܟܒ": {"def": "to lie down", "pos": "verb", "translit": "šǝkaḇ", "root": "š-k-ḇ"},
    "ܒܢܐ": {"def": "to build", "pos": "verb", "translit": "bǝnâʾ", "root": "b-n-ʾ"},
    "ܫܬܐ": {"def": "to drink", "pos": "verb", "translit": "šǝtâʾ", "root": "š-t-ʾ"},
    "ܠܚܡ": {"def": "to eat", "pos": "verb", "translit": "lǝḥem", "root": "l-ḥ-m"},
    "ܠܒܫ": {"def": "to clothe, put on", "pos": "verb", "translit": "lǝḇaš", "root": "l-ḇ-š"},
    "ܫܠܡ": {"def": "to be complete, finish", "pos": "verb", "translit": "šǝlam", "root": "š-l-m"},
    "ܫܕܪ": {"def": "to send", "pos": "verb", "translit": "šǝdaṛ", "root": "š-ḏ-ṛ"},
    "ܡܠܐ": {"def": "to fill, be full", "pos": "verb", "translit": "mallâʾ", "root": "m-l-ʾ"},
    "ܪܚܡ": {"def": "to love, have mercy", "pos": "verb", "translit": "rǝḥem", "root": "r-ḥ-m"},
    "ܚܒ": {"def": "to love", "pos": "verb", "translit": "ḥaḇ", "root": "ḥ-b"},
    "ܣܝܡ": {"def": "to place, put", "pos": "verb", "translit": "sîm", "root": "s-y-m"},
    "ܐܚܕ": {"def": "to take, seize", "pos": "verb", "translit": "ʾǝḥaḏ", "root": "ʾ-ḥ-ḏ"},
    "ܡܛܐ": {"def": "to arrive, reach", "pos": "verb", "translit": "maṭṭâʾ", "root": "m-ṭ-ʾ"},
    "ܫܪܐ": {"def": "to loose, forgive", "pos": "verb", "translit": "šǝrâʾ", "root": "š-r-ʾ"},
    
    # Prepositions
    "ܒ": {"def": "in, with, by", "pos": "preposition", "translit": "b-", "root": "b"},
    "ܠ": {"def": "to, for, of", "pos": "preposition", "translit": "l-", "root": "l"},
    "ܡܢ": {"def": "from, out of", "pos": "preposition", "translit": "men", "root": "m-n"},
    "ܥܠ": {"def": "upon, over, concerning", "pos": "preposition", "translit": "ʿal", "root": "ʿ-l"},
    "ܬܚܬ": {"def": "under, beneath", "pos": "preposition", "translit": "taḥt", "root": "t-ḥ-t"},
    "ܩܕܡ": {"def": "before", "pos": "preposition", "translit": "qǝḏam", "root": "q-ḏ-m"},
    "ܒܬܪ": {"def": "after, behind", "pos": "preposition", "translit": "baṯaṛ", "root": "b-ṯ-ṛ"},
    "ܒܝܢ": {"def": "between", "pos": "preposition", "translit": "bayn", "root": "b-y-n"},
    "ܥܡ": {"def": "with", "pos": "preposition", "translit": "ʿam", "root": "ʿ-m"},
    "ܠܘܬ": {"def": "with, near", "pos": "preposition", "translit": "lûaṯ", "root": "l-w-ṯ"},
    
    # Conjunctions
    "ܘ": {"def": "and", "pos": "conjunction", "translit": "w-", "root": "w"},
    "ܐܠܐ": {"def": "but, except", "pos": "conjunction", "translit": "ʾellâʾ", "root": "ʾ-l"},
    "ܕ": {"def": "that, because, which", "pos": "conjunction", "translit": "ḏ-", "root": "ḏ"},
    "ܐܢ": {"def": "if", "pos": "conjunction", "translit": "ʾen", "root": "ʾ-n"},
    "ܐܘ": {"def": "or", "pos": "conjunction", "translit": "ʾô", "root": "ʾ-w"},
    "ܡܛܠ": {"def": "because, on account of", "pos": "conjunction/preposition", "translit": "maṭṭǝl", "root": "m-ṭ-l"},
    "ܗܟܢܐ": {"def": "thus, so", "pos": "adverb/conjunction", "translit": "hāḵǝnâʾ", "root": "h-k-n"},
    
    # Negatives
    "ܠܐ": {"def": "no, not", "pos": "negative particle", "translit": "lâʾ", "root": "l-ʾ"},
    
    # Adjectives
    "ܛܒܐ": {"def": "good", "pos": "adjective", "translit": "ṭaḇâʾ", "root": "ṭ-ḇ", "state": "absolute"},
    "ܒܝܫܐ": {"def": "bad, evil", "pos": "adjective", "translit": "bîšâʾ", "root": "b-y-š"},
    "ܪܒܐ": {"def": "great, large, old", "pos": "adjective", "translit": "raḇâʾ", "root": "r-b"},
    "ܙܥܘܪܐ": {"def": "small, little", "pos": "adjective", "translit": "zʿûrâʾ", "root": "z-ʿ-w-r"},
    "ܩܕܝܫܐ": {"def": "holy", "pos": "adjective", "translit": "qǝḏîšâʾ", "root": "q-d-š"},
    "ܟܐܢܐ": {"def": "just, righteous", "pos": "adjective", "translit": "kǝʾennâʾ", "root": "k-ʾ-n"},
    "ܫܪܝܪܐ": {"def": "true, firm", "pos": "adjective", "translit": "šǝrîrâʾ", "root": "š-r-r"},
    "ܚܕܬܐ": {"def": "new", "pos": "adjective", "translit": "ḥǝḏattâʾ", "root": "ḥ-ḏ-ṯ"},
    "ܥܬܝܩܐ": {"def": "old, ancient", "pos": "adjective", "translit": "ʿattîqâʾ", "root": "ʿ-ṯ-y-q"},
    
    # Numbers
    "ܚܕ": {"def": "one (masculine)", "pos": "numeral", "translit": "ḥaḏ", "root": "ḥ-d"},
    "ܚܕܐ": {"def": "one (feminine)", "pos": "numeral", "translit": "ḥaḏâʾ", "root": "ḥ-d"},
    "ܬܪܝܢ": {"def": "two", "pos": "numeral", "translit": "tǝrayn", "root": "t-r"},
    "ܬܠܬܐ": {"def": "three", "pos": "numeral", "translit": "tǝlāṯâʾ", "root": "t-l-ṯ"},
    "ܐܪܒܥܐ": {"def": "four", "pos": "numeral", "translit": "ʾarbaʿâʾ", "root": "ʾ-r-b-ʿ"},
    "ܚܡܫܐ": {"def": "five", "pos": "numeral", "translit": "ḥammǝšâʾ", "root": "ḥ-m-š"},
    
    # Theological/Ecclesiastical Terms
    "ܟܗܢܐ": {"def": "priest", "pos": "noun", "translit": "kahnâʾ", "root": "k-h-n"},
    "ܕܝܪܐ": {"def": "monastery", "pos": "noun", "translit": "dayrâʾ", "root": "d-y-r"},
    "ܕܝܪܝܐ": {"def": "monk", "pos": "noun", "translit": "dayrâyâʾ", "root": "d-y-r"},
    "ܬܪܝܨܐ": {"def": "Trinity", "pos": "noun", "translit": "tǝrîṣâʾ", "root": "t-r-ṣ"},
    "ܩܘܕܫܐ": {"def": "holiness, sanctuary", "pos": "noun", "translit": "qûḏšâʾ", "root": "q-d-š"},
    "ܗܝܡܢܘܬܐ": {"def": "faith, belief", "pos": "noun", "translit": "haymânûṯâʾ", "root": "h-m-n"},
    "ܣܒܪܐ": {"def": "hope", "pos": "noun", "translit": "seḇrâʾ", "root": "s-b-r"},
    "ܚܘܒܐ": {"def": "love", "pos": "noun", "translit": "ḥûḇâʾ", "root": "ḥ-w-b"},
    "ܫܠܡܐ": {"def": "peace, completion", "pos": "noun", "translit": "šelâmâʾ", "root": "š-l-m"},
    "ܪܚܡܐ": {"def": "mercy, compassion", "pos": "noun", "translit": "raḥmâʾ", "root": "r-ḥ-m"},
    "ܚܛܝܬܐ": {"def": "sin", "pos": "noun", "translit": "ḥaṭṭâytâʾ", "root": "ḥ-ṭ-ʾ"},
    "ܙܕܝܩܘܬܐ": {"def": "righteousness, justice", "pos": "noun", "translit": "zǝdîqûṯâʾ", "root": "z-d-q"},
    "ܣܘܥܪܐ": {"def": "grace", "pos": "noun", "translit": "sûʿarâʾ", "root": "s-w-ʿ-r"},
    "ܡܠܦܢܘܬܐ": {"def": "teaching, doctrine", "pos": "noun", "translit": "mallp̄anûṯâʾ", "root": "m-l-p̄"},
    "ܬܘܕܝܬܐ": {"def": "thanksgiving, confession", "pos": "noun", "translit": "tûḏîṯâʾ", "root": "t-w-ḏ"},
    "ܨܠܘܬܐ": {"def": "prayer", "pos": "noun", "translit": "ṣelôṯâʾ", "root": "ṣ-l-ʾ"},
    "ܨܘܡܐ": {"def": "fast, fasting", "pos": "noun", "translit": "ṣômâʾ", "root": "ṣ-w-m"},
    "ܩܝܡܐ": {"def": "resurrection, standing", "pos": "noun", "translit": "qîyâmâʾ", "root": "q-w-m"},
    "ܥܘܕܪܢܐ": {"def": "salvation", "pos": "noun", "translit": "ʿûdrānâʾ", "root": "ʿ-w-d-r"},
    "ܐܘܢܓܠܝܘܢ": {"def": "gospel", "pos": "noun", "translit": "ʾewangeliyôn", "root": "Greek: εὐαγγέλιον"},
    "ܬܘܪܐ": {"def": "law", "pos": "noun", "translit": "tûrâʾ", "root": "t-w-r", "note": "From Hebrew תּוֹרָה"},
    "ܢܒܝܐ": {"def": "prophet", "pos": "noun", "translit": "neḇyâʾ", "root": "n-b-ʾ"},
    "ܫܠܝܚܐ": {"def": "apostle, sent one", "pos": "noun", "translit": "šlîḥâʾ", "root": "š-l-ḥ"},
    "ܟܘܪܣܝܐ": {"def": "throne, chair", "pos": "noun", "translit": "kûrsayâʾ", "root": "k-w-r-s-y"},
    "ܡܕܒܚܐ": {"def": "altar", "pos": "noun", "translit": "maḏbaḥâʾ", "root": "ḏ-b-ḥ"},
    "ܕܪܘܢܐ": {"def": "gift, offering", "pos": "noun", "translit": "deṛônâʾ", "root": "d-r-n"},
}

# Extended vocabulary - Peshitta specific terms and phrases
SYRIAC_EXTENDED_VOCABULARY = {
    # More body parts
    "ܪܓܠܐ": {"def": "foot", "pos": "noun", "translit": "raḡlâʾ", "root": "r-ḡ-l"},
    "ܐܨܒܥܐ": {"def": "finger, toe", "pos": "noun", "translit": "ʾeṣbaʿâʾ", "root": "ʾ-ṣ-b-ʿ"},
    "ܨܦܪܐ": {"def": "nail", "pos": "noun", "translit": "ṣeprâʾ", "root": "ṣ-p-r"},
    "ܓܘܕܐ": {"def": "skin", "pos": "noun", "translit": "gûḏâʾ", "root": "g-w-ḏ"},
    "ܬܪܝܐ": {"def": "hair", "pos": "noun", "translit": "taryâʾ", "root": "t-r-y"},
    "ܩܕܠܐ": {"def": "neck", "pos": "noun", "translit": "qeḏlâʾ", "root": "q-ḏ-l"},
    "ܟܬܦܐ": {"def": "shoulder", "pos": "noun", "translit": "kaṯpâʾ", "root": "k-ṯ-p"},
    "ܚܕܝܐ": {"def": "breast, chest", "pos": "noun", "translit": "ḥaḏyâʾ", "root": "ḥ-ḏ-y"},
    "ܓܘܐ": {"def": "belly, inside", "pos": "noun", "translit": "gawwâʾ", "root": "g-w"},
    "ܚܠܝܐ": {"def": "thigh, loin", "pos": "noun", "translit": "ḥaḷyâʾ", "root": "ḥ-ḷ-y"},
    "ܒܣܪܐ": {"def": "flesh", "pos": "noun", "translit": "besrâʾ", "root": "b-s-r"},
    "ܓܪܡܐ": {"def": "bone", "pos": "noun", "translit": "gaṛmâʾ", "root": "g-ṛ-m"},
    "ܡܘܚܐ": {"def": "marrow, brain", "pos": "noun", "translit": "mûḥâʾ", "root": "m-w-ḥ"},
    "ܕܡܥܐ": {"def": "tear", "pos": "noun", "translit": "deʿâʾ", "root": "d-ʿ"},
    "ܥܘܩܒܐ": {"def": "heel", "pos": "noun", "translit": "ʿûqbeḇâʾ", "root": "ʿ-q-ḇ"},
    "ܐܝܕܝܐ": {"def": "hand (feminine)", "pos": "noun", "translit": "ʾîḏayyâʾ", "root": "y-d"},
    
    # More nature
    "ܛܘܪܐ": {"def": "mountain", "pos": "noun", "translit": "ṭûrâʾ", "root": "ṭ-w-r"},
    "ܓܒܥܐ": {"def": "hill", "pos": "noun", "translit": "gaḇʿâʾ", "root": "g-ḇ-ʿ"},
    "ܦܩܥܬܐ": {"def": "valley", "pos": "noun", "translit": "pqaʿṯâʾ", "root": "p-q-ʿ"},
    "ܝܡܐ": {"def": "sea, lake", "pos": "noun", "translit": "yammâʾ", "root": "y-m"},
    "ܢܗܪܐ": {"def": "river", "pos": "noun", "translit": "nahraʾ", "root": "n-h-r"},
    "ܡܥܝܢܐ": {"def": "spring, fountain", "pos": "noun", "translit": "maʿyannâʾ", "root": "m-ʿ-y-n"},
    "ܒܐܪܐ": {"def": "well", "pos": "noun", "translit": "beʾârâʾ", "root": "b-ʾ-r"},
    "ܚܘܪܐ": {"def": "hole, pit", "pos": "noun", "translit": "ḥûrâʾ", "root": "ḥ-w-r"},
    "ܩܝܛܐ": {"def": "summer", "pos": "noun", "translit": "qayṭâʾ", "root": "q-y-ṭ"},
    "ܣܬܘܐ": {"def": "winter", "pos": "noun", "translit": "sǝtawâʾ", "root": "s-t-w"},
    "ܦܘܩܕܢܐ": {"def": "commandment", "pos": "noun", "translit": "pûqdaṇâʾ", "root": "p-q-ḏ"},
    "ܡܛܪܐ": {"def": "rain", "pos": "noun", "translit": "maṭṭârâʾ", "root": "m-ṭ-r"},
    "ܓܫܡܐ": {"def": "rain, shower", "pos": "noun", "translit": "gešmâʾ", "root": "g-š-m"},
    "ܥܢܢܐ": {"def": "cloud", "pos": "noun", "translit": "ʿannânâʾ", "root": "ʿ-n-n"},
    "ܪܥܡܐ": {"def": "thunder", "pos": "noun", "translit": "raʿmâʾ", "root": "r-ʿ-m"},
    "ܒܪܩܐ": {"def": "lightning", "pos": "noun", "translit": "barqâʾ", "root": "b-r-q"},
    "ܩܛܝܪܐ": {"def": "smoke, vapor", "pos": "noun", "translit": "qaṭṭîrâʾ", "root": "q-ṭ-r"},
    "ܐܦܐ": {"def": "dust, ashes", "pos": "noun", "translit": "ʾâpâʾ", "root": "ʾ-p"},
    "ܛܝܢܐ": {"def": "mud, clay", "pos": "noun", "translit": "ṭaynâʾ", "root": "ṭ-y-n"},
    "ܚܠܐ": {"def": "sand", "pos": "noun", "translit": "ḥelâʾ", "root": "ḥ-l"},
    "ܟܐܦܐ": {"def": "stone, rock", "pos": "noun", "translit": "kêp̄âʾ", "root": "k-ʾ-p"},
    
    # Time and measurements
    "ܫܥܐ": {"def": "hour, time", "pos": "noun", "translit": "šâʿâʾ", "root": "š-ʿ-ʾ"},
    "ܫܢܬܐ": {"def": "year", "pos": "noun", "translit": "šattâʾ", "root": "š-n-ṯ"},
    "ܝܪܚܐ": {"def": "month", "pos": "noun", "translit": "yarḥâʾ", "root": "y-r-ḥ"},
    "ܫܒܘܥܐ": {"def": "week", "pos": "noun", "translit": "šaḇûʿâʾ", "root": "š-b-ʿ"},
    "ܥܕܢܐ": {"def": "time, season", "pos": "noun", "translit": "ʿeḏannâʾ", "root": "ʿ-ḏ-n"},
    "ܩܕܡ": {"def": "morning", "pos": "noun", "translit": "qǝḏem", "root": "q-ḏ-m"},
    "ܪܡܫܐ": {"def": "evening", "pos": "noun", "translit": "remešâʾ", "root": "r-m-š"},
    "ܠܝܠܝܐ": {"def": "night", "pos": "noun", "translit": "lelyâʾ", "root": "l-l-y"},
    "ܝܘܡܐ": {"def": "day", "pos": "noun", "translit": "yômâʾ", "root": "y-w-m"},
    "�ܡܘܢܐ": {"def": "week", "pos": "noun", "translit": "šawwâʾ", "root": "š-w-ʾ"},
    
    # Abstract concepts
    "ܡܠܠܐ": {"def": "word, speech", "pos": "noun", "translit": "mellâʾ", "root": "m-l-l"},
    "ܡܕܥܐ": {"def": "knowledge, mind", "pos": "noun", "translit": "maḏʿâʾ", "root": "y-d-ʿ"},
    "ܚܟܡܬܐ": {"def": "wisdom", "pos": "noun", "translit": "ḥokmǝṯâʾ", "root": "ḥ-k-m"},
    "ܓܒܪܘܬܐ": {"def": "manliness, virtue", "pos": "noun", "translit": "gaḇrûṯâʾ", "root": "g-b-r"},
    "ܚܝܠܐ": {"def": "strength, power, army", "pos": "noun", "translit": "ḥaylâʾ", "root": "ḥ-y-l"},
    "ܬܩܢܐ": {"def": "correction, discipline", "pos": "noun", "translit": "tûqnâʾ", "root": "t-q-n"},
    "ܒܘܣܝܢܐ": {"def": "comfort, encouragement", "pos": "noun", "translit": "bûsâynnâʾ", "root": "b-w-s"},
    "ܡܘܕܥܢܘܬܐ": {"def": "thanksgiving, confession", "pos": "noun", "translit": "môḏaʿanûṯâʾ", "root": "y-d-ʿ"},
    "ܪܘܙܐ": {"def": "mystery, secret", "pos": "noun", "translit": "râzâʾ", "root": "r-w-z"},
    "ܬܘܪܣܝܐ": {"def": "will, pleasure", "pos": "noun", "translit": "tûrsâyâʾ", "root": "t-r-s-y"},
    "ܒܥܘܬܐ": {"def": "request, petition", "pos": "noun", "translit": "baʿûṯâʾ", "root": "b-ʿ-ʾ"},
    "ܡܘܠܕܐ": {"def": "birth, generation", "pos": "noun", "translit": "mawleḏâʾ", "root": "m-w-l-ḏ"},
    "ܬܝܒܘܬܐ": {"def": "repentance", "pos": "noun", "translit": "tûyḇûṯâʾ", "root": "t-w-ḇ"},
    "ܫܘܠܡܢܐ": {"def": "peace, prosperity", "pos": "noun", "translit": "šûlêmânâʾ", "root": "š-l-m"},
    "ܚܕܘܬܐ": {"def": "joy, gladness", "pos": "noun", "translit": "ḥeḏwâṯâʾ", "root": "ḥ-ḏ-ʾ"},
    "ܥܘܠܐ": {"def": "iniquity, wrong", "pos": "noun", "translit": "ʿawlâʾ", "root": "ʿ-w-l"},
    "ܦܘܪܥܢܐ": {"def": "reward, recompense", "pos": "noun", "translit": "pûrʿānâʾ", "root": "p-ʿ-n"},
    "ܒܘܕܩܐ": {"def": "examination, trial", "pos": "noun", "translit": "bûḏâqâʾ", "root": "b-d-q"},
    
    # Social/Political
    "ܥܡܡܐ": {"def": "people, nation", "pos": "noun", "translit": "ʿammâmâʾ", "root": "ʿ-m-m"},
    "ܟܢܫܐ": {"def": "assembly, gathering", "pos": "noun", "translit": "kǝnešâʾ", "root": "k-n-š"},
    "ܩܗܠܐ": {"def": "assembly, congregation", "pos": "noun", "translit": "qahhâlâʾ", "root": "q-h-l"},
    "ܐܘܡܬܐ": {"def": "nation, people", "pos": "noun", "translit": "ʾûmmaṯâʾ", "root": "ʾ-w-m-m"},
    "ܠܫܢܐ": {"def": "language, tongue", "pos": "noun", "translit": "leššannâʾ", "root": "l-š-n"},
    "ܬܪܓܡܢܐ": {"def": "interpreter, translator", "pos": "noun", "translit": "targǝmânâʾ", "root": "t-r-g-m"},
    "ܦܘܩܕܢܐ": {"def": "command, order", "pos": "noun", "translit": "pûqdaṇâʾ", "root": "p-q-ḏ"},
    "ܫܘܠܛܢܐ": {"def": "authority, power", "pos": "noun", "translit": "šûlṭānâʾ", "root": "š-l-ṭ"},
    "ܡܠܟܐ": {"def": "king", "pos": "noun", "translit": "malkâʾ", "root": "m-l-k"},
    "ܡܠܟܘܬܐ": {"def": "kingdom", "pos": "noun", "translit": "malkûṯâʾ", "root": "m-l-k"},
    "ܡܕܝܢܬܐ": {"def": "city", "pos": "noun", "translit": "maḏînǝṯâʾ", "root": "ḏ-y-n"},
    "ܩܪܝܬܐ": {"def": "village", "pos": "noun", "translit": "qaryâʾ", "root": "q-r-y"},
    "ܫܘܩܐ": {"def": "street, market", "pos": "noun", "translit": "šûqâʾ", "root": "š-w-q"},
    "ܒܬܐ": {"def": "house, home", "pos": "noun", "translit": "baytâʾ", "root": "b-y-t"},
    "ܕܪܬܐ": {"def": "dwelling, abode", "pos": "noun", "translit": "dârǝṯâʾ", "root": "d-r"},
    "ܦܬܓܡܐ": {"def": "decree, word", "pos": "noun", "translit": "paṯgâmâʾ", "root": "p-ṯ-g-m"},
    "ܬܢܝܢܐ": {"def": "law, custom", "pos": "noun", "translit": "tǝnayyânâʾ", "root": "t-n-ʾ"},
    
    # Actions
    "ܥܣܪ": {"def": "to bind", "pos": "verb", "translit": "ʿǝsar", "root": "ʿ-s-r"},
    "ܫܪܝ": {"def": "to loose, begin", "pos": "verb", "translit": "šǝrê", "root": "š-r-y"},
    "ܫܦܪ": {"def": "to please, be beautiful", "pos": "verb", "translit": "šǝpaṛ", "root": "š-p-ṛ"},
    "ܫܟܚ": {"def": "to find", "pos": "verb", "translit": "šǝkaḥ", "root": "š-k-ḥ"},
    "ܚܫܒ": {"def": "to think, account", "pos": "verb", "translit": "ḥǝšaḇ", "root": "ḥ-š-ḇ"},
    "ܓܠܐ": {"def": "to reveal, uncover", "pos": "verb", "translit": "gǝlâʾ", "root": "g-l-ʾ"},
    "ܟܣܐ": {"def": "to cover, hide", "pos": "verb", "translit": "kǝsâʾ", "root": "k-s-ʾ"},
    "ܦܪܓ": {"def": "to reward, recompense", "pos": "verb", "translit": "pǝraḡ", "root": "p-r-ḡ"},
    "ܝܩܕ": {"def": "to burn", "pos": "verb", "translit": "yǝqaḏ", "root": "y-q-ḏ"},
    "ܩܪܝ": {"def": "to happen, befall", "pos": "verb", "translit": "qǝrê", "root": "q-r-y"},
    "ܦܢܐ": {"def": "to turn", "pos": "verb", "translit": "pǝnâʾ", "root": "p-n-ʾ"},
    "ܗܦܟ": {"def": "to turn, convert", "pos": "verb", "translit": "hǝpǝḵ", "root": "h-p-ḵ"},
    "ܩܘܡ": {"def": "to stand, rise", "pos": "verb", "translit": "qûm", "root": "q-w-m"},
    "ܝܬܒ": {"def": "to sit, dwell", "pos": "verb", "translit": "yǝṯeḇ", "root": "y-ṯ-ḇ"},
    "ܕܡܟ": {"def": "to sleep", "pos": "verb", "translit": "dǝmak", "root": "d-m-k"},
    "ܥܪܩ": {"def": "to flee", "pos": "verb", "translit": "ʿǝraq", "root": "ʿ-r-q"},
    "ܪܗܛ": {"def": "to run", "pos": "verb", "translit": "rǝhaṭ", "root": "r-h-ṭ"},
    
    # Colors and qualities
    "ܚܘܪܐ": {"def": "white", "pos": "adjective", "translit": "ḥûrâʾ", "root": "ḥ-w-r"},
    "ܟܘܡܬܐ": {"def": "black", "pos": "adjective", "translit": "kûmǝṯâʾ", "root": "k-w-m"},
    "ܣܘܡܩܐ": {"def": "red", "pos": "adjective", "translit": "sûmâqâʾ", "root": "s-w-m-q"},
    "ܝܘܩܪܐ": {"def": "green", "pos": "adjective", "translit": "yûqraʾ", "root": "y-w-q-r"},
    "ܨܚܘܐ": {"def": "yellow", "pos": "adjective", "translit": "ṣeḥwâʾ", "root": "ṣ-ḥ-w"},
    "ܩܨܬܐ": {"def": "hard, difficult", "pos": "adjective", "translit": "qeṣṣâʾ", "root": "q-ṣ-ʾ"},
    "ܪܟܝܟܐ": {"def": "soft, tender", "pos": "adjective", "translit": "raḵîḵâʾ", "root": "r-k-ḵ"},
    "ܚܠܝܛܐ": {"def": "smooth", "pos": "adjective", "translit": "ḥalîṭâʾ", "root": "ḥ-l-ṭ"},
    "ܩܡܛܐ": {"def": "rough", "pos": "adjective", "translit": "qammâṭâʾ", "root": "q-m-ṭ"},
    "ܝܬܝܪܐ": {"def": "more, abundant", "pos": "adjective", "translit": "yaṯîrâʾ", "root": "y-ṯ-r"},
    "ܒܨܝܪܐ": {"def": "less, few", "pos": "adjective", "translit": "baṣîrâʾ", "root": "b-ṣ-r"},
    "ܡܠܝܐ": {"def": "full", "pos": "adjective", "translit": "mallâʾ", "root": "m-l-ʾ"},
    "ܣܦܝܩܐ": {"def": "empty", "pos": "adjective", "translit": "sefîqâʾ", "root": "s-f-q"},
    
    # Materials
    "ܦܛܝܠܐ": {"def": "thread, cord", "pos": "noun", "translit": "pṭîlâʾ", "root": "p-ṭ-l"},
    "ܓܘܕܬܐ": {"def": "leather", "pos": "noun", "translit": "gûḏaṯâʾ", "root": "g-w-ḏ"},
    "ܦܪܙܠܐ": {"def": "iron", "pos": "noun", "translit": "pǝrazzǝlâʾ", "root": "p-r-z-l"},
    "ܢܚܫܐ": {"def": "copper, bronze", "pos": "noun", "translit": "neḥāšâʾ", "root": "n-ḥ-š"},
    "ܩܝܣܐ": {"def": "wood, beam", "pos": "noun", "translit": "qîsâʾ", "root": "q-y-s"},
    "ܣܐܡܐ": {"def": "fastener, nail", "pos": "noun", "translit": "sâʾmâʾ", "root": "s-ʾ-m"},
    "ܟܐܦܐ": {"def": "stone", "pos": "noun", "translit": "kêp̄âʾ", "root": "k-ʾ-p"},
    
    # Clothing
    "ܡܐܢܐ": {"def": "garment, vessel", "pos": "noun", "translit": "maʾnâʾ", "root": "m-ʾ-n"},
    "ܟܘܬܝܢܐ": {"def": "robe, tunic", "pos": "noun", "translit": "kûtînâʾ", "root": "k-w-t-n"},
    "ܚܡܝܠܐ": {"def": "cloak", "pos": "noun", "translit": "ḥǝmîlâʾ", "root": "ḥ-m-l"},
    "ܣܘܕܪܐ": {"def": "turban, head covering", "pos": "noun", "translit": "sûḏarâʾ", "root": "s-ḏ-r"},
    "ܡܢܝܠܐ": {"def": "sandal", "pos": "noun", "translit": "manyâlâʾ", "root": "m-n-y-l"},
    "ܚܓܪܐ": {"def": "girdle, belt", "pos": "noun", "translit": "ḥaḡrâʾ", "root": "ḥ-ḡ-r"},
    "ܡܟܒܠܐ": {"def": "chain, fetter", "pos": "noun", "translit": "makleḇlâʾ", "root": "k-l-ḇ"},
}

class SyriacLexicon:
    """Syriac-English lexicon"""
    
    def __init__(self):
        self.entries = {}
        self.root_index = defaultdict(list)
        
    def build(self):
        """Build lexicon from vocabulary lists"""
        print("[*] Building Syriac lexicon...")
        
        # Combine vocabularies
        all_vocab = {**SYRIAC_CORE_VOCABULARY, **SYRIAC_EXTENDED_VOCABULARY}
        
        for word, data in all_vocab.items():
            entry = {
                "word": word,
                "definition": data["def"],
                "part_of_speech": data["pos"],
                "transliteration": data["translit"],
                "root": data["root"]
            }
            
            # Add optional note
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
                "title": "Syriac Lexicon",
                "language": "Syriac (Classical/Edessan)",
                "script": "Syriac (Estrangela, Serto, East Syriac)",
                "period": "Classical Syriac (200-700 CE), Peshitta translation",
                "total_entries": len(self.entries),
                "format": "JSON",
                "notes": "Peshitta Syriac is the language of the Syriac Bible and early Eastern Christianity. It is a dialect of Aramaic."
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
            f.write("# Syriac Lexicon\n\n")
            f.write("**Syriac-English Dictionary (Peshitta and Classical)**\n\n")
            f.write(f"Total Entries: {len(self.entries)}\n\n")
            f.write("---\n\n")
            
            # Sort by Syriac word
            sorted_entries = sorted(self.entries.items(), key=lambda x: x[0])
            
            for word, entry in sorted_entries:
                f.write(f"## {word}\n\n")
                f.write(f"**Transliteration:** *{entry['transliteration']}*\n\n")
                f.write(f"**Part of Speech:** {entry['part_of_speech']}\n\n")
                f.write(f"**Definition:** {entry['definition']}\n\n")
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
            f.write("SYRIAC LEXICON\n")
            f.write("Syriac-English Dictionary (Peshitta)\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("About Syriac:\n")
            f.write("  - Dialect of Aramaic (Eastern Aramaic)\n")
            f.write("  - Language of the Peshitta (Syriac Bible)\n")
            f.write("  - Classical period: 200-700 CE\n")
            f.write("  - Three scripts: Estrangela, Serto (West), East Syriac (Nestorian)\n")
            f.write("  - Written right to left like Hebrew and Arabic\n\n")
            
            f.write("Pronunciation Guide:\n")
            f.write("  ܐ = ʾ (glottal stop or silent)\n")
            f.write("  ܒ = b (soft) or ḇ (hard/v, when marked with hard dot)\n")
            f.write("  ܓ = g (soft) or ḡ (hard/gh, when marked)\n")
            f.write("  ܕ = d (soft) or ḏ (hard/dh, when marked)\n")
            f.write("  ܚ = ḥ (voiceless pharyngeal, like Arabic ح)\n")
            f.write("  ܛ = ṭ (emphatic t)\n")
            f.write("  ܥ = ʿ (voiced pharyngeal, like Arabic ع)\n")
            f.write("  ܨ = ṣ (emphatic s)\n")
            f.write("  ܩ = q (emphatic k)\n")
            f.write("  ܪ = r (rolled)\n")
            f.write("  ܫ = š (sh)\n")
            f.write("  ܬ = t (soft) or ṯ (hard/th, when marked)\n\n")
            
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
    lexicon = SyriacLexicon()
    
    # Build from vocabulary
    lexicon.build()
    
    # Create output directory
    out_dir = Path("/root/syriac_lexicon_output")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Export all formats
    lexicon.export_json(out_dir / "syriac_lexicon.json")
    lexicon.export_markdown(out_dir / "syriac_lexicon.md")
    lexicon.export_websters_style(out_dir / "websters_syriac.txt")
    
    # Sample entries
    print("\n" + "=" * 70)
    print("SAMPLE ENTRIES")
    print("=" * 70 + "\n")
    
    sample_words = ['ܐܠܗܐ', 'ܡܪܝܐ', 'ܝܫܘܥ', 'ܡܫܝܚܐ', 'ܪܘܚܐ', 'ܫܠܡܐ']
    for word in sample_words:
        if word in lexicon.entries:
            e = lexicon.entries[word]
            print(f"{word} ({e['transliteration']})")
            print(f"  {e['definition']}")
            print(f"  [{e['part_of_speech']}] Root: {e['root']}\n")
    
    print("=" * 70)
    print("SYRIAC LEXICON COMPLETE")
    print("=" * 70)
    print(f"\nOutput files in {out_dir.absolute()}:")
    print(f"  - syriac_lexicon.json (full)")
    print(f"  - syriac_lexicon.md (human-readable)")
    print(f"  - websters_syriac.txt (Webster's style)")
    print(f"\nTo search: python search_syriac.py <word>")


if __name__ == "__main__":
    main()
