# The Revival of the Word

A comprehensive forensic and linguistic research toolkit for analyzing ancient biblical texts, witness statements, and sacred narratives across 8 ancient languages.

## 🎯 Mission

Building the most complete ancient biblical language research suite with forensic-grade analysis tools for:
- Multi-witness narrative coherence analysis
- Cross-language biblical translation verification
- Ancient text pattern detection and unification

## 📚 Tools Overview

### Language Lexicons (8 Languages, 15,890+ Entries)

| Language | Entries | Family | Period | Location |
|----------|---------|--------|--------|----------|
| **Ancient Hebrew** | 8,674 | Semitic | 1000 BCE-70 CE | `ancient-hebrew-lexicon/` |
| **Koine Greek** | 5,523 | Indo-European | 300 BCE-300 CE | `koine-greek-lexicon/` |
| **Latin** | 657 | Indo-European | 100 BCE-present | `latin-lexicon/` |
| **Syriac** | 268 | Semitic | 200-700 CE | `syriac-lexicon/` |
| **Old Georgian** | 309 | Kartvelian | 5th-11th c. CE | `old-georgian-lexicon/` |
| **Aramaic** | 149 | Semitic | 600 BCE-30 CE | `aramaic-lexicon/` |
| **Coptic** | 148 | Afro-Asiatic | 100-800 CE | `coptic-lexicon/` |
| **Ge'ez** | 162 | Semitic | 100-900 CE | `geez-lexicon/` |

**Total: 15,890 dictionary entries across 4 language families**

### Forensic Analysis Tools

| Tool | Purpose | Status |
|------|---------|--------|
| **Enhanced Narrative Analyzer** | Database-backed witness analysis with SQLite | ✅ Ready |
| **Multi-Phase Processor** | Batch processing 1000+ statements | ✅ Ready |
| **Pattern Detection Suite** | Hidden pattern analysis | ✅ Ready |
| **Cross-Reference Lookup** | Search all 8 languages simultaneously | ✅ Ready |

## 🚀 Quick Start

### Biblical Language Lookup

```bash
cd 00_Tools_And_Sources/cross-reference-lookup

# Quick cross-reference
python quick_lookup.py god
python quick_lookup.py jesus
python quick_lookup.py love

# Full search
python cross_reference_lookup.py --stats
```

### Forensic Narrative Analysis

```bash
cd 00_Tools_And_Sources/narrative-analyzer

# Run demo
python enhanced_narrative_analyzer.py

# Batch process statements
python multi_phase_processor.py

# Detect patterns
python pattern_detection_suite.py
```

### Individual Language Search

```bash
# Hebrew
cd ancient-hebrew-lexicon
python search_hebrew.py "love"

# Greek
cd koine-greek-lexicon
python search_greek.py "θεός"

# Latin
cd latin-lexicon
python search_latin.py "Deus"
```

## 📊 Complete Translation Chain

| English | Hebrew | Aramaic | Greek | Latin | Syriac | Coptic | Ge'ez | Georgian |
|---------|--------|---------|-------|-------|--------|--------|-------|----------|
| **God** | אֱלֹהִים | אֱלָהָא | θεός | Deus | ܐܠܗܐ | ⲛⲟⲩⲧⲉ | አምላክ | ღმერთი |
| **Lord** | יְהֹוָה | מָרֵא | κύριος | Dominus | ܡܪܝܐ | ⲕⲩⲣⲓⲟⲥ | እግዚአብሔር | უფალი |
| **Jesus** | יֵשׁוּעַ | יֵשׁוּעַ | Ἰησοῦς | Iesus | ܝܫܘܥ | ⲓⲏⲥⲟⲩⲥ | ኢየሱስ | იესუ |
| **Christ** | מָשִׁיחַ | מְשִׁיחָא | Χριστός | Christus | ܡܫܝܚܐ | ⲭⲣⲓⲥⲧⲟⲥ | ክርስቶስ | ქრისტე |
| **Spirit** | רוּחַ | רוּחַ | πνεῦμα | Spiritus | ܪܘܚܐ | ⲡⲛⲉⲩⲙⲁ | መንፈስ | სული |
| **Peace** | שָׁלוֹם | שְׁלָם | εἰρήνη | pax | ܫܠܡܐ | ϩⲓⲣⲏⲛⲏ | ሰላም | მშვიდობა |

