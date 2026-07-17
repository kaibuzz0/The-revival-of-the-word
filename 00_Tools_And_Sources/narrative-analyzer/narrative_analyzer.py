#!/usr/bin/env python3
"""
Forensic Narrative Analyzer
Analyzes witness statements for truth detection through narrative coherence.
"""
import json
import re
import os
import sys
import argparse
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Set, Tuple, Optional
from datetime import datetime
import hashlib

@dataclass
class Claim:
    """A single claim extracted from a statement"""
    witness_id: str
    claim_type: str  # who, what, when, where, why
    subject: str     # e.g., "John Doe", "the robbery"
    content: str     # The actual claim text
    confidence: float = 1.0
    timestamp: str = ""
    location: str = ""
    entities: List[str] = field(default_factory=list)

@dataclass
class Witness:
    """A witness and their statements"""
    witness_id: str
    name: str
    statement_text: str
    claims: List[Claim] = field(default_factory=list)
    credibility_score: float = 50.0
    contradictions: List[Dict] = field(default_factory=list)
    corroborations: List[Dict] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

class NarrativeAnalyzer:
    """Main analyzer for forensic narrative coherence"""
    
    def __init__(self):
        self.witnesses: Dict[str, Witness] = {}
        self.all_claims: List[Claim] = []
        self.convergence_map: Dict[str, Dict] = defaultdict(lambda: {"count": 0, "witnesses": [], "confidence": 0.0})
        self.entity_graph: Dict[str, Set[str]] = defaultdict(set)
        
    def load_statements(self, directory: str) -> List[Witness]:
        """Load all witness statements from a directory"""
        witnesses = []
        stmt_dir = Path(directory)
        
        if not stmt_dir.exists():
            print(f"[!] Directory not found: {directory}")
            return []
        
        # Support multiple formats: .txt, .json, .md
        statement_files = []
        for ext in ['*.txt', '*.json', '*.md']:
            statement_files.extend(stmt_dir.glob(ext))
        
        print(f"[*] Found {len(statement_files)} statement files")
        
        for filepath in statement_files:
            try:
                content = filepath.read_text(encoding='utf-8')
                witness_id = filepath.stem
                
                # Try to extract name from first line or filename
                name = self._extract_name(content, witness_id)
                
                witness = Witness(
                    witness_id=witness_id,
                    name=name,
                    statement_text=content
                )
                witnesses.append(witness)
                self.witnesses[witness_id] = witness
                
            except Exception as e:
                print(f"[!] Error loading {filepath}: {e}")
        
        return witnesses
    
    def _extract_name(self, content: str, fallback: str) -> str:
        """Extract witness name from statement"""
        # Try common patterns
        patterns = [
            r'(?:name|witness|subject)[\s:]+([^\n]+)',
            r'(?:i am|my name is)[\s:]+([^\n\.]+)',
            r'^([A-Z][a-z]+ [A-Z][a-z]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        return fallback
    
    def extract_claims(self, witness: Witness) -> List[Claim]:
        """Extract structured claims from statement text"""
        claims = []
        text = witness.statement_text
        
        # WHO claims - people mentioned
        who_patterns = [
            r'(?:\bwas\b|\bwere\b|\bsaw\b|\bmet\b|\btalked to\b|\bspoke with\b)[\s]+([A-Z][a-z]+ [A-Z][a-z]+)',
            r'(?:\bsaid\b|\bstated\b|\btold\b)[\s]+([A-Z][a-z]+)',
            r'([A-Z][a-z]+ [A-Z][a-z]+)[\s]+(?:was|were|did|had)',
            r'(?:with|and|by)[\s]+([A-Z][a-z]+ [A-Z][a-z]+)',
        ]
        
        people_mentioned = set()
        for pattern in who_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                person = match.group(1).strip()
                if len(person) > 2 and person.lower() not in ['the', 'and', 'was', 'were']:
                    people_mentioned.add(person)
        
        for person in people_mentioned:
            claims.append(Claim(
                witness_id=witness.witness_id,
                claim_type='who',
                subject=person,
                content=f"Witness claims presence/knowledge of: {person}",
                entities=[person, witness.name]
            ))
        
        # WHEN claims - temporal markers
        time_patterns = [
            r'(?:at|around)[\s]+(\d{1,2}:\d{2}[\s]?(?:AM|PM|am|pm)?)',
            r'(?:at|around)[\s]+(\d{1,2}[\s]?(?:AM|PM|am|pm)?)',
            r'(?:on|during)[\s]+([A-Z][a-z]+(?:day|night)?)',
            r'(?:on)[\s]+([A-Z][a-z]+ \d{1,2}(?:st|nd|rd|th)?,? \d{4})',
            r'(?:before|after|during)[\s]+([a-z\s]+?)(?:,|\.|;|$)',
        ]
        
        for pattern in time_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                time_ref = match.group(1).strip()
                claims.append(Claim(
                    witness_id=witness.witness_id,
                    claim_type='when',
                    subject=time_ref,
                    content=f"Temporal reference: {time_ref}",
                    timestamp=time_ref
                ))
        
        # WHERE claims - locations
        where_patterns = [
            r'(?:at|in|near)[\s]+(?:the\s+)?([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)',
            r'(?:went to|arrived at|came to)[\s]+(?:the\s+)?([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)',
            r'(?:location|place|scene)[\s:]+([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)',
        ]
        
        for pattern in where_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                location = match.group(1).strip()
                if len(location) > 2:
                    claims.append(Claim(
                        witness_id=witness.witness_id,
                        claim_type='where',
                        subject=location,
                        content=f"Location mentioned: {location}",
                        location=location
                    ))
        
        # WHAT claims - actions and events
        event_keywords = ['robbery', 'theft', 'incident', 'event', 'crime', 'attack', 'shooting', 'meeting', 'conversation']
        for keyword in event_keywords:
            if keyword in text.lower():
                # Extract context around the keyword
                pattern = rf'[^.]*\b{keyword}\b[^.]*\.?'
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    context = match.group(0).strip()
                    if len(context) > 10:
                        claims.append(Claim(
                            witness_id=witness.witness_id,
                            claim_type='what',
                            subject=keyword,
                            content=context[:200]  # Limit length
                        ))
        
        return claims
    
    def build_convergence_map(self):
        """Build map of how many witnesses corroborate each claim"""
        for claim in self.all_claims:
            key = f"{claim.claim_type}:{claim.subject}"
            self.convergence_map[key]["count"] += 1
            self.convergence_map[key]["witnesses"].append(claim.witness_id)
            self.convergence_map[key]["content"] = claim.content
            
            # Higher confidence with more witnesses
            count = self.convergence_map[key]["count"]
            self.convergence_map[key]["confidence"] = min(count / 10 * 100, 100)
    
    def detect_contradictions(self) -> List[Dict]:
        """Detect contradictions between witness statements"""
        contradictions = []
        
        # Group claims by type and subject
        claim_groups = defaultdict(list)
        for claim in self.all_claims:
            key = f"{claim.claim_type}:{claim.subject}"
            claim_groups[key].append(claim)
        
        # Look for temporal contradictions
        time_claims = [c for c in self.all_claims if c.claim_type == 'when']
        for i, claim1 in enumerate(time_claims):
            for claim2 in time_claims[i+1:]:
                if claim1.witness_id != claim2.witness_id:
                    # Check for mutually exclusive times
                    if self._times_conflict(claim1.timestamp, claim2.timestamp):
                        contradictions.append({
                            'type': 'temporal',
                            'subject': claim1.subject,
                            'witness_a': claim1.witness_id,
                            'witness_b': claim2.witness_id,
                            'claim_a': claim1.content,
                            'claim_b': claim2.content,
                            'severity': 'high'
                        })
        
        # Look for location contradictions (same person in different places)
        who_where = defaultdict(lambda: defaultdict(list))
        for claim in self.all_claims:
            if claim.claim_type == 'where' and claim.entities:
                for person in claim.entities:
                    who_where[person][claim.witness_id].append(claim.location)
        
        for person, witness_locs in who_where.items():
            if len(witness_locs) > 1:
                locations = set()
                for locs in witness_locs.values():
                    locations.update(locs)
                if len(locations) > 1:
                    contradictions.append({
                        'type': 'location',
                        'subject': person,
                        'locations': list(locations),
                        'witnesses': list(witness_locs.keys()),
                        'severity': 'medium'
                    })
        
        return contradictions
    
    def _times_conflict(self, time1: str, time2: str) -> bool:
        """Check if two time references conflict (simplified)"""
        # Normalize and compare
        t1 = time1.lower().strip()
        t2 = time2.lower().strip()
        
        # Direct conflict keywords
        conflicts = [
            ('morning', 'evening'),
            ('early', 'late'),
            ('before', 'after'),
        ]
        
        for a, b in conflicts:
            if (a in t1 and b in t2) or (b in t1 and a in t2):
                return True
        
        return False
    
    def calculate_credibility(self, witness: Witness) -> float:
        """Calculate credibility score for a witness"""
        score = 50.0  # Baseline
        
        # Corroboration bonus: +10 per corroborated claim
        corroborated = 0
        for claim in witness.claims:
            key = f"{claim.claim_type}:{claim.subject}"
            if key in self.convergence_map:
                if self.convergence_map[key]["count"] > 1:
                    corroborated += 1
        
        score += corroborated * 10
        
        # Contradiction penalty: -20 per contradiction
        contradictions = [c for c in witness.contradictions if c['witness_a'] == witness.witness_id or c['witness_b'] == witness.witness_id]
        score -= len(contradictions) * 20
        
        # Unique claim penalty (claims no one else makes)
        unique_claims = 0
        for claim in witness.claims:
            key = f"{claim.claim_type}:{claim.subject}"
            if key in self.convergence_map:
                if self.convergence_map[key]["count"] == 1:
                    unique_claims += 1
        
        score -= unique_claims * 5
        
        # Detail bonus (more claims = more detailed = more credible)
        detail_bonus = min(len(witness.claims) * 2, 20)
        score += detail_bonus
        
        # Clamp to 0-100
        return max(0, min(100, score))
    
    def analyze(self, statements_dir: str, output_dir: str):
        """Run full analysis"""
        print("=" * 60)
        print("FORENSIC NARRATIVE ANALYZER")
        print("=" * 60)
        
        # Load statements
        print("\n[1/5] Loading witness statements...")
        witnesses = self.load_statements(statements_dir)
        print(f"    Loaded {len(witnesses)} witness statements")
        
        # Extract claims
        print("\n[2/5] Extracting claims from statements...")
        for witness in witnesses:
            witness.claims = self.extract_claims(witness)
            self.all_claims.extend(witness.claims)
        
        total_claims = len(self.all_claims)
        print(f"    Extracted {total_claims} total claims")
        
        # Build convergence map
        print("\n[3/5] Building convergence analysis...")
        self.build_convergence_map()
        print(f"    Found {len(self.convergence_map)} unique claims")
        
        # Detect contradictions
        print("\n[4/5] Detecting contradictions...")
        all_contradictions = self.detect_contradictions()
        print(f"    Found {len(all_contradictions)} contradictions")
        
        # Assign contradictions to witnesses
        for contra in all_contradictions:
            if contra['witness_a'] in self.witnesses:
                self.witnesses[contra['witness_a']].contradictions.append(contra)
            if contra['witness_b'] in self.witnesses:
                self.witnesses[contra['witness_b']].contradictions.append(contra)
        
        # Calculate credibility
        print("\n[5/5] Calculating credibility scores...")
        for witness in witnesses:
            witness.credibility_score = self.calculate_credibility(witness)
        
        # Sort by credibility
        witnesses.sort(key=lambda w: w.credibility_score, reverse=True)
        
        # Generate reports
        self.generate_reports(witnesses, all_contradictions, output_dir)
        
        return witnesses
    
    def generate_reports(self, witnesses: List[Witness], contradictions: List[Dict], output_dir: str):
        """Generate all output reports"""
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        
        # 1. Credibility ranking (JSON)
        credibility_data = {
            "generated_at": datetime.now().isoformat(),
            "total_witnesses": len(witnesses),
            "total_claims": len(self.all_claims),
            "witness_ranking": [
                {
                    "rank": i + 1,
                    "witness_id": w.witness_id,
                    "name": w.name,
                    "credibility_score": round(w.credibility_score, 2),
                    "claim_count": len(w.claims),
                    "contradiction_count": len(w.contradictions),
                    "trust_level": "HIGH" if w.credibility_score >= 70 else ("MEDIUM" if w.credibility_score >= 40 else "LOW")
                }
                for i, w in enumerate(witnesses)
            ]
        }
        
        with open(out_path / "credibility_ranking.json", 'w') as f:
            json.dump(credibility_data, f, indent=2)
        print(f"    [+] credibility_ranking.json")
        
        # 2. Contradictions report (Markdown)
        with open(out_path / "contradictions_report.md", 'w') as f:
            f.write("# Contradictions Report\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            f.write(f"Total Contradictions Found: {len(contradictions)}\n\n")
            
            for i, contra in enumerate(contradictions, 1):
                f.write(f"## Contradiction {i}\n")
                f.write(f"- **Type:** {contra['type']}\n")
                f.write(f"- **Subject:** {contra['subject']}\n")
                f.write(f"- **Severity:** {contra['severity']}\n")
                f.write(f"- **Between:** {contra.get('witness_a', ', '.join(contra.get('witnesses', [])))}\n")
                if 'claim_a' in contra:
                    f.write(f"- **Claim A:** {contra['claim_a']}\n")
                    f.write(f"- **Claim B:** {contra['claim_b']}\n")
                f.write("\n")
        
        print(f"    [+] contradictions_report.md")
        
        # 3. Convergence map (JSON)
        convergence_sorted = dict(sorted(
            self.convergence_map.items(),
            key=lambda x: x[1]["count"],
            reverse=True
        ))
        
        with open(out_path / "convergence_map.json", 'w') as f:
            json.dump({
                "description": "Facts ranked by witness consensus (higher = more credible)",
                "facts": convergence_sorted
            }, f, indent=2)
        
        print(f"    [+] convergence_map.json")
        
        # 4. Summary report (Text)
        with open(out_path / "ANALYSIS_SUMMARY.txt", 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("FORENSIC NARRATIVE ANALYSIS SUMMARY\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Total Witnesses Analyzed: {len(witnesses)}\n")
            f.write(f"Total Claims Extracted: {len(self.all_claims)}\n")
            f.write(f"Contradictions Detected: {len(contradictions)}\n\n")
            
            f.write("-" * 70 + "\n")
            f.write("CREDIBILITY RANKING (Top 10)\n")
            f.write("-" * 70 + "\n")
            
            for w in witnesses[:10]:
                bar = "█" * int(w.credibility_score / 5)
                f.write(f"{w.credibility_score:5.1f} {bar} {w.name} ({w.witness_id})\n")
            
            f.write("\n")
            f.write("-" * 70 + "\n")
            f.write("MOST CORROBORATED FACTS (Top 10)\n")
            f.write("-" * 70 + "\n")
            
            for i, (key, data) in enumerate(list(convergence_sorted.items())[:10], 1):
                f.write(f"{i}. [{data['count']} witnesses] {key}\n")
                f.write(f"   {data['content'][:100]}...\n\n")
            
            f.write("-" * 70 + "\n")
            f.write("SUSPICIOUS WITNESSES (Low Credibility)\n")
            f.write("-" * 70 + "\n")
            
            suspicious = [w for w in witnesses if w.credibility_score < 40]
            if suspicious:
                for w in suspicious:
                    f.write(f"[!] {w.name}: {w.credibility_score:.1f}/100 - {len(w.contradictions)} contradictions\n")
            else:
                f.write("No witnesses flagged as suspicious\n")
        
        print(f"    [+] ANALYSIS_SUMMARY.txt")
        
        # Print summary to console
        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE")
        print("=" * 60)
        print(f"\nMost Credible Witness: {witnesses[0].name} ({witnesses[0].credibility_score:.1f}/100)")
        print(f"Least Credible Witness: {witnesses[-1].name} ({witnesses[-1].credibility_score:.1f}/100)")
        print(f"\nReports saved to: {out_path.absolute()}")


def main():
    parser = argparse.ArgumentParser(
        description="Forensic Narrative Analyzer - Detect truth in witness statements"
    )
    parser.add_argument(
        "--statements-dir", "-s",
        required=True,
        help="Directory containing witness statement files"
    )
    parser.add_argument(
        "--output", "-o",
        default="./analysis_output",
        help="Output directory for reports (default: ./analysis_output)"
    )
    
    args = parser.parse_args()
    
    analyzer = NarrativeAnalyzer()
    analyzer.analyze(args.statements_dir, args.output)


if __name__ == "__main__":
    main()
