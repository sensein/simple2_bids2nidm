#!/bin/bash
# Wrapper script to run csv2nidm non-interactively
# Provides default responses to any interactive prompts

# Pass all arguments to csv2nidm
# Provide sufficient newlines and default values for all potential prompts
(echo -e "\n\n3\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n") | micromamba run -n simple2 csv2nidm "$@"