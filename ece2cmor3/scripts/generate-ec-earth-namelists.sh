#!/bin/bash
# Thomas Reerink
#
# This scripts needs no arguments
#
# ${1} the first   argument is the MIP name
# ${2} the second  argument is the experiment name or MIP name in the latter case all MIP experiments are taken.
# ${3} the third   argument is the experiment tier (tier 1 is obligatory, higher tier is non-obligatory). In case tier 2 is specified, tier 1 and 2 experiments are considered.
# ${4} the fourth  argument is the maximum priority of the variables (1 is highest priority, 3 is lowest priority). In case priority 2 is specified, priority 1 and 2 variables are considered.
#
#
# Run example:
#  ./generate-ec-earth-namelists.sh CMIP amip 1 1
#


# Set the root directory of ece2cmor3 (default ${HOME}/cmorize/ece2cmor3/ ):
ece2cmor_root_directory=${HOME}/cmorize/ece2cmor3/

# Test whether the ece2cmor_root_directory exists:
if [ ! -d ${ece2cmor_root_directory} ]; then 
 echo
 echo ' The root directory of ece2cmor3: ' ${ece2cmor_root_directory} ' is not found.'
 echo ' Adjust the ece2cmor_root_directory at line 18 of the script: ' $0
 echo ' Stop'
 exit
 echo
fi

if [ "$#" -eq 4 ]; then
 mip=$1
 experiment=$2
 tier=$3
 priority=$4
 
 # Replace , by dot in label:
 mip_label=$(echo ${mip} | sed 's/,/./g')

#activateanaconda
 if ! type "drq" > /dev/null; then
  echo
  echo ' The CMIP6 data request tool drq is not available because of one of the following reasons:' 
  echo '  1. drq might be not installed'
  echo '  2. drq might be not active, as the anaconda environment is not activated'
  echo ' Stop'
  echo
  exit
 else
 #source activate ece2cmor3
  cd ${ece2cmor_root_directory}; python setup.py install; cd -;
  mkdir -p  ${ece2cmor_root_directory}/ece2cmor3/scripts/cmip6-data-request/; cd ${ece2cmor_root_directory}/ece2cmor3/scripts/cmip6-data-request/;
  drq -m ${mip} -t ${tier} -p ${priority} -e ${experiment} --xls --xlsDir cmip6-data-request-m=${mip_label}-e=${experiment}-t=${tier}-p=${priority}
  cd ${ece2cmor_root_directory}/ece2cmor3/scripts/
  # Note that the *TOTAL* selection below has the risk that more than one file is selected (causing a crash) which only could happen if externally files are added in this directory:
  ./drq2ppt.py --vars cmip6-data-request/cmip6-data-request-m=${mip_label}-e=${experiment}-t=${tier}-p=${priority}/cmvmm_${mip_label}_TOTAL_${tier}_${priority}.xlsx
 #./drq2ppt.py --vars cmip6-data-request/cmip6-data-request-m=${mip_label}-e=${experiment}-t=${tier}-p=${priority}/cmvmm_${mip_label}_${experiment}_${tier}_${priority}.xlsx
 #source deactivate
 fi
 mkdir -p ec-earth-namelists/ec-earth-namelists-m=${mip_label}-e=${experiment}-t=${tier}-p=${priority}/
 mv -f pptdddddd0300 pptdddddd0600 ec-earth-namelists/ec-earth-namelists-m=${mip_label}-e=${experiment}-t=${tier}-p=${priority}/
 

 # A block with calling drq2nemo_file_def.py has to be added here.


 echo
 echo 'The generated ppt files are:'
 ls -1 ec-earth-namelists/ec-earth-namelists-m=${mip_label}-e=${experiment}-t=${tier}-p=${priority}/pptdddddd0[3,6]00
 echo

else
    echo '  '
    echo '  This scripts requires four arguments: MIP, MIP experiment, experiment tier, priority of variable, e.g.:'
    echo '  ' $0 CMIP amip 1 1
    echo '  '
fi

# ./generate-ec-earth-namelists.sh.sh AerChemMIP   amip 1 1
# ./generate-ec-earth-namelists.sh.sh C4MIP        amip 1 1
# ./generate-ec-earth-namelists.sh.sh DCPP         amip 1 1
# ./generate-ec-earth-namelists.sh.sh HighResMIP   amip 1 1
# ./generate-ec-earth-namelists.sh.sh ISMIP6       amip 1 1
# ./generate-ec-earth-namelists.sh.sh LS3MIP       amip 1 1
# ./generate-ec-earth-namelists.sh.sh LUMIP        amip 1 1
# ./generate-ec-earth-namelists.sh.sh PMIP         amip 1 1
# ./generate-ec-earth-namelists.sh.sh RFMIP        amip 1 1
# ./generate-ec-earth-namelists.sh.sh ScenarioMIP  amip 1 1
# ./generate-ec-earth-namelists.sh.sh VolMIP       amip 1 1
# ./generate-ec-earth-namelists.sh.sh CORDEX       amip 1 1
# ./generate-ec-earth-namelists.sh.sh DynVar       amip 1 1
# ./generate-ec-earth-namelists.sh.sh SIMIP        amip 1 1
# ./generate-ec-earth-namelists.sh.sh VIACSAB      amip 1 1
# ./generate-ec-earth-namelists.sh.sh DAMIP        amip 1 1

# diff ec-earth-namelists/ec-earth-namelists-m=CMIP-e=amip-t=1-p=1/pptdddddd0300 bup-pptdddddd0300 ; diff ec-earth-namelists/ec-earth-namelists-m=CMIP-e=amip-t=1-p=1/pptdddddd0600 bup-pptdddddd0600

