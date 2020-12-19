#!/bin/bash

source $CONDA_PREFIX/etc/profile.d/conda.sh
conda activate reachy-env

cd /reachy
jupyter notebook --port=8888 --no-browser --ip=0.0.0.0 --NotebookApp.token='' --allow-root --NotebookApp.password=''

