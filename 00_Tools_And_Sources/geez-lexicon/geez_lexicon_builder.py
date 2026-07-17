#!/usr/bin/env python3
"""
Ge'ez (Gəʿəz) Lexicon Builder
Builds a Ge'ez-English dictionary for liturgical and biblical texts
"""
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

# Core Ge'ez vocabulary - liturgical and biblical terms
# Based on Ethiopian Orthodox liturgy and biblical texts

GEEZ_CORE_VOCABULARY = {
    # Articles and Pronouns
    "ዘ": {"def": "which, who, that (relative pronoun)", "pos": "pronoun", "translit": "zə", "root": "z"},
    "ወ": {"def": "and, but", "pos": "conjunction", "translit": "wə", "root": "w"},
    "ሎ": {"def": "to him", "pos": "pronoun", "translit": "lo", "root": "l"},
    "ይ": {"def": "he/it (prefix)", "pos": "pronoun", "translit": "yə", "root": "y"},
    
    # Divine Names
    "አምላክ": {"def": "God", "pos": "noun", "translit": "amlāk", "root": "ʾ-l-k"},
    "እግዚአብሔር": {"def": "The Lord", "pos": "proper noun", "translit": "Ǝgziʾabəḥer", "root": "g-z-y"},
    "ኢየሱስ": {"def": "Jesus", "pos": "proper noun", "translit": "Iyesus", "root": "y-s-ʿ"},
    "ክርስቶስ": {"def": "Christ", "pos": "proper noun", "translit": "Krəstos", "root": "k-r-s"},
    "መንፈስ_ቅዱስ": {"def": "Holy Spirit", "pos": "proper noun", "translit": "Mänfäs qədus", "root": "n-f-s; q-d-s"},
    "ማርያም": {"def": "Mary", "pos": "proper noun", "translit": "Maryam", "root": "m-r-y"},
    "ጌታ": {"def": "Lord, Master", "pos": "noun", "translit": "Geta", "root": "g-t-y"},
    "አብ": {"def": "Father", "pos": "noun", "translit": "Ab", "root": "ʾ-b"},
    "ወልድ": {"def": "Son", "pos": "noun", "translit": "Wäld", "root": "w-l-d"},
    "ጸሎት": {"def": "prayer", "pos": "noun", "translit": "Ṣälot", "root": "ṣ-l-y"},
    
    # Common Nouns
    "ሰብእ": {"def": "man, human", "pos": "noun", "translit": "Səbʾ", "root": "s-b-ʾ"},
    "አንስት": {"def": "woman", "pos": "noun", "translit": "ʾAnəst", "root": "ʾ-n-s"},
    "ወለድ": {"def": "child, son", "pos": "noun", "translit": "Wälad", "root": "w-l-d"},
    "ቤተ": {"def": "house", "pos": "noun", "translit": "Bet", "root": "b-y-t"},
    "መንግሥት": {"def": "kingdom, reign", "pos": "noun", "translit": "Mängəśt", "root": "n-g-ś"},
    "ንጉሥ": {"def": "king", "pos": "noun", "translit": "Nəguś", "root": "n-g-ś"},
    "ነፍስ": {"def": "soul, breath", "pos": "noun", "translit": "Näfs", "root": "n-f-s"},
    "ስጋ": {"def": "flesh, body", "pos": "noun", "translit": "Səga", "root": "s-g-w"},
    "ደም": {"def": "blood", "pos": "noun", "translit": "Däm", "root": "d-m-m"},
    "ልብ": {"def": "heart", "pos": "noun", "translit": "Ləb", "root": "l-b-b"},
    "አእምሮ": {"def": "mind, intellect", "pos": "noun", "translit": "ʾAəmro", "root": "ʾ-m-r"},
    "ፍኖተ": {"def": "way, road", "pos": "noun", "translit": "Fənot", "root": "f-n-y"},
    "ብርሃን": {"def": "light", "pos": "noun", "translit": "Bərhan", "root": "b-r-h-n"},
    "ጸለመት": {"def": "darkness", "pos": "noun", "translit": "Ṣälamät", "root": "ṣ-l-m"},
    "ሰማይ": {"def": "heaven, sky", "pos": "noun", "translit": "Samay", "root": "s-m-y"},
    "ምድር": {"def": "earth, land", "pos": "noun", "translit": "Mədər", "root": "m-d-r"},
    "ውሃ": {"def": "water", "pos": "noun", "translit": "Wəha", "root": "w-h-y"},
    "እሳት": {"def": "fire", "pos": "noun", "translit": "ʾƏsat", "root": "ʾ-s-y"},
    "ዛፍ": {"def": "tree", "pos": "noun", "translit": "Zaf", "root": "z-f-f"},
    "ብር": {"def": "silver, money", "pos": "noun", "translit": "Bər", "root": "b-r-r"},
    "ወርቅ": {"def": "gold", "pos": "noun", "translit": "Wärq", "root": "w-r-q"},
    
    # Verbs
    "በለ": {"def": "to say, speak", "pos": "verb", "translit": "Bäla", "root": "b-l-y"},
    "ነበረ": {"def": "to be, exist", "pos": "verb", "translit": "Näbärä", "root": "n-b-r"},
    "ወረደ": {"def": "to descend, go down", "pos": "verb", "translit": "Wärädä", "root": "w-r-d"},
    "ዐለ": {"def": "to ascend, go up", "pos": "verb", "translit": "ʿƏla", "root": "ʿ-l-y"},
    "ሞተ": {"def": "to die", "pos": "verb", "translit": "Motä", "root": "m-w-t"},
    "ኖረ": {"def": "to live, dwell", "pos": "verb", "translit": "Nora", "root": "n-w-r"},
    "ሐየ": {"def": "to see", "pos": "verb", "translit": "Ḥäya", "root": "ḥ-y-y"},
    "ሰምዐ": {"def": "to hear", "pos": "verb", "translit": "Sämʿa", "root": "s-m-ʿ"},
    "አግዐዘ": {"def": "to rise, stand up", "pos": "verb", "translit": "ʾAgʿäza", "root": "ʾ-g-z"},
    "ቆመ": {"def": "to stand", "pos": "verb", "translit": "Qoma", "root": "q-w-m"},
    "አመነ": {"def": "to believe, trust", "pos": "verb", "translit": "ʾAmäna", "root": "ʾ-m-n"},
    "ፈረየ": {"def": "to judge", "pos": "verb", "translit": "Färäya", "root": "f-r-y"},
    "ጸለየ": {"def": "to pray", "pos": "verb", "translit": "Ṣälaya", "root": "ṣ-l-y"},
    "ሐከየ": {"def": "to love", "pos": "verb", "translit": "Ḥäkaya", "root": "ḥ-k-y"},
    "በዘወ": {"def": "to do, make", "pos": "verb", "translit": "Bäzäwa", "root": "b-z-y"},
    "ተቀበለ": {"def": "to receive, accept", "pos": "verb", "translit": "Täqäbalä", "root": "q-b-l"},
    "ሰደደ": {"def": "to send", "pos": "verb", "translit": "Sädäda", "root": "s-d-d"},
    "ወጠነ": {"def": "to begin", "pos": "verb", "translit": "Wäṭäna", "root": "w-ṭ-n"},
    
    # Adjectives
    "ቅዱስ": {"def": "holy", "pos": "adjective", "translit": "Qədus", "root": "q-d-s"},
    "ጻድቅ": {"def": "righteous, just", "pos": "adjective", "translit": "Ṣadəq", "root": "ṣ-d-q"},
    "ኅሩይ": {"def": "beloved", "pos": "adjective", "translit": "Ḫəruy", "root": "ḫ-r-y"},
    "ሐሳየ": {"def": "merciful", "pos": "adjective", "translit": "Ḥasaya", "root": "ḥ-s-y"},
    "ብዙኅ": {"def": "many, much", "pos": "adjective", "translit": "Bəzuḫ", "root": "b-z-ḫ"},
    "ትንሹ": {"def": "small, little", "pos": "adjective", "translit": "Tənišu", "root": "t-n-š"},
    "ዓቢይ": {"def": "great, big", "pos": "adjective", "translit": "ʿAbiy", "root": "ʿ-b-y"},
    "ረቂቅ": {"def": "thin, fine", "pos": "adjective", "translit": "Räqiq", "root": "r-q-q"},
    "ጥብጥበ": {"def": "thick, dense", "pos": "adjective", "translit": "Ṭəbtäbä", "root": "ṭ-b-b"},
    "ጽቡሕ": {"def": "beautiful", "pos": "adjective", "translit": "Ṣəbuḥ", "root": "ṣ-b-ḥ"},
    
    # Prepositions
    "እም": {"def": "from, out of", "pos": "preposition", "translit": "Əm", "root": "m"},
    "ከመ": {"def": "as, like", "pos": "preposition", "translit": "Käma", "root": "k-m"},
    "በ": {"def": "in, with, by", "pos": "preposition", "translit": "Ba", "root": "b"},
    "ለ": {"def": "to, for", "pos": "preposition", "translit": "Lä", "root": "l"},
    "ቅድመ": {"def": "before", "pos": "preposition", "translit": "Qədma", "root": "q-d-m"},
    "ድኅረ": {"def": "after", "pos": "preposition", "translit": "Dəḫrä", "root": "d-ḫ-r"},
    "ላዕለ": {"def": "upon, over", "pos": "preposition", "translit": "Laʿlä", "root": "l-ʿ-l"},
    "ትሕቴ": {"def": "under, beneath", "pos": "preposition", "translit": "Təḥtä", "root": "t-ḥ-t"},
    
    # Numbers
    "አሐዱ": {"def": "one", "pos": "numeral", "translit": "ʾAḥadu", "root": "ʾ-ḥ-d"},
    "ክልኤ": {"def": "two", "pos": "numeral", "translit": "Kəleʾ", "root": "k-l-ʾ"},
    "ሣልስ": {"def": "three", "pos": "numeral", "translit": "Śaləs", "root": "ś-l-s"},
    "አርባዕ": {"def": "four", "pos": "numeral", "translit": "ʾArbaʿ", "root": "ʾ-r-b-ʿ"},
    "ኀምስ": {"def": "five", "pos": "numeral", "translit": "Ḫaməs", "root": "ḫ-m-s"},
    
    # Liturgical Terms
    "መጽሐፍ": {"def": "book, scripture", "pos": "noun", "translit": "Mäṣḥaf", "root": "ṣ-ḥ-f"},
    "ትምህርት": {"def": "teaching, doctrine", "pos": "noun", "translit": "Təməhərt", "root": "m-h-r"},
    "በዓል": {"def": "feast, festival", "pos": "noun", "translit": "Baʿal", "root": "b-ʿ-l"},
    "ጾም": {"def": "fast, fasting", "pos": "noun", "translit": "Ṣom", "root": "ṣ-w-m"},
    "መስዓል": {"def": "crucifixion", "pos": "noun", "translit": "Mäśʿal", "root": "ś-ʿ-l"},
    "ትንሣኤ": {"def": "resurrection", "pos": "noun", "translit": "Tənsaʾe", "root": "n-ś-ʾ"},
    "ወንጌል": {"def": "gospel", "pos": "noun", "translit": "Wänagäl", "root": "n-g-l"},
    "ሥላሴ": {"def": "Trinity", "pos": "noun", "translit": "Śəllase", "root": "ś-l-s"},
    "ወርኅ": {"def": "month, moon", "pos": "noun", "translit": "Wärḫ", "root": "w-r-ḫ"},
    "ዓመት": {"def": "year", "pos": "noun", "translit": "ʿAmät", "root": "ʿ-m-t"},
    "እሑድ": {"def": "Sunday", "pos": "noun", "translit": "ʾƏhud", "root": "ʾ-h-d"},
    "ሰንበተ": {"def": "Sabbath", "pos": "noun", "translit": "Sänbät", "root": "s-b-t"},
    
    # Abstract Concepts
    "ፍቅር": {"def": "love", "pos": "noun", "translit": "Fəqər", "root": "f-q-r"},
    "ሃይማኖት": {"def": "faith", "pos": "noun", "translit": "Haymanot", "root": "h-m-n"},
    "ትዕዛዝ": {"def": "commandment", "pos": "noun", "translit": "Təʿzaz", "root": "ʿ-w-z"},
    "ኀጢአት": {"def": "sin", "pos": "noun", "translit": "Ḫaṭiʾat", "root": "ḫ-ṭ-ʾ"},
    "ሥርዓት": {"def": "law, ordinance", "pos": "noun", "translit": "Śərʿat", "root": "ś-r-ʿ"},
    "ሞት": {"def": "death", "pos": "noun", "translit": "Mot", "root": "m-w-t"},
    "ሕይወት": {"def": "life", "pos": "noun", "translit": "Ḥəywät", "root": "ḥ-y-w"},
    "ጥበብ": {"def": "wisdom", "pos": "noun", "translit": "Ṭəbab", "root": "ṭ-b-b"},
    "ኅድገት": {"def": "mercy", "pos": "noun", "translit": "Ḫədqät", "root": "ḫ-d-q"},
    
    # Apostles/Saints
    "ጴጥሮስ": {"def": "Peter", "pos": "proper noun", "translit": "Peṭros", "root": "p-ṭ-r"},
    "ጳውሎስ": {"def": "Paul", "pos": "proper noun", "translit": "Ṗawlos", "root": "p-w-l"},
    "ዮሐንስ": {"def": "John", "pos": "proper noun", "translit": "Yohannəs", "root": "y-ḥ-n"},
    "ማቴዎስ": {"def": "Matthew", "pos": "proper noun", "translit": "Matewos", "root": "m-t-w"},
    "ማርቆስ": {"def": "Mark", "pos": "proper noun", "translit": "Marqos", "root": "m-r-q"},
    "ሉቃስ": {"def": "Luke", "pos": "proper noun", "translit": "Luqas", "root": "l-q-s"},
    "ሐዋርያ": {"def": "apostle", "pos": "noun", "translit": "Ḥawarya", "root": "ḥ-w-r"},
    "ቅዱስ": {"def": "saint", "pos": "noun", "translit": "Qədus", "root": "q-d-s"},
}

