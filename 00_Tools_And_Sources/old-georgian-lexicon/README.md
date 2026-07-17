# Old Georgian Lexicon

## Overview

An **Old Georgian-English dictionary** for the ancient Georgian language (Kartvelian). Old Georgian (5th-11th centuries CE) is the language of the ancient Georgian Orthodox Church and represents one of the most complete ancient biblical traditions in a non-Indo-European, non-Semitic language.

## What This Contains

| Feature | Description |
|---------|-------------|
| **Entries** | 309 core Old Georgian words |
| **Language** | Old Georgian (Kartvelian) |
| **Script** | Georgian (Mkhedruli, Asomtavruli) |
| **Period** | 5th-11th centuries CE |
| **Sources** | Georgian Bible, ancient texts |
| **Format** | JSON + Markdown + Webster's style |

## Files

| File | Purpose |
|------|---------|
| `old_georgian_lexicon.json` | Full 309 entry dictionary (74KB) |
| `old_georgian_lexicon.md` | Human-readable format (40KB) |
| `websters_old_georgian.txt` | Webster's dictionary style (24KB) |
| `old_georgian_lexicon_builder.py` | Build/regenerate script |
| `search_old_georgian.py` | Lookup tool |

## Quick Start

```bash
# Search
python3 search_old_georgian.py "God"          # Returns: ღმერთი (ghmerti)
python3 search_old_georgian.py "Jesus"        # Returns: იესუ (iesu)
python3 search_old_georgian.py "ღმერთი"       # Georgian characters
python3 search_old_georgian.py "upali"         # Transliteration

# Rebuild from source
python3 old_georgian_lexicon_builder.py
```

## Sample Entries

### ღმერთი (ghmerti)
- **Georgian:** ღმერთი
- **Transliteration:** ghmerti
- **Part of Speech:** noun
- **Definition:** God
- **Root:** ghmer
- **Note:** The standard word for God in Georgian

### უფალი (upali)
- **Georgian:** უფალი
- **Transliteration:** upali
- **Part of Speech:** noun
- **Definition:** Lord, Master
- **Root:** upal
- **Note:** Used for 'Lord' in Georgian Bible

### იესუ (iesu)
- **Georgian:** იესუ
- **Transliteration:** iesu
- **Part of Speech:** proper noun
- **Definition:** Jesus
- **Root:** iesu

### ქრისტე (kriste)
- **Georgian:** ქრისტე
- **Transliteration:** kriste
- **Part of Speech:** proper noun
- **Definition:** Christ
- **Root:** krist

## Data Structure (JSON)

```json
{
  "ღმერთი": {
    "word": "ღმერთი",
    "definition": "God",
    "part_of_speech": "noun",
    "transliteration": "ghmerti",
    "root": "ghmer",
    "note": "The standard word for God in Georgian"
  }
}
```

## Old Georgian: The Kartvelian Language

**Georgian** (ქართული ენა) is:
1. **A Kartvelian (South Caucasian) language** - Unique language family native to the Caucasus
2. **UNRELATED to Indo-European, Semitic, or Turkic** - Completely separate language family
3. **Language of the Georgian Orthodox Church** - With ancient biblical tradition
4. **Spoken in Georgia** - Located at the crossroads of Europe and Asia

### Historical Timeline

| Period | Usage |
|--------|-------|
| 4th century CE | Christianization of Georgia (St. Nino) |
| 5th century | First Georgian alphabet (Asomtavruli) |
| 5th-11th centuries | **Old Georgian** (literary language) |
| 9th-10th centuries | Nuskhuri script develops |
| 11th-18th centuries | Middle Georgian |
| 19th century-present | Modern Georgian (Mkhedruli script) |

### The Georgian Bible

The **Georgian Bible** is one of the oldest and most complete translations:

| Feature | Description |
|---------|-------------|
| **Old Testament** | Translated from Greek (LXX) |
| **New Testament** | Translated from Greek |
| **Date** | 5th century CE |
| **Significance** | Complete Bible in non-Indo-European, non-Semitic language |
| **Canon** | **81 books** (most complete biblical canon) |

### Georgian Alphabet Evolution

| Script | Period | Description |
|--------|--------|-------------|
| **Asomtavruli** | 5th-9th centuries | Oldest, monumental, rounded |
| **Nuskhuri** | 9th-19th centuries | Ecclesiastical, cursive |
| **Mkhedruli** | 19th century-present | Modern, secular script |

## Unique Features of Georgian

### Completely Unique Language Family

Georgian is **NOT related** to:
- ❌ Indo-European (Greek, Latin, English, Persian)
- ❌ Semitic (Hebrew, Arabic, Aramaic)
- ❌ Turkic (Turkish, Azerbaijani)

Georgian **IS related** to:
- ✅ **Kartvelian family**: Svan, Mingrelian, Laz

### Agglutinative Language

Georgian builds meaning by **adding suffixes**:

| Word | Meaning |
|------|---------|
| კაცი (katsi) | man |
| კაცებს (katsebs) | to the men |
| კაცებთან (katsebtan) | with the men |
| კაცებთანაც (katsebtanats) | with the men too |

### Three Georgian Scripts

