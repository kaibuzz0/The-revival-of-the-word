# Ge'ez (Gəʿəz) Lexicon

## Overview

A **Ge'ez-English dictionary** for the classical Ethiopic language - the liturgical language of the Ethiopian Orthodox Tewahedo Church and the Ethiopian Bible (the most complete biblical canon with 81 books).

## What This Contains

| Feature | Description |
|---------|-------------|
| **Entries** | 162 core Ge'ez words |
| **Language** | Ge'ez (Classical Ethiopic) |
| **Script** | Ethiopic (Fidel) |
| **Period** | Classical (100-900 CE), Liturgical (to present) |
| **Sources** | Ethiopian liturgy, Bible, and classical texts |
| **Format** | JSON + Markdown + Webster's style |

## Files

| File | Purpose |
|------|---------|
| `geez_lexicon.json` | Full 162 entry dictionary (35KB) |
| `geez_lexicon.md` | Human-readable format (20KB) |
| `websters_geez.txt` | Webster's dictionary style (11KB) |
| `geez_lexicon_builder.py` | Build/regenerate script |
| `search_geez.py` | Lookup tool |

## Quick Start

```bash
# Search
python3 search_geez.py "God"         # Returns: አምላክ (amlāk)
python3 search_geez.py "love"        # Returns: ፍቅር (fəqər)
python3 search_geez.py "አምላክ"        # Ge'ez characters
python3 search_geez.py "q-d-s"       # Root search

# Rebuild from source
python3 geez_lexicon_builder.py
```

## Sample Entries

### አምላክ (amlāk)
- **Ge'ez:** አምላክ
- **Transliteration:** amlāk
- **Part of Speech:** noun
- **Definition:** God
- **Root:** ʾ-l-k

### ኢየሱስ (Iyesus)
- **Ge'ez:** ኢየሱስ
- **Transliteration:** Iyesus
- **Part of Speech:** proper noun
- **Definition:** Jesus
- **Root:** y-s-ʿ

### ፍቅር (fəqər)
- **Ge'ez:** ፍቅር
- **Transliteration:** fəqər
- **Part of Speech:** noun
- **Definition:** love
- **Root:** f-q-r

### ቅዱስ (qədus)
- **Ge'ez:** ቅዱስ
- **Transliteration:** qədus
- **Part of Speech:** adjective/noun
- **Definition:** holy, saint
- **Root:** q-d-s

## Data Structure (JSON)

```json
{
  "አምላክ": {
    "word": "አምላክ",
    "definition": "God",
    "part_of_speech": "noun",
    "transliteration": "amlāk",
    "root": "ʾ-l-k"
  }
}
```

## Ge'ez: Classical Ethiopic

**Ge'ez** (ግዕዝ) is:
1. **Ancient South Semitic language** (related to Arabic, Hebrew)
2. **Liturgical language** of Ethiopian Orthodox Tewahedo Church
3. **Literary language** with extensive religious literature
4. **Ancestor of modern Ethiopian languages** (Amharic, Tigrinya, Tigre)

### Historical Timeline

| Period | Usage |
|--------|-------|
| 100-900 CE | Classical Ge'ez (royal inscriptions, literature) |
| 900-1500 CE | Continued literary production |
| 1500-present | Liturgical use (still used in church services) |

### Script: Ethiopic (Fidel)

The Ge'ez script is a **featural abugida** (segmental writing system):

| Letter | Sound | Category |
|--------|-------|----------|
| ሀ | h | Labial |
| ለ | l | Alveolar |
| ሐ | ḫ | Pharyngeal |
| መ | m | Labial |
| ሠ | ś | Palatal |
| ረ | r | Alveolar |
| ሰ | s | Alveolar |
| ቀ | q | Velar |
| በ | b | Labial |
| ተ | t | Alveolar |
| ኀ | ḫ | Pharyngeal |
| ነ | n | Alveolar |
| አ | ʾ | Glottal stop |
| ከ | k | Velar |
| ወ | w | Labial-velar |
| ዐ | ʿ | Pharyngeal |
| ዘ | z | Alveolar |
| የ | y | Palatal |
| ደ | d | Alveolar |
| ገ | g | Velar |
| ጠ | ṭ | Emphatic |
| ፀ | ḍ | Emphatic |
| ፐ | p | Labial |

### Triliteral Root System

Like Hebrew and Arabic, Ge'ez has a **triliteral root** system:

| Root | Pattern | Meaning |
|------|---------|---------|
| q-d-s | ቅ-ዱ-ስ (qədu-s) | holy |
| k-t-b | ከ-ተ-በ (kätabä) | write |
| ʾ-m-n | አ-መ-ነ (ʾamana) | believe |
| m-l-ʾ | መ-ል-አ (mälaʾ) | full |
| s-l-ʾ | ሰ-ላ-እ (sälāʾ) | peace |

## The Ethiopian Bible: 81 Books

