#!/bin/sh 

LIB_FILES=" -v /p/fdk/fdk73/builds/stdcells/stdcell734_rc.0.0/verilog/ln/d04_ln_udp.v -v /p/fdk/fdk73/builds/stdcells/stdcell734_rc.0.0/verilog/ln/d04_ln.v -v /p/fdk/fdk73/builds/stdcells/stdcell734_rc.0.0/verilog/nn/d04_nn_udp.v -v /p/fdk/fdk73/builds/stdcells/stdcell734_rc.0.0/verilog/nn/d04_nn.v -v /p/fdk/fdk73/builds/stdcells/stdcell734_rc.0.0/verilog/wn/d04_wn_udp.v -v /p/fdk/fdk73/builds/stdcells/stdcell734_rc.0.0/verilog/wn/d04_wn.v -v ../inputs/pll/pll_simulation_model.v" 
DEFINES=" +define+tmax_diag=1" 
OPTIONS="+v2k -l vcs.sim.stuckat.log +delay_mode_zero +tetramax" 
NETLIST_FILES="../inputs/no_compression/fdkex.syn.vg" 
TBENCH_FILE="../vcs_sim/fdkex.stuckat_occ_bypass_parallel.v" 
SIMULATOR="vcs" 

${SIMULATOR} -R ${DEFINES} ${OPTIONS} ${TBENCH_FILE} ${NETLIST_FILES} ${LIB_FILES} 

SIMSTATUS=$? 
if [ ${SIMSTATUS} -ne 0 ] 
then echo "WARNING: simulation command returned error status ${SIMSTATUS}"; exit ${SIMSTATUS}; 
fi 
