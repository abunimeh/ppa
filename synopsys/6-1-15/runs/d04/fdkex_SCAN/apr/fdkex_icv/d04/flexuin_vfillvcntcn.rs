process_name = "1273.3";
use_drawn_kor = true;
top_level_only_kor = true;
use_route_kor = true; 
use_fill_kor = true; 
use_global_kor = true; 
fill_net_names = {"floatiss_",};
hookup_regions = {
     {
 region = CELLBOUNDARY ,
nets_above = {"floatiss_",},
nets_below = {"floatiss_",},
break_above = false,
break_below = false,
density_target = 0.007,
     },
};
iteration_count = 2;
connect_dummy_250 = true;
density_fill_upto = false;
density_target = 0.007;
near_fill_density_target = 0.007;
far_fill_density_target = 0.007;
//density_target = 0.001;
//near_fill_density_target = 0.001;
//far_fill_density_target = 0.001;

density_window_size = 3.5;
