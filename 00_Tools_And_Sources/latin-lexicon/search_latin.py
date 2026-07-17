#!/usr/bin/env python3
"""
Latin Lexicon Search Tool
"""
import json
import sys
from pathlib import Path

def load_lexicon():
    """Load the Latin lexicon"""
    lexicon_file = Path(__file__).parent / "latin_lexicon.json"
    
    if not lexicon_file.exists():
        print(f"[!] Lexicon not found: {lexicon_file}")
        print("Run latin_lexicon_builder.py first.")
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
        elif 'root' in entry and query_lower in entry['root'].lower():
            match = True
        
        if match:
            results.append((word, entry))
    
    return results

def display_entry(word, entry):
    """Format and display an entry"""
    print(f"\n{'='*60}")
    print(f"Latin: {word}")
    print(f"{'='*60}")
    print(f"\nTransliteration: {entry['transliteration']}")
    print(f"Part of Speech: {entry['part_of_speech']}")
    print(f"\nDefinition: {entry['definition']}")
    
    if 'declension' in entry:
        print(f"\nDeclension: {entry['declension']}")
    if 'conjugation' in entry:
        print(f"Conjugation: {entry['conjugation']}")
    if 'gender' in entry:
        print(f"Gender: {entry['gender']}")
    if 'root' in entry:
        print(f"Root: {entry['root']}")
    
    print(f"{'='*60}")

def main():
    if len(sys.argv) < 2:
        print("Latin Lexicon Search")
        print("Usage: python search_latin.py <search_term>")
        print()
        print("Examples:")
        print("  python search_latin.py God")
        print("  python search_latin.py love")
        print("  python search_latin.py Deus")
        print("  python search_latin.py caritas")
        sys.exit(0)
    
    query = sys.argv[1]
    
    print(f"Loading lexicon...")
    data = load_lexicon()
    
    print(f"Searching for: '{query}'...")
    results = search_lexicon(data, query)
    
    if not results:
        print(f"\n[!] No results found for '{query}'")
        print("\nTips:")
        print("  - Try Latin words (Deus, caritas, veritas)")
        print("  - Search by English meaning (God, love, truth)")
        print("  - Try root forms")
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
