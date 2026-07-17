# Syriac Lexicon

## Overview

A **Syriac-English dictionary** for the Peshitta (Syriac Bible) and classical Syriac literature. Syriac is an Eastern Aramaic dialect that became the liturgical language of the Syriac Orthodox Church and the language of the Peshitta (Syriac translation of the Bible).

## What This Contains

| Feature | Description |
|---------|-------------|
| **Entries** | 268 core Syriac words |
| **Language** | Syriac (Classical/Peshitta) |
| **Script** | Syriac (Estrangela, Serto, East Syriac) |
| **Period** | Classical Syriac (200-700 CE) |
| **Sources** | Peshitta Bible, classical Syriac texts |
| **Format** | JSON + Markdown + Webster's style |

## Files

| File | Purpose |
|------|---------|
| `syriac_lexicon.json` | Full 268 entry dictionary (59KB) |
| `syriac_lexicon.md` | Human-readable format (34KB) |
| `websters_syriac.txt` | Webster's dictionary style (19KB) |
| `syriac_lexicon_builder.py` | Build/regenerate script |
| `search_syriac.py` | Lookup tool |

## Quick Start

```bash
# Search
python3 search_syriac.py "God"          # Returns: ܐܠܗܐ (ʾalâhâʾ)
python3 search_syriac.py "Jesus"        # Returns: ܝܫܘܥ (yešûʿ)
python3 search_syriac.py "ܐܠܗܐ"       # Syriac characters
python3 search_syriac.py "marya"         # Transliteration

# Rebuild from source
python3 syriac_lexicon_builder.py
```

## Sample Entries

### ܐܠܗܐ (ʾalâhâʾ)
- **Syriac:** ܐܠܗܐ
- **Transliteration:** ʾalâhâʾ
- **Part of Speech:** noun
- **Definition:** God
- **Root:** ʾ-l-h
- **Note:** The standard word for God in Syriac

### ܡܪܝܐ (mâryâʾ)
- **Syriac:** ܡܪܝܐ
- **Transliteration:** mâryâʾ
- **Part of Speech:** proper noun
- **Definition:** the Lord
- **Root:** m-r-ʾ
- **Note:** Used for YHWH in the Peshitta

### ܝܫܘܥ (yešûʿ)
- **Syriac:** ܝܫܘܥ
- **Transliteration:** yešûʿ
- **Part of Speech:** proper noun
- **Definition:** Jesus
- **Root:** y-š-ʿ
- **Note:** Jesus' name in Syriac

### ܡܫܝܚܐ (mešîḥâʾ)
- **Syriac:** ܡܫܝܚܐ
- **Transliteration:** mešîḥâʾ
- **Part of Speech:** proper noun
- **Definition:** Christ, the Anointed
- **Root:** m-š-ḥ

## Data Structure (JSON)

```json
{
  "ܐܠܗܐ": {
    "word": "ܐܠܗܐ",
    "definition": "God",
    "part_of_speech": "noun",
    "transliteration": "ʾalâhâʾ",
    "root": "ʾ-l-h",
    "note": "The standard word for God in Syriac"
  }
}
```

## Syriac: The Language of the Peshitta

**Syriac** (ܠܫܢܐ ܣܘܪܝܝܐ) is:
1. **An Eastern Aramaic dialect** - From Edessa (modern Şanlıurfa, Turkey)
2. **Language of the Peshitta** - The standard Syriac translation of the Bible
3. **Liturgical language** - Of the Syriac Orthodox Church, Church of the East
4. **Written in Syriac script** - Three varieties: Estrangela, Serto, East Syriac

### Historical Timeline

| Period | Usage |
|--------|-------|
| 200 BCE-200 CE | Old Syriac (inscriptions) |
| 200-400 CE | Early Classical (Peshitta translated) |
| 400-700 CE | Golden Age (Ephrem, Narsai, Theodore) |
| 700-1300 CE | Post-classical (commentaries, poetry) |
| 1300-present | Modern liturgical use |

### The Peshitta

**Peshitta** (ܦܫܝܛܬܐ = "simple, common") is the standard Syriac Bible:

| Feature | Description |
|---------|-------------|
| Translation | Hebrew/Greek → Syriac |
| Date | 2nd-3rd century CE |
| OT Base | Hebrew (with some revisions) |
| NT Base | Greek |
| Significance | Standard Bible for Syriac Christianity |

### Three Syriac Scripts

| Script | Tradition | Appearance |
|--------|-----------|------------|
| **Estrangela** | Early, scholarly | Angular, monumental |
| **Serto** (West Syriac) | Syriac Orthodox, Maronite | Rounded, cursive |
| **East Syriac** (Nestorian) | Church of the East | Angular, vowel marks |

## Aramaic Family Tree

```
Aramaic
├── Western Aramaic (Palestine)
│   ├── Jewish Palestinian Aramaic
│   ├── Samaritan Aramaic
│   └── **Galilean Aramaic (Jesus' language!)**
├── Central Aramaic
│   └── Nabatean, Palmyrene
└── Eastern Aramaic
    ├── Jewish Babylonian Aramaic
    ├── Mandaic
    └── **Syriac** (Peshitta)
        ├── Classical Syriac
        └── Neo-Aramaic dialects
```

