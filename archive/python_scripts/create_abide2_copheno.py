#!/usr/bin/env python
import pandas as pd
import os
from pathlib import Path

def create_abide2_cophenotype():
    """Combine all ABIDE2 participants.tsv files into a single co-phenotype CSV"""
    
    base_dir = Path("/orcd/data/satra/002/datasets/simple2_datalad/abide2")
    output_file = Path("/home/yibei/simple2_bids2nidm/ABIDE2_Cophenotype.csv")
    
    # Get all ABIDE2 sites
    sites = sorted([d.name for d in base_dir.iterdir() if d.name.startswith('ABIDEII-') and d.is_dir()])
    
    print(f"Found {len(sites)} ABIDE2 sites")
    
    all_dfs = []
    successful_sites = []
    failed_sites = []
    
    for site in sites:
        participants_file = base_dir / site / "participants.tsv"
        
        if not participants_file.exists():
            print(f"Warning: {site} - participants.tsv not found")
            failed_sites.append(site)
            continue
        
        try:
            # Try different encodings if UTF-8 fails
            encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(participants_file, sep='\t', encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                print(f"Error: {site} - Could not read file with any encoding")
                failed_sites.append(site)
                continue
            
            # Add site column if not present (for tracking)
            if 'site_id' not in df.columns:
                df['site_id'] = site
            
            all_dfs.append(df)
            successful_sites.append(site)
            print(f"✓ {site}: {len(df)} participants")
            
        except Exception as e:
            print(f"Error: {site} - {e}")
            failed_sites.append(site)
    
    # Combine all dataframes
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        
        # Save to CSV
        combined_df.to_csv(output_file, index=False)
        
        print(f"\n" + "="*60)
        print(f"Successfully combined {len(successful_sites)} sites")
        print(f"Total participants: {len(combined_df)}")
        print(f"Total columns: {len(combined_df.columns)}")
        print(f"Output file: {output_file}")
        
        if failed_sites:
            print(f"\nFailed sites ({len(failed_sites)}):")
            for site in failed_sites:
                print(f"  - {site}")
        
        # Print summary statistics
        print(f"\n" + "="*60)
        print("Summary Statistics:")
        print(f"Unique site_ids: {combined_df['site_id'].nunique()}")
        
        if 'dx_group' in combined_df.columns:
            dx_counts = combined_df['dx_group'].value_counts()
            print(f"\nDiagnosis groups:")
            for dx, count in dx_counts.items():
                print(f"  Group {dx}: {count} participants")
        
        if 'sex' in combined_df.columns:
            sex_counts = combined_df['sex'].value_counts()
            print(f"\nSex distribution:")
            for sex, count in sex_counts.items():
                print(f"  Sex {sex}: {count} participants")
        
        if 'age_at_scan ' in combined_df.columns:  # Note the space in column name
            age_col = 'age_at_scan '
            print(f"\nAge statistics:")
            print(f"  Mean: {combined_df[age_col].mean():.2f}")
            print(f"  Std: {combined_df[age_col].std():.2f}")
            print(f"  Min: {combined_df[age_col].min():.2f}")
            print(f"  Max: {combined_df[age_col].max():.2f}")
        
        return combined_df
    else:
        print("Error: No data to combine")
        return None

if __name__ == "__main__":
    df = create_abide2_cophenotype()