default_tp: track_pattern = {
    {0, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.168, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.168, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
    {0.056, 0.056, "", "floatiss_"},
};
ndr_tp1: track_pattern = {
{0.000,	0.150, "", "floatiss_"},
{0.074,	0.150, "", "floatiss_"},
{0.074,	0.150, "", "floatiss_"},
{0.074,	0.150, "", "floatiss_"},

{0.065,	0.168, "", "floatiss_"},

{0.065,	0.150, "", "floatiss_"},
{0.074,	0.150, "", "floatiss_"},
{0.074,	0.150, "", "floatiss_"},
{0.074,	0.150, "", "floatiss_"},
{0.074,	0.150, "", "floatiss_"},
{0.074,	0.150, "", "floatiss_"},

{0.065,	0.168, "", "floatiss_"},

{0.065,	0.150, "", "floatiss_"},
{0.074,	0.150, "", "floatiss_"},
{0.074,	0.150, "", "floatiss_"},

};
region_grids = {
    {
        region = CELLBOUNDARY,
        grid_pattern = default_tp,
        period = 3.36,
        offset = 0.028,
    },
#ifdef ENABLE_NDR_UIN
    {
        region = CELLBOUNDARY,
        grid_pattern = ndr_tp1,
         period = 3.36,
         offset = -0.075,
     },
    {
        region = CELLBOUNDARY,
        grid_pattern = default_tp,
        period = 3.36,
        offset = 0.028,
     },
#endif
};




//write_out_orig = false;;
//do_ungridded_fill = false;
process_name = "1273.3";
//offset = 0.028 ;
//period = 2*1.68;
fill_length = 30;
dfmg_extensions = true;
//hybrid = false;
use_drawn_kor = true;
top_level_only_kor = false; 
 use_route_kor = false; 
 use_fill_kor = true; 
 use_global_kor = true;
drawn_kor_x_space = 0.028;
drawn_kor_y_space = 0.045;
keepout_cells_list = {""};
keepout_cells_x_space = 0.028;
keepout_cells_y_space = 0.045;
//no_extend_cells_list = {"cx*",};
//near_fill_density_target = 1.0;
//far_fill_density_target = 1.0;
density_window_size = 2.8;
path = "./";
//change half_dr_end_to_end to 0 based on Luke's email (1/9)
half_dr_end_to_end = 0.045;
//write_milkyway_output = false;
//mw_cellname = "";
//mw_library = "";
//mw_path = "";
//mw_view = "FILL";
//mw_append = true;
//region_grids = {};
// use_fill_markers = true;
consider_off_grid = false;
#ifdef ENABLE_NDR_UIN     
consider_off_grid = true;
metal_max_unrestricted_space = 0.056;
#endif
//write_out_c_tracks = false;
//write_out_c_wires = false;
//break_pattern = {};
//break_offset = 0.0;
//break_period = 0.0;
//write_out_b_tracks = false;
//transition_pattern = {};
//transition_offset = 0.0;
//transition_period = 0.0;


