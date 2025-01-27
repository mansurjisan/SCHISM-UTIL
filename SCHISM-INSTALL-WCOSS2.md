# Installing SCHISM on WCOSS2

## Prerequisites

Before beginning the installation, ensure you have appropriate access to WCOSS2 and sufficient disk space in your working directory.

## Step 1: Load Required Modules

First, create a module loading script (e.g., `load_modules.sh`) with the following content:

```bash
module purge
module load envvar/$envvar_ver
module load intel/$intel_ver
module load PrgEnv-intel/$PrgEnv_intel_ver
module load craype/$craype_ver
module load cray-mpich/$cray_mpich_ver
module load hdf5/$hdf5_ver
module load netcdf/$netcdf_ver
```


## Step 2: Clone the Repository

First, clone the SCHISM repository with its submodules:

```bash
git clone --recurse-submodules https://github.com/schism-dev/schism.git
```

The `--recurse-submodules` flag is essential as it ensures all required submodules are also cloned.

Then, navigate to your working director; for my case it is below directory:

```bash
cd /lfs/h1/nos/estofs/noscrub/mansur.jisan/packages/schism
```

## Step 3: Configure Build with CMake

### Basic SCHISM Build
For a basic SCHISM build:
```bash
cmake -S ./src -B ./build -C ./cmake/SCHISM.local.wcoss2 -DBLD_STANDALONE=ON -DNO_PARMETIS=OFF
```

### SCHISM with PaHM Coupling
For building SCHISM coupled with PaHM:
```bash
cmake -S ./src -B ./build -C ./cmake/SCHISM.local.wcoss2 -DBLD_STANDALONE=ON -DUSE_PAHM=ON -DNO_PARMETIS=OFF
```

These cmake options:
- `-DBLD_STANDALONE=ON`: Enables standalone build mode
- `-DUSE_PAHM=ON`: Activates PaHM coupling
- `-DNO_PARMETIS=OFF`: Enables ParMETIS support for domain decomposition

## Step 4: Compile SCHISM

```bash
cd build
make -j 8 pschism
```

The `-j 8` flag enables parallel compilation with 8 threads. Adjust this number based on your system's capabilities and restrictions.

## Troubleshooting Tips

1. If you encounter module loading errors:
   - Verify module versions are available on your system
   - Check for module conflicts
   - Ensure modules are loaded in the correct order

2. If CMake configuration fails:
   - Verify all required modules are loaded
   - Check if `SCHISM.local.wcoss2` contains correct paths
   - Ensure you have write permissions in the build directory

3. If compilation fails:
   - Check compiler error messages
   - Verify MPI environment is properly configured
   - Ensure sufficient memory and disk space

## Verification

After successful compilation:

### Locating the Executable
1. The executable will be located in the `/build/bin` directory
2. For standalone builds with PaHM coupling, the executable name will follow this pattern:
   ```
   pschism_HERCULES_PAHM_BLD_STANDALONE_TVD-VL
   ```

## Additional Notes

- Keep track of the specific module versions used for reproducibility
- Document any custom modifications to the build configuration
- Consider creating a backup of working configurations
