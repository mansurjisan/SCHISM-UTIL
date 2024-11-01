#!/bin/bash

module purge
module use /work/noaa/nems/tufuk/COASTAL/ufs-coastal/modulefiles # change this path and point your ufs-coastal
module load ufs_orion.intel # chnage this if it is different platform

ifile=`ls *.SCRIP.*`
ofile=${ifile/.SCRIP./_ESMFmesh_}
ESMF_Scrip2Unstruct $ifile $ofile 0 ESMF
