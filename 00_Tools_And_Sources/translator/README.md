# Ancient Biblical Language Translator

Translate between 8 ancient biblical languages using the lexicon database.

## Supported Languages

| Language | Code | Script |
|----------|------|--------|
| Ancient Hebrew | `hebrew` | Hebrew |
| Biblical Aramaic | `aramaic` | Hebrew/Aramaic |
| Koine Greek | `greek` | Greek |
| Classical Latin | `latin` | Latin |
| Classical Syriac | `syriac` | Syriac |
| Sahidic Coptic | `coptic` | Coptic |
| Classical Ge'ez | `geez` | Ge'ez |
| Old Georgian | `old_georgian` | Georgian |

## Usage

### Show Word in All Languages
```bash
python3 translator.py parallel god
```

### Translate Single Word
```bash
python3 translator.py translate אֱלֹהִים hebrew greek
```

### Search by English Gloss
```bash
python3 translator.py search love
```

## Examples

```bash
# See how "god" appears in all 8 languages
python3 translator.py parallel god

# Translate Hebrew word to Greek
python3 translator.py translate שָׁלוֹם hebrew greek

# Find all words meaning "love"
python3 translator.py search love
```

## API

```python
from translator import AncientTranslator

t = AncientTranslator()

# Translate word
result = t.translate_word('אֱלֹהִים', 'hebrew', 'greek')
print(result['word'])  # θεός

# Get word info
info = t.get_word_info('θεός', 'greek')

# Search by gloss
matches = t.search_by_gloss('love', 'hebrew')
```

## Dependencies

Uses the lexicon JSON files from:
- `../ancient-hebrew-lexicon/`
- `../aramaic-lexicon/`
- `../koine-greek-lexicon/`
- `../latin-lexicon/`
- `../syriac-lexicon/`
- `../coptic-lexicon/`
- `../geez-lexicon/`
- `../old-georgian-lexicon/`

---
*Part of The Revival of the Word project*
