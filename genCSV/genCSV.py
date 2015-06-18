#!/usr/bin/env python3.3.1
# MAIN

# import os
import sys
# import genCSV
import Metrics.GenerateMetric
# sys_args = ["C:\dev\intel\ppa\cadence\mult_1bit_scan(copy)"]

Metrics.GenerateMetric.determine_testcases(sys.argv)

