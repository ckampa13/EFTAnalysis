import os
import argparse
import ROOT

from parabola_fit import construct_EFT_terms_all
from yield_transforms import yield_prune_first_pass, yield_add_WCs_params, yield_split_dim6_dim8
from datacard_writer import write_datacards

# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict, WC_ALL
from MISC_CONFIGS import (
    datacard_dir,
    template_filename_yields,
    template_filename,
    dim6_ops,
)

# if any string is incorrect in the histogram names, add the fixes here
# key = wrong (what's in the file)
# val = right (what to replace it with)
# e.g. "FT0" : "cT0" is a common one.
replacements_all = {
    '0Lepton_2FJ': {},
    '0Lepton_3FJ': {},
}

# this is maybe the same for each channel
# any hit of this flag in a histogram name means it is not a background process nominal yield
not_bg_flags_all = {
    '0Lepton_2FJ': ['Up', 'Down', 'sm', 'quad', 'data'],
    '0Lepton_3FJ': ['Up', 'Down', 'sm', 'quad', 'data'],
}

def check_dir(ddir):
    if not os.path.isdir(ddir):
        print('Creating directory: ', ddir)
        os.mkdir(ddir)

def run_datacard_processing(channel='0Lepton_2FJ', subchannel='', version='vTEST', use_autoMCStats=True, verbose=True):
    WCs = versions_dict[channel]['EFT_ops']
    has_dim8 = False
    for WC in WCs:
        if not WC in dim6_ops:
            has_dim8 = True
            break
    rawdir = os.path.join(datacard_dir, channel, 'raw_yields')
    outdir = os.path.join(datacard_dir, channel, version)
    check_dir(outdir)
    sname_ch = datacard_dict[channel]['info']['short_name']
    sname_sch = datacard_dict[channel]['subchannels'][subchannel]['info']['short_name']
    input_file = template_filename_yields.substitute(channel=sname_ch, subchannel=sname_sch, purpose='DataCard_Yields', proc='', version=version, file_type='root')
    pass1_file = template_filename_yields.substitute(channel=sname_ch, subchannel=sname_sch, purpose='DataCard_Yields', proc='_1', version=version, file_type='root')
    out_file = template_filename_yields.substitute(channel=sname_ch, subchannel=sname_sch, purpose='DataCard_Yields', proc='_Cleaned', version=version, file_type='root')
    dc_file = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC='WC', ScanType='_1D', purpose='DataCard_Yields', proc='', version=version, file_type='txt')
    txt_dc_file = os.path.join(outdir, dc_file)
    if has_dim8:
        out_file_dim8 = template_filename_yields.substitute(channel=sname_ch, subchannel=sname_sch, purpose='DataCard_Yields', proc='_Cleaned_dim8', version=version, file_type='root')
        root_file_out_dim8 = os.path.join(outdir, out_file_dim8)
    else:
        out_file_dim8 = None
    root_file_in = os.path.join(rawdir, input_file)
    root_file_1 = os.path.join(rawdir, pass1_file)
    root_file_out = os.path.join(outdir, out_file)
    print('Reading in from: %s' % root_file_in)
    # check point scan or direct parameters
    if versions_dict[channel]['EFT_type'] == 'points':
        print('Building EFT parabola parameters from point scan...')
    else:
        raise NotImplementedError('Sorry, only point scan processing is implemented (talk to Cole).')
    # channel specifics
    if (channel == '0Lepton_2FJ') or (channel == '0Lepton_3FJ'):
        # fit parabolas
        results_np_dict, x_vals_dict, y_vals_bins_dict = construct_EFT_terms_all(WCs, root_file_in, rchi2_cut=0.1, verbose=verbose)
        # prune (first pass) and add WC params
        root_in = ROOT.TFile(root_file_in, 'read')
        root_out = ROOT.TFile(root_file_1, 'recreate')
        yield_prune_first_pass(root_in, root_out, drop_flags=['VVV', 'WWW', 'WZZ', 'ZZZ'], replacements=replacements_all[channel])
        yield_add_WCs_params(WCs, root_out, results_np_dict)
        # close files
        root_in.Close()
        root_out.Close()
        # dim6 / dim8 split
        root_in = ROOT.TFile(root_file_1, 'read')
        root_out = ROOT.TFile(root_file_out, 'recreate')
        if has_dim8:
            root_out_dim8 = ROOT.TFile(root_file_out_dim8, 'recreate')
        else:
            root_out_dim8 = None
        yield_split_dim6_dim8(WCs, root_in=root_in, root_out=root_out, root_out_dim8=root_out_dim8, has_dim8=has_dim8)
        root_in.Close()
        # get keys to pass to datcard creator
        keys_out = [k.GetName().split(';')[0] for k in root_out.GetListOfKeys() if "TH1" in k.GetClassName()]
        root_out.Close()
        if has_dim8:
            # get keys to pass to datcard creator
            keys_out_dim8 = [k.GetName().split(';')[0] for k in root_out_dim8.GetListOfKeys() if "TH1" in k.GetClassName()]
            root_out_dim8.Close()
        else:
            keys_out_dim8 = None
        # make the datacards
        not_bg_flags = not_bg_flags_all[channel]
        dc_str_dict = write_datacards(WCs, sname_ch, keys_out, keys_out_dim8, out_file, out_file_dim8,
                                      not_bg_flags, txt_dc_file, use_autoMCStats=use_autoMCStats)
        print('\n\nProcessing for %s %s version %s is complete!' % (channel, subchannel, version))
    else:
        raise NotImplementedError('Sorry, processing for the %s channel has not been implemented yet (talk to Cole).' % channel)

if __name__=='__main__':
    # channel = '0Lepton_2FJ'
    # version = 'vTEST'
    # MCStat = True
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    # FIXME! Add "all" channels option?
    parser.add_argument('-c', '--Channel',
                        help='Which channel? ["0Lepton_2FJ" (default), "0Lepton_3FJ", "2Lepton_OS", "2Lepton_SS"]')
    parser.add_argument('-M', '--IncludeMCStat',
                        help='Should bin stat errors be used to represent MC stat uncertainties? y(default)/n')
    parser.add_argument('-v', '--Version',
                        help='Which yield version are you processing? "vTEST" (default)')
    parser.add_argument('-V', '--Verbose',
                        help='Verbose output during processing? 0 / 1 (default).')
    args = parser.parse_args()
    # list of channels
    if args.Channel is None:
        args.Channel = '0Lepton_2FJ'
    # if args.Channel == 'all':
    #     channels = datacard_dict.keys()
    # else:
    channels = [args.Channel]
    if args.IncludeMCStat is None:
        MCStat = True
    else:
        MCStat = args.IncludeMCStat != 'n'
    if args.Version is None:
        version = 'vTEST'
    else:
        version = args.Version
    if args.Verbose is None:
        args.Verbose = 1
    else:
        args.Verbose = int(args.Verbose)
    if args.Verbose > 0:
        verbose = True
    else:
        verbose = False
    # loop and run processing function
    for channel in channels:
        print('Processing Channel: %s' % channel)
        # loop through subchannels
        subchannels = datacard_dict[channel]['subchannels'].keys()
        for subchannel in subchannels:
            print('Subchannel: %s' % subchannel)
            run_datacard_processing(channel, subchannel, version, use_autoMCStats=MCStat, verbose=verbose)

