# Koine Greek Lexicon

## Overview

A **complete Webster-style Greek dictionary** for the Koine (Common) Greek period - the language of the New Testament, early Christian literature, and the Mediterranean world during Jesus' lifetime.

## What This Contains

| Feature | Description |
|---------|-------------|
| **Entries** | 5,523 Greek words |
| **Period** | Koine Greek (300 BCE - 300 CE) |
| **Language** | New Testament and early Christian Greek |
| **Base** | Strong's Concordance + OpenScriptures |
| **Format** | JSON (machine) + Webster's style (human) |

## Files

| File | Purpose |
|------|---------|
| `greek_lexicon.json` | Full 5,523 entry dictionary (1.6MB) |
| `greek_lexicon_compact.json` | Compressed format (582KB) |
| `greek_lexicon_builder.py` | Build script - regenerates from source |
| `search_greek.py` | Quick lookup tool |

## Quick Start

```bash
# Search by word
python3 search_greek.py "love"          # Returns multiple results
python3 search_greek.py "25"            # Strong's number
python3 search_greek.py "ἀγάπη"         # Search Greek directly

# Rebuild from source
python3 greek_lexicon_builder.py
```

## Sample Entries

### G25 - ἀγαπάω (agapaō)
- **Greek:** ἀγαπάω
- **Transliteration:** agapaō
- **Part of Speech:** verb
- **Definition:** to love (in a social or moral sense)
- **KJV Equivalents:** (be-)love(-ed)

### G26 - ἀγάπη (agapē)
- **Greek:** ἀγάπη
- **Transliteration:** agapē
- **Part of Speech:** noun
- **Definition:** love, i.e. affection or benevolence; specially (plural) a love-feast
- **KJV Equivalents:** charity, dear, love

### G2424 - Ἰησοῦς (Iēsous)
- **Greek:** Ἰησοῦς
- **Transliteration:** Iēsous
- **Part of Speech:** proper noun
- **Definition:** Jesus (i.e. Jehoshua), the name of our Lord
- **KJV Equivalents:** Jesus

### G2316 - θεός (theos)
- **Greek:** θεός
- **Transliteration:** theos
- **Part of Speech:** noun
- **Definition:** figuratively, a magistrate; by Hebraism, very
- **KJV Equivalents:** God, god(-ly, -ward)

## Data Structure (JSON)

```json
{
  "G25": {
    "strongs": "G25",
    "lemma": "ἀγαπάω",
    "translit": "agapaō",
    "strongs_def": "to love (in a social or moral sense)",
    "kjv_def": "(be-)love(-ed).",
    "derivation": "perhaps from ἄγαν (agan);"
  }
}
```

## Fields Explained

| Field | Meaning |
|-------|---------|
| `strongs` | Strong's number (G1-G5624) |
| `lemma` | Greek word in Unicode |
| `translit` | Academic transliteration |
| `strongs_def` | Primary definition |
| `kjv_def` | KJV translation equivalents |
| `derivation` | Etymology |

## Koine Greek: Jesus' Language

**Koine Greek** (κοινή = "common") was:

1. **The lingua franca** of the Roman Mediterranean
2. **The language of the New Testament** (written 50-100 CE)
3. **The spoken language** of educated Jews in Jesus' time
4. **Simpler than Classical** Greek - more accessible

### Key Differences from Classical Greek

| Classical Greek | Koine Greek |
|---------------|-------------|
| Complex syntax | Simplified grammar |
| Many dialects | Unified standard |
| Philosophical works | Everyday speech |
| Attic (Athens) | Pan-Mediterranean |

### Hebrew-to-Greek Translation

Many Hebrew concepts were translated into Greek:

| Hebrew | Greek | English |
|--------|-------|---------|
| מָשִׁיחַ (H4899) | Χριστός (G5547) | Christ/Anointed |
| תּוֹרָה (H8451) | νόμος (G3551) | Law |
| שָׁלוֹם (H7965) | εἰρήνη (G1515) | Peace |
| רוּחַ (H7307) | πνεῦμα (G4151) | Spirit/Wind |
| חֶסֶד (H2617) | ἔλεος (G1656) | Mercy/Lovingkindness |

