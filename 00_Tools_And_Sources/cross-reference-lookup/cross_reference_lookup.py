#!/usr/bin/env python3
"""
Cross-Reference Lookup Tool
Search across all 8 ancient biblical languages simultaneously
Hebrew, Greek, Latin, Syriac, Old Georgian, Aramaic, Coptic, Ge'ez
"""
import json
import sys
from pathlib import Path
from collections import defaultdict

# Base directory for all lexicons
BASE_DIR = Path(__file__).parent.parent

LANGUAGE_CONFIG = {
    "hebrew": {
        "name": "Ancient Hebrew",
        "script": "Hebrew",
        "family": "Semitic",
        "period": "1000 BCE-70 CE",
        "file": "ancient-hebrew-lexicon/hebrew_lexicon.json",
        "search_key": "word",
        "color": "\033[38;5;196m",  # Red
    },
    "greek": {
        "name": "Koine Greek",
        "script": "Greek",
        "family": "Indo-European",
        "period": "300 BCE-300 CE",
        "file": "koine-greek-lexicon/greek_lexicon.json",
        "search_key": "word",
        "color": "\033[38;5;33m",   # Blue
    },
    "latin": {
        "name": "Latin",
        "script": "Latin",
        "family": "Indo-European",
        "period": "100 BCE-present",
        "file": "latin-lexicon/latin_lexicon.json",
        "search_key": "word",
        "color": "\033[38;5;208m",  # Orange
    },
    "syriac": {
        "name": "Syriac",
        "script": "Syriac",
        "family": "Semitic",
        "period": "200-700 CE",
        "file": "syriac-lexicon/syriac_lexicon.json",
        "search_key": "word",
        "color": "\033[38;5;93m",   # Purple
    },
    "georgian": {
        "name": "Old Georgian",
        "script": "Georgian",
        "family": "Kartvelian",
        "period": "5th-11th c. CE",
        "file": "old-georgian-lexicon/old_georgian_lexicon.json",
        "search_key": "word",
        "color": "\033[38;5;28m",   # Green
    },
    "aramaic": {
        "name": "Aramaic",
        "script": "Aramaic",
        "family": "Semitic",
        "period": "600 BCE-30 CE",
        "file": "aramaic-lexicon/aramaic_lexicon.json",
        "search_key": "word",
        "color": "\033[38;5;130m",  # Brown
    },
    "coptic": {
        "name": "Coptic",
        "script": "Coptic",
        "family": "Afro-Asiatic",
        "period": "100-800 CE",
        "file": "coptic-lexicon/coptic_lexicon.json",
        "search_key": "word",
        "color": "\033[38;5;214m",  # Gold
    },
    "geez": {
        "name": "Ge'ez",
        "script": "Ge'ez",
        "family": "Semitic",
        "period": "100-900 CE",
        "file": "geez-lexicon/geez_lexicon.json",
        "search_key": "word",
        "color": "\033[38;5;88m",    # Dark red
    },
}

RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

