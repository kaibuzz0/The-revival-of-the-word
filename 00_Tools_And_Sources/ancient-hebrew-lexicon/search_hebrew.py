#!/usr/bin/env python3
"""
Ancient Hebrew Lexicon Search Tool
Quick lookup for Hebrew words
"""
import json
import re
import sys
from pathlib import Path

def load_lexicon():
    """Load the Hebrew lexicon"""
    lexicon_file = Path(__file__).parent / "hebrew_lexicon.json"
    
    if not lexicon_file.exists():
        print(f"[!] Lexicon not found: {lexicon_file}")
        print("Run build_lexicon.py first to generate the lexicon.")
        sys.exit(1)
    
    with open(lexicon_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def search_lexicon(lexicon, query):
    """Search for words"""
    results = []
    query_clean = query.lower().strip()
    
    for strongs, entry in lexicon['entries'].items():
        match = False
        
        # Check Strong's number (H3068, h3068, 3068)
        if re.match(r'^h?\d+$', query_clean):
            strong_num = re.sub(r'[^0-9]', '', query_clean)
            if strongs == f"H{strong_num}" or strongs == query_clean.upper():
                match = True
        # Check various fields
        elif query_clean in entry.get('lemma', '').lower():
            match = True
        elif query_clean in entry.get('strongs_def', '').lower():
            match = True
        elif query_clean in entry.get('kjv_def', '').lower():
            match = True
        elif query_clean in entry.get('xlit', '').lower():
            match = True
        elif query in entry.get('lemma', ''):  # Exact Hebrew match
            match = True
        
        if match:
            results.append((strongs, entry))
    
    return results

def display_entry(entry):
    """Format and display an entry"""
    print(f"\n{'='*60}")
    print(f"Strong's {entry.get('strongs', 'N/A')}")
    print(f"{'='*60}")
    
    # Hebrew
    if 'lemma' in entry:
        print(f"\nHebrew: {entry['lemma']}")
    
    # Transliteration
    if 'xlit' in entry:
        print(f"Transliteration: {entry['xlit']}")
    
    # Pronunciation
    if 'pron' in entry:
        print(f"Pronunciation: /{entry['pron']}/")
    
    # Definition
    if 'strongs_def' in entry:
        print(f"\nDefinition: {entry['strongs_def']}")
    
    # KJV equivalents
    if 'kjv_def' in entry:
        print(f"\nKJV Usage: {entry['kjv_def']}")
    
    # Etymology
    if 'derivation' in entry:
        print(f"\nEtymology: {entry['derivation']}")
    
    print(f"{'='*60}")

def main():
    if len(sys.argv) < 2:
        print("Ancient Hebrew Lexicon Search")
        print("Usage: python search_hebrew.py <search_term>")
        print()
        print("Examples:")
        print("  python search_hebrew.py love")
        print("  python search_hebrew.py אָב")
        print("  python search_hebrew.py H1")
        print("  python search_hebrew.py ab")
        sys.exit(0)
    
    query = sys.argv[1]
    
    print(f"Loading lexicon...")
    data = load_lexicon()
    
    print(f"Searching for: '{query}'...")
    results = search_lexicon(data, query)
    
    if not results:
        print(f"\n[!] No results found for '{query}'")
        print("\nTips:")
        print("  - Try searching for partial words")
        print("  - Use Strong's number (H1, H430, etc.)")
        print("  - Try Hebrew characters (א, ב, ג, etc.)")
        sys.exit(0)
    
    print(f"\nFound {len(results)} result(s):")
    
    if len(results) == 1:
        display_entry(results[0][1])
    else:
        print("\nMultiple matches found. Showing summary:")
        print("-" * 60)
        for i, (strongs, entry) in enumerate(results[:20], 1):
            lemma = entry.get('lemma', 'N/A')
            sdef = entry.get('strongs_def', 'N/A')[:60]
            print(f"{i}. {strongs}: {lemma}")
            print(f"   {sdef}...")
            print()
            
        if len(results) > 20:
            print(f"... and {len(results) - 20} more results")
            
        # Auto-display first result in non-interactive mode
        print("\nShowing full entry for first result:")
        display_entry(results[0][1])

if __name__ == "__main__":
    main()
