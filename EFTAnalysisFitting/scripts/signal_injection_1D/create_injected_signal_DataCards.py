import os
import argparse
import sys
import shutil
import numpy as np
import ROOT

# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict, WC_ALL
from MISC_CONFIGS import template_filename_yields, template_filename, datacard_dir, dim6_ops

def make_dir(ddir):
    # check directory
    os.makedirs(ddir, exist_ok=True)

def copy_files(ddir_start, ddir_end, files_list):
    for file in files_list:
        file_old = os.path.join(ddir_start, file)
        file_new = os.path.join(ddir_end, file)
        shutil.copyfile(file_old, file_new)

def channel_copy_to_signal_inject(WC, channel, datacard_dict, datacard_dir=datacard_dir):
    # dim8 check
    if WC in dim6_ops:
        suff_proc = ''
    else:
        suff_proc = '_dim8'
    # first check if dir exists
    # version number
    v = versions_dict[channel]['v']
    version = 'v'+str(v)
    # MAIN REPO
#     dcdir = os.path.join(datacard_dir, channel, version)
    # FOR DEV ONLY
    dcdir = datacard_dir
    inject_dir = os.path.join(dcdir, 'signal_injection_'+WC)
    make_dir(inject_dir)
    # get the channel string
    sname_ch = datacard_dict[channel]['info']['short_name']
    subchannels = datacard_dict[channel]['subchannels'].keys()
    # loop through subchannels
    files_ch = []
    for i, subch in enumerate(subchannels):
        #print('Subchannel: '+subch+', ', end=': ')
        #print(subch)
        sname_sch = datacard_dict[channel]['subchannels'][subch]['info']['short_name']
        # update subchannel name if there is rescaling
        if versions_dict[channel]['lumi'] == '2018':
            sname_sch += '_2018_scaled'
            print(' (2018 scaled)', end='')
        scanfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType='_1D', purpose='DataCard_Yields', proc='', version=version, file_type='txt')
        scanfile_SO = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=WC, ScanType='_1D', purpose='DataCard_Yields', proc='_StatOnly', version=version, file_type='txt')
        yieldfile = template_filename_yields.substitute(channel=sname_ch, subchannel=sname_sch, purpose='DataCard_Yields', proc='_Cleaned'+suff_proc, version=version, file_type='root')
        files_ch.append(scanfile)
        files_ch.append(scanfile_SO)
        files_ch.append(yieldfile)
    print()
    # copy files
    copy_files(ddir_start=dcdir, ddir_end=inject_dir, files_list=files_ch)

def update_data_obs(WC, WC_value, channel, datacard_dir=datacard_dir, verbose=False):
    # dim8 check
    if WC in dim6_ops:
        suff_proc = ''
    else:
        suff_proc = '_dim8'
    # version number
    v = versions_dict[channel]['v']
    version = 'v'+str(v)
    inject_dir = os.path.join(datacard_dir, 'signal_injection_'+WC)
    # get the channel string
    sname_ch = datacard_dict[channel]['info']['short_name']
    subchannels = datacard_dict[channel]['subchannels'].keys()
    for i, subch in enumerate(subchannels):
        #print('Subchannel: '+subch+', ', end=': ')
        #print(subch)
        sname_sch = datacard_dict[channel]['subchannels'][subch]['info']['short_name']
        # update subchannel name if there is rescaling
        if versions_dict[channel]['lumi'] == '2018':
            sname_sch += '_2018_scaled'
            print(' (2018 scaled)', end='')
        yieldfile = template_filename_yields.substitute(channel=sname_ch, subchannel=sname_sch, purpose='DataCard_Yields', proc='_Cleaned'+suff_proc, version=version, file_type='root')
        yieldfile = os.path.join(inject_dir, yieldfile)
        #cpfile = yieldfile.replace('VVV', 'COPY_VVV')
        cpfile = os.path.join(inject_dir, 'hold.root')
        # copy file
        shutil.copyfile(yieldfile, cpfile)
        # load files
        infile = ROOT.TFile(cpfile, 'read')
        outfile = ROOT.TFile(yieldfile, 'recreate')
        keys_cleaned = [k.GetName().split(';')[0] for k in infile.GetListOfKeys() if "TH1" in k.GetClassName()]
        nbins = infile.Get(keys_cleaned[0]).GetNbinsX()
        injected_data = np.zeros(nbins)
        for k_ in keys_cleaned:
            if 'data_obs' in k_:
                continue
            hin = infile.Get(k_)
            # else check if needs to be added to data
            flags_not_bg = ['Up', 'Down', 'sm', 'quad', 'data', 'VVV', 'WWW', 'WWZ', 'WZZ', 'ZZZ']
            bg = True
            for flag in flags_not_bg:
                if flag in k_:
                    bg = False
            if bg:
                for i in range(nbins):
                    bin_n = i+1
                    injected_data[i] += hin.GetBinContent(bin_n)
            # check for EFT
            #if ('quad' in k_) and (WC in k_):
            if k_ == 'h_quad_'+WC:
                quad = np.array([hin.GetBinContent(i+1) for i in range(nbins)])
            #if ('lin' in k_) and (WC in k_):
            if k_ == 'h_sm_lin_quad_'+WC:
                sm_lin_quad = np.array([hin.GetBinContent(i+1) for i in range(nbins)])
            if k_ == 'h_sm':
                sm = np.array([hin.GetBinContent(i+1) for i in range(nbins)])
        # add in the injected EFT
#         if verbose:
        print('Data before injection: ', injected_data)
        lin = sm_lin_quad - sm - quad
        injected_data += sm + lin*WC_value + quad*WC_value**2
        if verbose:
            print('Parameters:')
            print('SM: ', sm)
            print('Lin: ', lin)
            print('Quad: ', quad)
            print('SM_Lin_Quad: ', sm_lin_quad)
        print('Data after injection: ', injected_data)
        print()
        # now loop through again and save to file with new data_obs
        for k_ in keys_cleaned:
            hin = infile.Get(k_)
            if 'data_obs' in k_:
                # set injected signal values
                for i in range(nbins):
                    bin_n = i+1
                    hin.SetBinContent(bin_n, injected_data[i])
                    hin.SetBinError(bin_n, 0.0)
            # else nothing to adjust
            outfile.WriteObject(hin, k_)
        # close files
        infile.Close()
        outfile.Close()

def setup_signal_injection(WC, WC_value, datacard_dict, datacard_dir=datacard_dir):
    print('Injecting a signal: ', WC, '=', WC_value)
    for channel in datacard_dict.keys():
        if WC not in versions_dict[channel]['EFT_ops']:
            continue
        print(f'Channel: {channel}')
        # first copy relevant files to the signal injection directory
        channel_copy_to_signal_inject(WC, channel=channel, datacard_dict=datacard_dict, datacard_dir=ddir)
        # then update h_data_obs
        update_data_obs(WC, WC_value, channel, datacard_dir=ddir, verbose=False)


if __name__=='__main__':
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--WC',
                        help='Which Wilson Coefficient to use to inject a signal? ["cW" (default), ...]')
    parser.add_argument('-v', '--value',
                        help='What value are you setting the WC to?')
    args = parser.parse_args()
    if args.WC is None:
        args.WC = 'cW'
    WC = args.WC
    WC_value = float(args.value)
    # run the main function
    setup_signal_injection(WC, WC_value, datacard_dict, datacard_dir=datacard_dir)
