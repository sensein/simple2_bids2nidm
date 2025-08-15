#!/usr/bin/env python3
"""
Fix trailing spaces in ABIDE2 participants.tsv column headers
"""
import os
from pathlib import Path
import shutil

def fix_tsv_headers(tsv_path):
    """Remove trailing spaces from TSV column headers"""
    # Read the file
    with open(tsv_path, 'r') as f:
        lines = f.readlines()
    
    if not lines:
        return False
    
    # Check if header has trailing spaces
    header = lines[0].rstrip('\n')
    columns = header.split('\t')
    cleaned_columns = [col.strip() for col in columns]
    
    if columns != cleaned_columns:
        print(f"Fixing headers in {tsv_path}")
        print(f"  Found columns with spaces: {[col for col in columns if col != col.strip()]}")
        
        # Create backup
        backup_path = str(tsv_path) + '.bak'
        shutil.copy2(tsv_path, backup_path)
        print(f"  Created backup: {backup_path}")
        
        # Write fixed file
        lines[0] = '\t'.join(cleaned_columns) + '\n'
        with open(tsv_path, 'w') as f:
            f.writelines(lines)
        
        print(f"  Fixed headers in {tsv_path}")
        return True
    
    return False

def main():
    """Fix all ABIDE2 participants.tsv files"""
    base_dir = Path("/orcd/data/satra/002/datasets/simple2_datalad/abide2")
    
    # Get all sites
    sites = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith("ABIDEII-")]
    
    print(f"Found {len(sites)} ABIDE2 sites")
    
    fixed_count = 0
    for site in sites:
        participants_tsv = site / "participants.tsv"
        if participants_tsv.exists():
            if fix_tsv_headers(participants_tsv):
                fixed_count += 1
        else:
            print(f"Warning: No participants.tsv in {site}")
    
    print(f"\nSummary: Fixed {fixed_count} files")

if __name__ == "__main__":
    main()