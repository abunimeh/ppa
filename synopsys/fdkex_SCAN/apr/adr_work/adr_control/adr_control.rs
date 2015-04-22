
G_XN_LIBRARY : integer = 0;
G_TG_LIBRARY : integer = 0;

// Needed to reuse fill uin files
DFM_M2_MAX_FILL_LENGTH : double = 30;
DFM_M3_MAX_FILL_LENGTH : double = 30;
DFM_FILL_METAL2_TARG :double     = 45;
DFM_FILL_METAL3_TARG :double     = 45;
// Need following definition when reading in uin
keepout_cells_list:list of string = {""};
overlong_fill_thresh_buckets:list of double = {};
