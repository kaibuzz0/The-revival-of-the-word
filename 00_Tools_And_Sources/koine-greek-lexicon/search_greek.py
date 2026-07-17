#!/usr/bin/env python3
"""
Koine Greek Lexicon Search Tool
"""
import json
import re
import sys
from pathlib import Path

def load_lexicon():
    """Load the Greek lexicon"""
    lexicon_file = Path(__file__).parent / "greek_lexicon.json"
    
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
        
        # Check Strong's number (G25, g25, 25)
        if re.match(r'^g?\d+$', query_clean):
            strong_num = re.sub(r'[^0-9]', '', query_clean)
            if strongs == f"G{strong_num}" or strongs == query_clean.upper():
                match = True
        # Check various fields
        elif query_clean in entry.get('lemma', '').lower():
            match = True
        elif query_clean in entry.get('strongs_def', '').lower():
            match = True
        elif query_clean in entry.get('kjv_def', '').lower():
            match = True
        elif query_clean in entry.get('translit', '').lower():
            match = True
        elif query in entry.get('lemma', ''):  # Exact Greek match
            match = True
        
        if match:
            results.append((strongs, entry))
    
    return results

def display_entry(entry):
    """Format and display an entry"""
    print(f"\n{'='*60}")
    print(f"Strong's {entry.get('strongs', 'N/A')}")
    print(f"{'='*60}")
    
    # Greek
    if 'lemma' in entry:
        print(f"\nGreek: {entry['lemma']}")
    
    # Transliteration
    if 'translit' in entry:
        print(f"Transliteration: {entry['translit']}")
    
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
        print("Koine Greek Lexicon Search")
        print("Usage: python search_greek.py <search_term>")
        print()
        print("Examples:")
        print("  python search_greek.py love")
        print("  python search_greek.py ἀγάπη")
        print("  python search_greek.py G25")
        print("  python search_greek.py agape")
        sys.exit(0)
    
    query = sys.argv[1]
    
    print(f"Loading lexicon...")
    data = load_lexicon()
    
    print(f"Searching for: '{query}'...")
    results = search_lexicon(data, query)
    
    if not results:
        print(f"\n[!] No results found for '{query}'")
        print("\nTips:")
        print("  - Try Greek characters (ἀ, β, γ, etc.)")
        print("  - Use Strong's number (G1, G26, G2424, etc.)")
        print("  - Try transliteration (agape, logos, christos)")
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
        
        # Auto-display first result
        print("\nShowing full entry for first result:")
        display_entry(results[0][1])

if __name__ == "__main__":
    main()