## Hebrew → Aramaic → Syriac Connections

| Hebrew | Aramaic | Syriac | Meaning |
|--------|---------|--------|---------|
| אֱלֹהִים | אֱלָהָא | ܐܠܗܐ | God |
| יְהֹוָה | מָרֵא | ܡܪܝܐ | Lord |
| אָב | אֲבָא | ܐܒܐ | father |
| רוּחַ | רוּחַ | ܪܘܚܐ | spirit |
| שָׁלוֹם | שְׁלָם | ܫܠܡܐ | peace |
| מָשִׁיחַ | מְשִׁיחָא | ܡܫܝܚܐ | Messiah/Christ |
| תּוֹרָה | תּוֹרָה | ܬܘܪܐ | law |
| אֱמֶת | שְׁרָרָה | ܫܪܝܪܐ | truth |

## Pronunciation Guide

### Consonants

| Letter | Name | Sound |
|--------|------|-------|
| ܐ | ʾālaph | glottal stop or silent |
| ܒ | bēṯ | b or �v (hard dot) |
| ܓ | gāmal | g or ḡ (hard dot) |
| ܕ | dālaṯ | d or ḏ (hard dot) |
| ܗ | hē | h |
| ܘ | wāw | w or ō/ū (vowel) |
| ܙ | zayn | z |
| ܚ | ḥēṯ | voiceless pharyngeal (Arabic ح) |
| ܛ | �ēṯ | emphatic ṭ |
| ܝ | yōḏ | y or ī (vowel) |
| ܟ | kāph | k or ḵ (hard dot) |
| ܠ | lāmaḏ | l |
| ܡ | mīm | m |
| ܢ | nūn | n |
| ܣ | semkaṯ | s |
| ܥ | ʿē | voiced pharyngeal (Arabic ع) |
| ܦ | pē | p or ḟ (hard dot) |
| ܨ | �āḏē | emphatic ṣ |
| ܩ | qōph | emphatic q |
| ܪ | rēš | rolled r |
| ܫ | šīn | š (sh) |
| ܬ | �āw | t or ṯ (hard dot) |

### Vowels

Syriac uses **matres lectionis** (consonant letters for vowels):

| Symbol | Sound |
|--------|-------|
| ܰ | ă (a as in cat) |
| ܳ | ā (long a) |
| ܶ | ĕ (short e) |
| ܺ | ī (long i) |
| ܽ | ū (long u) |
| ܱ | ŏ (short o) |
| ܴ | ō (long o) |

## Triliteral Root System

Like Hebrew and Arabic, Syriac uses **triliteral roots**:

| Root | Word | Meaning |
|------|------|---------|
| ʾ-l-h | ܐܠܗܐ | God |
| m-r-ʾ | ܡܪܝܐ | Lord |
| y-š-ʿ | ܝܫܘܥ | Jesus |
| m-š-ḥ | ܡܫܝܚܐ | Christ |
| š-l-m | ܫܠܡܐ | peace |
| r-ḥ-m | ܪܚܡܐ | mercy |
| q-d-š | ܩܕܝܫܐ | holy |

## Building the Full Lexicon

This is a **seed lexicon** (268 entries). For complete coverage:

1. **Add Payne Smith** - *Thesaurus Syriacus* (1901) - Standard reference
2. **Add Brockelmann** - *Lexicon Syriacum* (1895)
3. **Add Peshitta concordance** - Complete biblical vocabulary

```python
# To expand, edit the vocabulary dictionaries in
# syriac_lexicon_builder.py and rebuild

from syriac_lexicon_builder import SyriacLexicon, SYRIAC_EXTENDED_VOCABULARY

# Add new words
SYRIAC_EXTENDED_VOCABULARY["ܚܕܬܐ"] = {
    "def": "new",
    "pos": "adjective",
    "translit": "ḥǝḏattâʾ",
    "root": "ḥ-ḏ-ṯ"
}

# Rebuild
lexicon = SyriacLexicon()
lexicon.build()
lexicon.export_json("syriac_lexicon.json")
```

## Sources

1. **Payne Smith, J.** - *Thesaurus Syriacus* (1901) - Standard dictionary
2. **Brockelmann, C.** - *Lexicon Syriacum* (1895)
3. **Jennings, W.** - *Lexicon to the Syriac New Testament* (1894)
4. **Kiraz, G.A.** - *Comparative Edition of the Syriac Gospels* (1996)

## Related Tools

- `ancient-hebrew-lexicon/` - Hebrew (8,674 entries)
- `koine-greek-lexicon/` - Greek (5,523 entries)
- `aramaic-lexicon/` - Aramaic (149 entries)
- `coptic-lexicon/` - Coptic (148 entries)
- `geez-lexicon/` - Ge'ez (162 entries)
- `latin-lexicon/` - Latin (657 entries)
- `narrative-analyzer/` - For analyzing texts

---

**Built:** 2026-07-16
**Current Entries:** 268
**Target:** 10,000+ (with Payne Smith)
**Language:** Classical Syriac (Peshitta)
**Primary Use:** Peshitta Bible, Syriac liturgy, Eastern Christianity
