#!/usr/bin/env python3
"""
Quick Cross-Reference Lookup
Fast command-line tool for biblical term translations
"""
import sys

# Predefined translation data for quick lookups
CROSS_REFS = {
    "god": {
        "hebrew": "אֱלֹהִים (Elohim)",
        "greek": "θεός (theos)",
        "latin": "Deus",
        "syriac": "ܐܠܗܐ (ʾalâhâʾ)",
        "georgian": "ღმერთი (ghmerti)",
        "aramaic": "אֱלָהָא (ʾĕlâhâʾ)",
        "coptic": "ⲛⲟⲩⲧⲉ (noute)",
        "geez": "አምላክ (Amlak)",
    },
    "lord": {
        "hebrew": "יְהֹוָה (YHWH)",
        "greek": "κύριος (kyrios)",
        "latin": "Dominus",
        "syriac": "ܡܪܝܐ (mâryâʾ)",
        "georgian": "უფალი (upali)",
        "aramaic": "מָרֵא (mârêʾ)",
        "coptic": "ⲕⲩⲣⲓⲟⲥ (kyrios)",
        "geez": "እግዚአብሔር (Ǝgziabhēr)",
    },
    "jesus": {
        "hebrew": "יֵשׁוּעַ (Yēšûaʿ)",
        "greek": "Ἰησοῦς (Iēsous)",
        "latin": "Iesus",
        "syriac": "ܝܫܘܥ (yešûʿ)",
        "georgian": "იესუ (iesu)",
        "aramaic": "יֵשׁוּעַ (Yēšûaʿ)",
        "coptic": "ⲓⲏⲥⲟⲩⲥ (iēsous)",
        "geez": "ኢየሱስ (Iyesus)",
    },
    "christ": {
        "hebrew": "מָשִׁיחַ (māšîaḥ)",
        "greek": "Χριστός (Christos)",
        "latin": "Christus",
        "syriac": "ܡܫܝܚܐ (mešîḥâʾ)",
        "georgian": "ქრისტე (kriste)",
        "aramaic": "מְשִׁיחָא (məšîḥāʾ)",
        "coptic": "ⲭⲣⲓⲥⲧⲟⲥ (christos)",
        "geez": "ክርስቶስ (Krǝstos)",
    },
    "spirit": {
        "hebrew": "רוּחַ (rûaḥ)",
        "greek": "πνεῦμα (pneuma)",
        "latin": "Spiritus",
        "syriac": "ܪܘܚܐ (rûḥâʾ)",
        "georgian": "სული (suli)",
        "aramaic": "רוּחַ (rûaḥ)",
        "coptic": "ⲡⲛⲉⲩⲙⲁ (pneuma)",
        "geez": "መንፈስ (mänfäs)",
    },
    "father": {
        "hebrew": "אָב (ʾāḇ)",
        "greek": "πατήρ (patēr)",
        "latin": "Pater",
        "syriac": "ܐܒܐ (ʾaḇâʾ)",
        "georgian": "მამა (mama)",
        "aramaic": "אֲבָא (ʾăḇāʾ)",
        "coptic": "ⲉⲓⲱⲧ (eit)",
        "geez": "አብ (Ab)",
    },
    "son": {
        "hebrew": "בֵּן (bēn)",
        "greek": "υἱός (huios)",
        "latin": "Filius",
        "syriac": "ܒܪܐ (brâʾ)",
        "georgian": "ძე (dze)",
        "aramaic": "בַּר (bar)",
        "coptic": "ϣⲏⲣⲓ (shēri)",
        "geez": "ወልድ (Wäld)",
    },
    "love": {
        "hebrew": "אַהֲבָה (ʾăhăḇâ)",
        "greek": "ἀγάπη (agapē)",
        "latin": "caritas",
        "syriac": "ܚܘܒܐ (ḥûḇâʾ)",
        "georgian": "სიყვარული (siq'varuli)",
        "aramaic": "רַחֲמִין (raḥămîn)",
        "coptic": "ⲁⲅⲁⲡⲏ (agapē)",
        "geez": "ፍቅር (fǝqr)",
    },
    "peace": {
        "hebrew": "שָׁלוֹם (šālôm)",
        "greek": "εἰρήνη (eirēnē)",
        "latin": "pax",
        "syriac": "ܫܠܡܐ (šelâmâʾ)",
        "georgian": "მშვიდობა (mshvidoba)",
        "aramaic": "שְׁלָם (šĕlām)",
        "coptic": "ϩⲓⲣⲏⲛⲏ (hirēnē)",
        "geez": "ሰላም (salām)",
    },
    "truth": {
        "hebrew": "אֱמֶת (ʾĕmeṯ)",
        "greek": "ἀλήθεια (alētheia)",
        "latin": "veritas",
        "syriac": "ܫܪܝܪܐ (šǝrîrâʾ)",
        "georgian": "ჭეშმარიტება (ch'eshmariteba)",
        "aramaic": "שְׁרָרָה (šĕrārâ)",
        "coptic": "ⲙⲉ (mē)",
        "geez": "ጥብቅ (tǝbq)",
    },
    "holy": {
        "hebrew": "קָדוֹשׁ (qāḏôš)",
        "greek": "ἅγιος (hagios)",
        "latin": "sanctus",
        "syriac": "ܩܕܝܫܐ (qǝḏîšâʾ)",
        "georgian": "წმიდა (tsmida)",
        "aramaic": "קַדִּישׁ (qădḏîš)",
        "coptic": "ⲉⲑⲟⲩⲁⲃ (ethouab)",
        "geez": "ቅዱስ (qǝdus)",
    },
    "sin": {
        "hebrew": "חַטָּאת (ḥaṭṭāʾṯ)",
        "greek": "ἁμαρτία (hamartia)",
        "latin": "peccatum",
        "syriac": "ܚܛܝܬܐ (ḥaṭṭâytâʾ)",
        "georgian": "ცოდვა (tsodva)",
        "aramaic": "חֲטָאָה (ḥăṭāʾâ)",
        "coptic": "ⲛⲟⲃⲉ (nobe)",
        "geez": "ኀጢአት (ḫǝṭiʾat)",
    },
    "salvation": {
        "hebrew": "יְשׁוּעָה (yəšûʿâ)",
        "greek": "σωτηρία (sōtēria)",
        "latin": "salus",
        "syriac": "ܥܘܕܪܢܐ (ʿûdrānâʾ)",
        "georgian": "მიხსნელობა (mikhsneloba)",
        "aramaic": "פּוּרְקָן (pûrqān)",
        "coptic": "ⲥⲱⲧⲉ (sōte)",
        "geez": "መድኀኒት (madḫanit)",
    },
    "resurrection": {
        "hebrew": "תְּחִיָּה (təḥiyyâ)",
        "greek": "ἀνάστασις (anastasis)",
        "latin": "resurrectio",
        "syriac": "ܩܝܡܐ (qîyâmâʾ)",
        "georgian": "განკვდომა (gank'vdoma)",
        "aramaic": "אֲתָה (ʾăṯâ)",
        "coptic": "ⲁⲛⲁⲥⲧⲁⲥⲓⲥ (anastasis)",
        "geez": "ትንሣኤ (tǝnśāʾe)",
    },
}

