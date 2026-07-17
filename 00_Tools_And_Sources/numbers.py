#!/usr/bin/env python3
"""
Numbers.py - Biblical Number Patterns and Gematria Analysis
"""

class BiblicalNumbers:
    """Analyze biblical number patterns and significance"""
    
    SIGNIFICANT_NUMBERS = {
        1: {"meaning": "Unity, God", "references": ["Deut 6:4", "Mark 12:29"]},
        2: {"meaning": "Division, witness", "references": ["Gen 1:6-7", "Matt 18:16"]},
        3: {"meaning": "Divine perfection", "references": ["Matt 28:19", "1 John 5:7"]},
        4: {"meaning": "Creation, earth", "references": ["Gen 1:14-19", "Rev 7:1"]},
        5: {"meaning": "Grace, Torah", "references": ["Gen 1:20-23", "Matt 14:17-21"]},
        6: {"meaning": "Man, incomplete", "references": ["Gen 1:26-31", "Rev 13:18"]},
        7: {"meaning": "Perfection, Sabbath", "references": ["Gen 2:2-3", "Rev 1:20"]},
        8: {"meaning": "New beginnings", "references": ["Gen 17:12", "1 Peter 3:20"]},
        10: {"meaning": "Completeness, commandments", "references": ["Ex 34:28", "Rev 2:10"]},
        12: {"meaning": "Government, tribes", "references": ["Gen 49:28", "Rev 21:12"]},
        40: {"meaning": "Testing, trial", "references": ["Gen 7:4", "Matt 4:2"]},
        70: {"meaning": "Nations, elders", "references": ["Gen 10", "Ex 24:1"]},
        153: {"meaning": "Abundance", "references": ["John 21:11"]},
        666: {"meaning": "Number of the beast", "references": ["Rev 13:18"]},
        777: {"meaning": "Divine perfection tripled", "references": []},
        1000: {"meaning": "Completeness, millennium", "references": ["Rev 20:1-7"]},
    }
    
    def analyze_number(self, n):
        """Get significance of a number"""
        return self.SIGNIFICANT_NUMBERS.get(n, {"meaning": "Not specifically documented"})
    
    def is_significant(self, n):
        """Check if number has biblical significance"""
        return n in self.SIGNIFICANT_NUMBERS
    
    def get_multiples(self, n, max_val=1000):
        """Get significant multiples of a number"""
        multiples = []
        for i in range(n, max_val + 1, n):
            if self.is_significant(i):
                multiples.append((i, self.analyze_number(i)))
        return multiples


class Gematria:
    """Hebrew Gematria calculations"""
    
    HEBREW_VALUES = {
        'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
        'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60, 'ע': 70, 'פ': 80, 'צ': 90,
        'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
        'ך': 20, 'ם': 40, 'ן': 50, 'ף': 80, 'ץ': 90,  # Final forms
    }
    
    def calculate(self, hebrew_text):
        """Calculate gematria value"""
        total = 0
        for char in hebrew_text:
            if char in self.HEBREW_VALUES:
                total += self.HEBREW_VALUES[char]
        return total
    
    def find_matches(self, target_value, word_list):
        """Find words with matching gematria"""
        matches = []
        for word in word_list:
            if self.calculate(word) == target_value:
                matches.append(word)
        return matches


def main():
    """Demo"""
    bn = BiblicalNumbers()
    
    print("Biblical Numbers Analysis")
    print("=" * 40)
    
    for num in [7, 12, 40, 666]:
        info = bn.analyze_number(num)
        print(f"\n{num}: {info['meaning']}")
        if info['references']:
            print(f"   References: {', '.join(info['references'])}")


if __name__ == "__main__":
    main()
