#!/bin/bash

# Simple script to process all ABIDE2 sites
# Each line processes one site

cd /home/yibei/simple2_bids2nidm

./scripts/process/process_abide2_sites.sh ABIDEII-BNI_1
./scripts/process/process_abide2_sites.sh ABIDEII-EMC_1
./scripts/process/process_abide2_sites.sh ABIDEII-ETHZ_1
#./scripts/process/process_abide2_sites.sh ABIDEII-GU_1  # Unicode error in participants.tsv
./scripts/process/process_abide2_sites.sh ABIDEII-IP_1
./scripts/process/process_abide2_sites.sh ABIDEII-IU_1
./scripts/process/process_abide2_sites.sh ABIDEII-KKI_1
./scripts/process/process_abide2_sites.sh ABIDEII-KUL_3
#./scripts/process/process_abide2_sites.sh ABIDEII-NYU_1  # Missing bvec files
#./scripts/process/process_abide2_sites.sh ABIDEII-NYU_2  # Missing bvec files
./scripts/process/process_abide2_sites.sh ABIDEII-OHSU_1
./scripts/process/process_abide2_sites.sh ABIDEII-ONRC_2
./scripts/process/process_abide2_sites.sh ABIDEII-SDSU_1
./scripts/process/process_abide2_sites.sh ABIDEII-TCD_1
./scripts/process/process_abide2_sites.sh ABIDEII-UCD_1
./scripts/process/process_abide2_sites.sh ABIDEII-UCLA_1
./scripts/process/process_abide2_sites.sh ABIDEII-UCLA_Long
./scripts/process/process_abide2_sites.sh ABIDEII-UPSM_Long
./scripts/process/process_abide2_sites.sh ABIDEII-USM_1

echo "All sites processing complete!"