```
Asomtavruli (5th c.): Ⴀ Ⴁ Ⴂ Ⴃ Ⴄ Ⴅ Ⴆ Ⴇ Ⴈ Ⴉ Ⴊ Ⴋ Ⴌ Ⴍ Ⴎ Ⴏ Ⴐ Ⴑ Ⴒ Ⴓ Ⴔ Ⴕ Ⴖ Ⴗ Ⴘ Ⴙ Ⴚ Ⴛ Ⴜ Ⴝ Ⴞ Ⴟ Ⴠ
Nuskhuri (9th c.): ⴀ ⴁ ⴂ ⴃ ⴄ ⴅ ⴆ ⴇ ⴈ ⴉ ⴊ ⴋ ⴌ ⴍ ⴎ ⴏ ⴐ ⴑ ⴒ ⴓ ⴔ ⴕ ⴖ ⴗ ⴘ ⴙ ⴚ ⴛ ⴜ ⴝ ⴞ ⴟ ⴠ
Mkhedruli (modern): ა ბ გ დ ე ვ ზ თ ი კ ლ მ ნ ო პ ჟ რ ს ტ უ ფ ქ ღ ყ შ ჩ ც ძ წ ჭ ხ ჯ ჰ
```

## Hebrew → Greek → Georgian Connections

| Hebrew | Greek | Georgian | Meaning |
|--------|-------|----------|---------|
| אֱלֹהִים | θεός | ღმერთი | God |
| יְהֹוָה | κύριος | უფალი | Lord |
| יְהוֹשֻׁעַ | Ἰησοῦς | იესუ | Jesus |
| מָשִׁיחַ | Χριστός | ქრისტე | Christ |
| רוּחַ | πνεῦμα | სული | spirit |
| שָׁלוֹם | εἰρήνη | მშვიდობა | peace |
| אֱמֶת | ἀλήθεια | ჭეშმარიტება | truth |
| תּוֹרָה | νόμος | რწმენა | law/faith |
| חֶסֶד | ἔλεος | მოწყალება | mercy |
| אַהֲבָה | ἀγάπη | სიყვარული | love |

## Pronunciation Guide

### Vowels

| Letter | Sound |
|--------|-------|
| ა | a (father) |
| ე | e (pet) |
| ი | i (machine) |
| ო | o (note) |
| უ | u (rule) |

### Consonants

| Letter | Sound |
|--------|-------|
| ბ | b (boy) |
| გ | g (go) |
| დ | d (dog) |
| ვ | v (very) |
| ზ | z (zebra) |
| თ | t (top) |
| კ | k' (emphatic, ejective) |
| ლ | l (love) |
| მ | m (man) |
| ნ | n (no) |
| პ | p' (emphatic, ejective) |
| რ | r (rolled) |
| ს | s (see) |
| ტ | t' (emphatic, ejective) |
| ფ | p (spin) |
| ქ | k (king) |
| ღ | gh (Arabic غ, uvular fricative) |
| ყ | q (uvular stop, like Arabic ق) |
| შ | sh (ship) |
| ჩ | ch (church) |
| ც | ts (cats) |
| ძ | dz (adze) |
| წ | ts' (emphatic, ejective) |
| ჭ | ch' (emphatic, ejective) |
| ხ | kh (Scottish loch) |
| ჯ | j (jump) |
| ჰ | h (hat) |

## The Georgian Orthodox Church

The **Georgian Orthodox Church** is one of the oldest Christian churches:

| Event | Date |
|-------|------|
| Christianization | 4th century CE (St. Nino) |
| First bishop | 4th century |
| Autocephaly | 5th century |
| Georgian Bible | 5th century |
| **Complete canon** | **81 books** (largest biblical canon) |

### The 81-Book Canon

The Georgian Bible contains **81 books**:

- **Old Testament**: 51 books (more than Protestant 39)
- **New Testament**: 27 books (standard)
- **Apocrypha**: Various ancient Jewish texts

Books unique to Georgian canon:
- 3rd Ezra
- 4th Maccabees
- Various wisdom literature

## Building the Full Lexicon

This is a **seed lexicon** (309 entries). For complete coverage:

1. **Add K'ik'vadze** - *Old Georgian Dictionary* (standard reference)
2. **Add Georgian National Corpus** - Complete ancient texts
3. **Add Georgian Academy Dictionary** - Comprehensive coverage

```python
# To expand, edit the vocabulary dictionaries in
# old_georgian_lexicon_builder.py and rebuild

from old_georgian_lexicon_builder import OldGeorgianLexicon, OLD_GEORGIAN_EXTENDED_VOCABULARY

# Add new words
OLD_GEORGIAN_EXTENDED_VOCABULARY["ახალი"] = {
    "def": "new",
    "pos": "adjective",
    "translit": "akhali",
    "root": "akhal"
}

# Rebuild
lexicon = OldGeorgianLexicon()
lexicon.build()
lexicon.export_json("old_georgian_lexicon.json")
```

## Sources

1. **K'ik'vadze, Z.** - *Old Georgian Dictionary* (1960s) - Standard reference
2. **Fähnrich, H.** - *Old Georgian Reader* (2008)
3. **Cherkesi, M.** - *Georgian Grammar* (various editions)
4. **Tschenkéli, K.** - *Georgisch-Deutsches Wörterbuch*

## Related Tools

- `ancient-hebrew-lexicon/` - Hebrew (8,674 entries)
- `koine-greek-lexicon/` - Greek (5,523 entries)
- `latin-lexicon/` - Latin (657 entries)
- `syriac-lexicon/` - Syriac (268 entries)
- `aramaic-lexicon/` - Aramaic (149 entries)
- `coptic-lexicon/` - Coptic (148 entries)
- `geez-lexicon/` - Ge'ez (162 entries)
- `narrative-analyzer/` - For analyzing texts

---

**Built:** 2026-07-16
**Current Entries:** 309
**Target:** 10,000+ (with full academic dictionary)
**Language:** Old Georgian (Kartvelian)
**Primary Use:** Georgian Bible, Georgian Orthodox Church, 81-book canon
**Note:** UNIQUE language - not related to Indo-European or Semitic families!
