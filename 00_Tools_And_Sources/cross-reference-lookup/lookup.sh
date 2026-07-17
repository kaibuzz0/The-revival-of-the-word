#!/bin/bash
# Cross-Reference Tool Suite Launcher
# Convenient launcher for the cross-reference lookup tools

cd "$(dirname "$0")"

echo "=========================================="
echo "Ancient Biblical Language Cross-Reference"
echo "=========================================="
echo ""

show_menu() {
    echo "1. Quick Lookup (instant)"
    echo "2. Full Search (comprehensive)"
    echo "3. Show Statistics"
    echo "4. Cross-Reference Mode"
    echo "5. List Quick Terms"
    echo "6. Exit"
    echo ""
}

while true; do
    show_menu
    read -p "Select option [1-6]: " choice
    
    case $choice in
        1)
            read -p "Enter term (god, jesus, love, etc.): " term
            python3 quick_lookup.py "$term"
            ;;
        2)
            read -p "Enter search term: " term
            python3 cross_reference_lookup.py "$term"
            ;;
        3)
            python3 cross_reference_lookup.py --stats
            ;;
        4)
            read -p "Enter term for cross-reference: " term
            python3 cross_reference_lookup.py --xref "$term"
            ;;
        5)
            python3 quick_lookup.py --list
            ;;
        6)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid option"
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
    echo ""
done