# Extended vocabulary
GEEZ_EXTENDED_VOCABULARY = {
    # More body parts
    "ራስ": {"def": "head", "pos": "noun", "translit": "Ras", "root": "r-ʾ-s"},
    "አንገት": {"def": "neck", "pos": "noun", "translit": "ʾAngät", "root": "ʾ-n-g"},
    "እጅ": {"def": "hand", "pos": "noun", "translit": "ʾƏǧ", "root": "ʾ-ǧ"},
    "እግር": {"def": "foot, leg", "pos": "noun", "translit": "ʾƏgr", "root": "ʾ-g-r"},
    "ዓይን": {"def": "eye", "pos": "noun", "translit": "ʿAyn", "root": "ʿ-y-n"},
    "እዝኒ": {"def": "ear", "pos": "noun", "translit": "ʾƏzni", "root": "ʾ-z-n"},
    "አፍ": {"def": "mouth", "pos": "noun", "translit": "Af", "root": "ʾ-f"},
    "እስት": {"def": "belly, stomach", "pos": "noun", "translit": "ʾƏst", "root": "ʾ-s-t"},
    
    # More nature
    "ደብር": {"def": "mountain", "pos": "noun", "translit": "Däbr", "root": "d-b-r"},
    "ሀይቅ": {"def": "sea, lake", "pos": "noun", "translit": "Hayq", "root": "h-y-q"},
    "ወአብ": {"def": "river", "pos": "noun", "translit": "Wäʾb", "root": "w-ʾ-b"},
    "ሐመድ": {"def": "desert, wilderness", "pos": "noun", "translit": "Ḥamäd", "root": "ḥ-m-d"},
    "አየር": {"def": "air, wind", "pos": "noun", "translit": "ʾAyyär", "root": "ʾ-y-r"},
    "ዝናም": {"def": "rain", "pos": "noun", "translit": "Zənām", "root": "z-n-m"},
    
    # Animals
    "ላም": {"def": "cow, cattle", "pos": "noun", "translit": "Lam", "root": "l-m"},
    "ከብት": {"def": "cattle, livestock", "pos": "noun", "translit": "Käbt", "root": "k-b-t"},
    "በግዕ": {"def": "sheep", "pos": "noun", "translit": "Bägʿ", "root": "b-g-ʿ"},
    "ፍድል": {"def": "goat", "pos": "noun", "translit": "Fədl", "root": "f-d-l"},
    "አነብስ": {"def": "leopard", "pos": "noun", "translit": "ʾAnäbs", "root": "ʾ-n-b-s"},
    "አውራሪስ": {"def": "eagle", "pos": "noun", "translit": "ʾAwərraris", "root": "ʾ-w-r"},
    
    # Food/Drink
    "ኅብስተ": {"def": "bread", "pos": "noun", "translit": "Ḫəbstä", "root": "ḫ-b-s"},
    "ወይን": {"def": "wine, grape", "pos": "noun", "translit": "Wäyn", "root": "w-y-n"},
    "ተለአለ": {"def": "oil", "pos": "noun", "translit": "Tälaʾälä", "root": "l-ʾ"},
    "ማህያ": {"def": "honey", "pos": "noun", "translit": "Mahya", "root": "m-h-y"},
    
    # Materials
    "ዕፅ": {"def": "wood, tree", "pos": "noun", "translit": "ʿƏḍ", "root": "ʿ-ḍ"},
    "አብን": {"def": "stone", "pos": "noun", "translit": "ʾAbn", "root": "ʾ-b-n"},
    "ብሩር": {"def": "iron", "pos": "noun", "translit": "Bərur", "root": "b-r-r"},
    "ናስ": {"def": "brass, copper", "pos": "noun", "translit": "Nas", "root": "n-s"},
    
    # Colors
    "ቀይር": {"def": "red", "pos": "adjective", "translit": "Qäyər", "root": "q-y-r"},
    "ጻዕዳ": {"def": "white", "pos": "adjective", "translit": "Ṣaʿda", "root": "ṣ-ʿ-d"},
    "ክሩም": {"def": "black", "pos": "adjective", "translit": "Kərum", "root": "k-r-m"},
    "ሳበላ": {"def": "green", "pos": "adjective", "translit": "Säbala", "root": "s-b-l"},
    
    # Actions
    "ሐየደ": {"def": "to run", "pos": "verb", "translit": "Ḥäyadä", "root": "ḥ-y-d"},
    "ሐረመ": {"def": "to sit", "pos": "verb", "translit": "Ḥärämä", "root": "ḥ-r-m"},
    "ነፈወ": {"def": "to fly", "pos": "verb", "translit": "Näfäwa", "root": "n-f-w"},
    "ሐመ": {"def": "to be sick", "pos": "verb", "translit": "Ḥäma", "root": "ḥ-m-m"},
    "ሐወረ": {"def": "to plow", "pos": "verb", "translit": "Ḥäwärä", "root": "ḥ-w-r"},
    
    # Social
    "ሥዩመ": {"def": "name", "pos": "noun", "translit": "Śəyuma", "root": "ś-w-m"},
    "አርድእት": {"def": "friend", "pos": "noun", "translit": "ʾArdəʾt", "root": "ʾ-r-d"},
    "ጠቢብ": {"def": "wise person", "pos": "noun", "translit": "Ṭäbib", "root": "ṭ-b-b"},
    "ሰራዊት": {"def": "army, host", "pos": "noun", "translit": "Särawit", "root": "s-r-w"},
    "መካን": {"def": "place", "pos": "noun", "translit": "Mäkan", "root": "m-k-n"},
    
    # Time
    "ሰዓት": {"def": "hour, time", "pos": "noun", "translit": "Saʿat", "root": "s-ʿ-t"},
    "ጎዳት": {"def": "morning", "pos": "noun", "translit": "Godat", "root": "g-d-t"},
    "ሠርክ": {"def": "evening", "pos": "noun", "translit": "Śärk", "root": "ś-r-k"},
    "ሌሊት": {"def": "night", "pos": "noun", "translit": "Lelit", "root": "l-l-t"},
    
    # Qualities
    "ጥቀ": {"def": "near", "pos": "adjective", "translit": "Ṭəqä", "root": "ṭ-q-y"},
    "ሩዓቅ": {"def": "far", "pos": "adjective", "translit": "Ruʿaq", "root": "r-ʿ-q"},
    "መልአ": {"def": "full", "pos": "adjective", "translit": "Mälaʾ", "root": "m-l-ʾ"},
    "ረባሕ": {"def": "empty", "pos": "adjective", "translit": "Räbaḥ", "root": "r-b-ḥ"},
    "ጣዕረ": {"def": "sweet", "pos": "adjective", "translit": "Ṭaʿrä", "root": "ṭ-ʿ-r"},
    "መርሐ": {"def": "bitter", "pos": "adjective", "translit": "Marḥa", "root": "m-r-ḥ"},
    "ጣኒ": {"def": "narrow", "pos": "adjective", "translit": "Ṭani", "root": "ṭ-n-y"},
    "ሳዕበ": {"def": "wide", "pos": "adjective", "translit": "Saʿbä", "root": "s-ʿ-b"},
    
    # Directions
    "ሰማይ_መልዓ": {"def": "east", "pos": "noun", "translit": "Samay Mälaʿ", "root": "s-m-y; ʿ-l-y"},
    "ሰማይ_ይነዘር": {"def": "west", "pos": "noun", "translit": "Samay Yənäzär", "root": "s-m-y; n-z-r"},
    "ጸደና": {"def": "north", "pos": "noun", "translit": "Ṣädäna", "root": "ṣ-d-n"},
    "ደቡብ": {"def": "south", "pos": "noun", "translit": "Däbub", "root": "d-b-b"},
}

