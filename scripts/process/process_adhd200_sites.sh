#!/bin/bash

# ADHD200 BIDS to NIDM Processing Script
# Process ADHD200 sites using bidsmri2nidm (no phenotypic integration)

set -euo pipefail

# Configuration
BASE_DIR="/orcd/data/satra/002/datasets/simple2_datalad/adhd200"
JSON_MAP="$(pwd)/data/mappings/adhd200_vars_to_terms_v5.json"
OUTPUT_DIR="$(pwd)/nidm_outputs/adhd200"
LOG_DIR="$(pwd)/logs/adhd200"

# Create directories
mkdir -p "$OUTPUT_DIR" "$LOG_DIR"

# Check prerequisites
if [[ ! -f "$JSON_MAP" ]]; then
    echo "ERROR: JSON mapping file not found: $JSON_MAP"
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
    local site_log="$LOG_DIR/${site}_processing.log"
    
    echo "Processing site: $site"
    
    # Check if site directory exists
    if [[ ! -d "$site_dir" ]]; then
        echo "ERROR: Site directory not found: $site_dir"
        return 1
    fi
    
    # Check if already processed
    if [[ -f "$nidm_output" ]]; then
        echo "  Already processed, skipping"
        return 0
    fi
    
    # Run bidsmri2nidm
    echo "  Running bidsmri2nidm..."
    if ! micromamba run -n simple2 bidsmri2nidm \
        -json_map "$JSON_MAP" \
        -d "$site_dir" \
        -o "$nidm_output" \
        -no_concepts >> "$site_log" 2>&1; then
        echo "  ERROR: bidsmri2nidm failed"
        return 1
    fi
    
    echo "  Completed successfully"
    return 0
}

# Main
if [[ $# -eq 0 ]] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    echo "Usage: $0 SITE"
    echo "  Process a single ADHD200 site"
    echo ""
    echo "Examples:"
    echo "  $0 KKI"
    echo "  $0 NYU"
    exit 0
fi

process_site "$1"