

** Technology
* STAR_INSTALL_PATH = <KIT_ROOT>/extraction/starrc/techfiles
* FILE_NXTGRD = STAR_INSTALL_PATH/p1273_3x1r6.<SKEW>.nxtgrd
* SKEW = See release notes for available skews
TCAD_GRD_FILE: /p/fdk/fdk73/builds/pdk733_r1.7/extraction/starrc/techfiles/p1273_3x1r6.tttt.nxtgrd
* starrc.map = <KIT_ROOT>/extraction/starrc/cmdfiles/asic.starrc.map
MAPPING_FILE: /p/fdk/fdk73/builds/pdk733_r1.7/extraction/starrc/cmdfiles/asic.starrc.map

** Via Handling
* FILE_ASIC_VIACOV = STAR_INSTALL_PATH/p1273_3x1r6.<SKEW>.via_coverage.asic
VIA_COVERAGE_OPTION_FILE: /p/fdk/fdk73/builds/pdk733_r1.7/extraction/starrc/techfiles/p1273_3x1r6.tttt.via_coverage.asic
MERGE_VIAS_IN_ARRAY: NO
TRANSLATE_VIA_LAYERS: YES

** Black box cells
SKIP_CELLS: * 

** Output database
STAR_DIRECTORY: star_fdkex_mw
SUMMARY_FILE: star_fdkex_mw.sum

** Extraction options
EXTRACTION: RC
FILL_COUPLING_THRESHOLD: 1.0e-19
KEEP_VIA_NODES: YES
INSTANCE_PORT: SUPERCONDUCTIVE
REMOVE_FLOATING_NETS: YES
REMOVE_DANGLING_NETS: NO
REPORT_SMIN_VIOLATION: YES
* <VALUE_TEMPERATURE> to be referenced from userguide
OPERATING_TEMPERATURE: -10
NETS: *
NET_TYPE: SCHEMATIC
POWER_NETS: vcc vcc* vss vss*
POWER_EXTRACT: NO

** Reduction
* VALUE_REDUCTION_MODE = YES or NO
REDUCTION: NO
* VALUE_POWER_REDUCTION_MODE = YES or NO
POWER_REDUCTION: NO
REDUCTION_MAX_DELAY_ERROR: 1.0e-15

** Accuracy
MODE: 400
FSCOMPARE_THRESHOLD: 1e-16
FSCOMPARE_COUPLING_RATIO: 0.05
FSCOMPARE_OPTIONS: -abs_self 1e-17 -perc_self 1 -abs_coup 1e-17 -perc_coup 1

** Netlisting options
* VALUE_FORMAT = spef or sbpf
NETLIST_FILE: fdkex_mw.spef.gz
NETLIST_COMPRESS_COMMAND: /bin/gzip
NETLIST_FORMAT: SPEF
NETLIST_NODE_SECTION: YES
NETLIST_INSTANCE_SECTION: YES
SHORT_PINS: YES
NETLIST_NAME_MAP: NO
NETLIST_CONNECT_SECTION: YES
NETLIST_UNSCALED_COORDINATES: YES
NETLIST_CONNECT_OPENS: !*
NETLIST_REMOVE_ISOLATED_PORTS: ALL
* VALUE_TAILCOMMENTS = YES or NO based on REDUCTION setting
NETLIST_TAIL_COMMENTS: NO
NETLIST_POWER_FILE: 
NETLIST_INPUT_DRIVERS: YES
NETLIST_TYPE: RCc
NETLIST_SELECT_NETS: * !*zone*
NETLIST_COUPLE_UNSELECTED_NETS: IDEAL
NETLIST_GROUND_NODE_NAME: VSS
NETLIST_PASSIVE_PARAMS: YES
* VALUE_NODE_MODE = NODE or NONE or NODE RES
EXTRA_GEOMETRY_INFO: NODE

** Fill handling
METAL_FILL_POLYGON_HANDLING: FLOATING
TRANSLATE_FLOATING_AS_FILL: YES
METAL_FILL_RECONNECT: YES
UNIMPORTANT_NETS: METAL_FILL

** Coupling cap options
* NOTE:Some of the options like COUPLING_ABS/REL_THRESHOLD, are from Synopsys ICC/StarRC parasitic correlation checklist (Doc Id: 023289)
GROUND_CROSS_COUPLING: NO
COUPLING_ABS_THRESHOLD: 5e-16
COUPLING_REL_THRESHOLD: 0.03
COUPLE_TO_GROUND: NO



** Milkyway flow
MILKYWAY_DATABASE: /p/fdkgt/adf_qa/nightly_adf_kit_build_regr/builds_regr/nightly/1273/dot3/synopsys/2015-03-31/runs/d04/fdkex_SCAN/ext/../apr/mwdb/fdkex_fill_LIB
BLOCK: fdkex
* Set VALUE_MILKYWAY_VIEW: FILL for milkyway fill view
MILKYWAY_ADDITIONAL_VIEWS: FILL

* LEF/DEF flow
* TOP_DEF_FILE: <FILE_TOPCELL_DEF>
* LEF_FILE: <FILE_TECHNOLOGY_LEF>
* LEF_FILE: <LIST_CELL_LEF_FILES>

** GDS fill
* FILE_GDSFILL_MAPFILE = <KIT_ROOT>/extraction/starrc/cmdfiles/gds.fill.starrc.map for Active fill on DT251
* METAL_FILL_GDS_FILE: <PATH_GDS_FILL>
* GDS_LAYER_MAP_FILE: <FILE_GDSFILL_MAPFILE>

** OASIS fill
* METAL_FILL_OASIS_FILE: <PATH_OASIS_FILL>
* OASIS_LAYER_MAP_FILE: <FILE_GDSFILL_MAPFILE>


** Field Solver extraction
* <ENABLE_STARRC_FIELD_SOLVER>FS_EXTRACT_NETS: *

** Simultaneous Multi Corner flow
* <ENABLE_SMC_FLOW>CORNERS_FILE: corners.defines
* <ENABLE_SMC_FLOW>SIMULTANEOUS_MULTI_CORNER: YES
* <ENABLE_SMC_FLOW>SELECTED_CORNERS: <SELECTED_CORNER_LIST>


** Distributed processing
* For Star
* <ENABLE_DISTRIBUTED_PROCESSING>NUM_CORES: <VALUE_NUMBER_DP_CPUS>
* <ENABLE_DISTRIBUTED_PROCESSING>STARRC_DP_STRING: <SSH_STRING_STARRC_JOB_DP>
* For Field Solver
* <ENABLE_DISTRIBUTED_PROCESSING><ENABLE_STARRC_FIELD_SOLVER>FSCOMPARE_OPTIONS: -np <VALUE_NUMBER_DP_CPUS>
* <ENABLE_DISTRIBUTED_PROCESSING><ENABLE_STARRC_FIELD_SOLVER>FS_DP_STRING: <SSH_STRING_STARRC_JOB_DP>

* Added For Temperature Sensitivity Flow (Single corner and multiple temperatures)
TEMPERATURE_SENSITIVITY: YES
NETLIST_CORNER_FILE: corners.defines
NETLIST_CORNER_NAMES: tttt_-10 tttt_-40 tttt_110 tttt_90

* Added for Multiple CPUs processing on local machine
NUM_CORES: 4
STARRC_DP_STRING: list localhost:4