#!/usr/bin/env python3
"""
Pattern Detection Suite for Narrative Analysis
Hidden consistency/contradiction patterns in 1000+ witness statements
"""

import sqlite3
import json
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PatternMatch:
    """Represents a detected pattern"""
    pattern_type: str
    description: str
    confidence: float
    involved_witnesses: List[str]
    supporting_evidence: List[str]
    severity: str = 'info'  # info, warning, critical

class PatternDetectionSuite:
    """Detect hidden patterns in witness statements"""
    
    def __init__(self, db_path: str = "narrative_analysis.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
    
    # ============== CONSISTENCY PATTERNS ==============
    
    def detect_linguistic_resonance(self, min_frequency: int = 3) -> List[PatternMatch]:
        """Detect repeated phrases across statements (possible collusion or genuine recall)"""
        patterns = []
        
        # Get all statements
        self.cursor.execute("SELECT witness_id, raw_text FROM statements")
        statements = self.cursor.fetchall()
        
        # Extract phrases (3-5 words)
        phrase_counter = Counter()
        witness_phrases = defaultdict(list)
        
        for witness_id, text in statements:
            words = re.findall(r'\b\w+\b', text.lower())
            for i in range(len(words) - 2):
                phrase = ' '.join(words[i:i+3])
                phrase_counter[phrase] += 1
                witness_phrases[phrase].append(witness_id)
        
        # Find phrases used by multiple witnesses
        for phrase, count in phrase_counter.most_common(20):
            if count >= min_frequency:
                witnesses = list(set(witness_phrases[phrase]))
                if len(witnesses) >= 2:
                    # Check if it's suspicious (exact same phrase)
                    patterns.append(PatternMatch(
                        pattern_type="Linguistic Resonance",
                        description=f"Phrase '{phrase}' used by {len(witnesses)} witnesses",
                        confidence=0.7,
                        involved_witnesses=witnesses,
                        supporting_evidence=[f"Used {count} times total"],
                        severity="warning" if len(witnesses) > 3 else "info"
                    ))
        
        return patterns
    
    def detect_temporal_consistency(self) -> List[PatternMatch]:
        """Check if timeline events are consistent across witnesses"""
        patterns = []
        
        self.cursor.execute("SELECT * FROM timeline_events ORDER BY event_date, event_time")
        events = self.cursor.fetchall()
        
        # Group by time window
        time_groups = defaultdict(list)
        for event in events:
            date = event[1] or 'unknown'
            time = event[2] or 'unknown'
            time_key = f"{date}_{time[:2] if time != 'unknown' else 'XX'}"  # Group by hour
            time_groups[time_key].append(event)
        
        # Find time clusters with multiple witnesses
        for time_key, event_group in time_groups.items():
            witnesses = set()
            descriptions = []
            for event in event_group:
                wids = json.loads(event[4])
                witnesses.update(wids)
                descriptions.append(event[3])
            
            if len(witnesses) >= 2:
                patterns.append(PatternMatch(
                    pattern_type="Temporal Cluster",
                    description=f"{len(witnesses)} witnesses report events around {time_key}",
                    confidence=0.8,
                    involved_witnesses=list(witnesses),
                    supporting_evidence=descriptions[:3],
                    severity="info"
                ))
        
        return patterns
    
    def detect_detail_progression(self) -> List[PatternMatch]:
        """Detect if witness statements get more detailed over time (suspicious)"""
        patterns = []
        
        # Get statements with timestamps
        self.cursor.execute("""
            SELECT w.witness_id, w.statement_date, s.word_count, s.raw_text
            FROM witnesses w
            JOIN statements s ON w.witness_id = s.witness_id
            WHERE w.statement_date IS NOT NULL
            ORDER BY w.statement_date
        """)
        
        statements_by_date = defaultdict(list)
        for row in self.cursor.fetchall():
            date = row[1]
            if date:
                statements_by_date[date].append({
                    'witness_id': row[0],
                    'word_count': row[2],
                    'text': row[3]
                })
        
        # Check for increasing detail trend
        if len(statements_by_date) >= 2:
            dates = sorted(statements_by_date.keys())
            early_avg = sum(s['word_count'] for s in statements_by_date[dates[0]]) / len(statements_by_date[dates[0]])
            late_avg = sum(s['word_count'] for s in statements_by_date[dates[-1]]) / len(statements_by_date[dates[-1]])
            
            if late_avg > early_avg * 2:
                patterns.append(PatternMatch(
                    pattern_type="Detail Inflation",
                    description=f"Statements grew from avg {early_avg:.0f} to {late_avg:.0f} words",
                    confidence=0.6,
                    involved_witnesses=[s['witness_id'] for s in statements_by_date[dates[-1]]],
                    supporting_evidence=[f"Early date: {dates[0]}", f"Late date: {dates[-1]}"],
                    severity="warning"
                ))
        
        return patterns
    
    # ============== CONTRADICTION PATTERNS ==============
    
    def detect_exclusive_claims(self) -> List[PatternMatch]:
        """Find mutually exclusive claims (A says X, B says definitely not X)"""
        patterns = []
        
        # Get contradictions with high confidence
        self.cursor.execute("""
            SELECT * FROM contradictions 
            WHERE confidence >= 0.7 AND severity IN ('high', 'critical')
            ORDER BY confidence DESC
        """)
        
        contradictions = self.cursor.fetchall()
        
        # Group by entity type
        by_type = defaultdict(list)
        for c in contradictions:
            by_type[c[3]].append(c)
        
        for entity_type, contras in by_type.items():
            if len(contras) >= 3:
                witnesses = set()
                for c in contras:
                    witnesses.add(c[1])
                    witnesses.add(c[2])
                
                patterns.append(PatternMatch(
                    pattern_type="Exclusive Claims",
                    description=f"{len(contras)} contradictions on {entity_type}",
                    confidence=0.85,
                    involved_witnesses=list(witnesses),
                    supporting_evidence=[f"{c[4]} vs {c[5]}" for c in contras[:3]],
                    severity="critical"
                ))
        
        return patterns
    
    def detect_memory_drift(self) -> List[PatternMatch]:
        """Detect when witness details change over multiple statements"""
        patterns = []
        
        # Find witnesses with multiple statements
        self.cursor.execute("""
            SELECT witness_id, COUNT(*) as cnt FROM statements
            GROUP BY witness_id HAVING cnt > 1
        """)
        
        multi_statement_witnesses = self.cursor.fetchall()
        
        for witness_id, count in multi_statement_witnesses:
            # Get entities from different statements
            self.cursor.execute("""
                SELECT entity_type, entity_value FROM entities
                WHERE witness_id = ?
                ORDER BY statement_id
            """, (witness_id,))
            
            entities = self.cursor.fetchall()
            
            # Check for changes in key facts
            key_facts = defaultdict(list)
            for ent_type, value in entities:
                if ent_type in ['PERSON', 'LOCATION', 'TIME']:
                    key_facts[ent_type].append(value)
            
            # Find inconsistencies within same witness
            for fact_type, values in key_facts.items():
                unique_values = set(values)
                if len(unique_values) > 1:
                    patterns.append(PatternMatch(
                        pattern_type="Memory Drift",
                        description=f"Witness {witness_id} gave different {fact_type} values",
                        confidence=0.75,
                        involved_witnesses=[witness_id],
                        supporting_evidence=list(unique_values),
                        severity="warning"
                    ))
        
        return patterns
    
    def detect_outlier_witnesses(self) -> List[PatternMatch]:
        """Find witnesses who contradict the majority on key facts"""
        patterns = []
        
        # Get convergence points (majority views)
        self.cursor.execute("""
            SELECT * FROM convergence WHERE witness_count >= 3
            ORDER BY witness_count DESC
        """)
        
        majority_views = self.cursor.fetchall()
        
        for view in majority_views[:5]:  # Top 5 majority views
            entity_type = view[1]
            value = view[2]
            majority_witnesses = json.loads(view[4])
            
            # Find who contradicts this majority view
            self.cursor.execute("""
                SELECT DISTINCT witness_id FROM entities
                WHERE entity_type = ? AND entity_value != ?
            """, (entity_type, value))
            
            contradictors = [r[0] for r in self.cursor.fetchall()]
            
            # Check if they have a conflicting value
            if contradictors and len(majority_witnesses) >= 3:
                patterns.append(PatternMatch(
                    pattern_type="Outlier Witness",
                    description=f"{len(contradicters)} witness(es) contradict majority view on {entity_type}",
                    confidence=0.8,
                    involved_witnesses=contradicters,
                    supporting_evidence=[
                        f"Majority ({len(majority_witnesses)}): {value}",
                        f"Outliers: {', '.join(contradicters)}"
                    ],
                    severity="warning"
                ))
        
        return patterns
    
    # ============== ANALYSIS METHODS ==============
    
    def run_full_analysis(self) -> Dict:
        """Run complete pattern detection suite"""
        print("[*] Running Pattern Detection Suite...")
        
        all_patterns = []
        
        print("  [*] Checking linguistic resonance...")
        all_patterns.extend(self.detect_linguistic_resonance())
        
        print("  [*] Checking temporal consistency...")
        all_patterns.extend(self.detect_temporal_consistency())
        
        print("  [*] Checking detail progression...")
        all_patterns.extend(self.detect_detail_progression())
        
        print("  [*] Checking exclusive claims...")
        all_patterns.extend(self.detect_exclusive_claims())
        
        print("  [*] Checking memory drift...")
        all_patterns.extend(self.detect_memory_drift())
        
        print("  [*] Checking for outlier witnesses...")
        all_patterns.extend(self.detect_outlier_witnesses())
        
        # Categorize patterns
        by_severity = defaultdict(list)
        by_type = defaultdict(list)
        
        for pattern in all_patterns:
            by_severity[pattern.severity].append(pattern)
            by_type[pattern.pattern_type].append(pattern)
        
        print(f"\n[+] Analysis complete!")
        print(f"    Total patterns found: {len(all_patterns)}")
        print(f"    Critical: {len(by_severity['critical'])}")
        print(f"    Warnings: {len(by_severity['warning'])}")
        print(f"    Info: {len(by_severity['info'])}")
        
        return {
            'all_patterns': all_patterns,
            'by_severity': dict(by_severity),
            'by_type': dict(by_type),
            'stats': {
                'total': len(all_patterns),
                'critical': len(by_severity['critical']),
                'warning': len(by_severity['warning']),
                'info': len(by_severity['info'])
            }
        }
    
    def generate_pattern_report(self, output_path: str = None) -> str:
        """Generate detailed pattern analysis report"""
        results = self.run_full_analysis()
        
        report = []
        report.append("=" * 80)
        report.append("PATTERN DETECTION SUITE REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append(f"Database: {self.db_path}")
        report.append("")
        
        # Summary
        report.append("EXECUTIVE SUMMARY")
        report.append("-" * 40)
        stats = results['stats']
        report.append(f"  Total Patterns Detected: {stats['total']}")
        report.append(f"  Critical Issues: {stats['critical']}")
        report.append(f"  Warnings: {stats['warning']}")
        report.append(f"  Informational: {stats['info']}")
        report.append("")
        
        # Critical patterns
        if results['by_severity'].get('critical'):
            report.append("CRITICAL PATTERNS")
            report.append("-" * 40)
            for p in results['by_severity']['critical']:
                report.append(f"  [{p.pattern_type}]")
                report.append(f"    {p.description}")
                report.append(f"    Witnesses: {', '.join(p.involved_witnesses)}")
                report.append(f"    Confidence: {p.confidence:.0%}")
                report.append("")
        
        # Warning patterns
        if results['by_severity'].get('warning'):
            report.append("WARNING PATTERNS")
            report.append("-" * 40)
            for p in results['by_severity']['warning']:
                report.append(f"  [{p.pattern_type}] {p.description}")
                report.append(f"    Witnesses: {', '.join(p.involved_witnesses[:5])}")
                if len(p.involved_witnesses) > 5:
                    report.append(f"    ... and {len(p.involved_witnesses) - 5} more")
                report.append("")
        
        # Pattern type breakdown
        report.append("PATTERN TYPE BREAKDOWN")
        report.append("-" * 40)
        for pattern_type, patterns in results['by_type'].items():
            report.append(f"  {pattern_type}: {len(patterns)} instances")
        
        report.append("")
        report.append("=" * 80)
        
        report_text = "\n".join(report)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"[+] Pattern report saved to {output_path}")
        
        return report_text


def demo():
    """Demonstrate pattern detection"""
    print("=" * 80)
    print("PATTERN DETECTION SUITE - DEMO")
    print("=" * 80)
    
    # Use the demo database created by enhanced_narrative_analyzer
    suite = PatternDetectionSuite("demo_narrative.db")
    
    print("\n[*] Running full pattern analysis...")
    report = suite.generate_pattern_report("demo_pattern_report.txt")
    
    print("\n" + report)
    
    print("\n[+] Demo complete!")
    print("    Report: demo_pattern_report.txt")


if __name__ == "__main__":
    demo()
