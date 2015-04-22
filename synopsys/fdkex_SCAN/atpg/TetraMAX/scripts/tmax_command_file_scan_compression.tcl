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

if { ![file isdirectory ../logs ]   } { file mkdir ../logs }
if { ![file isdirectory ../outputs] } { file mkdir ../outputs }
if { ![file isdirectory ../reports] } { file mkdir ../reports }
if { ![file isdirectory ../vcs_sim] } { file mkdir ../vcs_sim }

set INTEL_LIB                 "d04"
set INTEL_DESIGN_NAME         "fdkex"
set INTEL_DESIGN_NETLIST      "fdkex.syn.vg"

set_messages -level expert -log ../logs/${INTEL_DESIGN_NAME}.tmax.scan_compress.log -replace

read_netlist -lib -define INTCNOPWR $env(INTEL_STDCELLS)/verilog/ln/${INTEL_LIB}_ln_udp.v
read_netlist -lib -define INTCNOPWR $env(INTEL_STDCELLS)/verilog/nn/${INTEL_LIB}_nn_udp.v
read_netlist -lib -define INTCNOPWR $env(INTEL_STDCELLS)/verilog/wn/${INTEL_LIB}_wn_udp.v
read_netlist ../inputs/pll/pll_dft_model.v

read_netlist ../inputs/compression/${INTEL_DESIGN_NETLIST}

run_build_model $INTEL_DESIGN_NAME

#------Transition Delay Faults in Compression mode -----

add_pi_constraint 0 scan_enable
add_pi_constraint 1 rstb

set_drc ../inputs/compression/${INTEL_DESIGN_NAME}.syn.scan_compress.spf 
run_drc -patternexec ScanCompression_mode_occ_bypass

set_faults -model transition 
set_delay -launch_cycle system_clock

set_faults -summary verbose
add_faults -all

set_patterns -histogram_summary

set_atpg -abort 10
run_atpg -auto

set_atpg -abort 10 -capture_cycles 4
run_atpg -auto
report_summaries

write_patterns ../outputs/${INTEL_DESIGN_NAME}.scan_compress.transition_occ_bypass.stil -format stil -last 5 -replace

foreach MODE {serial parallel} { 
  cd ../vcs_sim
  write_testbench \
	-input  ../outputs/${INTEL_DESIGN_NAME}.scan_compress.transition_occ_bypass.stil \
	-output ../vcs_sim/${INTEL_DESIGN_NAME}.scan_compress.transition_occ_bypass_${MODE} \
	-replace \
	-parameters "-v_file ../inputs/compression/${INTEL_DESIGN_NETLIST} -v_lib \"$env(INTEL_STDCELLS)/verilog/ln/${INTEL_LIB}_ln_udp.v,$env(INTEL_STDCELLS)/verilog/ln/${INTEL_LIB}_ln.v,$env(INTEL_STDCELLS)/verilog/nn/${INTEL_LIB}_nn_udp.v,$env(INTEL_STDCELLS)/verilog/nn/${INTEL_LIB}_nn.v,$env(INTEL_STDCELLS)/verilog/wn/${INTEL_LIB}_wn_udp.v,$env(INTEL_STDCELLS)/verilog/wn/${INTEL_LIB}_wn.v,../inputs/pll/pll_simulation_model.v\" -log ../logs/${INTEL_DESIGN_NAME}.scan_compress.transition_occ_bypass.${MODE}.tb.log -${MODE} -sim_script vcs -config_file ../inputs/config/${INTEL_DESIGN_NAME}.transition.config" 
}

#------Atspeed Faults in Compression mode (with OCC ON) ------

build -force
read_netlist -delete

read_netlist -lib -define INTCNOPWR $env(INTEL_STDCELLS)/verilog/ln/${INTEL_LIB}_ln_udp.v
read_netlist -lib -define INTCNOPWR $env(INTEL_STDCELLS)/verilog/nn/${INTEL_LIB}_nn_udp.v
read_netlist -lib -define INTCNOPWR $env(INTEL_STDCELLS)/verilog/wn/${INTEL_LIB}_wn_udp.v
read_netlist ../inputs/pll/pll_dft_model.v

