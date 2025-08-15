#!/bin/bash

# ABIDE1 BIDS to NIDM Processing Script
# Processes a single site: bidsmri2nidm -> copy -> csv2nidm

set -euo pipefail

# Configuration
BASE_DIR="/orcd/data/satra/002/datasets/simple2_datalad/abide1"
JSON_MAP="$(pwd)/data/mappings/abide_phenotypic_v1_0b_vars_to_terms_v5.json"
CSV_FILE="$(pwd)/data/phenotypes/Phenotypic_V1_0b.csv"
OUTPUT_DIR="$(pwd)/nidm_outputs/abide1"
LOG_DIR="$(pwd)/logs/abide1"

# Create directories
mkdir -p "$OUTPUT_DIR" "$LOG_DIR"

# Check prerequisites
if [[ ! -f "$JSON_MAP" ]]; then
    echo "ERROR: JSON mapping file not found: $JSON_MAP"
    exit 1
fi

if [[ ! -f "$CSV_FILE" ]]; then
    echo "ERROR: CSV file not found: $CSV_FILE"
    exit 1
fi

if ! command -v micromamba &> /dev/null; then
    echo "ERROR: micromamba not found"
    exit 1
fi

# Process a single site
process_site() {
    local site="$1"
    local site_dir="$BASE_DIR/$site"
    local nidm_output="$OUTPUT_DIR/${site}_nidm.ttl"
    local phenotype_output="$OUTPUT_DIR/${site}_phenotype.ttl"
    local site_log="$LOG_DIR/${site}_processing.log"
    
    echo "Processing site: $site"
    
    # Check if site directory exists
    if [[ ! -d "$site_dir" ]]; then
        echo "ERROR: Site directory not found: $site_dir"
        return 1
    fi
    
    # Check if already processed
    if [[ -f "$phenotype_output" ]]; then
        echo "  Already processed, skipping"
        return 0
    fi
    
    # Step 1: Run bidsmri2nidm
    echo "  Step 1/3: Running bidsmri2nidm..."
    if ! micromamba run -n simple2 bidsmri2nidm \
        -json_map "$JSON_MAP" \
        -d "$site_dir" \
        -o "$nidm_output" \
        -no_concepts >> "$site_log" 2>&1; then
        echo "  ERROR: bidsmri2nidm failed"
        return 1
    fi
    
    # Step 2: Copy for phenotype integration
    echo "  Step 2/3: Creating copy..."
    cp "$nidm_output" "$phenotype_output"
    
    # Step 3: Run csv2nidm
    echo "  Step 3/3: Running csv2nidm..."
    if ! micromamba run -n simple2 csv2nidm \
        -csv "$CSV_FILE" \
        -json_map "$JSON_MAP" \
        -nidm "$phenotype_output" \
        -log "$LOG_DIR" \
        -no_concepts >> "$site_log" 2>&1; then
        echo "  ERROR: csv2nidm failed"
        return 1
    fi
    
    # Clean up backup
    rm -f "${phenotype_output}.bak"
    
    echo "  Completed successfully"
    return 0
}

# Main
if [[ $# -eq 0 ]] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    echo "Usage: $0 SITE"
    echo "  Process a single ABIDE1 site"
    echo ""
    echo "Examples:"
    echo "  $0 Caltech"
    echo "  $0 NYU"
    exit 0
fi

process_site "$1"