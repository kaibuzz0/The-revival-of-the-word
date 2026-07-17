# Cross-Reference Lookup Tool

Search across **8 ancient biblical languages simultaneously**! This powerful tool allows you to find translations and cognates across Hebrew, Greek, Latin, Syriac, Old Georgian, Aramaic, Coptic, and Ge'ez.

## Features

- ✅ **Search across 8 languages at once**
- ✅ **15,890+ entries** loaded instantly
- ✅ **Quick cross-reference mode** for common biblical terms
- ✅ **Full search** across definitions, transliterations, and roots
- ✅ **Statistics dashboard** showing coverage by language family
- ✅ **Colored output** for easy reading

## Tools Included

| Tool | Purpose | Speed | Usage |
|------|---------|-------|-------|
| `quick_lookup.py` | Instant cross-references | Fast | `python quick_lookup.py god` |
| `cross_reference_lookup.py` | Full lexicon search | Slower | `python cross_reference_lookup.py love` |

## Quick Start

### Quick Lookup (Fast)

```bash
# Show translation for common biblical term
python quick_lookup.py god
python quick_lookup.py jesus
python quick_lookup.py love
python quick_lookup.py salvation

# List all available quick terms
python quick_lookup.py --list
```

**Available quick terms:** god, lord, jesus, christ, spirit, father, son, love, peace, truth, holy, sin, salvation, resurrection

### Full Cross-Reference Search (Comprehensive)

```bash
# Search across all 8 languages
python cross_reference_lookup.py "God"
python cross_reference_lookup.py "resurrection"

# Search specific languages only
python cross_reference_lookup.py "love" --langs hebrew,greek

# Show statistics
python cross_reference_lookup.py --stats

# Show predefined cross-references
python cross_reference_lookup.py --xref love

# Show help
python cross_reference_lookup.py --help
```

## Sample Output

### Quick Lookup
```
================================================================================
GOD - Biblical Translations
================================================================================

HEBREW       אֱלֹהִים (Elohim)
GREEK        θεός (theos)
LATIN        Deus
SYRIAC       ܐܠܗܐ (ʾalâhâʾ)
GEORGIAN     ღმერთი (ghmerti)
ARAMAIC      אֱלָהָא (ʾĕlâhâʾ)
COPTIC       ⲛⲟⲩⲧⲉ (noute)
GEEZ         አምላክ (Amlak)

================================================================================
```

### Full Search
```
CROSS-LANGUAGE SEARCH RESULTS: 'Jesus'

Found 6 matches across 6 languages

Ancient Hebrew (Semitic | 1000 BCE-70 CE)
  1. יֵשׁוּעַ (Yēšûaʿ) - Jesus

Koine Greek (Indo-European | 300 BCE-300 CE)
  1. Ἰησοῦς (Iēsous) - Jesus

Latin (Indo-European | 100 BCE-present)
  1. Iesus - Jesus

Syriac (Semitic | 200-700 CE)
  1. ܝܫܘܥ (yešûʿ) - Jesus
     Root: y-š-ʿ

Old Georgian (Kartvelian | 5th-11th c. CE)
  1. იესუ (iesu) - Jesus

... etc
```

## Language Coverage

| Language | Family | Script | Entries | Period |
|----------|--------|--------|---------|--------|
| **Hebrew** | Semitic | Hebrew | 8,674 | 1000 BCE-70 CE |
| **Greek** | Indo-European | Greek | 5,523 | 300 BCE-300 CE |
| **Latin** | Indo-European | Latin | 657 | 100 BCE-present |
| **Syriac** | Semitic | Syriac | 268 | 200-700 CE |
| **Old Georgian** | Kartvelian | Georgian | 309 | 5th-11th c. CE |
| **Aramaic** | Semitic | Aramaic | 149 | 600 BCE-30 CE |
| **Coptic** | Afro-Asiatic | Coptic | 148 | 100-800 CE |
| **Ge'ez** | Semitic | Ge'ez | 162 | 100-900 CE |

**Total: 15,890 entries across 4 language families**

## The Complete Biblical Language Chain

### Translation Example: "God"

| Language | Word | Transliteration |
|----------|------|-----------------|
| **Hebrew** | אֱלֹהִים | Elohim |
| **Aramaic** | אֱלָהָא | ʾĕlâhâʾ |
| **Greek** | θεός | theos |
| **Latin** | Deus | Deus |
| **Syriac** | ܐܠܗܐ | ʾalâhâʾ |
| **Coptic** | ⲛⲟⲩⲧⲉ | noute |
| **Ge'ez** | አምላክ | Amlak |
| **Georgian** | ღმერთი | ghmerti |

