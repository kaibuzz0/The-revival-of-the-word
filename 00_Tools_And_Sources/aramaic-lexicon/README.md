# Aramaic Lexicon

## Overview

An **Aramaic-English dictionary** for Biblical Aramaic (Daniel/Ezra) and Galilean Aramaic (Jesus' spoken language). Aramaic was the lingua franca of the Middle East and the native tongue of Jesus and his disciples.

## What This Contains

| Feature | Description |
|---------|-------------|
| **Entries** | 149 core Aramaic words |
| **Language** | Biblical and Galilean Aramaic |
| **Script** | Hebrew square script |
| **Period** | Biblical (600-400 BCE), Galilean (30 CE) |
| **Sources** | Daniel, Ezra, New Testament Aramaicisms |
| **Format** | JSON + Markdown + Webster's style |

## Files

| File | Purpose |
|------|---------|
| `aramaic_lexicon.json` | Full 149 entry dictionary (34KB) |
| `aramaic_lexicon.md` | Human-readable format (20KB) |
| `websters_aramaic.txt` | Webster's dictionary style (12KB) |
| `aramaic_lexicon_builder.py` | Build/regenerate script |
| `search_aramaic.py` | Lookup tool |

## Quick Start

```bash
# Search
python3 search_aramaic.py "God"         # Returns: אֱלָהָא (ʾĕlāhāʾ)
python3 search_aramaic.py "father"      # Returns: אֲבָא (ʾăḇāʾ)
python3 search_aramaic.py "Abba"        # Returns: אֲבָא
python3 search_aramaic.py "אֱלָהָא"      # Aramaic characters

# Rebuild from source
python3 aramaic_lexicon_builder.py
```

## Sample Entries

### אֱלָהָא (ʾĕlāhāʾ)
- **Aramaic:** אֱלָהָא
- **Transliteration:** ʾĕlāhāʾ
- **Part of Speech:** noun
- **Definition:** God
- **Root:** ʾ-l-h

### אֲבָא (ʾăḇāʾ)
- **Aramaic:** אֲבָא
- **Transliteration:** ʾăḇāʾ
- **Part of Speech:** noun
- **Definition:** father (Jesus' Aramaic)
- **Root:** ʾ-b
- **Note:** Mark 14:36, "Abba Father"

### שְׁמַע (šəmaʿ)
- **Aramaic:** שְׁמַע
- **Transliteration:** šəmaʿ
- **Part of Speech:** verb
- **Definition:** to hear
- **Root:** š-m-ʿ

### מַלְכוּתָא (malkûṯāʾ)
- **Aramaic:** מַלְכוּתָא
- **Transliteration:** malkûṯāʾ
- **Part of Speech:** noun
- **Definition:** kingdom
- **Root:** m-l-k

## Data Structure (JSON)

```json
{
  "אֱלָהָא": {
    "word": "אֱלָהָא",
    "definition": "God",
    "part_of_speech": "noun",
    "transliteration": "ʾĕlāhāʾ",
    "root": "ʾ-l-h"
  }
}
```

## Aramaic: Jesus' Language

**Aramaic** (אַרָּמִית) is:
1. **Semitic language** (like Hebrew and Arabic)
2. **Jesus' native language** (Galilean dialect)
3. **Lingua franca** of the Middle East (600 BCE - 600 CE)
4. **Written in Hebrew script** (square letters)

### Historical Timeline

| Period | Usage |
|--------|-------|
| 1000-600 BCE | Old Aramaic (Syrian kingdoms) |
| 600-200 BCE | Imperial Aramaic (Persian Empire) |
| 200 BCE-200 CE | Middle Aramaic (Jesus' era) |
| 200-600 CE | Late Aramaic (Talmudic, Syriac) |

### Jesus Spoke Aramaic

The New Testament preserves several Aramaic words spoken by Jesus:

| Aramaic | Transliteration | Greek | English | Reference |
|---------|-----------------|-------|---------|-----------|
| אֲבָא | ʾăḇāʾ | ἀββά | Abba/Father | Mark 14:36 |
| טַלִיתָא קוּמִי | ṭalîṯāʾ qûmî | ταλιθα κουμ | Talitha cumi | Mark 5:41 |
| אֶפְפַתַח | ʾep̱paṯaḥ | ἐφφαθα | Be opened! | Mark 7:34 |
| גְּבוּרְתָּא | gəḇûrəṯāʾ | δύναμις | power | Matthew 6:13 |
| מַלְכוּתָךְ | malkûṯāḵ | βασιλεία σου | thy kingdom | Matthew 6:9-13 |

## Biblical Aramaic

The Hebrew Bible contains **Aramaic passages**:

| Book | Chapters | Content |
|------|----------|---------|
| Genesis 31:47 | — | Laban's Aramaic verse |
| Jeremiah 10:11 | — | Single Aramaic verse |
| Daniel 2:4b-7:28 | Ch. 2-7 | Court tales, visions |
| Ezra 4:8-6:18, 7:12-26 | Ch. 4-7 | Official correspondence |

### Key Differences from Hebrew

| Feature | Hebrew | Aramaic |
|---------|--------|---------|
| Definite article | הַ (ha-) | usually suffix -א (-ā) |
| Relative pronoun | אֲשֶׁר (ʾăšer) | דִּי (dî) |
| "that" | כִּי (kî) | דִּי (dî) |
| "not" | לֹא (lô) | לָא (lāʾ) |
| "he was" | הָיָה (hāyāh) | הֲוָה (hăwāh) |
| "he came" | בָּא (bāʾ) | אֲתָה (ʾăṯāh) |

## Triliteral Root System

Like Hebrew and Arabic, Aramaic uses **triliteral roots**:

| Root | Pattern | Meaning |
|------|---------|---------|
| ʾ-l-h | אֱלָהָא | God |
| ʾ-b | אֲבָא | father |
| m-l-k | מַלְכוּתָא | kingdom |
| š-m-ʿ | שְׁמַע | hear |
| y-d-ʿ | יְדַע | know |
| q-ṭ-l | קְטַל | kill |
| ʿ-l-h | עֲלָה | go up |

## Pronunciation Guide

### Consonants

| Symbol | Sound | Example |
|--------|-------|---------|
| ʾ | glottal stop | uh-**oh** |
| ḥ/ḫ | voiceless pharyngeal | Scottish lo**ch** |
| ʿ | voiced pharyngeal | **ayin** (Semitic) |
| ṣ/ṣ | emphatic s | s with tension |
| ṭ | emphatic t | t with tension |
| q | emphatic k | k with tension |

### Vowels

| Symbol | Sound |
|--------|-------|
| ā | long a (father) |
| ē | long e (say) |
| ō | long o (tone) |
| û | long u (rule) |
| ă | short a (cat) |
| ə | schwa (about) |

## Aramaic in the Talmud

After the destruction of the Second Temple (70 CE), **Jewish Aramaic** became the language of rabbinic scholarship:

| Text | Language | Period |
|------|----------|--------|
| Mishnah | Hebrew | 200 CE |
| Tosefta | Hebrew/Aramaic | 300 CE |
| Talmud Yerushalmi | Aramaic | 400 CE |
| Talmud Bavli | Aramaic | 500 CE |
| Zohar | Aramaic | 1300 CE |

## Hebrew → Aramaic → Arabic Connections

| Hebrew | Aramaic | Arabic | Meaning |
|--------|---------|--------|---------|
| אָב (ʾāḇ) | אֲבָא (ʾăḇāʾ) | أب (ʾab) | father |
| אֱלֹהִים (ʾĕlōhîm) | אֱלָהָא (ʾĕlāhāʾ) | إله (ʾilāh) | God |
| מֶלֶךְ (meleḵ) | מֶלֶךְ (meleḵ) | ملك (malik) | king |
| שָׁלוֹם (šālôm) | שְׁלָם (šəlām) | سلام (salām) | peace |
| חֶסֶד (ḥeseḏ) | חֲסַד (ḥăsaḏ) | حسن (ḥasan) | kindness |
| קֹדֶשׁ (qōḏeš) | קַדִּישׁ (qadiš) | قدوس (quddūs) | holy |
| יָדַע (yāḏaʿ) | יְדַע (yəḏaʿ) | علم (ʿalima) | know |

## Syriac vs. Jewish Aramaic

| Feature | Jewish Aramaic | Syriac (Christian) |
|---------|----------------|--------------------|
| Scripture | Talmud, Targum | Peshitta NT |
| Region | Palestine, Babylon | Syria, Mesopotamia |
| Script | Hebrew square | Syriac cursive |
| "the" | -ā (emphatic) | -ā (emphatic) |
| Jesus' language | Yes | No |

## Building the Full Lexicon

This is a **seed lexicon** (149 entries). For complete coverage:

1. **Add Targumic Aramaic**
   - Targum Onkelos (Torah)
   - Targum Jonathan (Prophets)
   
2. **Add Peshitta Syriac**
   - Syriac New Testament
   - Ephrem the Syrian

3. **Add Jewish Palestinian Aramaic**
   - Talmud Yerushalmi
   - Midrashim

4. **Add Babylonian Aramaic**
   - Talmud Bavli
   - Gaonic literature

```python
# To expand, edit the vocabulary dictionaries in
# aramaic_lexicon_builder.py and rebuild

from aramaic_lexicon_builder import AramaicLexicon, ARAMAIC_EXTENDED_VOCABULARY

# Add new words
ARAMAIC_EXTENDED_VOCABULARY["חָכִים"] = {
    "def": "wise",
    "pos": "adjective",
    "translit": "ḥāḵîm",
    "root": "ḥ-k-m"
}

# Rebuild
lexicon = AramaicLexicon()
lexicon.build()
lexicon.export_json("aramaic_lexicon.json")
```

## Sources

1. **Gesenius, Wilhelm** - *Hebraeisches und Aramaeisches Handwörterbuch*
2. **Marcus, David** - *A Manual of Biblical Hebrew* (Aramaic sections)
3. **Stevenson, William B.** - *Grammar of Palestinian Jewish Aramaic*
4. **Kautzsch, E.** - *Grammatik des Biblisch-Aramaeischen*

## Related Tools

- `ancient-hebrew-lexicon/` - Hebrew (8,674 entries)
- `koine-greek-lexicon/` - Greek (5,523 entries)
- `coptic-lexicon/` - Coptic (148 entries)
- `geez-lexicon/` - Ge'ez (162 entries)
- `narrative-analyzer/` - For analyzing texts

---

**Built:** 2026-07-16
**Current Entries:** 149
**Target:** 5,000+ (with Targum and Peshitta)
**Language:** Biblical and Galilean Aramaic
**Primary Use:** Jesus' words, Daniel/Ezra, early Christianity
