#!/bin/bash

# Simple script to process all ABIDE1 sites
# Each line processes one site

cd /home/yibei/simple2_bids2nidm

./scripts/process/process_abide1_sites.sh Caltech
./scripts/process/process_abide1_sites.sh CMU_a
./scripts/process/process_abide1_sites.sh CMU_b
./scripts/process/process_abide1_sites.sh KKI
./scripts/process/process_abide1_sites.sh Leuven_1
./scripts/process/process_abide1_sites.sh Leuven_2
./scripts/process/process_abide1_sites.sh MaxMun_a
./scripts/process/process_abide1_sites.sh MaxMun_b
./scripts/process/process_abide1_sites.sh MaxMun_c
./scripts/process/process_abide1_sites.sh MaxMun_d
./scripts/process/process_abide1_sites.sh NYU
./scripts/process/process_abide1_sites.sh OHSU
./scripts/process/process_abide1_sites.sh Olin
./scripts/process/process_abide1_sites.sh Pitt
./scripts/process/process_abide1_sites.sh SBL
./scripts/process/process_abide1_sites.sh SDSU
./scripts/process/process_abide1_sites.sh Stanford
./scripts/process/process_abide1_sites.sh Trinity
./scripts/process/process_abide1_sites.sh UCLA_1
./scripts/process/process_abide1_sites.sh UCLA_2
./scripts/process/process_abide1_sites.sh UM_1
./scripts/process/process_abide1_sites.sh UM_2
./scripts/process/process_abide1_sites.sh USM
./scripts/process/process_abide1_sites.sh Yale

echo "All sites processing complete!"