class CrossReferenceLookup:
    def __init__(self):
        self.lexicons = {}
        self.translation_map = {}
        self._build_translation_map()
        
    def load_lexicon(self, lang_code):
        """Load a lexicon file"""
        config = LANGUAGE_CONFIG[lang_code]
        file_path = BASE_DIR / config["file"]
        
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('entries', data)  # Handle both formats
        except Exception as e:
            print(f"Error loading {lang_code}: {e}")
            return None
    
    def load_all(self):
        """Load all available lexicons"""
        print("[*] Loading lexicons...")
        total = 0
        for lang_code, config in LANGUAGE_CONFIG.items():
            entries = self.load_lexicon(lang_code)
            if entries:
                self.lexicons[lang_code] = entries
                count = len(entries)
                total += count
                print(f"    [+] {config['name']}: {count} entries")
            else:
                print(f"    [!] {config['name']}: NOT FOUND")
        print(f"\n    [+] Total loaded: {total} entries across {len(self.lexicons)} languages\n")
    
    def _build_translation_map(self):
        """Build map of common biblical terms across languages"""
        # Key biblical concepts mapped across languages
        self.translation_map = {
            "god": {
                "hebrew": ["אֱלֹהִים", "אֵל", "אֱלוֹהַּ"],
                "greek": ["θεός"],
                "latin": ["Deus"],
                "syriac": ["ܐܠܗܐ"],
                "georgian": ["ღმერთი"],
                "aramaic": ["אֱלָהָא"],
                "coptic": ["ⲛⲟⲩⲧⲉ"],
                "geez": ["አምላክ", "እግዚአብሔር"],
            },
            "lord": {
                "hebrew": ["יְהֹוָה", "אֲדֹנָי", "אָדוֹן"],
                "greek": ["κύριος"],
                "latin": ["Dominus"],
                "syriac": ["ܡܪܝܐ"],
                "georgian": ["უფალი"],
                "aramaic": ["מָרֵא", "אֲדֹנָי"],
                "coptic": ["ⲕⲩⲣⲓⲟⲥ"],
                "geez": ["እግዚአብሔር", "ጌታ"],
            },
            "jesus": {
                "hebrew": ["יֵשׁוּעַ"],
                "greek": ["Ἰησοῦς"],
                "latin": ["Iesus"],
                "syriac": ["ܝܫܘܥ"],
                "georgian": ["იესუ"],
                "aramaic": ["יֵשׁוּעַ", "יֵשׁוּ"],
                "coptic": ["ⲓⲏⲥⲟⲩⲥ"],
                "geez": ["ኢየሱስ"],
            },
            "christ": {
                "hebrew": ["מָשִׁיחַ"],
                "greek": ["Χριστός"],
                "latin": ["Christus"],
                "syriac": ["ܡܫܝܚܐ"],
                "georgian": ["ქრისტე"],
                "aramaic": ["מְשִׁיחָא"],
                "coptic": ["ⲭⲣⲓⲥⲧⲟⲥ"],
                "geez": ["ክርስቶስ"],
            },
            "spirit": {
                "hebrew": ["רוּחַ"],
                "greek": ["πνεῦμα"],
                "latin": ["Spiritus"],
                "syriac": ["ܪܘܚܐ"],
                "georgian": ["სული"],
                "aramaic": ["רוּחַ"],
                "coptic": ["ⲡⲛⲉⲩⲙⲁ"],
                "geez": ["መንፈስ"],
            },
            "father": {
                "hebrew": ["אָב"],
                "greek": ["πατήρ"],
                "latin": ["Pater"],
                "syriac": ["ܐܒܐ"],
                "georgian": ["მამა"],
                "aramaic": ["אֲבָא", "אַבָּא"],
                "coptic": ["ⲉⲓⲱⲧ"],
                "geez": ["አብ", "አባ"],
            },
            "son": {
                "hebrew": ["בֵּן"],
                "greek": ["υἱός"],
                "latin": ["Filius"],
                "syriac": ["ܒܪܐ"],
                "georgian": ["ძე"],
                "aramaic": ["בַּר"],
                "coptic": ["ϣⲏⲣⲓ"],
                "geez": ["ወልድ"],
            },
            "peace": {
                "hebrew": ["שָׁלוֹם"],
                "greek": ["εἰρήνη"],
                "latin": ["pax"],
                "syriac": ["ܫܠܡܐ"],
                "georgian": ["მშვიდობა"],
                "aramaic": ["שְׁלָם"],
                "coptic": ["ϩⲓⲣⲏⲛⲏ"],
                "geez": ["ሰላም"],
            },
            "love": {
                "hebrew": ["אַהֲבָה", "אָהַב"],
                "greek": ["ἀγάπη", "φιλέω", "ἔρως"],
                "latin": ["caritas", "amor"],
                "syriac": ["ܚܘܒܐ"],
                "georgian": ["სიყვარული"],
                "aramaic": ["רַחֲמִין"],
                "coptic": ["ⲁⲅⲁⲡⲏ"],
                "geez": ["ፍቅር"],
            },
            "truth": {
                "hebrew": ["אֱמֶת"],
                "greek": ["ἀλήθεια"],
                "latin": ["veritas"],
                "syriac": ["ܫܪܝܪܐ"],
                "georgian": ["ჭეშმარიტება"],
                "aramaic": ["שְׁרָרָה", "קְשׁוֹט"],
                "coptic": ["ⲙⲉ"],
                "geez": ["ጥብቅ", "ጤና"],
            },
            "king": {
                "hebrew": ["מֶלֶךְ"],
                "greek": ["βασιλεύς"],
                "latin": ["Rex"],
                "syriac": ["ܡܠܟܐ"],
                "georgian": ["მეფე"],
                "aramaic": ["מַלְכָּא"],
                "coptic": ["ⲣⲣⲟ"],
                "geez": ["ንጉሥ"],
            },
            "holy": {
                "hebrew": ["קָדוֹשׁ"],
                "greek": ["ἅγιος"],
                "latin": ["sanctus"],
                "syriac": ["ܩܕܝܫܐ"],
                "georgian": ["წმიდა"],
                "aramaic": ["קַדִּישׁ"],
                "coptic": ["ⲉⲑⲟⲩⲁⲃ"],
                "geez": ["ቅዱስ"],
            },
            "sin": {
                "hebrew": ["חַטָּאת", "עָוֹן"],
                "greek": ["ἁμαρτία"],
                "latin": ["peccatum"],
                "syriac": ["ܚܛܝܬܐ"],
                "georgian": ["ცოდვა"],
                "aramaic": ["חֲטָאָה"],
                "coptic": ["ⲛⲟⲃⲉ"],
                "geez": ["ኀጢአት"],
            },
            "salvation": {
                "hebrew": ["יְשׁוּעָה"],
                "greek": ["σωτηρία"],
                "latin": ["salus"],
                "syriac": ["ܥܘܕܪܢܐ"],
                "georgian": ["მიხსნელობა"],
                "aramaic": ["פּוּרְקָן"],
                "coptic": ["ϥⲱⲧⲉ"],
                "geez": ["መድኀኒት"],
            },
            "resurrection": {
                "hebrew": ["תְּחִיָּה"],
                "greek": ["ἀνάστασις"],
                "latin": ["resurrectio"],
                "syriac": ["ܩܝܡܐ"],
                "georgian": ["განკვდომა"],
                "aramaic": ["אֲתָה"],
                "coptic": ["ⲁⲛⲁⲥⲧⲁⲥⲓⲥ"],
                "geez": ["ትንሣኤ"],
            },
        }
    
    def search(self, query, languages=None):
        """Search across all loaded languages"""
        if languages is None:
            languages = list(self.lexicons.keys())
        
        results = {}
        query_lower = query.lower()
        
        for lang_code in languages:
            if lang_code not in self.lexicons:
                continue
            
            lexicon = self.lexicons[lang_code]
            lang_results = []
            
            for word, entry in lexicon.items():
                match = False
                
                # Check word itself
                if query_lower in word.lower():
                    match = True
                # Check definition
                elif 'definition' in entry and query_lower in entry['definition'].lower():
                    match = True
                # Check transliteration
                elif 'transliteration' in entry and query_lower in entry['transliteration'].lower():
                    match = True
                # Check root
                elif 'root' in entry and query_lower in entry['root'].lower():
                    match = True
                
                if match:
                    lang_results.append((word, entry))
            
            if lang_results:
                results[lang_code] = lang_results
        
        return results
    
    def get_cross_references(self, concept):
        """Get translations of a concept across all languages"""
        concept_lower = concept.lower()
        
        # Check if concept is in our predefined map
        matches = {}
        for key, translations in self.translation_map.items():
            if concept_lower in key or key in concept_lower:
                matches[key] = translations
        
        return matches
    
    def display_results(self, query, results):
        """Display search results in a formatted way"""
        print(f"\n{'='*80}")
        print(f"CROSS-LANGUAGE SEARCH RESULTS: '{query}'")
        print(f"{'='*80}\n")
        
        total_matches = sum(len(r) for r in results.values())
        print(f"Found {total_matches} matches across {len(results)} languages\n")
        
        for lang_code in LANGUAGE_CONFIG.keys():
            if lang_code not in results:
                continue
            
            config = LANGUAGE_CONFIG[lang_code]
            lang_results = results[lang_code]
            
            print(f"{config['color']}{BOLD}{UNDERLINE}{config['name']}{RESET}")
            print(f"{config['color']}  Script: {config['script']} | Family: {config['family']} | Period: {config['period']}{RESET}\n")
            
            # Show top 10 results
            for i, (word, entry) in enumerate(lang_results[:10], 1):
                trans = entry.get('transliteration', '')
                pos = entry.get('part_of_speech', '')
                definition = entry.get('definition', '')
                
                print(f"  {i}. {config['color']}{BOLD}{word}{RESET}", end="")
                if trans:
                    print(f" ({trans})", end="")
                print()
                
                if pos:
                    print(f"     [{pos}]", end="")
                if definition:
                    print(f" {definition[:60]}", end="")
                    if len(definition) > 60:
                        print("...", end="")
                print()
                
                # Show root if available
                if 'root' in entry:
                    print(f"     Root: {entry['root']}")
                
                # Show strongs if available
                if 'strongs' in entry:
                    print(f"     Strong's: {entry['strongs']}")
                
                print()
            
            if len(lang_results) > 10:
                print(f"  ... and {len(lang_results) - 10} more results")
            
            print()
    
    def display_cross_references(self, concept):
        """Display cross-language translations of a concept"""
        refs = self.get_cross_references(concept)
        
        if not refs:
            print(f"\n[!] No predefined cross-references found for '{concept}'")
            print("Try searching the lexicons directly with: cross_ref_lookup.py <word>")
            return
        
        for concept_key, translations in refs.items():
            print(f"\n{'='*80}")
            print(f"CROSS-REFERENCE: {concept_key.upper()}")
            print(f"{'='*80}\n")
            
            for lang_code, words in translations.items():
                if lang_code in LANGUAGE_CONFIG:
                    config = LANGUAGE_CONFIG[lang_code]
                    print(f"{config['color']}{BOLD}{config['name']}{RESET}")
                    for word in words:
                        print(f"  {word}")
                    print()
    
    def show_statistics(self):
        """Display statistics about all loaded lexicons"""
        print(f"\n{'='*80}")
        print("ANCIENT LANGUAGE LEXICON STATISTICS")
        print(f"{'='*80}\n")
        
        total = 0
        print(f"{'Language':<20} {'Family':<18} {'Entries':<10} {'Period':<25}")
        print("-" * 80)
        
        for lang_code, config in LANGUAGE_CONFIG.items():
            if lang_code in self.lexicons:
                count = len(self.lexicons[lang_code])
                total += count
                color = config['color']
                print(f"{color}{config['name']:<20}{RESET} {config['family']:<18} {count:<10} {config['period']:<25}")
        
        print("-" * 80)
        print(f"{'TOTAL':<20} {'':<18} {BOLD}{total:<10}{RESET}")
        print(f"\nLanguages loaded: {len(self.lexicons)}")
        print(f"Total entries: {total:,}\n")
        
        # Language families
        families = defaultdict(int)
        for lang_code in self.lexicons.keys():
            families[LANGUAGE_CONFIG[lang_code]['family']] += len(self.lexicons[lang_code])
        
        print("\nBy Language Family:")
        for family, count in sorted(families.items(), key=lambda x: x[1], reverse=True):
            print(f"  {family}: {count:,} entries")