class GeezLexicon:
    """Ge'ez-English lexicon"""
    
    def __init__(self):
        self.entries = {}
        self.root_index = defaultdict(list)
        
    def build(self):
        """Build lexicon from vocabulary lists"""
        print("[*] Building Ge'ez lexicon...")
        
        # Combine vocabularies
        all_vocab = {**GEEZ_CORE_VOCABULARY, **GEEZ_EXTENDED_VOCABULARY}
        
        for word, data in all_vocab.items():
            entry = {
                "word": word,
                "definition": data["def"],
                "part_of_speech": data["pos"],
                "transliteration": data["translit"],
                "root": data["root"]
            }
            
            self.entries[word] = entry
            
            # Index by root
            if data["root"]:
                for root_part in data["root"].split(";"):
                    self.root_index[root_part.strip()].append(word)
        
        print(f"    [+] Built {len(self.entries)} entries")
        
    def export_json(self, output_path: str):
        """Export to JSON"""
        print(f"[*] Exporting to {output_path}...")
        
        data = {
            "metadata": {
                "title": "Ge'ez (Gəʿəz) Lexicon",
                "language": "Ge'ez (Classical Ethiopic)",
                "script": "Ethiopic (Fidel)",
                "period": "Classical Ge'ez (100-900 CE), Liturgical (to present)",
                "total_entries": len(self.entries),
                "format": "JSON",
                "notes": "Liturgical language of Ethiopian Orthodox Tewahedo Church. Ethiopian Bible has 81 books (most complete canon)."
            },
            "entries": self.entries,
            "root_index": dict(self.root_index)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"    [+] Exported {len(self.entries)} entries")
    
    def export_markdown(self, output_path: str):
        """Export to Markdown"""
        print(f"[*] Exporting markdown to {output_path}...")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Ge'ez (Gəʿəz) Lexicon\n\n")
            f.write("**Ge'ez-English Dictionary (Classical Ethiopic)**\n\n")
            f.write(f"Total Entries: {len(self.entries)}\n\n")
            f.write("---\n\n")
            
            # Sort by Ge'ez word
            sorted_entries = sorted(self.entries.items(), key=lambda x: x[0])
            
            for word, entry in sorted_entries:
                f.write(f"## {word}\n\n")
                f.write(f"**Transliteration:** *{entry['transliteration']}*\n\n")
                f.write(f"**Part of Speech:** {entry['part_of_speech']}\n\n")
                f.write(f"**Definition:** {entry['definition']}\n\n")
                if entry['root']:
                    f.write(f"**Root:** {entry['root']}\n\n")
                f.write("---\n\n")
        
        print(f"    [+] Exported {len(self.entries)} entries")
    
    def export_websters_style(self, output_path: str):
        """Export in Webster's dictionary format"""
        print(f"[*] Exporting Webster's style to {output_path}...")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("GE'EZ (GƏʿƏZ) LEXICON\n")
            f.write("Classical Ethiopic Dictionary\n")
            f.write("Liturgical Language of Ethiopian Christianity\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("About Ge'ez:\n")
            f.write("  - Ancient South Semitic language\n")
            f.write("  - Liturgical language of Ethiopian Orthodox Church\n")
            f.write("  - Ethiopian Bible: 81 books (most complete canon)\n")
            f.write("  - Written in Ethiopic script (Fidel)\n")
            f.write("  - Triliteral root system (like Hebrew and Arabic)\n\n")
            
            f.write("Pronunciation Guide:\n")
            f.write("  አ (ʾ) = glottal stop or silent\n")
            f.write("  ኀ (ḫ) = voiceless pharyngeal fricative\n")
            f.write("  ዐ (ʿ) = voiced pharyngeal fricative\n")
            f.write("  ጸ (ṣ) = emphatic s\n")
            f.write("  ፀ (ḍ) = emphatic ts\n")
            f.write("  ጰ (ṗ) = emphatic p\n\n")
            
            f.write("-" * 70 + "\n\n")
            
            sorted_entries = sorted(self.entries.items(), key=lambda x: x[0])
            
            for word, entry in sorted_entries:
                f.write(f"\n{word}")
                if entry['transliteration']:
                    f.write(f"  ({entry['transliteration']})")
                
                f.write(f"  [{entry['part_of_speech']}]")
                f.write("\n")
                
                # Definition
                f.write(f"    {entry['definition']}\n")
                
                # Root
                if entry['root']:
                    f.write(f"    Root: {entry['root']}\n")
                
                f.write("\n")
        
        print(f"    [+] Exported {len(self.entries)} entries")
    
    def search(self, query: str) -> list:
        """Search the lexicon"""
        results = []
        query_lower = query.lower()
        
        for word, entry in self.entries.items():
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


def main():
    lexicon = GeezLexicon()
    
    # Build from vocabulary
    lexicon.build()
    
    # Create output directory
    out_dir = Path("/root/geez_lexicon_output")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Export all formats
    lexicon.export_json(out_dir / "geez_lexicon.json")
    lexicon.export_markdown(out_dir / "geez_lexicon.md")
    lexicon.export_websters_style(out_dir / "websters_geez.txt")
    
    # Sample entries
    print("\n" + "=" * 70)
    print("SAMPLE ENTRIES")
    print("=" * 70 + "\n")
    
    sample_words = ['አምላክ', 'ኢየሱስ', 'ቅዱስ', 'ፍቅር', 'ሐየየ', 'ሰማይ']
    for word in sample_words:
        if word in lexicon.entries:
            e = lexicon.entries[word]
            print(f"{word} ({e['transliteration']})")
            print(f"  {e['definition']}")
            print(f"  [{e['part_of_speech']}] Root: {e['root']}\n")
    
    print("=" * 70)
    print("GE'EZ LEXICON COMPLETE")
    print("=" * 70)
    print(f"\nOutput files in {out_dir.absolute()}:")
    print(f"  - geez_lexicon.json (full)")
    print(f"  - geez_lexicon.md (human-readable)")
    print(f"  - websters_geez.txt (Webster's style)")
    print(f"\nTo search: python search_geez.py <word>")
    print("\nNOTE: This is a seed lexicon. For complete coverage,")
    print("add Leslau's Comparative Dictionary of Ge'ez (10,000+ entries)")


if __name__ == "__main__":
    main()