LANGUAGES = ["hebrew", "greek", "latin", "syriac", "georgian", "aramaic", "coptic", "geez"]

COLORS = {
    "hebrew": "\033[38;5;196m",    # Red
    "greek": "\033[38;5;33m",      # Blue
    "latin": "\033[38;5;208m",     # Orange
    "syriac": "\033[38;5;93m",     # Purple
    "georgian": "\033[38;5;28m",   # Green
    "aramaic": "\033[38;5;130m",   # Brown
    "coptic": "\033[38;5;214m",    # Gold
    "geez": "\033[38;5;88m",       # Dark red
    "header": "\033[1;4m",          # Bold + Underline
    "reset": "\033[0m",
}

def show_translation(term):
    """Show translation across all 8 languages"""
    term_lower = term.lower()
    
    if term_lower not in CROSS_REFS:
        print(f"[!] Term '{term}' not in quick reference database.")
        print(f"    Try: {', '.join(CROSS_REFS.keys())}")
        print(f"    Or use: python cross_reference_lookup.py {term}")
        return
    
    data = CROSS_REFS[term_lower]
    
    print(f"\n{'='*80}")
    print(f"{COLORS['header']}{term.upper()} - Biblical Translations{COLORS['reset']}")
    print(f"{'='*80}\n")
    
    for lang in LANGUAGES:
        if lang in data:
            color = COLORS.get(lang, "")
            reset = COLORS["reset"]
            print(f"{color}{lang.upper():<12}{reset} {data[lang]}")
    
    print(f"\n{'='*80}")


def show_all():
    """Show all available terms"""
    print("\nAvailable Terms for Quick Cross-Reference:\n")
    for i, term in enumerate(sorted(CROSS_REFS.keys()), 1):
        print(f"{i:2}. {term}")
    print(f"\nUsage: python quick_lookup.py <term>")
    print(f"       python quick_lookup.py god")
    print(f"       python quick_lookup.py love")


def main():
    if len(sys.argv) < 2:
        print("Quick Cross-Reference Lookup")
        print("Usage: python quick_lookup.py <term>")
        print("       python quick_lookup.py --list")
        print()
        show_all()
        sys.exit(0)
    
    if sys.argv[1] in ['--list', '-l', 'list']:
        show_all()
        sys.exit(0)
    
    show_translation(sys.argv[1])


if __name__ == "__main__":
    main()
