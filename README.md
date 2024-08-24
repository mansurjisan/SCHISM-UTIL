# SCHISM-UTIL

# Installation and Usage of combine_output11_MPI

## Environment Setup

Use Intel OneAPI compilers and MPI on the Hercules cluster. Load the following modules:

```bash
module load intel-oneapi-compilers/2023.2.4
module load intel-oneapi-mpi/2021.13.0
module load netcdf-c/4.9.2
module load netcdf-fortran/4.6.1
```

## Compilation

Compile the program using the Intel MPI Fortran wrapper (mpiifort):

mpiifort -cpp -O2 -mcmodel=medium -assume byterecl -o combine_output11_MPI \
../UtilLib/argparse.f90 ../UtilLib/schism_geometry.f90 combine_output11_MPI.F90 \
-I$NETCDF/include -I$NETCDF_FORTRAN/include \
-L$NETCDF/lib -L$NETCDF_FORTRAN/lib -lnetcdff -lnetcdf


## Environment Variables
Set the NETCDF and NETCDF_FORTRAN environment variables:

```bash
export NETCDF=/apps/spack-managed/oneapi-2023.2.4/netcdf-c-4.9.2-qgy4pbuiliwyxhppgqgyb2jtc2vgfhzf
export NETCDF_FORTRAN=/apps/spack-managed/oneapi-2023.2.4/netcdf-fortran-4.6.1-6agxmmk6cbyavt472y6ds2d3b5ppekni
```

## Running the Program
Create a SLURM job script to run the program on the cluster. Use srun to launch the MPI program:

```bash
srun --label -n 10 ./combine_output11_MPI -b 1 -e 10 -w 1 -v "elev,hvel" -o schout
```

## Job Script
Create a SLURM job script (e.g., run_combine.sh) with appropriate SLURM directives and the srun command. Here's an example:

```bash

#!/bin/sh
#SBATCH -e combine_err
#SBATCH -o combine_out
#SBATCH --account=nosofs
#SBATCH --qos=batch
#SBATCH --partition=hercules
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --time=02:00:00
#SBATCH --job-name="combine_output"
#SBATCH --exclusive

set -eux
echo -n " $( date +%s )," >  combine_timestamp.txt
set +x

# Load modules
module load intel-oneapi-compilers/2023.2.4
module load intel-oneapi-mpi/2021.13.0
module load netcdf-c/4.9.2
module load netcdf-fortran/4.6.1

set -x
ulimit -s unlimited

echo "Combine started:  " `date`

export OMP_STACKSIZE=512M
export KMP_AFFINITY=scatter
export OMP_NUM_THREADS=1

# Set NetCDF environment variables
export NETCDF=/apps/spack-managed/oneapi-2023.2.4/netcdf-c-4.9.2-qgy4pbuiliwyxhppgqgyb2jtc2vgfhzf
export NETCDF_FORTRAN=/apps/spack-managed/oneapi-2023.2.4/netcdf-fortran-4.6.1-6agxmmk6cbyavt472y6ds2d3b5ppekni

sync && sleep 1

# Run the combine program
srun --label -n 10 ./combine_output11_MPI -b 1 -e 10 -w 1 -v "elev,hvel" -o schout

echo "Combine ended:    " `date`
echo -n " $( date +%s )," >> combine_timestamp.txt
```

# Running Interactively ./combine_output11_MPI

1. request number of nodes you need
salloc --account=nosofs --qos=batch --partition=hercules --nodes=1 --ntasks-per-node=10 --time=07:00:00 --job-name="combine_output_interactive" --exclusive

2. ssh to the node
3. cd to output file directory
   cd /work/noaa/nosofs/mjisan/ufs-weather-model/tests/stmp/mjisan/FV3_RT/coastal_ian_atm2sch_v4/outputs
5. source load_env.sh
6. srun --label -n 10 ./combine_output11_MPI -b 1 -e 4 -w 1 -v "elev" -o schout
7. srun --label -n 10 ./combine_output11_MPI -b 1 -e 4 -w 1 -v "wind_speed" -o schout_wind

# New data

