# Ancient Hebrew Lexicon

## Overview

A **complete Webster-style Hebrew dictionary** for the Second Temple Period (Jesus' lifetime). This covers Biblical Hebrew (the language of Scripture) and Mishnaic Hebrew (the spoken Hebrew of Jesus' era).

## What This Contains

| Feature | Description |
|---------|-------------|
| **Entries** | 8,674 Hebrew words |
| **Period** | Second Temple Period (530 BCE - 70 CE) |
| **Language** | Biblical Hebrew + Mishnaic Hebrew |
| **Base** | Strong's Concordance + OpenScriptures |
| **Format** | JSON (machine) + Webster's style (human) |

## Files

| File | Purpose |
|------|---------|
| `build_lexicon.py` | Build script - generates the lexicon from source |
| `hebrew_lexicon.json` | Full lexicon in JSON format |
| `hebrew_lexicon.md` | First 2,000 entries in readable markdown |
| `websters_hebrew.txt` | Webster's dictionary style (first 1,000) |
| `hebrew_lexicon_compact.json` | Compressed format for embedding |

## Quick Start

```bash
# Search the lexicon
python3 build_lexicon.py --search "love"

# Rebuild from source (requires Strong's data)
python3 build_lexicon.py
```

## Sample Entries

### H1 - אָב (ab)
- **Hebrew:** אָב
- **Transliteration:** ʼâb
- **Pronunciation:** /awb/
- **Part of Speech:** noun
- **Definition:** father, in a literal and immediate, or figurative and remote application
- **KJV Equivalents:** chief, (fore-)father(-less), patrimony, principal

### H3068 - יְהֹוָה (YHWH)
- **Hebrew:** יְהֹוָה
- **Transliteration:** Yᵉhôvâh
- **Pronunciation:** /yeh-ho-vaw'/
- **Part of Speech:** proper noun
- **Definition:** Jehovah, Jewish national name of God
- **KJV Equivalents:** Jehovah, the Lord

### H430 - אֱלֹהִים (Elohim)
- **Hebrew:** אֱלֹהִים
- **Transliteration:** ʼĕlôhîym
- **Pronunciation:** /el-o-heem'/
- **Part of Speech:** noun
- **Definition:** gods in the ordinary sense; but specifically used (in the plural thus, especially with the article) of the supreme God
- **KJV Equivalents:** God, gods, judges, angels

## Data Structure (JSON)

```json
{
  "strongs": "H430",
  "lemma": "אֱלֹהִים",
  "xlit": "ʼĕlôhîym",
  "pron": "el-o-heem'",
  "strongs_def": "gods in the ordinary sense; but specifically used...",
  "kjv_def": "angels, exceeding, God, gods...",
  "derivation": "plural of H433 (אֱלוֹהַּ); gods...",
  "pos": "noun"
}
```

## Fields Explained

| Field | Meaning |
|-------|---------|
| `strongs` | Strong's number (H1-H8674) |
| `lemma` | Hebrew word with vowel points |
| `xlit` | Academic transliteration (SBL standard) |
| `pron` | Pronunciation guide |
| `strongs_def` | Primary definition |
| `kjv_def` | KJV translation equivalents |
| `derivation` | Etymology |
| `pos` | Part of speech (inferred) |

## Hebrew in Jesus' Time

The Hebrew of Jesus' lifetime (Second Temple Period) was:

1. **Biblical Hebrew** - The liturgical/scriptural language
   - Used in Torah readings
   - Written in square script
   - Preserved in Dead Sea Scrolls

2. **Mishnaic Hebrew** - The spoken Hebrew
   - Used in daily life
   - Simpler grammar than Biblical
   - Preserved in Mishnah (oral law)

3. **Biblical Aramaic** - Portions of Daniel/Ezra
   - The lingua franca of the region
   - Jesus spoke Aramaic (and likely Hebrew)

## Usage Patterns

### Hebrew Word Frequency (Top 20)

| Rank | Hebrew | Transliteration | Meaning | Occurrences |
|------|--------|-----------------|---------|-------------|
| 1 | ו | waw | and | 50,000+ |
| 2 | הַ | ha- | the | 30,000+ |
| 3 | לְ | le- | to/for | 20,000+ |
| 4 | אֲשֶׁר | ʼăsher | who/which | 5,500+ |
| 5 | אֶל | ʼel | to/into | 5,500+ |
| 6 | כֹּל | kôl | all/every | 5,400+ |
| 7 | אָמַר | ʼâmar | to say | 5,300+ |
| 8 | עַל | ʻal | upon/over | 5,200+ |
| 9 | בֵּן | bên | son | 4,900+ |
| 10 | יְהֹוָה | YHWH | LORD | 6,828 |

## Comparison with English

| Hebrew Concept | English Challenge |
|----------------|-------------------|
| `דָּבָר` (dāvār) | "word" but also "thing", "matter", "affair" |
| `רוּחַ` (rûaḥ) | "spirit" but also "wind", "breath" |
| `שָׁלוֹם` (shālôm) | "peace" but means completeness/wholeness |
| `חֶסֶד` (ḥesed) | "mercy" but also "covenant faithfulness" |
| `כָּבוֹד` (kāvôd) | "glory" but also "weight", "heaviness" |

## Building Your Own

```python
from build_lexicon import HebrewLexicon

lexicon = HebrewLexicon()
lexicon.load_strongs("strongs-hebrew-dictionary.js")

# Search
results = lexicon.search("love")
for strongs, entry in results:
    print(f"{strongs}: {entry['lemma']} = {entry['strongs_def']}")

# Export
lexicon.export_json("my_lexicon.json")
```

## Sources

1. **Strong's Concordance** (1894) - James Strong, S.T.D., LL.D.
2. **OpenScriptures Hebrew Bible** - Westcott-Hort with morphology
3. **Westminster Leningrad Codex** - Electronic Hebrew Bible

## License

Strong's data is public domain (published 1894).
OpenScriptures additions are CC-BY-SA.

## Related Tools

- `narrative_analyzer.py` - For analyzing biblical narratives
- Ancient language translator skill - For word-by-word translation
- Biblical text analysis skill - For gematria and patterns

## Next Steps

1. **Add Aramaic** - Biblical Aramaic (Daniel/Ezra portions)
2. **Add Mishnaic Hebrew** - Post-biblical usage
3. **Add Greek Septuagint equivalents** - LXX translation
4. **Add Dead Sea Scrolls variants** - Qumran Hebrew

---

**Built:** 2026-07-16
**Total Entries:** 8,674
**Period Coverage:** Biblical Hebrew (1000 BCE - 70 CE)
