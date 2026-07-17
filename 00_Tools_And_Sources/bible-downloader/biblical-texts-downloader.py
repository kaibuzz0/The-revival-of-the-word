#!/usr/bin/env python3
"""
Biblical Texts Downloader
Downloads ancient biblical and early Christian texts from public domain sources
Zero dependencies - uses only Python standard library
"""

import json
import urllib.request
import urllib.error
import os
from pathlib import Path
from datetime import datetime

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def log(message, level="info"):
    """Print colored log messages"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    if level == "info":
        print(f"[{timestamp}] {Colors.BLUE}[*]{Colors.END} {message}")
    elif level == "success":
        print(f"[{timestamp}] {Colors.GREEN}[+]{Colors.END} {message}")
    elif level == "warning":
        print(f"[{timestamp}] {Colors.WARNING}[!]{Colors.END} {message}")
    elif level == "error":
        print(f"[{timestamp}] {Colors.FAIL}[X]{Colors.END} {message}")
    elif level == "header":
        print(f"\n{Colors.HEADER}{Colors.BOLD}{message}{Colors.END}")

def download_file(url, output_path, timeout=30):
    """Download a file from URL to output_path"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
            
        # Create directory if needed
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(data)
        
        return True, len(data)
    except Exception as e:
        return False, str(e)

def load_manifest():
    """Load the download manifest"""
    manifest_path = Path(__file__).parent / "biblical-texts-download-manifest.json"
    
    if not manifest_path.exists():
        log(f"Manifest not found: {manifest_path}", "error")
        return None
    
    with open(manifest_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def download_category(category_name, category_data, base_dir, dry_run=False):
    """Download all texts in a category"""
    log(f"Category: {category_name}", "header")
    
    category_dir = base_dir / category_data['folder']
    category_dir.mkdir(parents=True, exist_ok=True)
    
    texts = category_data.get('texts', [])
    downloaded = 0
    failed = 0
    skipped = 0
    total_size = 0
    
    for text in texts:
        filename = text['filename']
        url = text['url']
        output_path = category_dir / filename
        
        # Check if already exists
        if output_path.exists():
            log(f"  Already exists: {filename}")
            skipped += 1
            continue
        
        if dry_run:
            log(f"  Would download: {filename}")
            continue
        
        log(f"  Downloading: {filename}...", end=' ')
        success, result = download_file(url, output_path)
        
        if success:
            log(f"OK ({result:,} bytes)", "success")
            downloaded += 1
            total_size += result
        else:
            log(f"FAILED: {result}", "error")
            failed += 1
    
    return {
        'downloaded': downloaded,
        'failed': failed,
        'skipped': skipped,
        'total_size': total_size
    }

def main():
    """Main download orchestrator"""
    print(f"""
{Colors.HEADER}{'='*70}{Colors.END}
{Colors.HEADER}{Colors.BOLD}  BIBLICAL TEXTS DOWNLOADER{Colors.END}
{Colors.HEADER}{'='*70}{Colors.END}

  Downloads ancient biblical and early Christian texts
  from public domain sources. Zero dependencies.
  
  Estimated download: ~5.5 GB
  Estimated time: 1-3 hours (depending on connection)
  
{Colors.HEADER}{'='*70}{Colors.END}
""")
    
    # Get base directory
    base_dir = Path(__file__).parent.parent.parent / 'EXTENDED_BIBLE'
    
    # Load manifest
    manifest = load_manifest()
    if not manifest:
        log("Failed to load manifest. Exiting.", "error")
        return 1
    
    log(f"Loaded manifest: {manifest['title']}")
    log(f"Version: {manifest['version']}")
    log(f"Total categories: {len(manifest['categories'])}")
    log(f"Total texts: {sum(len(c.get('texts', [])) for c in manifest['categories'].values())}")
    
    # Show categories
    print(f"\n{Colors.CYAN}Categories:{Colors.END}")
    for name, data in manifest['categories'].items():
        count = len(data.get('texts', []))
        print(f"  - {name}: {count} texts")
    
    # Ask for dry run
    print(f"\n{Colors.WARNING}Options:{Colors.END}")
    print("  1. Download all texts (will take time)")
    print("  2. Dry run (show what would be downloaded)")
    print("  3. Cancel")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == '3':
        log("Cancelled by user.")
        return 0
    
    dry_run = (choice == '2')
    
    if dry_run:
        log("DRY RUN MODE - No files will be downloaded\n")
    
    # Download each category
    results = {}
    for category_name, category_data in manifest['categories'].items():
        result = download_category(category_name, category_data, base_dir, dry_run)
        results[category_name] = result
    
    # Summary
    print(f"\n{Colors.HEADER}{'='*70}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}  DOWNLOAD SUMMARY{Colors.END}")
    print(f"{Colors.HEADER}{'='*70}{Colors.END}\n")
    
    total_downloaded = sum(r['downloaded'] for r in results.values())
    total_failed = sum(r['failed'] for r in results.values())
    total_skipped = sum(r['skipped'] for r in results.values())
    total_size = sum(r['total_size'] for r in results.values())
    
    print(f"  Total downloaded: {Colors.GREEN}{total_downloaded}{Colors.END}")
    print(f"  Total failed: {Colors.FAIL}{total_failed}{Colors.END}")
    print(f"  Already exists: {total_skipped}")
    print(f"  Total size: {total_size / (1024*1024):.1f} MB")
    
    if total_failed > 0:
        print(f"\n{Colors.WARNING}Some downloads failed. Check the output above for details.{Colors.END}")
    
    print(f"\n{Colors.GREEN}Done!{Colors.END}")
    print(f"Files saved to: {base_dir}")
    
    return 0

if __name__ == "__main__":
    exit(main())