## Usage Patterns

### Most Common Greek Words in the NT

| Rank | Greek | Transliteration | Meaning | Occurrences |
|------|-------|-----------------|---------|-------------|
| 1 | καί | kai | and | 9,000+ |
| 2 | ὁ | ho | the | 20,000+ |
| 3 | αὐτός | autos | he/she/it/they | 5,500+ |
| 4 | δέ | de | but/and | 2,800+ |
| 5 | ἐν | en | in | 2,700+ |
| 6 | εἰμί | eimi | I am | 2,500+ |
| 7 | λέγω | legō | I say | 2,300+ |
| 8 | εἰς | eis | into/to | 1,700+ |
| 9 | οὗτος | houtos | this | 1,400+ |
| 10 | θεός | theos | God | 1,300+ |

## Comparison: Greek vs Hebrew Concepts

### "Love"

| Greek | Hebrew | Meaning |
|-------|--------|---------|
| ἀγάπη (agapē) | אַהֲבָה (H160) | Divine love, charity |
| φιλέω (phileō) | אָהַב (H157) | Brotherly love, friendship |
| ἔρως | דֹּד (H1730) | Romantic/sexual love |
| στοργή | רַחֲמִים (H7356) | Family affection |

### "Word"

| Greek | Hebrew | Meaning |
|-------|--------|---------|
| λόγος (logos) | דָּבָר (H1697) | Word, reason, matter |
| ῥῆμα (rhēma) | אִמְרָה (H561) | Spoken word |
| γραφή (graphē) | כְּתָב (H3791) | Writing, Scripture |

## Theological Key Terms

### Gospel Core

| Strong's | Greek | Meaning | Occurrences |
|----------|-------|---------|-------------|
| G2098 | εὐαγγέλιον | good news/gospel | 77 |
| G266 | ἁμαρτία | sin | 173 |
| G4991 | σωτηρία | salvation | 45 |
| G4102 | πίστις | faith | 244 |
| G1343 | δικαιοσύνη | righteousness | 92 |
| G5485 | χάρις | grace | 155 |

### Christ Titles

| Greek | Translation | Occurrences |
|-------|-------------|-------------|
| Χριστός (G5547) | Christ/Anointed | 529 |
| υἱὸς τοῦ θεοῦ | Son of God | 37 |
| υἱὸς τοῦ ἀνθρώπου | Son of Man | 81 |
| κύριος (G2962) | Lord | 717 |
| σωτήρ (G4990) | Savior | 24 |

## Building Your Own

```python
from greek_lexicon_builder import GreekLexicon

lexicon = GreekLexicon()
lexicon.load_strongs("strongs-greek-dictionary.js")

# Search
results = lexicon.search("grace")
for strongs, entry in results:
    print(f"{strongs}: {entry['lemma']} = {entry['strongs_def']}")

# Export
lexicon.export_json("my_lexicon.json")
```

## Sources

1. **Strong's Concordance** (1894) - James Strong, S.T.D., LL.D.
2. **OpenScriptures Greek Bible** - Morphological analysis
3. **United Bible Societies (UBS) Greek New Testament**

## License

Strong's data is public domain (published 1894).
OpenScriptures additions are CC-BY-SA.

## Related Tools

- `ancient-hebrew-lexicon/` - Hebrew equivalent (8,674 entries)
- `narrative_analyzer.py` - For analyzing biblical narratives
- Ancient language translator skill - For word-by-word translation

## Next Steps

1. **Add LXX equivalents** - Septuagint Hebrew-to-Greek mappings
2. **Add morphology** - Case, gender, number parsing
3. **Add cross-references** - Hebrew-to-Greek connections
4. **Add patristic Greek** - Church Fathers' usage

---

**Built:** 2026-07-16
**Total Entries:** 5,523
**Period Coverage:** Koine Greek (300 BCE - 300 CE)
**Primary Use:** New Testament and early Christian literature
