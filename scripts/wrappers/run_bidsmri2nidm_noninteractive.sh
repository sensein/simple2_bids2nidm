#!/bin/bash
# Wrapper script to run bidsmri2nidm non-interactively
# Provides default responses to any interactive prompts

# Pass all arguments to bidsmri2nidm
# Provide sufficient newlines and default values for all potential prompts
# Using echo with -e to provide multiple lines of input
(echo -e "\n\n3\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n") | micromamba run -n simple2 bidsmri2nidm "$@"