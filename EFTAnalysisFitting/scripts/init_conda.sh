#!/usr/bin/env bash

# conda init bash

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('~/nobackup/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "~/nobackup/miniconda3/etc/profile.d/conda.sh" ]; then
        . "~/nobackup/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="~/nobackup/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

# activate VVV environment
eval "$(conda shell.bash hook)"
conda activate VVV
