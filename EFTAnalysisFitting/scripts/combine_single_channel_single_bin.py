import os
import subprocess
import argparse


if __name__=='__main__':
    # file globals
    datacard_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                '..')
    output_dir = os.path.join(datacard_dir, 'output', 'single_channel_single_bin')
    # make paths absolute
    datacard_dir = os.path.abspath(datacard_dir)
    output_dir = os.path.abspath(output_dir)
    print(f"Datacard base directory: {datacard_dir}")
    # print(f"Output directory: {output_dir}")
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--Channel',
                        help='Which VVV channel? ["1Lepton" (default),]')
    parser.add_argument('-s', '--SubChannel',
                        help='Which (if any) subchannel? ["" (default),'+
                        '"muon", "electron"]')
    parser.add_argument('-b', '--Bin', help='Which bin? ["1", "2", ... "N"]')
    parser.add_argument('-v', '--Version', help='Which datacard version? ["1" (default), ...]')
    parser.add_argument('-a', '--Asimov', help='Use Asimov? "y"(default)/"n".')
    args = parser.parse_args()
    # fill defauls if necessary
    if args.Channel is None:
        args.Channel = '1Lepton'
    if args.SubChannel is None:
        args.SubChannel = ''
    if args.Bin is None:
        args.Bin = "1"
    if args.Version is None:
        args.Version = '1'
    if args.Asimov is None:
        args.Asimov = 'y'
    if args.Asimov == 'y':
        asi_str = '-t -1'
    else:
        asi_str = ''
    # channel specific things
    if args.Channel == '1Lepton':
        file_channel = '1lepton'
    # construct filename from arguments
    cardfile_base = (f'datacard1opWithBkg_FT0_'+
                     f'bin{args.Bin}_{file_channel}_{args.SubChannel}')
    cardfile = os.path.join(datacard_dir, args.Channel, f'v{args.Version}', f'{cardfile_base}.txt')
    workspacefile = os.path.join(output_dir,'workspace_'+cardfile_base+f'_v{args.Version}.root')
    print(f"Attempting to read the following datacard: {cardfile}")
    # combine
    # make workspace
    print('Generating workspace')
    _ = subprocess.run(f'text2workspace.py {cardfile} -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative -o {workspacefile} --X-allow-no-signal --PO eftOperators=cG', shell=True)#, capture_output=True)
    # run combine
    os.chdir(output_dir)
    print('Running combine from output directory: {output_dir}')
    _ = subprocess.run(f'combine -M MultiDimFit {workspacefile} --algo=grid --points 2000 {asi_str} --redefineSignalPOIs k_cG --freezeParameters r --setParameters r=1 --setParameterRanges k_cG=-1.0,1.0 --verbose -1 -n _{cardfile_base}', shell=True)#, capture_output=True)
    print(f'Finished running combine. Expected file output: higgsCombine_{cardfile_base}.MultiDimFit.mH125.root')


# REF
# 'HiggsAnalyticAnomalousCoupling.AnomalousCouplingEFTNegative'
# 'HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative'
