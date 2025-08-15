#!/usr/bin/env python
import pandas as pd
import json

# Read one site to get all columns
df = pd.read_csv('/orcd/data/satra/002/datasets/simple2_datalad/abide2/ABIDEII-BNI_1/participants.tsv', sep='\t')

# Create comprehensive mapping for ABIDE2 columns
mapping = {}

# Define some common mappings
common_mappings = {
    'site_id': {
        'label': 'Site Identifier',
        'description': 'ABIDE2 site identifier',
        'valueType': 'http://www.w3.org/2001/XMLSchema#string',
        'associatedWith': 'NIDM'
    },
    'participant_id': {
        'label': 'Participant Identifier', 
        'description': 'Unique participant identifier',
        'valueType': 'http://www.w3.org/2001/XMLSchema#string',
        'associatedWith': 'NIDM'
    },
    'age_at_scan ': {  # Note the space in the column name
        'label': 'Age at Scan',
        'description': 'Age of participant at time of scan',
        'valueType': 'http://www.w3.org/2001/XMLSchema#float',
        'associatedWith': 'NIDM'
    },
    'sex': {
        'label': 'Sex',
        'description': 'Biological sex of participant',
        'valueType': 'http://www.w3.org/2001/XMLSchema#integer',
        'associatedWith': 'NIDM'
    },
    'dx_group': {
        'label': 'Diagnosis Group',
        'description': 'Diagnostic group (1=ASD, 2=TD)',
        'valueType': 'http://www.w3.org/2001/XMLSchema#integer',
        'associatedWith': 'NIDM'
    }
}

for col in df.columns:
    if col in common_mappings:
        mapping[col] = common_mappings[col]
    else:
        # Default mapping for other columns
        mapping[col] = {
            'label': col.replace('_', ' ').title(),
            'description': f'ABIDE2 {col} variable',
            'valueType': 'http://www.w3.org/2001/XMLSchema#string',
            'associatedWith': 'NIDM',
            'hasUnit': '',
            'minValue': '',
            'maxValue': '',
            'source_variable': col
        }
    
    # Ensure all have required fields
    if 'hasUnit' not in mapping[col]:
        mapping[col]['hasUnit'] = ''
    if 'minValue' not in mapping[col]:
        mapping[col]['minValue'] = ''
    if 'maxValue' not in mapping[col]:
        mapping[col]['maxValue'] = ''
    if 'source_variable' not in mapping[col]:
        mapping[col]['source_variable'] = col

# Save to JSON
with open('/home/yibei/simple2_bids2nidm/abide2_variables_to_terms_complete.json', 'w') as f:
    json.dump(mapping, f, indent=2)

print(f'Created complete mapping for {len(mapping)} columns')
print('Saved to: /home/yibei/simple2_bids2nidm/abide2_variables_to_terms_complete.json')