grid_pattern = {
    {0, 0.042, "B", "floatiss_"},
    {0.028, 0.028, "C", "floatiss_"},
    {0.028, 0.028, "B", "floatiss_"},
    {0.028, 0.028, "C", "floatiss_"},
    {0.028, 0.028, "B", "floatiss_"},
    {0.028, 0.040, "C", "floatiss_"},
    {0.028, 0.046, "B", "floatiss_"},
    {0.028, 0.040, "C", "floatiss_"},
    {0.028, 0.028, "B", "floatiss_"},
    {0.028, 0.028, "C", "floatiss_"},
    {0.028, 0.028, "B", "floatiss_"},
    {0.028, 0.028, "C", "floatiss_"},
    {0.028, 0.042, "B", "floatiss_"},
    {0.028, 0.042, "C", "floatiss_"},
    {0.028, 0.028, "B", "floatiss_"},
    {0.028, 0.028, "C", "floatiss_"},
    {0.028, 0.028, "B", "floatiss_"},
    {0.028, 0.028, "C", "floatiss_"},
    {0.028, 0.040, "B", "floatiss_"},
    {0.028, 0.046, "C", "floatiss_"},
    {0.028, 0.040, "B", "floatiss_"},
    {0.028, 0.028, "C", "floatiss_"},
    {0.028, 0.028, "B", "floatiss_"},
    {0.028, 0.028, "C", "floatiss_"},
    {0.028, 0.028, "B", "floatiss_"},
    {0.028, 0.042, "C", "floatiss_"},
};
offset = 0.014;
period = 1.596;



multicut_cut_moving = true;
multicut_threshold = 1.0;
//buckets for overlong fill trimming attempts in cut moving
overlong_fill_thresh_buckets = {0.07, 0.28 };  

//write_out_orig = false;;
//do_ungridded_fill = false;
process_name = "1273.3";
fill_length = 30;
dfmg_extensions = true;
center_initial_cuts = false;
//hybrid = false;
use_drawn_kor = true;
top_level_only_kor = false; 
 use_route_kor = false; 
 use_fill_kor = true; 
 use_global_kor = true; 
drawn_kor_x_space = 0.027;
drawn_kor_y_space = 0.014;
keepout_cells_list = {""};
keepout_cells_x_space = 0.027;
keepout_cells_y_space = 0.014;
//no_extend_cells_list = {"cx*",};
//near_fill_density_target = 1.0;
//far_fill_density_target = 1.0;
density_window_size = 2.1;
path = "./";
half_dr_end_to_end = 0.027;
//write_milkyway_output = false;
//mw_cellname = "";
//mw_library = "";
//mw_path = "";
//mw_view = "FILL";
//mw_append = true;
//region_grids = {};
 use_fill_markers = false;
 consider_off_grid = false;
write_out_c_tracks = true;
write_out_c_wires = false;
break_pattern = {
  {3.446, 0.054},
};
break_offset = -3.263;
break_period = 3.5;
//write_out_b_tracks = true;
//transition_pattern = {};
//transition_offset = 0.0;
//transition_period = 0.0;



