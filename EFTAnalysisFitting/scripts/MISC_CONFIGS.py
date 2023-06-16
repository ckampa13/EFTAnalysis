import os
from string import Template


fpath = os.path.dirname(os.path.realpath(__file__))
# datacard_dir = os.path.abspath(os.path.join(fpath,'..', '..'))
datacard_dir = os.path.abspath(os.path.join(fpath,'..'))

# template_filename = Template("VVV.$channel$subchannel.$WC$ScanType.DataCard_Yields$proc.$version.$file_type")
template_filename = Template("VVV.$channel$subchannel.$WC$ScanType.$purpose$proc.$version.$file_type")
template_outfilename = Template("higgsCombine_$asimov.$channel$subchannel.$WC$ScanType.$version.$syst.$method.mH120.root")
template_outfilename_stub = Template("_$asimov.$channel$subchannel.$WC$ScanType.$version.$syst")
