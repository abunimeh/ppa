##############################################################################
## Intel Top Secret                                                         ##
##############################################################################
## Copyright (C) 2012, Intel Corporation.  All rights reserved.             ##
##                                                                          ##
## This is the property of Intel Corporation and may only be utilized       ##
## pursuant to a written Restricted Use Nondisclosure Agreement             ##
## with Intel Corporation.  It may not be used, reproduced, or              ##
## disclosed to others except in accordance with the terms and              ##
## conditions of such agreement.                                            ##
##                                                                          ##
## All products, processes, computer systems, dates, and figures            ##
## specified are preliminary based on current expectations, and are         ##
## subject to change without notice.                                        ##
##############################################################################

if { ![file isdirectory logs ]   } { file mkdir ../logs }
if { ![file isdirectory outputs] } { file mkdir ../outputs }
if { ![file isdirectory reports] } { file mkdir ../reports }
if { ![file isdirectory vcs_sim] } { file mkdir ../vcs_sim }

set INTEL_LIB                 "d04"
set INTEL_DESIGN_NAME         "fdkex"
set INTEL_DESIGN_NETLIST      "fdkex.syn.vg"

set_messages -level expert -log ../logs/${INTEL_DESIGN_NAME}.tmax.log -replace

read_netlist -lib -define INTCNOPWR $env(INTEL_STDCELLS)/verilog/ln/${INTEL_LIB}_ln_udp.v
read_netlist -lib -define INTCNOPWR $env(INTEL_STDCELLS)/verilog/nn/${INTEL_LIB}_nn_udp.v
read_netlist -lib -define INTCNOPWR $env(INTEL_STDCELLS)/verilog/wn/${INTEL_LIB}_wn_udp.v
read_netlist ../inputs/pll/pll_dft_model.v

read_netlist ../inputs/no_compression/${INTEL_DESIGN_NETLIST}

run_build_model $INTEL_DESIGN_NAME

#####TRANSITION DELAY FAULTS#####
#--------------------------------

add_pi_constraint 0 scan_enable
add_pi_constraint 1 rstb

set_delay -launch_cycle system_clock
set_delay -common_launch_capture_clock
set_delay -nopi_changes -nopo_measures

add_po_mask -all

set_drc ../inputs/no_compression/${INTEL_DESIGN_NAME}.syn.spf 
run_drc -patternexec Internal_scan

set_faults -model transition 

set_faults -summary verbose
add_faults -all

set_patterns -histogram_summary

set_contention -severity error

set_atpg -abort 10
run_atpg -auto

set_atpg -abort 10 -capture_cycles 4
run_atpg -auto
report_summaries

write_patterns ../outputs/${INTEL_DESIGN_NAME}.transition_atspeed.stil -format stil -last 5 -replace

foreach MODE {serial parallel} { 
  cd ../vcs_sim
  write_testbench \
	-input  ../outputs/${INTEL_DESIGN_NAME}.transition_atspeed.stil \
	-output ../vcs_sim/${INTEL_DESIGN_NAME}.transition_atspeed_${MODE} \
	-replace \
	-parameters "-v_file ../inputs/no_compression/${INTEL_DESIGN_NETLIST} -v_lib \"$env(INTEL_STDCELLS)/verilog/ln/${INTEL_LIB}_ln_udp.v,$env(INTEL_STDCELLS)/verilog/ln/${INTEL_LIB}_ln.v,$env(INTEL_STDCELLS)/verilog/nn/${INTEL_LIB}_nn_udp.v,$env(INTEL_STDCELLS)/verilog/nn/${INTEL_LIB}_nn.v,$env(INTEL_STDCELLS)/verilog/wn/${INTEL_LIB}_wn_udp.v,$env(INTEL_STDCELLS)/verilog/wn/${INTEL_LIB}_wn.v,../inputs/pll/pll_simulation_model.v\" -log ../logs/${INTEL_DESIGN_NAME}.transition_atspeed.${MODE}.tb.log -${MODE} -sim_script vcs -config_file ../inputs/config/${INTEL_DESIGN_NAME}.transition.config" 
}

#####STUCK AT FAULTS#####
#--------------------------------  

build -force
read_netlist -delete

read_netlist -define INTCNOPWR $env(INTEL_STDCELLS)/verilog/ln/${INTEL_LIB}_ln_udp.v
read_netlist -define INTCNOPWR $env(INTEL_STDCELLS)/verilog/nn/${INTEL_LIB}_nn_udp.v
read_netlist -define INTCNOPWR $env(INTEL_STDCELLS)/verilog/wn/${INTEL_LIB}_wn_udp.v
read_netlist ../inputs/pll/pll_dft_model.v

read_netlist ../inputs/no_compression/${INTEL_DESIGN_NETLIST}

run_build_model $INTEL_DESIGN_NAME

drc -force
remove_pi_constraints -all

set_faults -model stuck

set_drc ../inputs/no_compression/${INTEL_DESIGN_NAME}.syn.spf 
run_drc -patternexec Internal_scan_occ_bypass

set_faults -summary verbose
add_faults -all

set_patterns -histogram_summary

set_atpg -abort 10
run_atpg -auto

update_faults -reset_au
set_atpg -abort 20 -capture_cycles 4
run_atpg -auto
report_summaries

write_patterns ../outputs/${INTEL_DESIGN_NAME}.stuckat_occ_bypass.stil -format stil -last 5 -replace

foreach MODE {serial parallel} { 
  cd ../vcs_sim
  write_testbench \
	-input ../outputs/${INTEL_DESIGN_NAME}.stuckat_occ_bypass.stil \
	-output ../vcs_sim/${INTEL_DESIGN_NAME}.stuckat_occ_bypass_${MODE} \
	-replace \
	-parameters "-v_file ../inputs/no_compression/${INTEL_DESIGN_NETLIST} -v_lib \"$env(INTEL_STDCELLS)/verilog/ln/${INTEL_LIB}_ln_udp.v,$env(INTEL_STDCELLS)/verilog/ln/${INTEL_LIB}_ln.v,$env(INTEL_STDCELLS)/verilog/nn/${INTEL_LIB}_nn_udp.v,$env(INTEL_STDCELLS)/verilog/nn/${INTEL_LIB}_nn.v,$env(INTEL_STDCELLS)/verilog/wn/${INTEL_LIB}_wn_udp.v,$env(INTEL_STDCELLS)/verilog/wn/${INTEL_LIB}_wn.v,../inputs/pll/pll_simulation_model.v\" -log ../logs/${INTEL_DESIGN_NAME}.stuckat_occ_bypass.${MODE}.tb.log -${MODE} -sim_script vcs -config_file ../inputs/config/${INTEL_DESIGN_NAME}.stuckat.config"
}

exit

