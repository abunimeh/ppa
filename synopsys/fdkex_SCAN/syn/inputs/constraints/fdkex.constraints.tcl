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


###############################
# Default Loading Constraints
###############################
#User should copy this file in ./inputs/constraints/${G_DESIGN_NAME}.constraints.tcl and overwrite the actual value

#Default setting input_delay & output_delay of 2/3rd  of fastest clock
#-----------------------------------------------------------------------
set delay_value [expr [lindex [lsort -real -decreasing [get_attribute [get_clocks ] period]] end] * 2/3]

set clock_name [get_clocks clk]
set_input_delay  -clock $clock_name $delay_value [remove_from_collection [all_inputs] [get_ports clk]]
set_output_delay -clock $clock_name $delay_value [all_outputs]


#Default input transition or loading cons
#-----------------------------------------

set my_driving_cell d04bfn00ln0b0
if {[get_lib_cells */$my_driving_cell -quiet] != ""} {
   set_driving_cell -lib_cell $my_driving_cell [all_inputs]
   puts "==>INFORMATION: Setting driving cell to $my_driving_cell"
} else {
   set_input_transition 50 [all_inputs]
   puts "==>INFORMATION: Specified driving cell $my_driving_cell was not found. Setting default input transition as 50"
}


set_load 10 [all_outputs]
set_max_transition 350 *
set_max_fanout 30 [get_designs *]
set_max_area 0