def print_help():
    """Print usage help"""
    print("""
Cross-Reference Lookup Tool
Search across 8 ancient biblical languages simultaneously

USAGE:
    python cross_reference_lookup.py <search_term> [options]
    
EXAMPLES:
    # Search for "God" across all languages
    python cross_reference_lookup.py God
    
    # Search in specific languages only
    python cross_reference_lookup.py God --langs hebrew,greek
    
    # Show cross-references for a concept
    python cross_reference_lookup.py --xref god
    
    # Show statistics
    python cross_reference_lookup.py --stats
    
    # Show help
    python cross_reference_lookup.py --help

AVAILABLE CONCEPTS FOR --xref:
    god, lord, jesus, christ, spirit, father, son, peace,
    love, truth, king, holy, sin, salvation, resurrection

SUPPORTED LANGUAGES:
    hebrew      - Ancient Hebrew (8,674 entries)
    greek       - Koine Greek (5,523 entries)
    latin       - Classical/Ecclesiastical Latin (657 entries)
    syriac      - Syriac/Peshitta (268 entries)
    georgian    - Old Georgian (309 entries)
    aramaic     - Biblical Aramaic (149 entries)
    coptic      - Sahidic Coptic (148 entries)
    geez        - Classical Ge'ez (162 entries)
""")