read_netlist ../inputs/compression/${INTEL_DESIGN_NETLIST}

run_build_model $INTEL_DESIGN_NAME

drc -force
remove_pi_constraints -all

add_pi_constraint 0 scan_enable
add_pi_constraint 1 rstb

add_po_mask -all

set_drc ../inputs/compression/${INTEL_DESIGN_NAME}.syn.scan_compress.spf 
run_drc -patternexec ScanCompression_mode

set_faults -model transition 
set_delay -launch_cycle system_clock
set_delay -nopi_changes -nopo_measures

set_faults -summary verbose
add_faults -all

set_patterns -histogram_summary

set_atpg -abort 10
run_atpg -auto

set_atpg -abort 20 -capture_cycles 4
run_atpg -auto
report_summaries

write_patterns ../outputs/${INTEL_DESIGN_NAME}.scan_compress.transition_with_occ.stil -format stil -last 5 -replace

foreach MODE {serial parallel} { 
  cd ../vcs_sim
  write_testbench \
	-input  ../outputs/${INTEL_DESIGN_NAME}.scan_compress.transition_with_occ.stil \
	-output ../vcs_sim/${INTEL_DESIGN_NAME}.scan_compress.transition_with_occ_${MODE} \
	-replace \
	-parameters "-v_file ../inputs/compression/${INTEL_DESIGN_NETLIST} -v_lib \"$env(INTEL_STDCELLS)/verilog/ln/${INTEL_LIB}_ln_udp.v,$env(INTEL_STDCELLS)/verilog/ln/${INTEL_LIB}_ln.v,$env(INTEL_STDCELLS)/verilog/nn/${INTEL_LIB}_nn_udp.v,$env(INTEL_STDCELLS)/verilog/nn/${INTEL_LIB}_nn.v,$env(INTEL_STDCELLS)/verilog/wn/${INTEL_LIB}_wn_udp.v,$env(INTEL_STDCELLS)/verilog/wn/${INTEL_LIB}_wn.v,../inputs/pll/pll_simulation_model.v\" -log ../logs/${INTEL_DESIGN_NAME}.scan_compress.transition_with_occ.${MODE}.tb.log -${MODE} -sim_script vcs -config_file ../inputs/config/${INTEL_DESIGN_NAME}.transition.config" 
}


#------Stuckat Faults in Compression mode, with occ_bypass ------

build -force
read_netlist -delete

read_netlist -lib -define INTCNOPWR $env(INTEL_STDCELLS)/verilog/ln/${INTEL_LIB}_ln_udp.v
read_netlist -lib -define INTCNOPWR $env(INTEL_STDCELLS)/verilog/nn/${INTEL_LIB}_nn_udp.v
read_netlist -lib -define INTCNOPWR $env(INTEL_STDCELLS)/verilog/wn/${INTEL_LIB}_wn_udp.v
read_netlist ../inputs/pll/pll_dft_model.v

read_netlist ../inputs/compression/${INTEL_DESIGN_NETLIST}

run_build_model $INTEL_DESIGN_NAME

drc -force
remove_pi_constraints -all

set_faults -model stuck 

set_drc ../inputs/compression/${INTEL_DESIGN_NAME}.syn.scan_compress.spf 
run_drc -patternexec ScanCompression_mode_occ_bypass

set_faults -summary verbose
add_faults -all

set_patterns -histogram_summary

set_atpg -abort 10
run_atpg -auto

update_faults -reset_au
set_atpg -abort 20 -capture_cycles 4
run_atpg -auto
report_summaries

write_patterns ../outputs/${INTEL_DESIGN_NAME}.scan_compress.stuckat.stil -format stil -last 5 -replace

