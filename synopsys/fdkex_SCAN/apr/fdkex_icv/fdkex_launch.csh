#!/bin/tcsh -f
setenv ICV_DISABLE_RUNSET_CACHE
setenv ICV_MW_WRITE_FILL_POLY_AS_RECT 1
setenv PDSSTM ./
cd /nfs/ch/disks/icf_fdk_regression001/nightly_adf_kit_build_regr/builds_regr/nightly/1273/dot3/synopsys/2015-03-31/runs/d04/fdkex_SCAN/apr/fdkex_icv/
if ( -d icv_fill ) rm -rf icv_fill/*
sleep 5
mkdir -p icv_fill
cd icv_fill
icv -i /nfs/ch/disks/icf_fdk_regression001/nightly_adf_kit_build_regr/builds_regr/nightly/1273/dot3/synopsys/2015-03-31/runs/d04/fdkex_SCAN/apr/fdkex_icv/fdkex.mwnofill.oas -c fdkex -f OASIS -dp8 -turbo -I /p/fdk/fdk73/builds/pdk733_r1.7/fill/icv/flexfill -I /p/fdk/fdk73/builds/pdk733_r1.7/fill/icv/PXL/ -I /nfs/ch/disks/icf_fdk_regression001/nightly_adf_kit_build_regr/builds_regr/nightly/1273/dot3/synopsys/2015-03-31/runs/d04/fdkex_SCAN/apr/fdkex_icv/d04 /p/fdk/fdk73/builds/pdk733_r1.7/fill/icv/flexfill/mfill_streamlined.rs >& fill.log
cd /nfs/ch/disks/icf_fdk_regression001/nightly_adf_kit_build_regr/builds_regr/nightly/1273/dot3/synopsys/2015-03-31/runs/d04/fdkex_SCAN/apr
exit 0
