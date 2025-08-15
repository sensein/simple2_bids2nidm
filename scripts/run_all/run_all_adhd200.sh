#!/bin/bash

# Simple script to process all ADHD200 sites
# Each line processes one site

cd /home/yibei/simple2_bids2nidm

./scripts/process/process_adhd200_sites.sh Brown
./scripts/process/process_adhd200_sites.sh KKI
./scripts/process/process_adhd200_sites.sh NeuroIMAGE
./scripts/process/process_adhd200_sites.sh NYU
./scripts/process/process_adhd200_sites.sh OHSU
./scripts/process/process_adhd200_sites.sh Peking_1
./scripts/process/process_adhd200_sites.sh Peking_2
./scripts/process/process_adhd200_sites.sh Peking_3
./scripts/process/process_adhd200_sites.sh Pittsburgh
./scripts/process/process_adhd200_sites.sh WashU

echo "All sites processing complete!"