#!/usr/bin/env python3
"""
Ancient Hebrew Lexicon Builder - Simplified Version
Builds a complete Hebrew dictionary from source files.
"""
import json
import re
import os
import csv
import sys
from pathlib import Path
from collections import defaultdict

class HebrewLexicon:
    """Complete Hebrew lexicon builder"""
    
    def __init__(self):
        self.entries = {}
        self.root_index = defaultdict(list)
        
    def load_strongs(self, filepath: str):
        """Load Strong's Hebrew dictionary"""
        print(f"[*] Loading Strong's from {filepath}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Use regex to extract all entries
        # Pattern matches "H123":{"lemma":"abc","xlit":"def",...}
        pattern = r'"(H\d+)"\s*:\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}'
        matches = re.findall(pattern, content)
        
        print(f"    Found {len(matches)} entries")
        
        for strongs_num, entry_text in matches:
            entry = self._parse_entry(entry_text)
            if entry:
                entry['strongs'] = strongs_num
                self.entries[strongs_num] = entry
                
                # Index by root
                if 'lemma' in entry:
                    root = self._extract_root(entry['lemma'])
                    self.root_index[root].append(strongs_num)
        
        print(f"    [+] Parsed {len(self.entries)} entries")
        
    def _parse_entry(self, text: str) -> dict:
        """Parse a single Strong's entry"""
        entry = {}
        
        # Extract fields using regex
        fields = {
            'lemma': r'"lemma"\s*:\s*"([^"]*)"',
            'xlit': r'"xlit"\s*:\s*"([^"]*)"',
            'pron': r'"pron"\s*:\s*"([^"]*)"',
            'strongs_def': r'"strongs_def"\s*:\s*"([^"]*)"',
            'kjv_def': r'"kjv_def"\s*:\s*"([^"]*)"',
            'derivation': r'"derivation"\s*:\s*"([^"]*)"',
        }
        
        for field, pattern in fields.items():
            match = re.search(pattern, text)
            if match:
                entry[field] = match.group(1)
        
        return entry if entry else None
    
    def _extract_root(self, lemma: str) -> str:
        """Extract consonantal root"""
        # Hebrew consonants
        consonants = ""
        for char in lemma:
            if '\u05d0' <= char <= '\u05ea':
                consonants += char
        return consonants[:3] if len(consonants) >= 3 else consonants
    
    def determine_pos(self, strongs_def: str, lemma: str) -> str:
        """Determine part of speech"""
        sdef = strongs_def.lower()
        
        if 'verb' in sdef or 'root' in sdef:
            return "verb"
        elif 'proper' in sdef or 'name' in sdef:
            return "proper noun"
        elif 'noun' in sdef:
            return "noun"
        elif 'adj' in sdef or 'num' in sdef:
            return "adjective"
        elif 'preposition' in sdef or lemma in ['ב', 'ל', 'מן', 'עד', 'על']:
            return "preposition"
        elif 'conjunction' in sdef or lemma in ['ו', 'כי', 'אם', 'אשר']:
            return "conjunction"
        elif 'pronoun' in sdef:
            return "pronoun"
        elif 'particle' in sdef:
            return "particle"
        elif 'adverb' in sdef:
            return "adverb"
        
        return "noun"  # Default
    
    def export_json(self, output_path: str):
        """Export to JSON"""
        print(f"[*] Exporting to {output_path}...")
        
        data = {
            "metadata": {
                "title": "Ancient Hebrew Lexicon",
                "period": "Second Temple Period (Biblical Hebrew)",
                "sources": ["Strong's Concordance", "OpenScriptures"],
                "total_entries": len(self.entries),
                "format": "JSON"
            },
            "entries": self.entries,
            "root_index": dict(self.root_index)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"    [+] Exported {len(self.entries)} entries")
    
    def export_markdown(self, output_path: str, limit: int = 2000):
        """Export human-readable markdown"""
        print(f"[*] Exporting markdown to {output_path}...")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Ancient Hebrew Lexicon\n\n")
            f.write("**Complete Dictionary of Biblical Hebrew**\n\n")
            f.write(f"Total Entries: {len(self.entries)}\n\n")
            f.write("---\n\n")
            
            # Sort by Strong's number
            sorted_entries = sorted(self.entries.items(), 
                key=lambda x: int(x[0][1:]))
            
            for strongs, entry in sorted_entries[:limit]:
                f.write(f"## {strongs}\n\n")
                
                if 'lemma' in entry:
                    f.write(f"**Hebrew:** {entry['lemma']}\n\n")
                
                if 'xlit' in entry:
                    f.write(f"**Transliteration:** *{entry['xlit']}*\n\n")
                
                if 'pron' in entry:
                    f.write(f"**Pronunciation:** /{entry['pron']}/\n\n")
                
                if 'strongs_def' in entry:
                    pos = self.determine_pos(entry['strongs_def'], entry.get('lemma', ''))
                    f.write(f"**Part of Speech:** {pos}\n\n")
                    f.write(f"**Definition:** {entry['strongs_def']}\n\n")
                
                if 'kjv_def' in entry:
                    f.write(f"**KJV Equivalents:** {entry['kjv_def']}\n\n")
                
                if 'derivation' in entry:
                    f.write(f"**Etymology:** {entry['derivation']}\n\n")
                
                f.write("---\n\n")
        
        print(f"    [+] Exported {min(limit, len(self.entries))} entries")
    
    def export_websters_style(self, output_path: str, limit: int = 1000):
        """Export in Webster's dictionary format"""
        print(f"[*] Exporting Webster's style to {output_path}...")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("ANCIENT HEBREW LEXICON\n")
            f.write("Complete Dictionary of Biblical Hebrew\n")
            f.write("Period: Second Temple Period (Jesus' Lifetime)\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("Pronunciation Guide:\n")
            f.write("  ' = primary stress    ˌ = secondary stress\n")
            f.write("  a as in father        e as in they\n")
            f.write("  i as in machine       o as in note\n")
            f.write("  u as in rule\n\n")
            
            f.write("-" * 70 + "\n\n")
            
            sorted_entries = sorted(self.entries.items(), 
                key=lambda x: int(x[0][1:]))
            
            for strongs, entry in sorted_entries[:limit]:
                lemma = entry.get('lemma', '')
                xlit = entry.get('xlit', '')
                pron = entry.get('pron', '')
                sdef = entry.get('strongs_def', '')
                kjv = entry.get('kjv_def', '')
                
                if not lemma:
                    continue
                
                # Main entry line
                f.write(f"\n{lemma}")
                if xlit:
                    f.write(f"  ({xlit})")
                if pron:
                    f.write(f"  /{pron}/")
                
                # Part of speech
                pos = self.determine_pos(sdef, lemma)
                f.write(f"  [{pos}]")
                f.write("\n")
                
                # Definition
                if sdef:
                    # Wrap long definitions
                    words = sdef.split()
                    lines = []
                    current = "    "
                    for word in words:
                        if len(current) + len(word) + 1 > 65:
                            lines.append(current)
                            current = "    " + word
                        else:
                            current += " " + word if current != "    " else word
                    lines.append(current)
                    f.write('\n'.join(lines) + "\n")
                
                # Usage
                if kjv:
                    # Clean up KJV equivalents
                    kjv_clean = kjv.replace('—', ', ').replace('[', '').replace(']', '')
                    if len(kjv_clean) > 100:
                        kjv_clean = kjv_clean[:100] + "..."
                    f.write(f"    Usage: {kjv_clean}\n")
                
                f.write("\n")
        
        print(f"    [+] Exported {min(limit, len(self.entries))} entries")
    
    def search(self, query: str) -> list:
        """Search the lexicon"""
        results = []
        query_lower = query.lower()
        
        for strongs, entry in self.entries.items():
            match = False
            
            if query_lower in entry.get('lemma', '').lower():
                match = True
            elif query_lower in entry.get('strongs_def', '').lower():
                match = True
            elif query_lower in entry.get('kjv_def', '').lower():
                match = True
            elif query_lower in entry.get('xlit', '').lower():
                match = True
            
            if match:
                results.append((strongs, entry))
        
        return results


def main():
    lexicon = HebrewLexicon()
    
    # Load Strong's data
    strongs_path = "/tmp/strongs/hebrew/strongs-hebrew-dictionary.js"
    lexicon.load_strongs(strongs_path)
    
    # Create output directory
    out_dir = Path("/root/hebrew_lexicon_output")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Export all formats
    lexicon.export_json(out_dir / "hebrew_lexicon.json")
    lexicon.export_markdown(out_dir / "hebrew_lexicon.md", limit=2000)
    lexicon.export_websters_style(out_dir / "websters_hebrew.txt", limit=1000)
    
    # Sample entries
    print("\n" + "=" * 70)
    print("SAMPLE ENTRIES")
    print("=" * 70 + "\n")
    
    sample_strongs = ['H1', 'H430', 'H3068', 'H853', 'H1004']
    for s in sample_strongs:
        if s in lexicon.entries:
            e = lexicon.entries[s]
            print(f"{s}: {e.get('lemma', 'N/A')}")
            print(f"  Def: {e.get('strongs_def', 'N/A')[:80]}...")
            print(f"  KJV: {e.get('kjv_def', 'N/A')[:60]}...\n")
    
    print("=" * 70)
    print("LEXICON COMPLETE")
    print("=" * 70)
    print(f"\nOutput files in {out_dir.absolute()}:")
    print(f"  - hebrew_lexicon.json (full machine-readable)")
    print(f"  - hebrew_lexicon.md (first 2000 entries)")
    print(f"  - websters_hebrew.txt (Webster's style, first 1000)")


if __name__ == "__main__":
    main()
