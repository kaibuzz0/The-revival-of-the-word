#!/usr/bin/env python3
"""
Ancient Biblical Language Translator
Translate between 8 ancient languages using the lexicon database
Hebrew, Aramaic, Greek, Latin, Syriac, Coptic, Ge'ez, Old Georgian
"""

import json
from pathlib import Path
from collections import defaultdict

class AncientTranslator:
    """Multi-language biblical translator"""
    
    LANGUAGES = ['hebrew', 'aramaic', 'greek', 'latin', 'syriac', 
                 'coptic', 'geez', 'old_georgian']
    
    def __init__(self):
        self.lexicons = {}
        self.translation_map = defaultdict(dict)
        self._load_all_lexicons()
        
    def _load_all_lexicons(self):
        """Load all 8 language lexicons"""
        base = Path(__file__).parent.parent
        
        lexicon_files = {
            'hebrew': 'ancient-hebrew-lexicon/hebrew_lexicon.json',
            'aramaic': 'aramaic-lexicon/aramaic_lexicon.json',
            'greek': 'koine-greek-lexicon/greek_lexicon.json',
            'latin': 'latin-lexicon/latin_lexicon.json',
            'syriac': 'syriac-lexicon/syriac_lexicon.json',
            'coptic': 'coptic-lexicon/coptic_lexicon.json',
            'geez': 'geez-lexicon/geez_lexicon.json',
            'old_georgian': 'old-georgian-lexicon/old_georgian_lexicon.json'
        }
        
        for lang, filepath in lexicon_files.items():
            full_path = base / filepath
            if full_path.exists():
                with open(full_path, 'r', encoding='utf-8') as f:
                    self.lexicons[lang] = json.load(f)
                    
    def translate_word(self, word, from_lang, to_lang):
        """Translate a single word between languages"""
        if from_lang not in self.lexicons or to_lang not in self.lexicons:
            return None
            
        # Find English gloss for source word
        english = None
        for entry in self.lexicons[from_lang].values():
            if entry.get('word') == word or entry.get('transliteration') == word:
                english = entry.get('gloss', '').lower()
                break
                
        if not english:
            return None
            
        # Find target language word for that gloss
        for entry in self.lexicons[to_lang].values():
            if entry.get('gloss', '').lower() == english:
                return {
                    'word': entry.get('word'),
                    'transliteration': entry.get('transliteration'),
                    'gloss': entry.get('gloss'),
                    'english_bridge': english
                }
                
        return None
        
    def get_word_info(self, word, lang):
        """Get full information about a word"""
        if lang not in self.lexicons:
            return None
            
        for entry in self.lexicons[lang].values():
            if entry.get('word') == word or entry.get('transliteration') == word:
                return entry
        return None
        
    def search_by_gloss(self, gloss, lang=None):
        """Search for words by English gloss"""
        results = []
        languages = [lang] if lang else self.LANGUAGES
        
        for l in languages:
            if l not in self.lexicons:
                continue
            for entry in self.lexicons[l].values():
                if gloss.lower() in entry.get('gloss', '').lower():
                    results.append({
                        'language': l,
                        'word': entry.get('word'),
                        'transliteration': entry.get('transliteration'),
                        'gloss': entry.get('gloss')
                    })
        return results
        
    def show_parallel(self, gloss):
        """Show how a concept appears in all 8 languages"""
        results = self.search_by_gloss(gloss)
        
        print(f"\n{'='*60}")
        print(f"  PARALLEL TRANSLATION: '{gloss.upper()}'")
        print(f"{'='*60}\n")
        
        for lang in self.LANGUAGES:
            lang_words = [r for r in results if r['language'] == lang]
            if lang_words:
                print(f"{lang.upper():15} {lang_words[0]['word']:20} ({lang_words[0]['transliteration']})")
            else:
                print(f"{lang.upper():15} [not found]")
                
        return results


def main():
    """CLI demo"""
    import sys
    
    t = AncientTranslator()
    
    if len(sys.argv) < 2:
        print("Usage: python3 translator.py <command>")
        print("\nCommands:")
        print("  parallel <word>     Show word in all 8 languages")
        print("  translate <word> <from> <to>  Translate word")
        print("  search <gloss>        Search by English gloss")
        print("\nExamples:")
        print("  python3 translator.py parallel god")
        print("  python3 translator.py translate אֱלֹהִים hebrew greek")
        print("  python3 translator.py search love")
        sys.exit(0)
        
    cmd = sys.argv[1]
    
    if cmd == 'parallel':
        word = sys.argv[2] if len(sys.argv) > 2 else 'god'
        t.show_parallel(word)
        
    elif cmd == 'translate':
        if len(sys.argv) < 5:
            print("Usage: translate <word> <from> <to>")
            sys.exit(1)
        word, from_lang, to_lang = sys.argv[2:5]
        result = t.translate_word(word, from_lang, to_lang)
        if result:
            print(f"{word} ({from_lang}) → {result['word']} ({to_lang})")
            print(f"  Transliteration: {result['transliteration']}")
            print(f"  Gloss: {result['gloss']}")
        else:
            print(f"Translation not found for '{word}'")
            
    elif cmd == 'search':
        gloss = sys.argv[2] if len(sys.argv) > 2 else 'love'
        results = t.search_by_gloss(gloss)
        print(f"\nFound {len(results)} matches for '{gloss}':")
        for r in results:
            print(f"  {r['language']:12} {r['word']:20} = {r['gloss']}")
    
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
