#!/usr/bin/env python3
"""
Koine Greek Lexicon Builder
Builds a complete Greek dictionary from Strong's data
"""
import json
import re
import os
import sys
from pathlib import Path
from collections import defaultdict

class GreekLexicon:
    """Complete Koine Greek lexicon builder"""
    
    def __init__(self):
        self.entries = {}
        self.root_index = defaultdict(list)  # Will track related words
        
    def load_strongs(self, filepath: str):
        """Load Strong's Greek dictionary"""
        print(f"[*] Loading Strong's Greek from {filepath}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract all entries using regex
        # Pattern: "G123":{"strongs_def":"...","lemma":"...",...}
        pattern = r'"(G\d+)"\s*:\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}'
        matches = re.findall(pattern, content)
        
        print(f"    Found {len(matches)} entries")
        
        for strongs_num, entry_text in matches:
            entry = self._parse_entry(entry_text)
            if entry:
                entry['strongs'] = strongs_num
                self.entries[strongs_num] = entry
        
        print(f"    [+] Parsed {len(self.entries)} entries")
        
    def _parse_entry(self, text: str) -> dict:
        """Parse a single Greek entry"""
        entry = {}
        
        # Extract fields - note Greek has different field names
        fields = {
            'lemma': r'"lemma"\s*:\s*"([^"]*)"',
            'translit': r'"translit"\s*:\s*"([^"]*)"',
            'strongs_def': r'"strongs_def"\s*:\s*"([^"]*)"',
            'kjv_def': r'"kjv_def"\s*:\s*"([^"]*)"',
            'derivation': r'"derivation"\s*:\s*"([^"]*)"',
        }
        
        for field, pattern in fields.items():
            match = re.search(pattern, text)
            if match:
                entry[field] = match.group(1)
        
        return entry if entry else None
    
    def determine_pos(self, strongs_def: str, lemma: str) -> str:
        """Determine part of speech from definition"""
        sdef = strongs_def.lower()
        
        if 'verb' in sdef or sdef.strip().startswith('to '):
            return "verb"
        elif 'noun' in sdef:
            return "noun"
        elif 'adjective' in sdef or lemma.endswith('ος') or lemma.endswith('ων'):
            return "adjective"
        elif 'adverb' in sdef or lemma.endswith('ως'):
            return "adverb"
        elif 'preposition' in sdef:
            return "preposition"
        elif 'conjunction' in sdef or lemma in ['καί', 'δέ', 'γάρ', 'ἀλλά']:
            return "conjunction"
        elif 'pronoun' in sdef or lemma in ['ἐγώ', 'σύ', 'αὐτός', 'οὗτος']:
            return "pronoun"
        elif 'article' in sdef or lemma in ['ὁ', 'ἡ', 'τό']:
            return "article"
        elif 'particle' in sdef or 'interjection' in sdef:
            return "particle"
        
        # Default based on common patterns
        if lemma.endswith('ω') or lemma.endswith('μι') or lemma.endswith('μαι'):
            return "verb"
        elif lemma.endswith('ος') or lemma.endswith('ον') or lemma.endswith('ης'):
            return "noun/adjective"
        
        return "unknown"
    
    def get_word_family(self, lemma: str) -> str:
        """Extract word family/stem for grouping"""
        # Remove common endings
        stem = lemma
        endings = ['ω', 'ομαι', 'μι', 'μαι', 'ος', 'ον', 'ης', 'ας', 'η', 'α', 'ος']
        for end in endings:
            if stem.endswith(end):
                stem = stem[:-len(end)]
                break
        return stem
    
    def export_json(self, output_path: str):
        """Export to JSON"""
        print(f"[*] Exporting to {output_path}...")
        
        data = {
            "metadata": {
                "title": "Koine Greek Lexicon",
                "period": "Koine Greek (New Testament Era, 300 BCE - 300 CE)",
                "sources": ["Strong's Concordance", "OpenScriptures"],
                "total_entries": len(self.entries),
                "format": "JSON",
                "coverage": "New Testament and early Christian literature"
            },
            "entries": self.entries,
            "word_families": dict(self.root_index)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"    [+] Exported {len(self.entries)} entries")
    
    def export_markdown(self, output_path: str, limit: int = 2000):
        """Export human-readable markdown"""
        print(f"[*] Exporting markdown to {output_path}...")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Koine Greek Lexicon\n\n")
            f.write("**Complete Dictionary of New Testament Greek**\n\n")
            f.write(f"Total Entries: {len(self.entries)}\n\n")
            f.write("---\n\n")
            
            # Sort by Strong's number
            sorted_entries = sorted(self.entries.items(), 
                key=lambda x: int(x[0][1:]))
            
            for strongs, entry in sorted_entries[:limit]:
                f.write(f"## {strongs}\n\n")
                
                if 'lemma' in entry:
                    f.write(f"**Greek:** {entry['lemma']}\n\n")
                
                if 'translit' in entry:
                    f.write(f"**Transliteration:** *{entry['translit']}*\n\n")
                
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
            f.write("KOINE GREEK LEXICON\n")
            f.write("Complete Dictionary of New Testament Greek\n")
            f.write("Period: 300 BCE - 300 CE (Jesus' Era)\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("Pronunciation Guide:\n")
            f.write("  α = a as in father    ε = e as in pet\n")
            f.write("  η = ay as in say      ι = i as in machine\n")
            f.write("  ο = o as in note      υ = u as in French tu\n")
            f.write("  ω = o as in tone      γ = g (before α,ο,ω) / ng (before ι,ε)\n")
            f.write("  χ = ch as in Bach     θ = th as in thin\n")
            f.write("  φ = ph as in phone    ψ = ps as in lips\n\n")
            
            f.write("-" * 70 + "\n\n")
            
            sorted_entries = sorted(self.entries.items(), 
                key=lambda x: int(x[0][1:]))
            
            for strongs, entry in sorted_entries[:limit]:
                lemma = entry.get('lemma', '')
                translit = entry.get('translit', '')
                sdef = entry.get('strongs_def', '')
                kjv = entry.get('kjv_def', '')
                
                if not lemma:
                    continue
                
                # Main entry line
                f.write(f"\n{lemma}")
                if translit:
                    f.write(f"  ({translit})")
                
                # Part of speech
                pos = self.determine_pos(sdef, lemma)
                f.write(f"  [{pos}]")
                f.write("\n")
                
                # Definition
                if sdef:
                    words = sdef.strip().split()
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
                    if len(kjv) > 100:
                        kjv = kjv[:100] + "..."
                    f.write(f"    Usage: {kjv}\n")
                
                f.write("\n")
        
        print(f"    [+] Exported {min(limit, len(self.entries))} entries")
    
    def export_compact(self, output_path: str):
        """Export compact format for embedding"""
        print(f"[*] Exporting compact format...")
        
        compact = {}
        for strongs, entry in self.entries.items():
            compact[strongs] = {
                'l': entry.get('lemma', ''),
                'd': entry.get('strongs_def', '')[:100],
                'k': entry.get('kjv_def', '')[:50]
            }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'meta': {'count': len(compact), 'format': 'compact'},
                'data': compact
            }, f, ensure_ascii=False, separators=(',', ':'))
        
        print(f"    [+] Exported {len(compact)} compact entries")
    
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
            elif query_lower in entry.get('translit', '').lower():
                match = True
            elif re.match(r'^g?\d+$', query_lower):
                if strongs == f"G{re.sub(r'[^0-9]', '', query)}" or strongs == query.upper():
                    match = True
            elif query in entry.get('lemma', ''):  # Exact Greek match
                match = True
            
            if match:
                results.append((strongs, entry))
        
        return results


