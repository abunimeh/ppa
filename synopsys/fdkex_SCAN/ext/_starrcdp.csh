#!/bin/csh -f

setenv SNPSLMD_LICENSE_FILE 26586@plxs0412.pdx.intel.com:26586@plxs0413.pdx.intel.com:26586@plxs0414.pdx.intel.com:26586@plxs0415.pdx.intel.com:26586@fmylic36a.fm.intel.com:26586@fmylic36c.fm.intel.com:26586@ilic2004.iil.intel.com:26586@ilic2005.iil.intel.com:26586@pgllic12.png.intel.com:26586@synopsys20p.elic.intel.com:26586@irslic003.ir.intel.com

setenv PATH .:/p/foundry/eda/em64t_SLES11/starrcxt/J-2014.06-SP3/bin:/p/foundry/env/bin:/p/foundry/fdk-env/env-core/15ww13a/bin:/p/foundry/fdk-env/env-core/15ww13a/isobin:/p/foundry/env/bin:/usr/intel/bin:/bin:/usr/bin:.:/usr/sbin:/usr/bin/X11:/usr/X11R6/bin:/usr/local/bin:/usr/local/adm/bin:/stor/common/bin:/p/foundry/env/pkgs/megatest/bin:/p/foundry/eda/em64t_SLES11/starrcxt/J-2014.06-SP3/suse64_starrc/bin

/p/foundry/eda/em64t_SLES11/starrcxt/J-2014.06-SP3/suse64_starrc/bin/StarXtract -clean star_rcxt.asic.cmd  -dp_sl
