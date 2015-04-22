default_tp: track_pattern = {
    {0, 0.044, "", "floatiss_"},
    {0.040, 0.044, "", "floatiss_"},
    {0.040, 0.044, "", "floatiss_"},
    {0.050, 0.108, "", "floatiss_"},
    {0.050, 0.044, "", "floatiss_"},
    {0.040, 0.044, "", "floatiss_"},
    {0.040, 0.044, "", "floatiss_"},
    {0.040, 0.044, "", "floatiss_"},
    {0.040, 0.044, "", "floatiss_"},
    {0.040, 0.044, "", "floatiss_"},
    {0.040, 0.044, "", "floatiss_"},
    {0.040, 0.044, "", "floatiss_"},
    {0.040, 0.044, "", "floatiss_"},
    {0.050, 0.108, "", "floatiss_"},
    {0.050, 0.044, "", "floatiss_"},
    {0.040, 0.044, "", "floatiss_"},
    {0.040, 0.044, "", "floatiss_"},
};
ndr_tp1: track_pattern = {
    {0.000, 0.108, "", "floatiss_"},
    {0.060, 0.108, "", "floatiss_"},

    {0.060, 0.108, "", "floatiss_"},
    
    {0.060, 0.108, "", "floatiss_"},
    {0.060, 0.108, "", "floatiss_"},
    {0.050, 0.044, "", "floatiss_"},
    {0.040, 0.044, "", "floatiss_"},
    {0.040, 0.044, "", "floatiss_"},
    {0.050, 0.108, "", "floatiss_"},

    {0.060, 0.108, "", "floatiss_"},

    {0.060, 0.108, "", "floatiss_"},
};
region_grids = {
    {
        region = CELLBOUNDARY,
        grid_pattern = default_tp,
        period = 1.596,
        offset = 0.020,
    },
#ifdef ENABLE_NDR_UIN
    {
        region = CELLBOUNDARY,
        grid_pattern = ndr_tp1,
         period = 1.596,
         offset = -0.054,
     },
    {
        region = CELLBOUNDARY,
        grid_pattern = default_tp,
        period = 1.596,
        offset = 0.020,
     },
#endif
};




//buckets for overlong fill trimming attempts in cut moving
overlong_fill_thresh_buckets = {0.04, 0.8 };  
multicut_cut_moving = true;
multicut_threshold = 1.0;

//write_out_orig = false;;
//do_ungridded_fill = false;
process_name = "1273.3";
fill_length = 30;
dfmg_extensions = true;
use_drawn_kor = true;
top_level_only_kor = false; 
 use_route_kor = false; 
 use_fill_kor = true; 
 use_global_kor = true; 
drawn_kor_x_space = 0.040;
drawn_kor_y_space = 0.020;
keepout_cells_list = {""};
keepout_cells_x_space = 0.040;
keepout_cells_y_space = 0.020;
//no_extend_cells_list = {"cx*",};
//near_fill_density_target = 1.0;
//far_fill_density_target = 1.0;
density_window_size = 2.8;
path = "./";
half_dr_end_to_end = 0.040;
consider_off_grid = false;
#ifdef ENABLE_NDR_UIN     
consider_off_grid = true;
metal_max_unrestricted_space = 0.040;
misaligned_ete_space = 0.080;
#endif
//write_out_c_tracks = false;
//write_out_c_wires = true;
//break_pattern = {};
//break_offset = 0.0;
//break_period = 0.0;
//write_out_b_tracks = false;
//transition_pattern = {};
//transition_offset = 0.0;
//transition_period = 0.0;