### Translation Example: "Jesus"

| Language | Word | Transliteration |
|----------|------|-----------------|
| **Hebrew** | יֵשׁוּעַ | Yēšûaʿ |
| **Aramaic** | יֵשׁוּעַ | Yēšûaʿ |
| **Greek** | Ἰησοῦς | Iēsous |
| **Latin** | Iesus | Iesus |
| **Syriac** | ܝܫܘܥ | yešûʿ |
| **Coptic** | ⲓⲏⲥⲟⲩⲥ | iēsous |
| **Ge'ez** | ኢየሱስ | Iyesus |
| **Georgian** | იესუ | iesu |

## Language Families Represented

### Semitic (9,253 entries)
- Hebrew (8,674)
- Syriac (268)
- Ge'ez (162)
- Aramaic (149)

### Indo-European (6,180 entries)
- Greek (5,523)
- Latin (657)

### Kartvelian (309 entries)
- Old Georgian (309) - **COMPLETELY UNIQUE!**

### Afro-Asiatic (148 entries)
- Coptic (148)

## Biblical Canon Coverage

This tool covers **every major biblical tradition**:

| Tradition | Books | Languages |
|-----------|-------|-----------|
| Hebrew Bible | 24/39 | Hebrew, Aramaic |
| Protestant | 66 | Hebrew, Greek |
| Catholic | 73 | Hebrew, Greek, Latin |
| Orthodox | 76-79 | +Church Slavonic |
| Ethiopian | **81** | **Ge'ez** |
| Syriac Peshitta | Full | **Syriac** |
| Georgian | **81** | **Old Georgian** |

## Jesus' Languages

✅ **Hebrew** - Written language of Scripture  
✅ **Aramaic** - **Spoken language of Jesus!**  
✅ **Greek** - Language of the New Testament  

## Usage Examples

### Find All Occurrences of "Love"

```bash
# Quick reference
python quick_lookup.py love

# Full search
python cross_reference_lookup.py love

# Cross-reference mode
python cross_reference_lookup.py --xref love
```

### Compare Biblical Terms

```bash
# Show statistics first
python cross_reference_lookup.py --stats

# Search for resurrection across all languages
python cross_reference_lookup.py resurrection

# Compare God/Lord translations
python quick_lookup.py god
python quick_lookup.py lord
```

### Filter by Language Family

```bash
# Search only Semitic languages
python cross_reference_lookup.py "spirit" --langs hebrew,aramaic,syriac,geez

# Search only Indo-European
python cross_reference_lookup.py "truth" --langs greek,latin
```

## Technical Details

### File Structure

```
cross-reference-lookup/
├── cross_reference_lookup.py    # Full search tool
├── quick_lookup.py              # Fast reference tool
└── README.md                    # This file
```

### Data Sources

All lexicons loaded from parent directory:
- `../ancient-hebrew-lexicon/hebrew_lexicon.json`
- `../koine-greek-lexicon/greek_lexicon.json`
- `../latin-lexicon/latin_lexicon.json`
- `../syriac-lexicon/syriac_lexicon.json`
- `../old-georgian-lexicon/old_georgian_lexicon.json`
- `../aramaic-lexicon/aramaic_lexicon.json`
- `../coptic-lexicon/coptic_lexicon.json`
- `../geez-lexicon/geez_lexicon.json`

## Tips for Best Results

1. **Use quick_lookup.py** for common biblical terms - it's instant
2. **Use cross_reference_lookup.py** for obscure terms or definitions
3. **Try different forms**: English gloss, transliteration, native script
4. **Check roots**: Many words share common roots (especially Semitic)
5. **Use --langs filter** when you know which languages you need

## Next Steps

- Use with `narrative-analyzer/` for biblical text analysis
- Export results for academic research
- Build translation glossaries from cross-references
- Study etymological connections across language families

---

**Total Coverage:** 15,890 entries across 8 languages  
**Language Families:** 4 (Semitic, Indo-European, Kartvelian, Afro-Asiatic)  
**Biblical Canons:** Hebrew, Protestant, Catholic, Orthodox, Ethiopian, Syriac, Georgian  

**The most comprehensive ancient biblical language cross-reference tool available!**
