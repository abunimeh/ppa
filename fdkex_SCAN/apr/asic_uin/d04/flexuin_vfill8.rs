process_name = "1273.3";
use_drawn_kor = true;
drawn_kor_x_space = 1;
drawn_kor_y_space = 1;
//keepout_cells_list = m9_prune_cells_list;
density_target = 0.6/100;
//density_boundary_assumption = 0.3/100;
density_window_size = 11;
density_window_y_size = 11;
fill_net_names = {"floatiss_", "*",};
iteration_count  = 2;
connect_dummy_250 = true ;

hookup_regions = {
     {
	 CELLBOUNDARY ,
         {"floatiss_",},
         {"floatiss_",},
         true,
         true,
         density_target,
     },
};

use_nps_advanced_density = true; 

///////////////////////////
//via_fill_options : newtype struct of {
//  write_out_orig:boolean = false;
//
//  process_name:string = "";
//
//  use_drawn_kor:boolean = true;
//  top_level_only_kor:boolean = true;
//  drawn_kor_x_space:double = 0.0;
//  drawn_kor_y_space:double = 0.0;
//
//  keepout_cells_list:list of string = {};
//  keepout_cells_x_space:double = 0.0;
//  keepout_cells_y_space:double = 0.0;
//
//  nofill_cells_list : list of string = {};
//  hookup_regions:list of hookup_region = {};
//
//  density_target:double = 1.0;
//  density_window_size:double = 15;
//
//  fill_container_name:string = "";
//  fill_net_names:list of string = {};
//
//  name_extensions:boolean = false;
//  iteration_count :integer = 8;
connect_dummy_250 = true ;
//
//};

