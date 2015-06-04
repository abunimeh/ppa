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


# This is a TEMPLATE file for CLOCK CONSTRAINTS FILE
# create_clock -name pxclk -period 6666.67 -waveform {0 3333.33} [get_ports {pxclk}]
# set_input_transition 150 -max [ get_ports pxclk ]
# set_input_transition 75 -min [ get_ports pxclk ]


# create_clock -name xtclk_13p5 -period 73337 -waveform {0 36668.5} [get_ports {xtclk_13p5}]
# set_input_transition 150 -max [ get_ports xtclk_13p5 ]
# set_input_transition 75 -min [ get_ports xtclk_13p5 ]

# Make sure all combinations are here
# for n clocks, there should be n^2 max clock uncertainty lines and n^2 min clock uncertainty
# set_clock_uncertainty -hold 300 -from pxclk -to pxclk
# set_clock_uncertainty -hold 300 -from pxclk -to xtclk_13p5
# set_clock_uncertainty -hold 300 -from xtclk_13p5 -to pxclk
# set_clock_uncertainty -hold 300 -from xtclk_13p5 -to xtclk_13p5

# set_clock_uncertainty -setup 235 -from pxclk -to pxclk
# set_clock_uncertainty -setup 235 -from pxclk -to xtclk_13p5
# set_clock_uncertainty -setup 235 -from xtclk_13p5 -to pxclk
# set_clock_uncertainty -setup 235 -from xtclk_13p5 -to xtclk_13p5

# clock insertion delay
# This is the same as specified for CTS in APR
# set_clock_latency <number> [get_clocks {pxclk}]
# set_clock_latency <number> [get_clocks {xtclk_13p5}]

#GENERATED CLOCKS
#create_generated_clock -name GEN_CLK -source [get_pins clk_div2_ckcorediv2/clockdivff_cknameout/ffout_reg/ck] -divide_by 2 [get_pins clk_div2_ckcorediv2/clockdivff_cknameout/ffout_reg/o]

#VIRTUAL CLOCKS
#create_clock -name  VIRTUAL_CLK   -period  1088   -waveform {0.000 0544}


create_clock -name clk -period 500 -waveform {0 250} [get_ports {clk}]
set_clock_uncertainty -setup 50 [get_clocks clk]
set_clock_uncertainty -hold  50 [get_clocks clk]
