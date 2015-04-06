grid_pattern = {
    {0, 0.028, "C", "floatiss_"},
    {0.024, 0.040, "B", "floatiss_"},
    {0.024, 0.028, "C", "floatiss_"},
    {0.024, 0.028, "B", "floatiss_"},
    {0.024, 0.028, "C", "floatiss_"},
    {0.024, 0.028, "B", "floatiss_"},
    {0.024, 0.028, "C", "floatiss_"},
    {0.024, 0.074, "B", "floatiss_"},
    {0.024, 0.028, "C", "floatiss_"},
    {0.024, 0.028, "B", "floatiss_"},
    {0.024, 0.028, "C", "floatiss_"},
    {0.024, 0.028, "B", "floatiss_"},
    {0.024, 0.028, "C", "floatiss_"},
    {0.024, 0.040, "B", "floatiss_"},
};
offset = -0.014;
period = 0.798;

//buckets for overlong fill trimming attempts in cut moving
multicut_cut_moving = true;
multicut_threshold = 1.0;
overlong_fill_thresh_buckets = {0.028, 0.28 };  



//write_out_orig = false;;
//do_ungridded_fill = false;
process_name = "1273.3";
fill_length = 30;
dfmg_extensions = true;
//hybrid = false;
use_drawn_kor = true;
top_level_only_kor = false; 
 use_route_kor = false; 
 use_fill_kor = true; 
 use_global_kor = true;


drawn_kor_x_space = 0.028;
drawn_kor_y_space = 0.024;
keepout_cells_list = {""};
keepout_cells_x_space = 0.028;
keepout_cells_y_space = 0.024;
//no_extend_cells_list = {"cx*",};
//near_fill_density_target = 1.0;
//far_fill_density_target = 1.0;
density_window_size = 2.1;
path = "./";
half_dr_end_to_end = 0.028;
//write_milkyway_output = false;
//mw_cellname = "";
//mw_library = "";
//mw_path = "";
//mw_view = "FILL";
//mw_append = true;
//region_grids = {};
// use_fill_markers = true;
 consider_off_grid = false;
write_out_c_tracks = true;
write_out_c_wires = false;
//break_pattern = {};
//break_offset = 0.0;
//break_period = 0.0;
//write_out_b_tracks = false;
//transition_pattern = {};
//transition_offset = 0.0;
//transition_period = 0.0;

