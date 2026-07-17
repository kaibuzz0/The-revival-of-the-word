# Coptic Lexicon

## Overview

A **Coptic-English dictionary** for the Sahidic dialect - the language of early Christian Egypt and the Nag Hammadi library (including the Gospel of Thomas and Gospel of Mary).

## What This Contains

| Feature | Description |
|---------|-------------|
| **Entries** | 148 core Coptic words |
| **Dialect** | Sahidic Coptic (Upper Egypt) |
| **Period** | 100-800 CE (Early Christian Egypt) |
| **Sources** | Common Coptic texts, Nag Hammadi library |
| **Format** | JSON + Markdown + Webster's style |

## Files

| File | Purpose |
|------|---------|
| `coptic_lexicon.json` | Full 148 entry dictionary (34KB) |
| `coptic_lexicon.md` | Human-readable format (20KB) |
| `websters_coptic.txt` | Webster's dictionary style (12KB) |
| `coptic_lexicon_builder.py` | Build/regenerate script |
| `search_coptic.py` | Lookup tool |

## Quick Start

```bash
# Search
python3 search_coptic.py "God"          # Returns: ⲛⲟⲩⲧⲉ (noute)
python3 search_coptic.py "love"         # Returns: ⲁⲅⲁⲡⲏ (agapē)
python3 search_coptic.py "ⲛⲟⲩⲧⲉ"      # Search Coptic directly

# Rebuild from source
python3 coptic_lexicon_builder.py
```

## Sample Entries

### ⲛⲟⲩⲧⲉ (noute)
- **Coptic:** ⲛⲟⲩⲧⲉ
- **Transliteration:** noute
- **Part of Speech:** noun
- **Definition:** God
- **Origin:** Egyptian nṯr

### ⲓⲥ (is)
- **Coptic:** ⲓⲥ
- **Transliteration:** is
- **Part of Speech:** proper noun
- **Definition:** Jesus
- **Origin:** Greek: Ἰησοῦς

### ⲁⲅⲁⲡⲏ (agapē)
- **Coptic:** ⲁⲅⲁⲡⲏ
- **Transliteration:** agapē
- **Part of Speech:** noun
- **Definition:** love
- **Origin:** Greek: ἀγάπη

### ⲥⲁϩⲛⲉ (sahne)
- **Coptic:** ⲥⲁϩⲛⲉ
- **Transliteration:** sahne
- **Part of Speech:** noun
- **Definition:** truth
- **Origin:** Egyptian mꜣꜣt (maat)

## Data Structure (JSON)

```json
{
  "ⲛⲟⲩⲧⲉ": {
    "word": "ⲛⲟⲩⲧⲉ",
    "definition": "God",
    "part_of_speech": "noun",
    "transliteration": "noute",
    "etymology": "Egyptian nṯr"
  }
}
```

## Coptic: The Last Egyptian Language

**Coptic** is:
1. **The final stage** of the Egyptian language (3000 years of evolution)
2. **Written in Greek alphabet** + 6 Demotic letters
3. **The language of early Christianity** in Egypt
4. **Still used today** in Coptic Orthodox Church liturgy

### Script

| Letter | Sound | Origin |
|--------|-------|--------|
| ⲁ | a | Greek α (alpha) |
| ⲃ | b | Greek β (beta) |
| ⲅ | g | Greek γ (gamma) |
| ⲇ | d | Greek δ (delta) |
| ⲉ | e | Greek ε (epsilon) |
| ⲍ | z | Greek ζ (zeta) |
| ⲏ | ē | Greek η (eta) |
| ⲑ | th | Greek θ (theta) |
| ⲓ | i | Greek ι (iota) |
| ⲕ | k | Greek κ (kappa) |
| ⲗ | l | Greek λ (lambda) |
| ⲙ | m | Greek μ (mu) |
| ⲛ | n | Greek ν (nu) |
| ⲝ | ks | Greek ξ (xi) |
| ⲟ | o | Greek ο (omicron) |
| ⲡ | p | Greek π (pi) |
| ⲣ | r | Greek ρ (rho) |
| ⲥ | s | Greek σ (sigma) |
| ⲧ | t | Greek τ (tau) |
| ⲩ | u/y | Greek υ (upsilon) |
| ⲫ | ph | Greek φ (phi) |
| ⲭ | kh | Greek χ (chi) |
| ⲯ | ps | Greek ψ (psi) |
| ⲱ | ō | Greek ω (omega) |
| ϣ | sh | Demotic (sh) |
| ϥ | f | Demotic (f) |
| ϩ | h | Demotic (h) |
| ϫ | j | Demotic (j) |
| ϭ | ky/ch | Demotic (ch) |
| ⳉ | ti | Special |

### Vocabulary Origins

Coptic vocabulary comes from three sources:

| Source | Percentage | Examples |
|--------|------------|----------|
| **Egyptian** | ~70% | ⲛⲟⲩⲧⲉ (god), ⲣⲱⲙⲉ (man), ⲙⲟⲩ (water) |
| **Greek** | ~25% | ⲓⲥ (Jesus), ⲁⲅⲁⲡⲏ (love), ⲉⲕⲕⲗⲏⲥⲓⲁ (church) |
| **Semitic/Other** | ~5% | Foreign loanwords |

## Coptic in the Nag Hammadi Library