foreach MODE {serial parallel} { 
  cd ../vcs_sim
  write_testbench \
	-input ../outputs/${INTEL_DESIGN_NAME}.scan_compress.stuckat.stil \
	-output ../vcs_sim/${INTEL_DESIGN_NAME}.scan_compress.stuckat_${MODE} \
	-replace \
	-parameters "-v_file ../inputs/compression/${INTEL_DESIGN_NETLIST} -v_lib \"$env(INTEL_STDCELLS)/verilog/ln/${INTEL_LIB}_ln_udp.v,$env(INTEL_STDCELLS)/verilog/ln/${INTEL_LIB}_ln.v,$env(INTEL_STDCELLS)/verilog/nn/${INTEL_LIB}_nn_udp.v,$env(INTEL_STDCELLS)/verilog/nn/${INTEL_LIB}_nn.v,$env(INTEL_STDCELLS)/verilog/wn/${INTEL_LIB}_wn_udp.v,$env(INTEL_STDCELLS)/verilog/wn/${INTEL_LIB}_wn.v,../inputs/pll/pll_simulation_model.v\" -log ../logs/${INTEL_DESIGN_NAME}.scan_compress.stuckat.${MODE}.tb.log -${MODE} -sim_script vcs -config_file ../inputs/config/${INTEL_DESIGN_NAME}.stuckat.config" 
}

#------Stuckat Faults in Compression_bypass mode, with occ_bypass ------

build -force
read_netlist -delete

read_netlist -lib -define INTCNOPWR $env(INTEL_STDCELLS)/verilog/ln/${INTEL_LIB}_ln_udp.v
read_netlist -lib -define INTCNOPWR $env(INTEL_STDCELLS)/verilog/nn/${INTEL_LIB}_nn_udp.v
read_netlist -lib -define INTCNOPWR $env(INTEL_STDCELLS)/verilog/wn/${INTEL_LIB}_wn_udp.v
read_netlist ../inputs/pll/pll_dft_model.v

read_netlist ../inputs/compression/${INTEL_DESIGN_NETLIST}

run_build_model $INTEL_DESIGN_NAME

drc -force
remove_pi_constraints -all

set_faults -model stuck 

set_drc ../inputs/compression/${INTEL_DESIGN_NAME}.syn.scan_internal.spf 
run_drc -patternexec Internal_scan_occ_bypass

set_faults -summary verbose
add_faults -all
remove_faults -module fdkex_SCCOMP_COMPRESSOR
remove_faults -module fdkex_SCCOMP_DECOMPRESSOR

set_patterns -histogram_summary

set_atpg -abort 10
run_atpg -auto

update_faults -reset_au
set_atpg -abort 20 -capture_cycles 4
run_atpg -auto
report_summaries

write_patterns ../outputs/${INTEL_DESIGN_NAME}.internal_scan.stuckat.stil -format stil -last 5 -replace

foreach MODE {serial parallel} { 
  cd ../vcs_sim
  write_testbench \
	-input ../outputs/${INTEL_DESIGN_NAME}.internal_scan.stuckat.stil \
	-output ../vcs_sim/${INTEL_DESIGN_NAME}.internal_scan.stuckat_${MODE} \
	-replace \
	-parameters "-v_file ../inputs/compression/${INTEL_DESIGN_NETLIST} -v_lib \"$env(INTEL_STDCELLS)/verilog/ln/${INTEL_LIB}_ln_udp.v,$env(INTEL_STDCELLS)/verilog/ln/${INTEL_LIB}_ln.v,$env(INTEL_STDCELLS)/verilog/nn/${INTEL_LIB}_nn_udp.v,$env(INTEL_STDCELLS)/verilog/nn/${INTEL_LIB}_nn.v,$env(INTEL_STDCELLS)/verilog/wn/${INTEL_LIB}_wn_udp.v,$env(INTEL_STDCELLS)/verilog/wn/${INTEL_LIB}_wn.v,../inputs/pll/pll_simulation_model.v\" -log ../logs/${INTEL_DESIGN_NAME}.internal_scan.stuckat.${MODE}.tb.log -${MODE} -sim_script vcs -config_file ../inputs/config/${INTEL_DESIGN_NAME}.stuckat.config" 
}
exit