def main():
    # Parse arguments
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help', 'help']:
        print_help()
        sys.exit(0)
    
    if sys.argv[1] == '--stats':
        lookup = CrossReferenceLookup()
        lookup.load_all()
        lookup.show_statistics()
        sys.exit(0)
    
    if sys.argv[1] == '--xref' and len(sys.argv) > 2:
        lookup = CrossReferenceLookup()
        lookup.load_all()
        lookup.display_cross_references(sys.argv[2])
        sys.exit(0)
    
    # Regular search
    query = sys.argv[1]
    
    # Check for language filter
    languages = None
    if '--langs' in sys.argv:
        idx = sys.argv.index('--langs')
        if idx + 1 < len(sys.argv):
            languages = sys.argv[idx + 1].split(',')
    
    # Initialize and load
    lookup = CrossReferenceLookup()
    lookup.load_all()
    
    # Perform search
    results = lookup.search(query, languages)
    
    if results:
        lookup.display_results(query, results)
    else:
        print(f"\n[!] No results found for '{query}'")
        print("\nTips:")
        print("  - Try English glosses (God, love, peace)")
        print("  - Try transliterations (Elohim, agape, shalom)")
        print("  - Try native scripts (אֱלֹהִים, θεός, ܐܠܗܐ)")
        print("  - Use --xref <concept> for known biblical terms")
        print("  - Use --langs <list> to search specific languages")


if __name__ == "__main__":
    main()