def main():
    lexicon = GreekLexicon()
    
    # Load Strong's data
    strongs_path = "/tmp/strongs/greek/strongs-greek-dictionary.js"
    lexicon.load_strongs(strongs_path)
    
    # Create output directory
    out_dir = Path("/root/greek_lexicon_output")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Export all formats
    lexicon.export_json(out_dir / "greek_lexicon.json")
    lexicon.export_markdown(out_dir / "greek_lexicon.md", limit=2000)
    lexicon.export_websters_style(out_dir / "websters_greek.txt", limit=1000)
    lexicon.export_compact(out_dir / "greek_lexicon_compact.json")
    
    # Sample entries
    print("\n" + "=" * 70)
    print("SAMPLE ENTRIES")
    print("=" * 70 + "\n")
    
    sample_strongs = ['G25', 'G26', 'G2424', 'G2316', 'G1100', 'G25', 'G907', 'G40']
    for s in sample_strongs:
        if s in lexicon.entries:
            e = lexicon.entries[s]
            print(f"{s}: {e.get('lemma', 'N/A')}")
            print(f"  Def: {e.get('strongs_def', 'N/A')[:80]}...")
            print(f"  KJV: {e.get('kjv_def', 'N/A')[:60]}...\n")
    
    print("=" * 70)
    print("GREEK LEXICON COMPLETE")
    print("=" * 70)
    print(f"\nOutput files in {out_dir.absolute()}:")
    print(f"  - greek_lexicon.json (full machine-readable)")
    print(f"  - greek_lexicon.md (first 2,000 entries)")
    print(f"  - websters_greek.txt (Webster's style, first 1,000)")
    print(f"  - greek_lexicon_compact.json (compressed)")


if __name__ == "__main__":
    main()
