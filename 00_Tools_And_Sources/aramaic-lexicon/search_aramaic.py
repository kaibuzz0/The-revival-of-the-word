#!/usr/bin/env python3
"""
Aramaic Lexicon Search Tool
"""
import json
import sys
from pathlib import Path

def load_lexicon():
    """Load the Aramaic lexicon"""
    lexicon_file = Path(__file__).parent / "aramaic_lexicon.json"
    
    if not lexicon_file.exists():
        print(f"[!] Lexicon not found: {lexicon_file}")
        print("Run aramaic_lexicon_builder.py first.")
        sys.exit(1)
    
    with open(lexicon_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def search_lexicon(lexicon, query):
    """Search for words"""
    results = []
    query_lower = query.lower()
    
    for word, entry in lexicon['entries'].items():
        match = False
        
        if query_lower in word.lower():
            match = True
        elif query_lower in entry['definition'].lower():
            match = True
        elif query_lower in entry['transliteration'].lower():
            match = True
        elif query_lower in entry['root'].lower():
            match = True
        
        if match:
            results.append((word, entry))
    
    return results

def display_entry(word, entry):
    """Format and display an entry"""
    print(f"\n{'='*60}")
    print(f"Aramaic: {word}")
    print(f"{'='*60}")
    print(f"\nTransliteration: {entry['transliteration']}")
    print(f"Part of Speech: {entry['part_of_speech']}")
    print(f"\nDefinition: {entry['definition']}")
    print(f"\nRoot: {entry['root']}")
    if 'note' in entry:
        print(f"\nNote: {entry['note']}")
    print(f"{'='*60}")

def main():
    if len(sys.argv) < 2:
        print("Aramaic Lexicon Search")
        print("Usage: python search_aramaic.py <search_term>")
        print()
        print("Examples:")
        print("  python search_aramaic.py God")
        print("  python search_aramaic.py father")
        print("  python search_aramaic.py Abba")
        print("  python search_aramaic.py אֱלָהָא")
        sys.exit(0)
    
    query = sys.argv[1]
    
    print(f"Loading lexicon...")
    data = load_lexicon()
    
    print(f"Searching for: '{query}'...")
    results = search_lexicon(data, query)
    
    if not results:
        print(f"\n[!] No results found for '{query}'")
        print("\nTips:")
        print("  - Try Aramaic/Hebrew characters (א, ב, ג, etc.)")
        print("  - Try transliteration (Elaha, Abba, Malkuta)")
        print("  - Search by root (ʾ-l-h, m-l-k, etc.)")
        print("  - Search by English meaning (God, kingdom, hear)")
        sys.exit(0)
    
    print(f"\nFound {len(results)} result(s):")
    
    if len(results) == 1:
        display_entry(results[0][0], results[0][1])
    else:
        print("\nMultiple matches found:")
        print("-" * 60)
        for i, (word, entry) in enumerate(results[:20], 1):
            print(f"{i}. {word} ({entry['transliteration']})")
            print(f"   {entry['definition'][:50]}...")
            print()
        
        if len(results) > 20:
            print(f"... and {len(results) - 20} more results")
        
        # Show first result
        print("\nShowing first result:")
        display_entry(results[0][0], results[0][1])

if __name__ == "__main__":
    main()