The Ethiopian Orthodox Tewahedo Church has the **most complete biblical canon**:

### Narrow Canon (73 books)
- **Old Testament:** 46 books (includes books counted as deuterocanonical in West)
- **New Testament:** 27 books

### Broader Canon (81 books)
Additional texts considered canonical:
- **Book of Enoch** (1 Enoch) - complete 108 chapters
- **Book of Jubilees** (Kufale)
- **1-3 Meqabyan** (Ethiopian Maccabees)
- **Testament of Isaac**
- **Testament of Jacob**
- **Testament of Adam**
- **Joseph ben Gurion**

## Hebrew → Arabic → Ge'ez Connections

| Hebrew | Arabic | Ge'ez | Meaning |
|--------|--------|-------|---------|
| קָדוֹשׁ (qādôsh) | قدوس (quddūs) | ቅዱስ (qədus) | holy |
| אָב (ʾāv) | أب (ʾab) | አብ (ab) | father |
| בֵּן (bēn) | ابن (ibn) | ወልድ (wäld) | son |
| לֵבָב (lēvāv) | قلب (qalb) | ልብ (ləb) | heart |
| מָוֶת (māvet) | موت (mawt) | ሞት (mot) | death |
| חַיִּים (ḥayyîm) | حياة (ḥayāh) | ሕይወት (ḥəywät) | life |
| שָׁלוֹם (shālôm) | سلام (salām) | ሰላም (sälām) | peace |

## Pronunciation Guide

### Special Consonants

| Symbol | Sound | Description |
|--------|-------|-------------|
| ʾ (አ) | glottal stop | Like uh-oh pause |
| ḫ (ኀ) | [ħ] | Voiceless pharyngeal fricative |
| ʿ (ዐ) | [ʕ] | Voiced pharyngeal fricative |
| ṣ (ጸ) | [sˤ] | Emphatic s |
| ḍ (ፀ) | [t͡sˤ] | Emphatic ts |
| ṭ (ጠ) | [tˤ] | Emphatic t |
| ṗ (ጰ) | [pˤ] | Emphatic p |
| ś (ሠ) | [ɬ] | Voiceless lateral fricative |
| ŋ | [ŋ] | Velar nasal |

### Vowels

Ge'ez has 7 vowel sounds:
- a [a] as in **father**
- u [u] as in **rule**
- i [i] as in **machine**
- ā [aː] long a
- ē [eː] long e
- ō [oː] long o
- ə [ə] schwa

## Liturgical Terms

| Ge'ez | Transliteration | Meaning | Usage |
|-------|-----------------|---------|-------|
| ጸሎት | ṣälot | prayer | Daily prayers |
| ብርክት | bərkt | blessing | Eucharistic prayer |
| ቅዳሴ | qədase | liturgy | Divine Liturgy |
| ዘመን | zämän | time, season | Liturgical seasons |
| ቀዳሚት | qädamit | first | First hour prayer |
| ሰዓት | saʿat | hour | Liturgical hours |

## Building the Full Lexicon

This is a **seed lexicon** (162 entries). For complete coverage:

1. **Add Leslau's Comparative Dictionary** (Wolf Leslau, 1987)
   - 10,000+ entries
   - Available from Internet Archive
   - The standard reference

2. **Add Dillmann's Lexicon** (August Dillmann, 1865)
   - The classic 19th-century dictionary
   - Updated by Bezold and others

3. **Add modern resources**
   - Ethiopian liturgical texts
   - Bible translations

```python
# To expand, edit the vocabulary dictionaries in
# geez_lexicon_builder.py and rebuild

from geez_lexicon_builder import GeezLexicon, GEEZ_EXTENDED_VOCABULARY

# Add new words
GEEZ_EXTENDED_VOCABULARY["አዲስ"] = {
    "def": "new",
    "pos": "adjective",
    "translit": "ʾAddis",
    "root": "ʾ-d-s"
}

# Rebuild
lexicon = GeezLexicon()
lexicon.build()
lexicon.export_json("geez_lexicon.json")
```

## Sources

1. **Wolf Leslau** - *Comparative Dictionary of Geʿez* (1987) - Standard reference
2. **August Dillmann** - *Lexicon Linguae Aethiopicae* (1865) - Classic dictionary
3. **Ethiopian Orthodox Liturgy** - Qəddase (Divine Liturgy)
4. **Ethiopian Bible** - Amharic and Ge'ez texts

## Related Tools

- `ancient-hebrew-lexicon/` - Hebrew (8,674 entries)
- `koine-greek-lexicon/` - Greek (5,523 entries)
- `coptic-lexicon/` - Coptic (148 entries)
- `narrative-analyzer/` - For analyzing texts

---

**Built:** 2026-07-16
**Current Entries:** 162
**Target:** 10,000+ (with Leslau integration)
**Language:** Ge'ez (Classical Ethiopic)
**Primary Use:** Ethiopian liturgy, Ethiopian Bible (81 books)
