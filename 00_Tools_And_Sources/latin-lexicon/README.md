# Latin Lexicon

## Overview

A **Latin-English dictionary** for Classical Latin (100 BCE - 200 CE) and Ecclesiastical Latin (400 CE - present). Latin was the language of the Roman Empire and later the language of the Church, scholarship, and the Vulgate Bible.

## What This Contains

| Feature | Description |
|---------|-------------|
| **Entries** | 657 Latin words |
| **Language** | Classical and Ecclesiastical Latin |
| **Script** | Latin alphabet |
| **Period** | Classical (100 BCE - 200 CE), Ecclesiastical (400 CE-present) |
| **Sources** | Classical texts, Vulgate Bible, Church Latin |
| **Format** | JSON + Markdown + Webster's style |

## Files

| File | Purpose |
|------|---------|
| `latin_lexicon.json` | Full 657 entry dictionary (133KB) |
| `latin_lexicon.md` | Human-readable format (92KB) |
| `websters_latin.txt` | Webster's dictionary style (37KB) |
| `latin_lexicon_builder.py` | Build/regenerate script |
| `search_latin.py` | Lookup tool |

## Quick Start

```bash
# Search
python3 search_latin.py "God"           # Returns: Deus
python3 search_latin.py "love"          # Returns: amo, caritas
python3 search_latin.py "Deus"          # Search Latin directly

# Rebuild from source
python3 latin_lexicon_builder.py
```

## Sample Entries

### Deus (Deus)
- **Latin:** Deus
- **Transliteration:** Deus
- **Part of Speech:** noun
- **Definition:** God
- **Declension:** 2nd
- **Gender:** masculine

### Iesus (Iesus)
- **Latin:** Iesus
- **Transliteration:** Iesus
- **Part of Speech:** proper noun
- **Definition:** Jesus
- **Gender:** masculine

### caritas (caritas)
- **Latin:** caritas
- **Transliteration:** caritas
- **Part of Speech:** noun
- **Definition:** love, charity
- **Declension:** 3rd
- **Gender:** feminine

### veritas (veritas)
- **Latin:** veritas
- **Transliteration:** veritas
- **Part of Speech:** noun
- **Definition:** truth
- **Declension:** 3rd
- **Gender:** feminine

### amo (amo)
- **Latin:** amo
- **Transliteration:** amo
- **Part of Speech:** verb
- **Definition:** to love
- **Conjugation:** 1st

## Data Structure (JSON)

```json
{
  "Deus": {
    "word": "Deus",
    "definition": "God",
    "part_of_speech": "noun",
    "transliteration": "Deus",
    "declension": "2nd",
    "gender": "masculine"
  }
}
```

## Latin: The Language of Rome and the Church

**Latin** is:
1. **Indo-European language** (Italic branch)
2. **Language of the Roman Empire** (civilization, law, literature)
3. **Language of the Catholic Church** (liturgy, theology, scholarship)
4. **Root of Romance languages** (Italian, Spanish, French, Portuguese, Romanian)

### Historical Timeline

| Period | Usage |
|--------|-------|
| 753 BCE | Founding of Rome |
| 100 BCE-200 CE | Classical Latin (Cicero, Virgil, Ovid) |
| 400 CE | Jerome's Vulgate (Latin Bible) |
| 500-1500 CE | Medieval Latin (scholarship, Church) |
| 1500-present | Neo-Latin (science, law, medicine) |

### Two Main Forms

| Classical Latin | Ecclesiastical Latin |
|-----------------|----------------------|
| Cicero, Caesar, Virgil | Vulgate Bible, Church Fathers |
| Rhetorical, elaborate | Simpler, more accessible |
| Pagan literature | Christian theology |
| Golden Age (100 BCE-14 CE) | Jerome (400 CE) to present |

## Grammar System

### Five Declensions (Nouns/Adjectives)

| Declension | Ending | Example |
|------------|--------|---------|
| 1st | -a/-ae | puella (girl) |
| 2nd | -us/-ī | Deus (God) |
| 3rd | various | veritas (truth) |
| 4th | -us/-ūs | manus (hand) |
| 5th | -ēs/-ēī | dies (day) |

### Six Cases

| Case | Function |
|------|----------|
| Nominative | Subject |
| Genitive | Possession (of) |
| Dative | Indirect object (to/for) |
| Accusative | Direct object |
| Ablative | By/with/from/in |
| Vocative | Direct address |

### Four Conjugations (Verbs)

| Conjugation | Ending | Example |
|-------------|--------|---------|
| 1st | -āre | amāre (to love) |
| 2nd | -ēre | vidēre (to see) |
| 3rd | -ere | ducere (to lead) |
| 4th | -īre | audīre (to hear) |

## The Vulgate Bible

**Jerome's Vulgate** (405 CE) is the official Latin translation:

| Feature | Description |
|---------|-------------|
| Translation | Hebrew/Greek → Latin |
| Goal | Common people's language (vulgus = common) |
| Influence | Standard Latin Bible for 1000+ years |
| Language | Ecclesiastical Latin |

### Famous Vulgate Phrases

| Latin | English | Reference |
|-------|---------|-----------|
| Fiat lux | Let there be light | Genesis 1:3 |
| In principio | In the beginning | John 1:1 |
| Verbum caro factum est | The Word became flesh | John 1:14 |
| Pax vobiscum | Peace be with you | Luke 24:36 |
| Et lux in tenebris lucet | Light shines in darkness | John 1:5 |

## Hebrew → Greek → Latin Connections

| Hebrew | Greek | Latin | English |
|--------|-------|-------|---------|
| אֱלֹהִים | θεός | Deus | God |
| יְהֹוָה | κύριος | Dominus | Lord |
| מָשִׁיחַ | Χριστός | Christus | Christ |
| רוּחַ | πνεῦμα | Spiritus | Spirit |
| שָׁלוֹם | εἰρήνη | pax | peace |
| אֱמֶת | ἀλήθεια | veritas | truth |
| חֶסֶד | ἔλεος | misericordia | mercy |
| תּוֹרָה | νόμος | lex | law |

## Pronunciation Guide

### Vowels

| Symbol | Sound | Example |
|--------|-------|---------|
| ā | long a (father) | pater |
| ē | long e (say) | mater |
| ī | long i (machine) | vīta |
| ō | long o (tone) | rōma |
| ū | long u (rule) | tūtus |

### Consonants

| Letter | Sound | Note |
|--------|-------|------|
| c | k (cat) | Always hard |
| g | g (go) | Always hard |
| v | w or v | Classical = w, Ecclesiastical = v |
| j | y (yes) | Ecclesiastical = j (jump) |
| r | trilled r | Rolled tongue |
| sc | sk or sh | sc before i/e = sh |
| gn | ny (canyon) | Like Spanish ñ |
| x | ks | Tax, box |

## Ecclesiastical Terms

| Latin | English | Usage |
|-------|---------|-------|
| sacramentum | sacrament | Baptism, Eucharist |
| gratia | grace | Divine favor |
| fides | faith | Theological virtue |
| spes | hope | Theological virtue |
| caritas | charity/love | Theological virtue |
| peccatum | sin | Original sin |
| resurrectio | resurrection | Easter |
| crux | cross | Good Friday |
| baptisma | baptism | Sacrament |
| evangelium | gospel | Matthew, Mark, Luke, John |

## Latin in Modern English

Thousands of English words come from Latin:

| Latin Root | English Examples |
|------------|------------------|
| amāre (to love) | amorous, amiable, amateur |
| verus (true) | verify, veracity, very |
| pax (peace) | pacify, pacific, pacifist |
| lex (law) | legal, illegal, legislate |
| crux (cross) | crucial, crucify, crusade |
| corpus (body) | corpse, corporation, corpus |
| sanguis (blood) | sanguine, consanguinity |
| anima (soul) | animate, animal, unanimous |

## Building the Full Lexicon

This is a **seed lexicon** (657 entries). For complete coverage:

1. **Add Lewis & Short** - The standard Latin dictionary (5,000+ entries)
2. **Add Oxford Latin Dictionary** - Comprehensive classical coverage
3. **Add Church Latin** - Canon law, liturgy, theology

```python
# To expand, edit the vocabulary dictionaries in
# latin_lexicon_builder.py and rebuild

from latin_lexicon_builder import LatinLexicon, LATIN_EXTENDED_VOCABULARY

# Add new words
LATIN_EXTENDED_VOCABULARY["novus"] = {
    "def": "new",
    "pos": "adjective",
    "translit": "novus",
    "declension": "1st/2nd",
    "gender": "masculine"
}

# Rebuild
lexicon = LatinLexicon()
lexicon.build()
lexicon.export_json("latin_lexicon.json")
```

## Sources

1. **Lewis & Short** - *A Latin Dictionary* (1879) - Standard reference
2. **Oxford Latin Dictionary** - Comprehensive classical coverage
3. **Stelten, Leo F.** - *Dictionary of Ecclesiastical Latin*
4. **Vulgate Bible** - Jerome's Latin translation

## Related Tools

- `ancient-hebrew-lexicon/` - Hebrew (8,674 entries)
- `koine-greek-lexicon/` - Greek (5,523 entries)
- `aramaic-lexicon/` - Aramaic (149 entries)
- `coptic-lexicon/` - Coptic (148 entries)
- `geez-lexicon/` - Ge'ez (162 entries)
- `narrative-analyzer/` - For analyzing texts

---

**Built:** 2026-07-16
**Current Entries:** 657
**Target:** 5,000+ (with Lewis & Short)
**Language:** Classical and Ecclesiastical Latin
**Primary Use:** Roman Empire, Church, Vulgate Bible, scholarship
