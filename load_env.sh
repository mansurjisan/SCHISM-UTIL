#!/bin/bash

# Load modules
module purge  # Clear all modules first
while read module; do
    module load $module
done < my_modules.txt

# Set environment variables
source /work/noaa/nosofs/mjisan/ufs-weather-model/tests/stmp/mjisan/FV3_RT/coastal_ian_atm2sch_v4/outputs/my_env.txt

# Add any additional setup commands here