## 🛠️ Enhanced Narrative Analyzer Features

### Entity Extraction
- **WHO**: Persons, suspects, victims
- **WHAT**: Actions, objects, weapons
- **WHERE**: Locations, addresses
- **WHEN**: Dates, times, temporal markers

### Credibility Scoring (0-100%)

| Score | Tier | Description |
|-------|------|-------------|
| 85-100 | Highly Reliable | Corroborated, detailed, consistent |
| 70-84 | Reliable | Minor issues, generally trustworthy |
| 50-69 | Questionable | Some red flags, needs verification |
| 30-49 | Unreliable | Major inconsistencies |
| 0-29 | Fabricated | Likely false statement |

### Pattern Detection

**Consistency Patterns:**
- Linguistic resonance (repeated phrases)
- Temporal consistency (event clustering)
- Detail progression (changing detail levels)

**Contradiction Patterns:**
- Exclusive claims (mutually exclusive statements)
- Memory drift (changing stories)
- Outlier witnesses (minority views)

## 📖 Biblical Canon Coverage

| Tradition | Books | Primary Languages |
|-----------|-------|-------------------|
| Hebrew Bible | 24/39 | Hebrew + Aramaic |
| Protestant | 66 | Hebrew + Greek |
| Catholic | 73 | Hebrew + Greek + Latin |
| Orthodox | 76-79 | Hebrew + Greek + Slavonic |
| **Ethiopian** | **81** | **Ge'ez** |
| **Syriac Peshitta** | Full | **Syriac** |
| **Georgian Orthodox** | **81** | **Old Georgian** |

## 🔬 Research Applications

### For Biblical Scholars
- Cross-language translation verification
- Ancient manuscript comparison
- Theological concept tracking across traditions

### For Forensic Investigators
- Multi-witness statement analysis
- Credibility assessment
- Timeline reconstruction
- Contradiction detection

### For Researchers
- Pattern detection in large text corpora
- Multi-phase text archive building
- Hidden practice identification

## 📁 Repository Structure

```
The-revival-of-the-word/
├── 00_Tools_And_Sources/
│   ├── ancient-hebrew-lexicon/      # 8,674 entries
│   ├── koine-greek-lexicon/         # 5,523 entries
│   ├── latin-lexicon/               # 657 entries
│   ├── syriac-lexicon/              # 268 entries
│   ├── old-georgian-lexicon/        # 309 entries
│   ├── aramaic-lexicon/             # 149 entries
│   ├── coptic-lexicon/              # 148 entries
│   ├── geez-lexicon/                # 162 entries
│   ├── narrative-analyzer/          # Forensic tools
│   │   ├── enhanced_narrative_analyzer.py
│   │   ├── multi_phase_processor.py
│   │   └── pattern_detection_suite.py
│   └── cross-reference-lookup/        # Multi-language search
│       ├── cross_reference_lookup.py
│       └── quick_lookup.py
├── README.md
└── LICENSE
```

## 🎓 Academic References

### Hebrew
- Strong's Concordance (H-numbers)
- Westminster Leningrad Codex (WLC)
- OpenScriptures Hebrew Bible

### Greek
- Strong's Greek Concordance (G-numbers)
- Nestle-Aland Novum Testamentum Graece
- SBL Greek New Testament

### Other Languages
- Payne Smith's Thesaurus Syriacus
- K'ik'vadze's Old Georgian Dictionary
- Crum's Coptic Dictionary
- Dillmann's Lexicon Linguae Aethiopicae

## 🤝 Contributing

This is a research project. Contributions welcome:
- Additional ancient languages
- Enhanced pattern detection algorithms
- UI/visualization tools
- Academic peer review

## ⚖️ License

MIT License - See LICENSE file

## 🙏 Acknowledgments

- Strong's Concordance system for Hebrew/Greek
- The Peshitta Institute for Syriac texts
- Ethiopian Orthodox Church for Ge'ez canon
- Georgian National Academy for Old Georgian texts
- Coptic Orthodox Church for Coptic tradition

---

**Built for forensic truth detection and ancient biblical research**

*Total: 15,890 entries across 8 languages | 13 research tools | 4 language families*
