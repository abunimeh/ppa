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

## Analyze verilog and SV files first

analyze -format sverilog ./inputs/rtl/alu_core.vs
analyze -format sverilog ./inputs/rtl/check_ecc_alu.vs
analyze -format sverilog ./inputs/rtl/check_ecc_in.vs
analyze -format sverilog ./inputs/rtl/fdkex.vs
analyze -format sverilog ./inputs/rtl/fifo.vs
analyze -format sverilog ./inputs/rtl/gen_ecc_alu.vs
analyze -format sverilog ./inputs/rtl/gen_ecc_in.vs
analyze -format sverilog ./inputs/rtl/init_mask_alu.vs
analyze -format sverilog ./inputs/rtl/init_mask_in.vs
analyze -format sverilog ./inputs/rtl/secded_alu.vs
analyze -format sverilog ./inputs/rtl/secded_in.vs
