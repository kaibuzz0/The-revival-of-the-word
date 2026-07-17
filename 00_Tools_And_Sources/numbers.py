#!/usr/bin/env python3
"""
Enhanced Numerology & Gematria Module
Biblical numerology and Hebrew/Aramaic letter-number analysis
Part of The Revival of the Word project
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Union


# =============================================================================
# MASTER NUMBERS AND CONSTANTS
# =============================================================================

MASTER_NUMBERS = {11, 22, 33}
KARMIC_DEBT_NUMBERS = {13, 14, 16, 19}
BIBLICAL_SIGNIFICANCE = {
    1: {"meaning": "Unity, God, Beginnings", "references": ["Deut 6:4", "Gen 1:1"]},
    2: {"meaning": "Division, Witness, Duality", "references": ["Gen 1:6-7", "Matt 18:16"]},
    3: {"meaning": "Divine Perfection, Trinity", "references": ["Matt 28:19", "1 John 5:7"]},
    4: {"meaning": "Creation, Earth, World", "references": ["Gen 1:14-19", "Rev 7:1"]},
    5: {"meaning": "Grace, Torah, Pentateuch", "references": ["Gen 1:20-23", "Ex 34:28"]},
    6: {"meaning": "Man, Sin, Imperfection", "references": ["Gen 1:26-31", "Rev 13:18"]},
    7: {"meaning": "Perfection, Sabbath, Completion", "references": ["Gen 2:2-3", "Rev 1:20"]},
    8: {"meaning": "New Beginnings, Resurrection", "references": ["Gen 17:12", "1 Peter 3:20"]},
    9: {"meaning": "Finality, Fruit of Spirit", "references": ["Gal 5:22-23", "Rev 21:9-21"]},
    10: {"meaning": "Completeness, Commandments", "references": ["Ex 34:28", "Rev 2:10"]},
    12: {"meaning": "Government, Tribes, Apostles", "references": ["Gen 49:28", "Matt 10:1-4"]},
    13: {"meaning": "Rebellion, Depravity", "references": ["Gen 14:4", "Mark 7:21-23"]},
    40: {"meaning": "Testing, Trial, Preparation", "references": ["Gen 7:4", "Matt 4:2"]},
    70: {"meaning": "Nations, Elders, Completion", "references": ["Gen 10", "Ex 24:1"]},
    153: {"meaning": "Abundance, Harvest", "references": ["John 21:11"]},
    666: {"meaning": "Number of the Beast", "references": ["Rev 13:18"]},
    777: {"meaning": "Divine Perfection Tripled", "references": ["Spiritual significance"]},
    1000: {"meaning": "Completeness, Millennium", "references": ["Rev 20:1-7"]},
}


# =============================================================================
# NUMEROLOGY FUNCTIONS
# =============================================================================

def reduce_to_single_digit(number: int, allow_master: bool = True) -> int:
    """
    Reduce a number to a single digit unless it's a master number (11, 22, 33).
    
    Args:
        number: Number to reduce
        allow_master: Whether to preserve master numbers
    
    Returns:
        Reduced number
    """
    if number < 0:
        number = abs(number)
    
    while number > 9:
        if allow_master and number in MASTER_NUMBERS:
            return number
        number = sum(int(digit) for digit in str(number))
    
    return number


def extract_digits(input_str: str) -> List[int]:
    """Extract all digits from a string."""
    return [int(char) for char in input_str if char.isdigit()]


def numerology_value(char: str) -> int:
    """
    Calculate Pythagorean numerology value of a character.
    A=1, B=2, C=3, ..., I=9, J=1, K=2, etc.
    """
    if not char.isalpha():
        return 0
    
    # Pythagorean numerology: 1-9 repeating
    position = (ord(char.upper()) - ord('A')) % 9 + 1
    return position


def chaldean_value(char: str) -> int:
    """
    Calculate Chaldean numerology value (alternative system).
    Different letter values based on vibration.
    """
    chaldean_mapping = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'U': 6, 'O': 7, 'F': 8,
        'I': 1, 'R': 2, 'Z': 7, 'K': 2, 'G': 3, 'M': 4, 'H': 5, 'V': 6,
        'P': 7, 'Y': 1, 'J': 1, 'L': 3, 'T': 4, 'N': 5, 'W': 6, 'Q': 1,
        'S': 3, 'X': 5
    }
    return chaldean_mapping.get(char.upper(), 0)


# =============================================================================
# NAME CALCULATIONS
# =============================================================================

def calculate_name_values(name: str, system: str = "pythagorean") -> Tuple[List[int], int]:
    """
    Calculate values for a name.
    
    Args:
        name: Full name
        system: 'pythagorean' or 'chaldean'
    
    Returns:
        Tuple of (letter_values, reduced_total)
    """
    if system == "chaldean":
        letter_values = [chaldean_value(char) for char in name if char.isalpha()]
    else:
        letter_values = [numerology_value(char) for char in name if char.isalpha()]
    
    return letter_values, reduce_to_single_digit(sum(letter_values))


def calculate_expression_number(name: str, system: str = "pythagorean") -> int:
    """
    Expression Number - full name reduced.
    Represents natural talents and abilities.
    """
    return calculate_name_values(name, system)[1]


def calculate_soul_urge(name: str) -> int:
    """
    Soul Urge / Heart's Desire - vowels only.
    Represents inner desires and motivations.
    """
    vowels = set("AEIOUY")
    total = sum(numerology_value(char) for char in name if char.upper() in vowels)
    return reduce_to_single_digit(total)


def calculate_personality_number(name: str) -> int:
    """
    Personality Number - consonants only.
    Represents outward personality and first impressions.
    """
    vowels = set("AEIOUY")
    total = sum(numerology_value(char) for char in name 
                if char.isalpha() and char.upper() not in vowels)
    return reduce_to_single_digit(total)


def calculate_cornerstone(name: str) -> int:
    """First letter of first name - approach to life."""
    if not name:
        return 0
    first_letter = name[0]
    return numerology_value(first_letter) if first_letter.isalpha() else 0


def calculate_capstone(name: str) -> int:
    """Last letter of first name - ability to finish."""
    if not name:
        return 0
    first_word = name.split()[0] if name.split() else name
    last_letter = first_word[-1]
    return numerology_value(last_letter) if last_letter.isalpha() else 0


def calculate_first_vowel(name: str) -> Optional[int]:
    """First vowel in name - inner self."""
    vowels = set("AEIOU")
    for char in name:
        if char.upper() in vowels:
            return numerology_value(char)
    return None


def calculate_karmic_lessons(name: str) -> List[int]:
    """
    Numbers 1-9 missing from the name.
    Areas where growth is needed.
    """
    present_values = set()
    for char in name:
        if char.isalpha():
            present_values.add(numerology_value(char))
    
    all_values = set(range(1, 10))
    return sorted(list(all_values - present_values))


def calculate_hidden_passion(name: str) -> int:
    """
    Number appearing most frequently in name.
    Special strength or talent.
    """
    from collections import Counter
    
    values = [numerology_value(char) for char in name if char.isalpha()]
    if not values:
        return 0
    
    counter = Counter(values)
    most_common = counter.most_common(1)[0][0]
    return most_common


def calculate_subconscious_self(name: str) -> int:
    """
    Number of different values present in name.
    Confidence and self-esteem indicator.
    """
    unique_values = set()
    for char in name:
        if char.isalpha():
            unique_values.add(numerology_value(char))
    
    return len(unique_values)


def calculate_balance_number(name: str) -> int:
    """
    Sum of initials reduced.
    Guidance for conflict resolution.
    """
    initials = [part[0] for part in name.split() if part]
    total = sum(numerology_value(char) for char in initials if char.isalpha())
    return reduce_to_single_digit(total)


# =============================================================================
# BIRTH DATE CALCULATIONS
# =============================================================================

def calculate_life_path(birthdate: str) -> int:
    """
    Life Path Number - sum of all birth date digits reduced.
    Represents life's purpose and path.
    """
    digits = extract_digits(birthdate)
    return reduce_to_single_digit(sum(digits))


def calculate_birthday_number(birthdate: str) -> int:
    """
    Birthday Number - day of birth reduced.
    Represents specific talents for this life.
    """
    try:
        day = int(birthdate.split('/')[1])
        return reduce_to_single_digit(day)
    except (IndexError, ValueError):
        return 0


def calculate_maturity_number(life_path: int, expression: int) -> int:
    """
    Maturity Number - sum of Life Path and Expression.
    Represents later life development.
    """
    return reduce_to_single_digit(life_path + expression)


def calculate_challenge_numbers(birthdate: str) -> List[int]:
    """
    Four challenge numbers representing life obstacles.
    """
    try:
        parts = birthdate.split('/')
        month = int(parts[0])
        day = int(parts[1])
        year = int(parts[2])
        
        month_reduced = reduce_to_single_digit(month)
        day_reduced = reduce_to_single_digit(day)
        year_reduced = reduce_to_single_digit(sum(int(d) for d in str(year)))
        
        # Four challenges
        challenge_1 = abs(month_reduced - day_reduced)
        challenge_2 = abs(day_reduced - year_reduced)
        challenge_3 = abs(challenge_1 - challenge_2)
        challenge_4 = abs(month_reduced - year_reduced)
        
        return [challenge_1, challenge_2, challenge_3, challenge_4]
    except (IndexError, ValueError):
        return [0, 0, 0, 0]


def calculate_pinnacle_numbers(birthdate: str) -> List[int]:
    """
    Four pinnacle numbers representing life cycles.
    """
    try:
        parts = birthdate.split('/')
        month = int(parts[0])
        day = int(parts[1])
        year = int(parts[2])
        
        month_reduced = reduce_to_single_digit(month)
        day_reduced = reduce_to_single_digit(day)
        year_reduced = reduce_to_single_digit(sum(int(d) for d in str(year)))
        
        # Four pinnacles
        pinnacle_1 = reduce_to_single_digit(month_reduced + day_reduced)
        pinnacle_2 = reduce_to_single_digit(day_reduced + year_reduced)
        pinnacle_3 = reduce_to_single_digit(pinnacle_1 + pinnacle_2)
        pinnacle_4 = reduce_to_single_digit(month_reduced + year_reduced)
        
        return [pinnacle_1, pinnacle_2, pinnacle_3, pinnacle_4]
    except (IndexError, ValueError):
        return [0, 0, 0, 0]


def calculate_age_digit(birthdate: str) -> int:
    """
    Current age reduced to single digit.
    Annual vibration.
    """
    try:
        from datetime import datetime
        birth_year = int(birthdate.split('/')[2])
        current_year = datetime.now().year
        age = current_year - birth_year
        return reduce_to_single_digit(age)
    except (IndexError, ValueError):
        return 0


def calculate_personal_year(life_path: int, current_year: int) -> int:
    """Annual cycle number based on life path."""
    return reduce_to_single_digit(life_path + current_year)


def calculate_personal_month(personal_year: int, current_month: int) -> int:
    """Monthly vibration within the personal year."""
    return reduce_to_single_digit(personal_year + current_month)


def calculate_personal_day(personal_month: int, current_day: int) -> int:
    """Daily vibration within the personal month."""
    return reduce_to_single_digit(personal_month + current_day)


def interpret_birth_time(time_of_birth: str) -> Dict[str, Optional[int]]:
    """
    Interpret birth time for numerological significance.
    """
    digits = extract_digits(time_of_birth)
    
    if not digits:
        return {
            "challenge_number": None,
            "outward_persona": None,
            "hidden_spiritual_key": None
        }
    
    challenge_number = reduce_to_single_digit(sum(digits))
    outward_persona = reduce_to_single_digit(digits[0]) if digits else None
    hidden_spiritual_key = reduce_to_single_digit(sum(digits[-2:])) if len(digits) > 1 else None
    
    return {
        "challenge_number": challenge_number,
        "outward_persona": outward_persona,
        "hidden_spiritual_key": hidden_spiritual_key
    }


# =============================================================================
# KARMIC CALCULATIONS
# =============================================================================

def calculate_karmic_debt_numbers(name: str) -> List[int]:
    """
    Karmic debt numbers present in name (13, 14, 16, 19).
    Represents unresolved past life issues.
    """
    letter_values = [numerology_value(char) for char in name if char.isalpha()]
    debts = []
    
    for debt_num in KARMIC_DEBT_NUMBERS:
        if debt_num in letter_values or sum(letter_values) == debt_num:
            debts.append(debt_num)
    
    return debts


def interpret_karmic_debt(number: int) -> str:
    """Interpretation of specific karmic debt numbers."""
    interpretations = {
        13: "Karmic Debt 13: Misuse of power in past lives. Need to learn proper use of authority.",
        14: "Karmic Debt 14: Abuse of freedom in past lives. Need to develop discipline and commitment.",
        16: "Karmic Debt 16: Ego issues in past lives. Need to develop humility and service.",
        19: "Karmic Debt 19: Selfishness in past lives. Need to learn independence and proper self-love."
    }
    return interpretations.get(number, "Unknown karmic debt")


# =============================================================================
# GEMATRIA FUNCTIONS (Hebrew)
# =============================================================================

class Gematria:
    """
    Hebrew Gematria calculator for biblical text analysis.
    """
    
    # Standard Hebrew letter values
    STANDARD_VALUES = {
        'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
        'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60, 'ע': 70, 'פ': 80, 'צ': 90,
        'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
        # Final forms (sofit) - same or different values depending on tradition
        'ך': 20, 'ם': 40, 'ן': 50, 'ף': 80, 'ץ': 90,
    }
    
    # Millui (full spelling) values for advanced study
    MILLUI_VALUES = {
        'א': 111, 'ב': 412, 'ג': 73, 'ד': 434, 'ה': 6, 'ו': 12, 'ז': 77, 'ח': 418, 'ט': 419,
        'י': 20, 'כ': 100, 'ל': 74, 'מ': 90, 'נ': 106, 'ס': 120, 'ע': 130, 'פ': 81, 'צ': 104,
        'ק': 186, 'ר': 510, 'ש': 360, 'ת': 406,
    }
    
    # Greek (Isopsephy) values
    GREEK_VALUES = {
        'α': 1, 'β': 2, 'γ': 3, 'δ': 4, 'ε': 5, 'ϛ': 6, 'ζ': 7, 'η': 8, 'θ': 9,
        'ι': 10, 'κ': 20, 'λ': 30, 'μ': 40, 'ν': 50, 'ξ': 60, 'ο': 70, 'π': 80, 'ϟ': 90,
        'ρ': 100, 'σ': 200, 'τ': 300, 'υ': 400, 'φ': 500, 'χ': 600, 'ψ': 700, 'ω': 800, 'ϡ': 900,
    }
    
    def __init__(self):
        self.load_lexicons()
    
    def load_lexicons(self):
        """Load Hebrew and other lexicons if available."""
        self.lexicons = {}
        base = Path(__file__).parent
        
        lexicon_files = {
            'hebrew': '../ancient-hebrew-lexicon/hebrew_lexicon.json',
            'greek': '../koine-greek-lexicon/greek_lexicon.json',
        }
        
        for lang, filepath in lexicon_files.items():
            full_path = base / filepath
            if full_path.exists():
                with open(full_path, 'r', encoding='utf-8') as f:
                    self.lexicons[lang] = json.load(f)
    
    def calculate(self, text: str, method: str = "standard") -> int:
        """
        Calculate gematria value of Hebrew or Greek text.
        
        Args:
            text: Hebrew or Greek text
            method: 'standard', 'millui', or 'greek'
        
        Returns:
            Total numerical value
        """
        if method == "millui":
            values = self.MILLUI_VALUES
        elif method == "greek":
            values = self.GREEK_VALUES
        else:
            values = self.STANDARD_VALUES
        
        total = 0
        for char in text:
            if char in values:
                total += values[char]
        
        return total
    
    def reduce(self, value: int) -> int:
        """Reduce gematria value while preserving master numbers."""
        return reduce_to_single_digit(value, allow_master=True)
    
    def find_matches(self, target_value: int, word_list: List[str]) -> List[str]:
        """Find words with matching gematria values."""
        matches = []
        for word in word_list:
            if self.calculate(word) == target_value:
                matches.append(word)
        return matches
    
    def analyze_verse(self, verse: str) -> Dict:
        """
        Analyze a biblical verse with gematria.
        Returns word-by-word analysis.
        """
        words = verse.split()
        analysis = []
        total_value = 0
        
        for word in words:
            value = self.calculate(word)
            total_value += value
            analysis.append({
                'word': word,
                'gematria': value,
                'reduced': self.reduce(value)
            })
        
        return {
            'words': analysis,
            'total': total_value,
            'total_reduced': self.reduce(total_value)
        }
    
    def biblical_significance(self, number: int) -> Dict:
        """Get biblical significance of a number if available."""
        return BIBLICAL_SIGNIFICANCE.get(number, {
            "meaning": "No specific biblical significance documented",
            "references": []
        })
    
    def letter_breakdown(self, word: str) -> List[Dict]:
        """Show letter-by-letter gematria breakdown."""
        breakdown = []
        for char in word:
            if char in self.STANDARD_VALUES:
                breakdown.append({
                    'letter': char,
                    'value': self.STANDARD_VALUES[char],
                    'name': self._letter_name(char)
                })
        return breakdown
    
    def _letter_name(self, letter: str) -> str:
        """Get name of Hebrew letter."""
        names = {
            'א': 'Aleph', 'ב': 'Bet', 'ג': 'Gimel', 'ד': 'Dalet', 'ה': 'He',
            'ו': 'Vav', 'ז': 'Zayin', 'ח': 'Het', 'ט': 'Tet', 'י': 'Yod',
            'כ': 'Kaf', 'ל': 'Lamed', 'מ': 'Mem', 'נ': 'Nun', 'ס': 'Samekh',
            'ע': 'Ayin', 'פ': 'Pe', 'צ': 'Tsade', 'ק': 'Qof', 'ר': 'Resh',
            'ש': 'Shin', 'ת': 'Tav',
            'ך': 'Final Kaf', 'ם': 'Final Mem', 'ן': 'Final Nun',
            'ף': 'Final Pe', 'ץ': 'Final Tsade'
        }
        return names.get(letter, 'Unknown')


# =============================================================================
# COMPREHENSIVE CALCULATION
# =============================================================================

def calculate_all_numerology(
    full_name: str,
    birthdate: str,
    time_of_birth: Optional[str] = None,
    current_year: Optional[int] = None,
    current_month: Optional[int] = None,
    current_day: Optional[int] = None
) -> Dict:
    """
    Comprehensive numerology calculation.
    
    Args:
        full_name: Complete birth name
        birthdate: MM/DD/YYYY format
        time_of_birth: Optional time string
        current_year: Optional for personal year calc
        current_month: Optional for personal month calc
        current_day: Optional for personal day calc
    
    Returns:
        Dictionary with all numerology numbers
    """
    # Core numbers
    life_path = calculate_life_path(birthdate)
    expression = calculate_expression_number(full_name)
    soul_urge = calculate_soul_urge(full_name)
    personality = calculate_personality_number(full_name)
    birthday = calculate_birthday_number(birthdate)
    maturity = calculate_maturity_number(life_path, expression)
    
    # Challenges and pinnacles
    challenges = calculate_challenge_numbers(birthdate)
    pinnacles = calculate_pinnacle_numbers(birthdate)
    
    # Name components
    first_name = full_name.split()[0] if full_name.split() else full_name
    cornerstone_val = calculate_cornerstone(first_name)
    capstone_val = calculate_capstone(first_name)
    first_vowel_val = calculate_first_vowel(first_name)
    balance = calculate_balance_number(full_name)
    
    # Karmic and passion
    karmic_lessons = calculate_karmic_lessons(full_name)
    karmic_debts = calculate_karmic_debt_numbers(full_name)
    hidden_passion = calculate_hidden_passion(full_name)
    subconscious = calculate_subconscious_self(full_name)
    
    # Birth time interpretation
    birth_time_interp = interpret_birth_time(time_of_birth) if time_of_birth else None
    
    # Personal cycles
    now = datetime.now()
    year = current_year or now.year
    month = current_month or now.month
    day = current_day or now.day
    
    personal_year = calculate_personal_year(life_path, year)
    personal_month = calculate_personal_month(personal_year, month)
    personal_day = calculate_personal_day(personal_month, day)
    
    return {
        # Core Numbers
        "Life Path Number": life_path,
        "Expression Number": expression,
        "Soul Urge Number": soul_urge,
        "Personality Number": personality,
        "Birthday Number": birthday,
        "Maturity Number": maturity,
        
        # Cycles
        "Challenge Numbers": challenges,
        "Pinnacle Numbers": pinnacles,
        "Personal Year": personal_year,
        "Personal Month": personal_month,
        "Personal Day": personal_day,
        
        # Name Analysis
        "Cornerstone": cornerstone_val,
        "Capstone": capstone_val,
        "First Vowel": first_vowel_val,
        "Balance Number": balance,
        "Karmic Lessons": karmic_lessons,
        "Karmic Debts": karmic_debts,
        "Hidden Passion": hidden_passion,
        "Subconscious Self": subconscious,
        
        # Birth Time
        "Birth Time Interpretation": birth_time_interp,
        
        # Biblical Significance
        "Life Path Biblical Meaning": BIBLICAL_SIGNIFICANCE.get(life_path, {}),
        "Expression Biblical Meaning": BIBLICAL_SIGNIFICANCE.get(expression, {}),
    }


def print_numerology_report(data: Dict):
    """Print formatted numerology report."""
    print("=" * 60)
    print("  COMPREHENSIVE NUMEROLOGY REPORT")
    print("=" * 60)
    print()
    
    # Core Numbers
    print("CORE NUMBERS:")
    print("-" * 40)
    core = ["Life Path Number", "Expression Number", "Soul Urge Number",
            "Personality Number", "Birthday Number", "Maturity Number"]
    for key in core:
        if key in data:
            print(f"  {key:25} {data[key]}")
    
    print()
    print("CYCLES:")
    print("-" * 40)
    if "Challenge Numbers" in data:
        print(f"  Challenge Numbers:        {data['Challenge Numbers']}")
    if "Pinnacle Numbers" in data:
        print(f"  Pinnacle Numbers:         {data['Pinnacle Numbers']}")
    if "Personal Year" in data:
        print(f"  Personal Year:            {data['Personal Year']}")
    
    print()
    print("KARMIC INDICATORS:")
    print("-" * 40)
    if "Karmic Lessons" in data:
        print(f"  Karmic Lessons:           {data['Karmic Lessons']}")
    if "Karmic Debts" in data:
        print(f"  Karmic Debts:             {data['Karmic Debts']}")
    if data.get("Karmic Debts"):
        for debt in data["Karmic Debts"]:
            print(f"    - {interpret_karmic_debt(debt)}")
    
    print()
    print("=" * 60)


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def main():
    """CLI for numerology calculations."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python3 numbers.py <command> <value>")
        print("\nCommands:")
        print("  report <name> <birthdate> [time]  Full numerology report")
        print("  lifepath <birthdate>              Calculate life path")
        print("  gematria <hebrew_word>            Calculate gematria")
        print("  reduce <number>                   Reduce to single digit")
        print("\nExamples:")
        print('  python3 numbers.py report "John Doe" 03/15/1985')
        print('  python3 numbers.py gematria "שלום"')
        print('  python3 numbers.py reduce 12345')
        sys.exit(0)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "report":
        if len(sys.argv) < 4:
            print("Error: report requires name and birthdate")
            sys.exit(1)
        name = sys.argv[2]
        birthdate = sys.argv[3]
        time_of_birth = sys.argv[4] if len(sys.argv) > 4 else None
        
        result = calculate_all_numerology(name, birthdate, time_of_birth)
        print_numerology_report(result)
        
    elif cmd == "lifepath":
        birthdate = sys.argv[2]
        result = calculate_life_path(birthdate)
        print(f"Life Path Number: {result}")
        if result in BIBLICAL_SIGNIFICANCE:
            print(f"  Meaning: {BIBLICAL_SIGNIFICANCE[result]['meaning']}")
        
    elif cmd == "gematria":
        word = sys.argv[2]
        g = Gematria()
        value = g.calculate(word)
        reduced = g.reduce(value)
        print(f"Gematria of '{word}': {value} -> {reduced}")
        
        # Letter breakdown
        print("\nLetter breakdown:")
        for letter_info in g.letter_breakdown(word):
            print(f"  {letter_info['letter']} ({letter_info['name']}): {letter_info['value']}")
        
        # Biblical significance
        significance = g.biblical_significance(reduced)
        print(f"\nBiblical significance: {significance['meaning']}")
        
    elif cmd == "reduce":
        number = int(sys.argv[2])
        result = reduce_to_single_digit(number)
        print(f"{number} reduces to: {result}")
        
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
