#!/usr/bin/env python
import subprocess
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import logging

# Set up logging - now logs to logs/abide2/ to match ABIDE1 structure
log_dir = Path("/home/yibei/simple2_bids2nidm/logs/abide2")
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'abide2_processing_all.log'),
        logging.StreamHandler()
    ]
)

def process_single_site(site_name):
    """Process a single site using the process_site script"""
    logging.info(f"Starting processing for site: {site_name}")
    
    cmd = ["python", "/home/yibei/simple2_bids2nidm/abide2_process_site.py", site_name]
    
    try:
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)  # 1 hour timeout
        elapsed_time = time.time() - start_time
        
        if result.returncode == 0:
            logging.info(f"Successfully processed {site_name} in {elapsed_time:.2f} seconds")
            return (site_name, True, elapsed_time)
        else:
            logging.error(f"Failed to process {site_name}: {result.stderr}")
            return (site_name, False, elapsed_time)
            
    except subprocess.TimeoutExpired:
        logging.error(f"Timeout processing {site_name} (exceeded 1 hour)")
        return (site_name, False, 3600)
    except Exception as e:
        logging.error(f"Exception processing {site_name}: {e}")
        return (site_name, False, 0)

def verify_outputs(site_name):
    """Verify that expected output files exist for a site"""
    output_dir = Path("/home/yibei/simple2_bids2nidm/nidm_outputs/abide2")
    site_lower = site_name.lower().replace("abideii-", "")
    
    nidm_file = output_dir / f"{site_lower}_nidm.ttl"
    phenotype_file = output_dir / f"{site_lower}_phenotype.ttl"
    
    outputs = {}
    outputs['nidm'] = nidm_file.exists()
    outputs['phenotype'] = phenotype_file.exists()
    
    if outputs['nidm'] and outputs['phenotype']:
        outputs['status'] = 'complete'
    elif outputs['nidm']:
        outputs['status'] = 'partial'
    else:
        outputs['status'] = 'missing'
    
    return outputs

def main():
    # Read sites from file
    sites_file = Path("/home/yibei/simple2_bids2nidm/abide2_sites.txt")
    
    if not sites_file.exists():
        logging.error(f"Sites file not found: {sites_file}")
        return
    
    with open(sites_file, 'r') as f:
        sites = [line.strip() for line in f if line.strip()]
    
    logging.info(f"Found {len(sites)} sites to process")
    
    # Create output directory if it doesn't exist
    output_dir = Path("/home/yibei/simple2_bids2nidm/nidm_outputs/abide2")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process sites in parallel
    max_workers = 4  # Adjust based on available resources
    successful = []
    failed = []
    
    start_time = time.time()
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_site = {executor.submit(process_single_site, site): site for site in sites}
        
        # Process completed tasks
        for future in as_completed(future_to_site):
            site = future_to_site[future]
            try:
                site_name, success, elapsed = future.result()
                if success:
                    successful.append(site_name)
                else:
                    failed.append(site_name)
            except Exception as e:
                logging.error(f"Exception getting result for {site}: {e}")
                failed.append(site)
    
    total_time = time.time() - start_time
    
    # Verify outputs and generate detailed report
    logging.info("=" * 50)
    logging.info("VERIFYING OUTPUTS")
    
    complete_sites = []
    partial_sites = []
    missing_sites = []
    
    for site in sites:
        outputs = verify_outputs(site)
        if outputs['status'] == 'complete':
            complete_sites.append(site)
        elif outputs['status'] == 'partial':
            partial_sites.append(site)
        else:
            missing_sites.append(site)
    
    # Print summary
    logging.info("=" * 50)
    logging.info("PROCESSING COMPLETE")
    logging.info(f"Total time: {total_time:.2f} seconds ({total_time/60:.1f} minutes)")
    logging.info(f"Total sites: {len(sites)}")
    logging.info(f"Complete (both files): {len(complete_sites)} sites")
    logging.info(f"Partial (NIDM only): {len(partial_sites)} sites")
    logging.info(f"Missing (no output): {len(missing_sites)} sites")
    
    if complete_sites:
        logging.info("\nCompletely processed sites (NIDM + phenotype):")
        for site in complete_sites:
            site_lower = site.lower().replace("abideii-", "")
            logging.info(f"  ✓ {site} -> {site_lower}_nidm.ttl, {site_lower}_phenotype.ttl")
    
    if partial_sites:
        logging.info("\nPartially processed sites (NIDM only):")
        for site in partial_sites:
            site_lower = site.lower().replace("abideii-", "")
            logging.info(f"  ⚠ {site} -> {site_lower}_nidm.ttl (phenotype missing)")
    
    if missing_sites:
        logging.info("\nFailed or missing sites:")
        for site in missing_sites:
            logging.info(f"  ✗ {site}")
    
    # Save summary to file
    summary_file = log_dir / "abide2_processing_summary.txt"
    with open(summary_file, "w") as f:
        f.write(f"ABIDE2 Processing Summary\n")
        f.write(f"=" * 50 + "\n")
        f.write(f"Processing completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total time: {total_time:.2f} seconds ({total_time/60:.1f} minutes)\n")
        f.write(f"Output directory: {output_dir}\n\n")
        
        f.write(f"Statistics:\n")
        f.write(f"  Total sites: {len(sites)}\n")
        f.write(f"  Complete (both files): {len(complete_sites)}\n")
        f.write(f"  Partial (NIDM only): {len(partial_sites)}\n")
        f.write(f"  Missing (no output): {len(missing_sites)}\n\n")
        
        f.write("Complete sites (NIDM + phenotype):\n")
        for site in complete_sites:
            site_lower = site.lower().replace("abideii-", "")
            f.write(f"  {site} -> {site_lower}_nidm.ttl, {site_lower}_phenotype.ttl\n")
        
        f.write("\nPartial sites (NIDM only):\n")
        for site in partial_sites:
            site_lower = site.lower().replace("abideii-", "")
            f.write(f"  {site} -> {site_lower}_nidm.ttl\n")
        
        f.write("\nFailed/missing sites:\n")
        for site in missing_sites:
            f.write(f"  {site}\n")
    
    logging.info(f"\nSummary saved to: {summary_file}")

if __name__ == "__main__":
    main()