The **Nag Hammadi library** (discovered 1945) contains:
- 52 texts in Coptic
- Gnostic and early Christian writings
- **Gospel of Thomas** - 114 sayings of Jesus
- **Gospel of Mary** - teachings of Mary Magdalene
- **Gospel of Philip** - sacramental theology

### Key Coptic Terms from Nag Hammadi

| Coptic | Transliteration | Meaning | Significance |
|--------|-----------------|---------|--------------|
| ⲅⲛⲱⲥⲓⲥ | gnōsis | knowledge | Divine knowledge/salvation |
| ⲥⲟⲫⲓⲁ | sophia | wisdom | Divine feminine wisdom |
| ⲥⲁϩⲛⲉ | sahne | truth | Ultimate reality |
| ⲣⲁϩⲧ | raht | kingdom | Realm of God |
| ⲡⲗⲏⲣⲱⲙⲁ | plērōma | fullness | Divine completeness |
| ⲛⲟⲩⲧⲉ | noute | God | The divine source |
| ⲡⲛⲉⲩⲙⲁ | pneuma | spirit | Holy spirit/breath |

## Hebrew → Greek → Coptic Connections

| Hebrew (H) | Greek (G) | Coptic | Meaning |
|------------|-----------|--------|---------|
| מָשִׁיחַ (H4899) | Χριστός (G5547) | ⲭⲣⲓⲥⲧⲟⲥ | Christ |
| אֱלֹהִים (H430) | θεός (G2316) | ⲛⲟⲩⲧⲉ | God |
| יְהֹוָה (H3068) | κύριος (G2962) | ⲕⲩⲣⲓⲟⲥ | Lord |
| רוּחַ (H7307) | πνεῦμα (G4151) | ⲡⲛⲉⲩⲙⲁ | Spirit |
| שָׁלוֹם (H7965) | εἰρήνη (G1515) | ϩⲓⲣⲏⲛⲏ | Peace |
| אֱמֶת (H571) | ἀλήθεια (G225) | ⲥⲁϩⲛⲉ | Truth |
| תּוֹרָה (H8451) | νόμος (G3551) | ⲛⲟⲙⲟⲥ | Law |
| מִצְוָה (H4687) | ἐντολή (G1785) | ⲉⲛⲧⲟⲗⲏ | Commandment |

## Pronunciation Guide

### Vowels
- ⲁ = a as in **father**
- ⲉ = e as in **pet**
- ⲏ = ē as in **say** (long e)
- ⲓ = i as in **machine**
- ⲟ = o as in **note**
- ⲩ = u/y as in French **tu**
- ⲱ = ō as in **tone** (long o)

### Consonants
- ϣ = **sh** as in ship
- ϥ = **f** as in fish
- ϩ = **h** as in hat
- ϫ = **j** as in judge
- ϭ = **ky** or **ch** as in church
- ⲑ = **th** as in **thin**

## Article System

Coptic has a complex article system:

| Article | Meaning | Example |
|---------|---------|---------|
| ⲡ- | the (masculine singular) | ⲡⲣⲱⲙⲉ (the man) |
| ⲧ- | the (feminine singular) | ⲧⲥϩⲓⲙⲉ (the woman) |
| ⲛ- | the (plural) | ⲛⲣⲱⲙⲉ (the people) |
| ⲟⲩ- | a/an | ⲟⲩⲣⲱⲙⲉ (a man) |
| ⲡⲉⲓ- | this | ⲡⲉⲓⲣⲱⲙⲉ (this man) |

## Building the Full Lexicon

This is a **seed lexicon** (148 entries). For complete coverage:

1. **Add Crum's Dictionary** (W.E. Crum, 1939)
   - 10,000+ entries
   - Available from Internet Archive
   - The definitive Coptic dictionary

2. **Add Coptic Scriptorium data**
   - Automatic linguistic annotations
   - POS tagging for corpora

3. **Add dialect variants**
   - Bohairic (modern liturgical Coptic)
   - Fayyumic, Akhmimic, etc.

```python
# To expand the lexicon, edit the vocabulary dictionaries
# in coptic_lexicon_builder.py and rebuild

from coptic_lexicon_builder import CopticLexicon, COPTIC_EXTENDED_VOCABULARY

# Add new words
COPTIC_EXTENDED_VOCABULARY["ⲛⲟⲩϥ"] = {
    "def": "gold",
    "pos": "noun",
    "translit": "nouf",
    "origin": "Egyptian nbw"
}

# Rebuild
lexicon = CopticLexicon()
lexicon.build()
lexicon.export_json("coptic_lexicon.json")
```

## Sources

1. **W.E. Crum** - *A Coptic Dictionary* (1939) - The standard reference
2. **Nag Hammadi Library** - Original Coptic texts
3. **Coptic Scriptorium** - Digital humanities project
4. **Coptic Treasures Project** - Online resources

## Related Tools

- `ancient-hebrew-lexicon/` - Hebrew (8,674 entries)
- `koine-greek-lexicon/` - Greek (5,523 entries)
- `narrative-analyzer/` - For analyzing texts

---

**Built:** 2026-07-16
**Current Entries:** 148
**Target:** 10,000+ (with Crum integration)
**Dialect:** Sahidic Coptic
**Primary Use:** Early Christian texts, Nag Hammadi library
