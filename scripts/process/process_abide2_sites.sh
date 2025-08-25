#!/bin/bash

# ABIDE2 BIDS to NIDM Processing Script
# Processes a single site: bidsmri2nidm

set -euo pipefail

# Configuration
BASE_DIR="/orcd/data/satra/002/datasets/simple2_datalad/abide2"
JSON_MAP="$(pwd)/data/mappings/abide2_variables_to_terms_complete.json"
OUTPUT_DIR="$(pwd)/nidm_outputs/abide2"
LOG_DIR="$(pwd)/logs/abide2"

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
    local site_lowercase=$(echo "$site" | tr '[:upper:]' '[:lower:]' | sed 's/abideii-//g')
    local nidm_output="$OUTPUT_DIR/${site_lowercase}_nidm.ttl"
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
    
    # Step 1: Run bidsmri2nidm
    echo "  Running bidsmri2nidm..."
    if [[ -f "$(pwd)/scripts/wrappers/run_bidsmri2nidm_noninteractive.sh" ]]; then
        # Use wrapper for non-interactive processing
        if ! $(pwd)/scripts/wrappers/run_bidsmri2nidm_noninteractive.sh \
            -json_map "$JSON_MAP" \
            -d "$site_dir" \
            -o "$nidm_output" \
            -no_concepts >> "$site_log" 2>&1; then
            echo "  ERROR: bidsmri2nidm failed"
            return 1
        fi
    else
        if ! micromamba run -n simple2 bidsmri2nidm \
            -json_map "$JSON_MAP" \
            -d "$site_dir" \
            -o "$nidm_output" \
            -no_concepts >> "$site_log" 2>&1; then
            echo "  ERROR: bidsmri2nidm failed"
            return 1
        fi
    fi
    
    echo "  Completed successfully"
    return 0
}

# Main
if [[ $# -eq 0 ]] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    echo "Usage: $0 SITE"
    echo "  Process a single ABIDE2 site"
    echo ""
    echo "Examples:"
    echo "  $0 ABIDEII-BNI_1"
    echo "  $0 ABIDEII-NYU_1"
    exit 0
fi

process_site "$1"