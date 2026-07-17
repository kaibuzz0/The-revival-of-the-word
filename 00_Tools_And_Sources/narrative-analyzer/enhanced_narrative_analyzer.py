#!/usr/bin/env python3
"""
Enhanced Narrative Analyzer - Database Backend Edition
Forensic analysis system for 1000+ witness statements
Features: Entity extraction, credibility scoring, contradiction detection, cross-referencing
"""

import sqlite3
import json
import re
import hashlib
from datetime import datetime
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional
import statistics

class NarrativeDatabase:
    """SQLite backend for storing and analyzing 1000+ witness statements"""
    
    def __init__(self, db_path: str = "narrative_analysis.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._init_tables()
    
    def _init_tables(self):
        """Initialize database schema"""
        # Witnesses table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS witnesses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                witness_id TEXT UNIQUE NOT NULL,
                name TEXT,
                age INTEGER,
                occupation TEXT,
                relationship_to_case TEXT,
                statement_date TEXT,
                credibility_score REAL DEFAULT 0.0,
                reliability_tier TEXT DEFAULT 'unverified',
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Statements table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS statements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                witness_id TEXT NOT NULL,
                raw_text TEXT NOT NULL,
                processed_text TEXT,
                word_count INTEGER,
                statement_hash TEXT UNIQUE,
                timestamp TEXT,
                location TEXT,
                FOREIGN KEY (witness_id) REFERENCES witnesses(witness_id)
            )
        """)
        
        # Entities table (WHO, WHAT, WHERE, WHEN)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                statement_id INTEGER NOT NULL,
                witness_id TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                entity_value TEXT NOT NULL,
                confidence REAL DEFAULT 1.0,
                context TEXT,
                FOREIGN KEY (statement_id) REFERENCES statements(id),
                FOREIGN KEY (witness_id) REFERENCES witnesses(witness_id)
            )
        """)
        
        # Credibility scores table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS credibility_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                witness_id TEXT NOT NULL,
                overall_score REAL DEFAULT 0.0,
                consistency_score REAL DEFAULT 0.0,
                detail_score REAL DEFAULT 0.0,
                corroboration_score REAL DEFAULT 0.0,
                emotional_markers TEXT,
                red_flags TEXT,
                scoring_breakdown TEXT,
                FOREIGN KEY (witness_id) REFERENCES witnesses(witness_id)
            )
        """)
        
        # Contradictions table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contradictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                witness_a_id TEXT NOT NULL,
                witness_b_id TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                value_a TEXT NOT NULL,
                value_b TEXT NOT NULL,
                severity TEXT DEFAULT 'medium',
                confidence REAL DEFAULT 0.5,
                context_a TEXT,
                context_b TEXT,
                detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Convergence table (agreements)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS convergence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_type TEXT NOT NULL,
                entity_value TEXT NOT NULL,
                witness_count INTEGER DEFAULT 1,
                witness_ids TEXT,
                confidence REAL DEFAULT 0.5
            )
        """)
        
        # Timeline events
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS timeline_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_date TEXT,
                event_time TEXT,
                description TEXT,
                witness_ids TEXT,
                source_statement_ids TEXT,
                event_type TEXT DEFAULT 'incident',
                confidence REAL DEFAULT 0.5
            )
        """)
        
        # Cross-reference matrix
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cross_references (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                witness_a_id TEXT NOT NULL,
                witness_b_id TEXT NOT NULL,
                agreement_score REAL DEFAULT 0.0,
                contradiction_count INTEGER DEFAULT 0,
                corroboration_count INTEGER DEFAULT 0,
                similarity_score REAL DEFAULT 0.0,
                relationship_type TEXT DEFAULT 'neutral'
            )
        """)
        
        self.conn.commit()
        print(f"[+] Database initialized: {self.db_path}")
    
    def add_witness(self, witness_id: str, name: str = None, **metadata) -> int:
        """Add a witness to the database"""
        self.cursor.execute("""
            INSERT OR REPLACE INTO witnesses 
            (witness_id, name, age, occupation, relationship_to_case, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            witness_id, name, 
            metadata.get('age'), 
            metadata.get('occupation'),
            metadata.get('relationship'),
            json.dumps(metadata)
        ))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def add_statement(self, witness_id: str, text: str, timestamp: str = None, location: str = None) -> int:
        """Add a witness statement"""
        # Calculate hash for deduplication
        statement_hash = hashlib.md5(text.encode()).hexdigest()
        word_count = len(text.split())
        
        self.cursor.execute("""
            INSERT INTO statements (witness_id, raw_text, word_count, statement_hash, timestamp, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (witness_id, text, word_count, statement_hash, timestamp, location))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_all_statements(self) -> List[Tuple]:
        """Retrieve all statements"""
        self.cursor.execute("SELECT * FROM statements")
        return self.cursor.fetchall()
    
    def get_statement_by_id(self, statement_id: int) -> Optional[Tuple]:
        """Get a specific statement"""
        self.cursor.execute("SELECT * FROM statements WHERE id = ?", (statement_id,))
        return self.cursor.fetchone()
    
    def get_statements_by_witness(self, witness_id: str) -> List[Tuple]:
        """Get all statements from a witness"""
        self.cursor.execute("SELECT * FROM statements WHERE witness_id = ?", (witness_id,))
        return self.cursor.fetchall()
    
    def add_entity(self, statement_id: int, witness_id: str, entity_type: str, 
                   value: str, confidence: float = 1.0, context: str = None):
        """Add extracted entity"""
        self.cursor.execute("""
            INSERT INTO entities (statement_id, witness_id, entity_type, entity_value, confidence, context)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (statement_id, witness_id, entity_type, value, confidence, context))
        self.conn.commit()
    
    def get_entities_by_type(self, entity_type: str) -> List[Tuple]:
        """Get all entities of a specific type"""
        self.cursor.execute("""
            SELECT e.*, s.raw_text FROM entities e
            JOIN statements s ON e.statement_id = s.id
            WHERE e.entity_type = ?
        """, (entity_type,))
        return self.cursor.fetchall()
    
    def get_witness_entities(self, witness_id: str) -> List[Tuple]:
        """Get all entities for a witness"""
        self.cursor.execute("SELECT * FROM entities WHERE witness_id = ?", (witness_id,))
        return self.cursor.fetchall()
    
    def update_credibility(self, witness_id: str, **scores):
        """Update credibility scores for a witness"""
        self.cursor.execute("""
            INSERT OR REPLACE INTO credibility_scores 
            (witness_id, overall_score, consistency_score, detail_score, 
             corroboration_score, emotional_markers, red_flags, scoring_breakdown)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            witness_id,
            scores.get('overall', 0.0),
            scores.get('consistency', 0.0),
            scores.get('detail', 0.0),
            scores.get('corroboration', 0.0),
            json.dumps(scores.get('emotional_markers', [])),
            json.dumps(scores.get('red_flags', [])),
            json.dumps(scores.get('breakdown', {}))
        ))
        
        # Update witness table
        reliability = self._tier_from_score(scores.get('overall', 0.0))
        self.cursor.execute("""
            UPDATE witnesses SET credibility_score = ?, reliability_tier = ?
            WHERE witness_id = ?
        """, (scores.get('overall', 0.0), reliability, witness_id))
        
        self.conn.commit()
    
    def _tier_from_score(self, score: float) -> str:
        """Convert score to reliability tier"""
        if score >= 85: return 'highly_reliable'
        if score >= 70: return 'reliable'
        if score >= 50: return 'questionable'
        if score >= 30: return 'unreliable'
        return 'fabricated'
    
    def add_contradiction(self, witness_a: str, witness_b: str, entity_type: str,
                         value_a: str, value_b: str, severity: str = 'medium',
                         confidence: float = 0.5, context_a: str = None, context_b: str = None):
        """Record a contradiction between witnesses"""
        self.cursor.execute("""
            INSERT INTO contradictions 
            (witness_a_id, witness_b_id, entity_type, value_a, value_b,
             severity, confidence, context_a, context_b)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (witness_a, witness_b, entity_type, value_a, value_b, 
              severity, confidence, context_a, context_b))
        self.conn.commit()
    
    def get_contradictions(self, witness_id: str = None) -> List[Tuple]:
        """Get all contradictions, optionally filtered by witness"""
        if witness_id:
            self.cursor.execute("""
                SELECT * FROM contradictions 
                WHERE witness_a_id = ? OR witness_b_id = ?
                ORDER BY severity DESC, confidence DESC
            """, (witness_id, witness_id))
        else:
            self.cursor.execute("SELECT * FROM contradictions ORDER BY severity DESC, confidence DESC")
        return self.cursor.fetchall()
    
    def add_convergence(self, entity_type: str, value: str, witness_ids: List[str], confidence: float = 0.5):
        """Record convergent (agreed-upon) information"""
        self.cursor.execute("""
            INSERT OR REPLACE INTO convergence (entity_type, entity_value, witness_count, witness_ids, confidence)
            VALUES (?, ?, ?, ?, ?)
        """, (entity_type, value, len(witness_ids), json.dumps(witness_ids), confidence))
        self.conn.commit()
    
    def get_convergence(self, min_witnesses: int = 2) -> List[Tuple]:
        """Get all convergence points with minimum witness threshold"""
        self.cursor.execute("""
            SELECT * FROM convergence WHERE witness_count >= ? ORDER BY witness_count DESC
        """, (min_witnesses,))
        return self.cursor.fetchall()
    
    def add_timeline_event(self, description: str, witness_ids: List[str], 
                          event_date: str = None, event_time: str = None,
                          event_type: str = 'incident', confidence: float = 0.5):
        """Add event to master timeline"""
        self.cursor.execute("""
            INSERT INTO timeline_events 
            (event_date, event_time, description, witness_ids, event_type, confidence)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (event_date, event_time, description, json.dumps(witness_ids), event_type, confidence))
        self.conn.commit()
    
    def get_timeline(self) -> List[Tuple]:
        """Get chronological timeline"""
        self.cursor.execute("""
            SELECT * FROM timeline_events 
            ORDER BY event_date, event_time
        """)
        return self.cursor.fetchall()
    
    def update_cross_reference(self, witness_a: str, witness_b: str, **data):
        """Update cross-reference matrix between two witnesses"""
        self.cursor.execute("""
            INSERT OR REPLACE INTO cross_references
            (witness_a_id, witness_b_id, agreement_score, contradiction_count, 
             corroboration_count, similarity_score, relationship_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            witness_a, witness_b,
            data.get('agreement', 0.0),
            data.get('contradictions', 0),
            data.get('corroborations', 0),
            data.get('similarity', 0.0),
            data.get('relationship', 'neutral')
        ))
        self.conn.commit()
    
    def get_cross_reference_matrix(self) -> List[Tuple]:
        """Get full cross-reference matrix"""
        self.cursor.execute("SELECT * FROM cross_references ORDER BY agreement_score DESC")
        return self.cursor.fetchall()
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        stats = {}
        
        # Count tables
        for table in ['witnesses', 'statements', 'entities', 'contradictions', 'convergence']:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            stats[table] = self.cursor.fetchone()[0]
        
        # Average credibility
        self.cursor.execute("SELECT AVG(credibility_score) FROM witnesses")
        stats['avg_credibility'] = self.cursor.fetchone()[0] or 0.0
        
        # Reliability distribution
        self.cursor.execute("""
            SELECT reliability_tier, COUNT(*) FROM witnesses GROUP BY reliability_tier
        """)
        stats['tier_distribution'] = dict(self.cursor.fetchall())
        
        return stats
    
    def export_to_json(self, output_path: str):
        """Export full database to JSON"""
        export_data = {
            'export_date': datetime.now().isoformat(),
            'statistics': self.get_statistics(),
            'witnesses': [],
            'timeline': [],
            'contradictions': [],
            'convergence': []
        }
        
        # Export witnesses with their data
        self.cursor.execute("SELECT * FROM witnesses")
        columns = [description[0] for description in self.cursor.description]
        for row in self.cursor.fetchall():
            witness_data = dict(zip(columns, row))
            witness_id = witness_data['witness_id']
            
            # Add statements
            witness_data['statements'] = []
            for stmt in self.get_statements_by_witness(witness_id):
                witness_data['statements'].append({
                    'id': stmt[0],
                    'text': stmt[2][:500] + '...' if len(stmt[2]) > 500 else stmt[2],
                    'word_count': stmt[4]
                })
            
            # Add entities
            witness_data['entities'] = []
            for ent in self.get_witness_entities(witness_id):
                witness_data['entities'].append({
                    'type': ent[3],
                    'value': ent[4],
                    'confidence': ent[5]
                })
            
            # Add credibility
            self.cursor.execute("SELECT * FROM credibility_scores WHERE witness_id = ?", (witness_id,))
            cred = self.cursor.fetchone()
            if cred:
                witness_data['credibility'] = {
                    'overall': cred[2],
                    'consistency': cred[3],
                    'detail': cred[4],
                    'corroboration': cred[5]
                }
            
            export_data['witnesses'].append(witness_data)
        
        # Export timeline
        for event in self.get_timeline():
            export_data['timeline'].append({
                'date': event[1],
                'time': event[2],
                'description': event[3],
                'type': event[6]
            })
        
        # Export contradictions
        for contr in self.get_contradictions():
            export_data['contradictions'].append({
                'witness_a': contr[1],
                'witness_b': contr[2],
                'entity_type': contr[3],
                'value_a': contr[4],
                'value_b': contr[5],
                'severity': contr[6],
                'confidence': contr[7]
            })
        
        # Export convergence
        for conv in self.get_convergence(2):
            export_data['convergence'].append({
                'entity_type': conv[1],
                'value': conv[2],
                'witness_count': conv[3],
                'witness_ids': json.loads(conv[4])
            })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"[+] Exported to {output_path}")
    
    def close(self):
        """Close database connection"""
        self.conn.close()


class EnhancedNarrativeAnalyzer:
    """Main analyzer class with all forensic capabilities"""
    
    def __init__(self, db_path: str = "narrative_analysis.db"):
        self.db = NarrativeDatabase(db_path)
        self.entity_patterns = self._compile_patterns()
    
    def _compile_patterns(self) -> Dict:
        """Compile regex patterns for entity extraction"""
        return {
            'PERSON': re.compile(r'\b([A-Z][a-z]+\s+[A-Z][a-z]+|[A-Z][a-z]+)\b'),
            'DATE': re.compile(r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}|January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}\b'),
            'TIME': re.compile(r'\b(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?|\d{1,2}\s*o\'clock)\b'),
            'LOCATION': re.compile(r'\b(at|in|near|outside)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', re.IGNORECASE),
            'WEAPON': re.compile(r'\b(gun|knife|weapon|pistol|rifle|blade|bat|crowbar)\b', re.IGNORECASE),
            'VEHICLE': re.compile(r'\b(car|truck|van|sedan|SUV|vehicle|automobile)\b', re.IGNORECASE),
            'ACTION': re.compile(r'\b(shot|stabbed|hit|punched|kicked|grabbed|pushed|threw|ran|drove|walked|entered|left)\b', re.IGNORECASE),
        }
    
    def process_witness(self, witness_id: str, name: str, statement: str, 
                       metadata: Dict = None) -> Dict:
        """Process a complete witness entry"""
        print(f"[*] Processing witness: {witness_id}")
        
        # Add to database
        self.db.add_witness(witness_id, name, **(metadata or {}))
        stmt_id = self.db.add_statement(witness_id, statement)
        
        # Extract entities
        entities = self.extract_entities(stmt_id, witness_id, statement)
        
        # Score credibility
        credibility = self.score_credibility(witness_id, statement, entities)
        
        # Detect timeline events
        events = self.extract_timeline(statement, witness_id, stmt_id)
        
        return {
            'witness_id': witness_id,
            'statement_id': stmt_id,
            'entities_extracted': len(entities),
            'credibility_score': credibility['overall'],
            'reliability_tier': self.db._tier_from_score(credibility['overall']),
            'timeline_events': len(events)
        }
    
    def extract_entities(self, statement_id: int, witness_id: str, text: str) -> List[Dict]:
        """Extract WHO, WHAT, WHERE, WHEN from text"""
        entities = []
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = pattern.findall(text)
            for match in matches:
                if isinstance(match, tuple):
                    match = ' '.join(match)
                
                # Get context (30 chars before and after)
                idx = text.find(match)
                context = text[max(0, idx-30):min(len(text), idx+len(match)+30)]
                
                entity = {
                    'type': entity_type,
                    'value': match,
                    'confidence': 0.8,
                    'context': context
                }
                entities.append(entity)
                
                # Store in database
                self.db.add_entity(statement_id, witness_id, entity_type, 
                                  match, 0.8, context)
        
        return entities
    
    def score_credibility(self, witness_id: str, text: str, entities: List[Dict]) -> Dict:
        """Calculate credibility score 0-100"""
        scores = {
            'consistency': 0.0,
            'detail': 0.0,
            'corroboration': 0.0,
            'emotional_markers': [],
            'red_flags': []
        }
        
        # Detail score (word count, entity density)
        word_count = len(text.split())
        entity_count = len(entities)
        
        if word_count > 200:
            scores['detail'] = min(30, 15 + (entity_count / word_count) * 100)
        elif word_count > 100:
            scores['detail'] = 20
        else:
            scores['detail'] = 10
            scores['red_flags'].append('Short statement')
        
        # Check for emotional markers
        emotional_words = ['scared', 'terrified', 'angry', 'shocked', 'surprised', 
                          'nervous', 'calm', 'confused', 'certain', 'remember']
        for word in emotional_words:
            if word in text.lower():
                scores['emotional_markers'].append(word)
        
        # Check for red flags
        red_flags = {
            'vague': ['someone', 'something', 'somewhere', 'sometime'],
            'uncertain': ['maybe', 'perhaps', 'i think', 'possibly', 'might have'],
            'inconsistent': ['but then', 'actually', 'wait', 'no,'],
        }
        
        for flag_type, words in red_flags.items():
            for word in words:
                if word in text.lower():
                    scores['red_flags'].append(f"{flag_type}: '{word}'")
        
        # Consistency penalty for red flags
        consistency_penalty = len(scores['red_flags']) * 5
        scores['consistency'] = max(0, 100 - consistency_penalty)
        
        # Calculate overall
        scores['overall'] = (scores['detail'] * 0.4 + 
                            scores['consistency'] * 0.4 + 
                            scores['corroboration'] * 0.2)
        
        # Store in database
        self.db.update_credibility(witness_id, **scores)
        
        return scores
    
    def extract_timeline(self, text: str, witness_id: str, statement_id: int) -> List[Dict]:
        """Extract chronological events from statement"""
        events = []
        
        # Simple sentence-based extraction
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:
                continue
            
            # Look for temporal markers
            temporal = re.search(r'\b(then|after|before|when|while|during|first|next|finally)\b', 
                                sentence, re.IGNORECASE)
            
            if temporal:
                event = {
                    'description': sentence,
                    'witness_id': witness_id,
                    'temporal_marker': temporal.group(0)
                }
                events.append(event)
                
                # Add to database
                self.db.add_timeline_event(sentence, [witness_id], 
                                          event_type='witness_account',
                                          confidence=0.6)
        
        return events
    
    def detect_contradictions(self, entity_type: str = None):
        """Find contradictions between witness statements"""
        print(f"[*] Detecting contradictions...")
        
        contradictions = []
        
        # Get entities to compare
        if entity_type:
            entities = self.db.get_entities_by_type(entity_type)
        else:
            # Compare all major entity types
            entities = []
            for etype in ['PERSON', 'LOCATION', 'DATE', 'TIME']:
                entities.extend(self.db.get_entities_by_type(etype))
        
        # Group by entity type and value
        entity_map = defaultdict(lambda: defaultdict(list))
        for ent in entities:
            ent_type = ent[3]
            ent_value = ent[4].lower()
            witness_id = ent[2]
            entity_map[ent_type][ent_value].append(witness_id)
        
        # Find contradictory values
        for ent_type, values in entity_map.items():
            value_list = list(values.keys())
            for i, val_a in enumerate(value_list):
                for val_b in value_list[i+1:]:
                    # Different values from different witnesses
                    witnesses_a = values[val_a]
                    witnesses_b = values[val_b]
                    
                    for wa in witnesses_a:
                        for wb in witnesses_b:
                            # Check if it's a real contradiction
                            if val_a != val_b and not self._are_similar(val_a, val_b):
                                self.db.add_contradiction(
                                    wa, wb, ent_type, val_a, val_b,
                                    severity='medium', confidence=0.7
                                )
                                contradictions.append({
                                    'type': ent_type,
                                    'witness_a': wa, 'value_a': val_a,
                                    'witness_b': wb, 'value_b': val_b
                                })
        
        print(f"    [+] Found {len(contradictions)} contradictions")
        return contradictions
    
    def _are_similar(self, a: str, b: str) -> bool:
        """Check if two values are similar (not contradictory)"""
        a, b = a.lower(), b.lower()
        
        # Exact match
        if a == b:
            return True
        
        # One contains the other
        if a in b or b in a:
            return True
        
        # Check edit distance for typos
        if len(a) > 3 and len(b) > 3:
            diff = sum(c1 != c2 for c1, c2 in zip(a[:10], b[:10]))
            if diff <= 2:
                return True
        
        return False
    
    def find_convergence(self, min_witnesses: int = 2) -> List[Dict]:
        """Find points of agreement between witnesses"""
        print(f"[*] Finding convergence points (min {min_witnesses} witnesses)...")
        
        convergence = []
        
        # Get all entities
        for entity_type in ['PERSON', 'LOCATION', 'DATE', 'ACTION']:
            entities = self.db.get_entities_by_type(entity_type)
            
            # Group by value
            value_witnesses = defaultdict(set)
            for ent in entities:
                value = ent[4]
                witness = ent[2]
                value_witnesses[value].add(witness)
            
            # Find convergent values
            for value, witnesses in value_witnesses.items():
                if len(witnesses) >= min_witnesses:
                    self.db.add_convergence(entity_type, value, list(witnesses), 
                                           confidence=len(witnesses) * 0.1)
                    convergence.append({
                        'type': entity_type,
                        'value': value,
                        'witness_count': len(witnesses),
                        'witnesses': list(witnesses)
                    })
        
        convergence.sort(key=lambda x: x['witness_count'], reverse=True)
        print(f"    [+] Found {len(convergence)} convergence points")
        return convergence
    
    def build_cross_reference_matrix(self):
        """Build matrix showing relationships between all witness pairs"""
        print("[*] Building cross-reference matrix...")
        
        # Get all witnesses
        witnesses = self.db.cursor.execute("SELECT witness_id FROM witnesses").fetchall()
        witness_ids = [w[0] for w in witnesses]
        
        matrix = []
        
        for i, wa in enumerate(witness_ids):
            for wb in witness_ids[i+1:]:
                # Calculate relationship metrics
                metrics = self._calculate_witness_relationship(wa, wb)
                
                # Determine relationship type
                if metrics['agreement'] > 70:
                    rel_type = 'strong_corroboration'
                elif metrics['contradictions'] == 0:
                    rel_type = 'neutral'
                elif metrics['contradictions'] > 3:
                    rel_type = 'conflicting'
                else:
                    rel_type = 'partial_agreement'
                
                self.db.update_cross_reference(wa, wb, **metrics, relationship=rel_type)
                
                matrix.append({
                    'witness_a': wa,
                    'witness_b': wb,
                    **metrics,
                    'relationship': rel_type
                })
        
        print(f"    [+] Built matrix with {len(matrix)} relationships")
        return matrix
    
    def _calculate_witness_relationship(self, wa: str, wb: str) -> Dict:
        """Calculate relationship metrics between two witnesses"""
        # Get entities for each
        ents_a = self.db.get_witness_entities(wa)
        ents_b = self.db.get_witness_entities(wb)
        
        # Find common entities
        values_a = {e[4].lower() for e in ents_a}
        values_b = {e[4].lower() for e in ents_b}
        
        common = values_a & values_b
        all_values = values_a | values_b
        
        # Calculate agreement score
        if all_values:
            agreement = (len(common) / len(all_values)) * 100
        else:
            agreement = 0
        
        # Count contradictions
        contras = self.db.cursor.execute("""
            SELECT COUNT(*) FROM contradictions 
            WHERE (witness_a_id = ? AND witness_b_id = ?) 
               OR (witness_a_id = ? AND witness_b_id = ?)
        """, (wa, wb, wb, wa)).fetchone()[0]
        
        return {
            'agreement': agreement,
            'contradictions': contras,
            'corroborations': len(common),
            'similarity': len(common) / max(len(values_a), len(values_b), 1) * 100
        }
    
    def generate_report(self, output_path: str = None):
        """Generate comprehensive analysis report"""
        stats = self.db.get_statistics()
        
        report = []
        report.append("=" * 80)
        report.append("ENHANCED NARRATIVE ANALYSIS REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append(f"Database: {self.db.db_path}")
        report.append("")
        
        # Statistics
        report.append("DATABASE STATISTICS")
        report.append("-" * 40)
        for key, value in stats.items():
            if isinstance(value, dict):
                report.append(f"  {key}:")
                for k, v in value.items():
                    report.append(f"    {k}: {v}")
            else:
                report.append(f"  {key}: {value}")
        report.append("")
        
        # Top convergence
        report.append("TOP CONVERGENCE POINTS")
        report.append("-" * 40)
        conv = self.db.get_convergence(3)
        for c in conv[:10]:
            witnesses = json.loads(c[4])
            report.append(f"  {c[1]}: {c[2]} ({c[3]} witnesses: {', '.join(witnesses)})")
        report.append("")
        
        # Top contradictions
        report.append("CRITICAL CONTRADICTIONS")
        report.append("-" * 40)
        contras = self.db.get_contradictions()
        for c in contras[:10]:
            report.append(f"  [{c[6]}] {c[1]} vs {c[2]}: {c[4]} vs {c[5]}")
        report.append("")
        
        # Reliability tiers
        report.append("WITNESS RELIABILITY DISTRIBUTION")
        report.append("-" * 40)
        for tier, count in stats.get('tier_distribution', {}).items():
            bar = "█" * int(count / max(stats.get('witnesses', 1), 1) * 20)
            report.append(f"  {tier:20s} {bar} ({count})")
        
        report.append("")
        report.append("=" * 80)
        
        report_text = "\n".join(report)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"[+] Report saved to {output_path}")
        
        return report_text
    
    def export_json(self, output_path: str):
        """Export full analysis to JSON"""
        self.db.export_to_json(output_path)
    
    def close(self):
        """Clean up resources"""
        self.db.close()


def demo():
    """Demonstrate the enhanced analyzer"""
    analyzer = EnhancedNarrativeAnalyzer("demo_narrative.db")
    
    # Sample witness data
    witnesses = [
        {
            'id': 'W001',
            'name': 'John Smith',
            'statement': """I was at the bank on Main Street around 3 PM when I saw a man in a blue jacket. 
            He was holding a gun and demanded money from the teller. The suspect was about 6 feet tall 
            with dark hair. After taking the money, he ran out and got into a black sedan. 
            I was terrified but tried to remember details. The whole incident lasted about 2 minutes.""",
            'metadata': {'age': 45, 'occupation': 'Accountant', 'relationship': 'bystander'}
        },
        {
            'id': 'W002',
            'name': 'Sarah Johnson',
            'statement': """I work at the bank on Main Street. At approximately 3:15 PM, a man entered wearing a 
            blue jacket and dark pants. He approached the counter and showed me a weapon, I think it was a pistol. 
            He demanded cash from the drawer. He was tall, maybe 5'10 or 6 feet. After getting the money, 
            he ran outside. I saw him get into a dark colored car, possibly black or dark blue. 
            It was a sedan, I believe. I was very scared during the whole thing.""",
            'metadata': {'age': 32, 'occupation': 'Bank Teller', 'relationship': 'victim'}
        },
        {
            'id': 'W003',
            'name': 'Mike Davis',
            'statement': """I was parking my car outside the bank on Main when I saw a guy run out around 3 PM. 
            He was wearing a jacket, maybe blue or dark colored. He jumped into a black car and drove away fast. 
            I didn't see a weapon but he looked suspicious. I think the car was a sedan. 
            I couldn't get a good look at his face.""",
            'metadata': {'age': 28, 'occupation': 'Delivery Driver', 'relationship': 'bystander'}
        },
        {
            'id': 'W004',
            'name': 'Lisa Brown',
            'statement': """I was walking past the bank on Main Street at about 3:30 PM when I heard shouting. 
            I saw a man running out, he had something in his hand but I'm not sure what. 
            He got into a vehicle, maybe blue or black, and drove off. I was confused about what happened. 
            Maybe someone was hurt, I'm not certain.""",
            'metadata': {'age': 24, 'occupation': 'Student', 'relationship': 'bystander'}
        }
    ]
    
    print("=" * 80)
    print("ENHANCED NARRATIVE ANALYZER - DEMO")
    print("=" * 80)
    print(f"Processing {len(witnesses)} witness statements...\n")
    
    # Process each witness
    for w in witnesses:
        result = analyzer.process_witness(
            w['id'], w['name'], w['statement'], w['metadata']
        )
        print(f"  {w['id']} ({w['name']}): Credibility {result['credibility_score']:.1f}% [{result['reliability_tier']}]")
    
    print("\n[*] Detecting contradictions...")
    contradictions = analyzer.detect_contradictions()
    
    print("[*] Finding convergence points...")
    convergence = analyzer.find_convergence(min_witnesses=2)
    
    print("[*] Building cross-reference matrix...")
    matrix = analyzer.build_cross_reference_matrix()
    
    print("\n[*] Generating report...")
    report = analyzer.generate_report("demo_report.txt")
    print(report)
    
    print("\n[*] Exporting to JSON...")
    analyzer.export_json("demo_export.json")
    
    print("\n[+] Demo complete!")
    print(f"    Database: demo_narrative.db")
    print(f"    Report: demo_report.txt")
    print(f"    Export: demo_export.json")
    
    analyzer.close()


if __name__ == "__main__":
    demo()
