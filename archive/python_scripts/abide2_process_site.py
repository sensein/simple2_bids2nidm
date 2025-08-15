#!/usr/bin/env python
import os
import sys
import subprocess
import shutil
from pathlib import Path
import logging

def setup_logging(site_name, log_dir):
    """Set up logging for the site processing"""
    log_file = log_dir / f"{site_name}_processing.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def process_site(site_name):
    """Process a single ABIDE2 site following ABIDE1 structure"""
    
    # Paths - matching ABIDE1 structure
    base_dir = Path("/orcd/data/satra/002/datasets/simple2_datalad/abide2")
    site_dir = base_dir / site_name
    
    # Use same structure as ABIDE1: nidm_outputs/abide2/
    output_dir = Path("/home/yibei/simple2_bids2nidm/nidm_outputs/abide2")
    log_dir = Path("/home/yibei/simple2_bids2nidm/logs/abide2")
    
    # Create output and log directories
    output_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Set up logging
    logger = setup_logging(site_name, log_dir)
    
    # Convert site name to lowercase for output files (matching ABIDE1)
    site_lower = site_name.lower().replace("abideii-", "")  # Remove ABIDEII- prefix and lowercase
    nidm_output = output_dir / f"{site_lower}_nidm.ttl"
    phenotype_output = output_dir / f"{site_lower}_phenotype.ttl"
    
    # Check if site directory exists
    if not site_dir.exists():
        logger.error(f"Site directory {site_dir} does not exist")
        return 1
    
    logger.info(f"Processing site: {site_name}")
    logger.info(f"Input directory: {site_dir}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Output files: {nidm_output}, {phenotype_output}")
    
    # Check if output files already exist
    if nidm_output.exists() or phenotype_output.exists():
        logger.warning(f"Output files already exist for {site_name}")
        if nidm_output.exists():
            logger.warning(f"  - {nidm_output}")
        if phenotype_output.exists():
            logger.warning(f"  - {phenotype_output}")
        logger.info(f"Skipping {site_name} (use --force to overwrite)")
        return 0
    
    # Step 1: Run bidsmri2nidm
    logger.info(f"Step 1/3: Running bidsmri2nidm for {site_name}...")
    
    json_map = Path("/home/yibei/simple2_bids2nidm/abide2_variables_to_terms_complete.json")
    
    # Check if JSON mapping file exists
    if not json_map.exists():
        logger.error(f"JSON mapping file not found: {json_map}")
        return 1
    
    # Use wrapper script to handle any interactive prompts
    wrapper_script = Path("/home/yibei/simple2_bids2nidm/run_bidsmri2nidm_noninteractive.sh")
    
    cmd = [
        str(wrapper_script),
        "-d", str(site_dir),
        "-o", str(nidm_output),
        "-json_map", str(json_map),
        "-no_concepts"  # Match ABIDE1 processing
    ]
    
    logger.info(f"Command: {' '.join(cmd)}")
    
    try:
        # Run with wrapper script that handles prompts
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                              universal_newlines=True, timeout=3600)
        
        if result.returncode != 0:
            logger.error(f"bidsmri2nidm failed for {site_name}")
            logger.error(f"STDOUT: {result.stdout}")
            logger.error(f"STDERR: {result.stderr}")
            return 1
        
        logger.info(f"bidsmri2nidm completed successfully for {site_name}")
        
    except subprocess.TimeoutExpired:
        logger.error(f"Timeout processing {site_name} with bidsmri2nidm (exceeded 1 hour)")
        return 1
    except Exception as e:
        logger.error(f"Exception running bidsmri2nidm for {site_name}: {e}")
        return 1
    
    # Step 2: Copy NIDM file for phenotype integration
    logger.info(f"Step 2/3: Creating copy for phenotype integration...")
    
    try:
        shutil.copy2(nidm_output, phenotype_output)
        logger.info(f"Copy created: {phenotype_output}")
    except Exception as e:
        logger.error(f"Failed to copy NIDM file for {site_name}: {e}")
        return 1
    
    # Step 3: Run csv2nidm for phenotype integration
    logger.info(f"Step 3/3: Running csv2nidm for phenotype integration...")
    
    csv_file = Path("/home/yibei/simple2_bids2nidm/ABIDE2_Cophenotype.csv")
    
    # Check if CSV file exists
    if not csv_file.exists():
        logger.error(f"CSV file not found: {csv_file}")
        return 1
    
    # Use wrapper script for csv2nidm too
    csv_wrapper_script = Path("/home/yibei/simple2_bids2nidm/run_csv2nidm_noninteractive.sh")
    
    cmd = [
        str(csv_wrapper_script),
        "-csv", str(csv_file),
        "-json_map", str(json_map),
        "-nidm", str(phenotype_output),
        "-out", str(phenotype_output),
        "-log", str(log_dir),
        "-no_concepts"  # Match ABIDE1 processing
    ]
    
    logger.info(f"Command: {' '.join(cmd)}")
    
    try:
        # Run with wrapper script that handles prompts
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                              universal_newlines=True, timeout=3600)
        
        if result.returncode != 0:
            logger.error(f"csv2nidm failed for {site_name}")
            logger.error(f"STDOUT: {result.stdout}")
            logger.error(f"STDERR: {result.stderr}")
            # Don't fail completely if csv2nidm fails, we still have the NIDM file
            logger.warning(f"Phenotype integration failed, but NIDM file is available")
            return 0  # Return success since we have the NIDM file
        
        logger.info(f"csv2nidm completed successfully for {site_name}")
        logger.info(f"Successfully processed {site_name} - both NIDM and phenotype files created")
        
    except subprocess.TimeoutExpired:
        logger.error(f"Timeout processing {site_name} with csv2nidm (exceeded 1 hour)")
        logger.warning(f"Phenotype integration failed, but NIDM file is available")
        return 0
    except Exception as e:
        logger.error(f"Exception running csv2nidm for {site_name}: {e}")
        logger.warning(f"Phenotype integration failed, but NIDM file is available")
        return 0
    
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python abide2_process_site.py <site_name>")
        sys.exit(1)
    
    site_name = sys.argv[1]
    exit_code = process_site(site_name)
    sys.exit(exit_code)