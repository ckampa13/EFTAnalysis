import os
import shutil
import ROOT
import subprocess
import argparse
fpath = os.path.dirname(os.path.realpath(__file__))
# local imports
import sys
sys.path.append(os.path.join(fpath,'..'))
from DATACARD_DICT import datacard_dict
from CONFIG_VERSIONS import versions_dict, WC_ALL, WCs_clip_dim6, WCs_clip_dim8
from MISC_CONFIGS import template_filename, datacard_dir, dim6_ops, NPs_to_promote_dict

def modify_wsfile(wsfile_name, NPs_to_promote=['PDF_']):
    # Open original workspace file
    # fin = os.path.join(os.path.abspath(os.path.join(fpath, '..', '..', 'unblind', 'workspaces', 'full_analysis')), '')
    # fin += 'VVV.all_combined.dim8_All.workspace.vCONFIG_VERSIONS.root'
    # print(fin)
    print("Opening file: %s" % wsfile_name)
    print("Promoting NPs to POIs: %s" % NPs_to_promote)
    f_in = ROOT.TFile.Open(wsfile_name, "UPDATE")
    w = f_in.Get("w")  # get workspace

    # Access ModelConfig
    mc = w.obj("ModelConfig") # get ModelConfig

    # Get the current POI and nuisance sets
    pois = mc.GetParametersOfInterest()
    nuis = mc.GetNuisanceParameters()

    # Clones of param sets to modify
    pois = pois.clone("new_poi")
    nuis = nuis.clone("new_nuis")

    # loop through NPs to promote
    for NP in NPs_to_promote:
        np_var = w.var(NP)
        if not np_var:
            raise ValueError("%s not found in workspace" % NP)
        else:
            if nuis.contains(np_var):
                nuis.remove(np_var)
            if not pois.contains(np_var):
                pois.add(np_var)
    # update the ModelConfig
    mc.SetParametersOfInterest(pois)
    mc.SetNuisanceParameters(nuis)
    print("Done. %s promoted to POI" % NPs_to_promote)

    # Write changes in ws file
    w.Write("", ROOT.TObject.kOverwrite)
    f_in.Close()

def update_wsfile_channels(NPs_to_promote, wscopy_suff, dim, channels, datacard_dict, ScanType, StatOnly=False, vsuff='', Unblind=True):
    LinO_str = ''
    suff_purp = ''
    if StatOnly:
        SO_lab = '_StatOnly'
    else:
        SO_lab = ''
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    # comb_dcdir = os.path.join(dcdir, 'combined_datacards', 'channel')
    for i, ch in enumerate(channels):
        print('Channel: %s' % ch)
        if vsuff == '_NDIM':
            v = versions_dict[ch]['v_NDIM']
        else:
            v = versions_dict[ch]['v']
        version = 'v'+str(v)
        version_full = version + vsuff
        sname_ch = datacard_dict[ch]['info']['short_name']
        wsfile = template_filename.substitute(channel=sname_ch, subchannel='_combined', WC=dim, ScanType=ScanType+LinO_str, purpose='workspace'+suff_purp, proc=SO_lab, version=version_full, file_type='root')
        wsfile = os.path.join(dcdir, 'workspaces', 'channel', wsfile)
        wsfile_new = template_filename.substitute(channel=sname_ch, subchannel='_combined', WC=dim, ScanType=ScanType+LinO_str, purpose='workspace'+suff_purp+wscopy_suff, proc=SO_lab, version=version_full, file_type='root')
        wsfile_new = os.path.join(dcdir, 'workspaces', 'channel', wsfile_new)
        # copy the file and modify it
        print("Copying %s to %s for modification." % (wsfile, wsfile_new))
        shutil.copyfile(wsfile, wsfile_new)
        modify_wsfile(wsfile_new, NPs_to_promote=NPs_to_promote)

def update_wsfile_full_analysis(NPs_to_promote, wscopy_suff, dim, ScanType, StatOnly=False, vsuff='', Unblind=True):
    LinO_str = ''
    suff_purp = ''
    if StatOnly:
        SO_lab = '_StatOnly'
    else:
        SO_lab = ''
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    # comb_dcdir = os.path.join(dcdir, 'combined_datacards', 'channel')
    print('Full Analysis')
    wsfile = template_filename.substitute(channel='all', subchannel='_combined', WC=dim, ScanType=ScanType+LinO_str, purpose='workspace'+suff_purp, proc=SO_lab, version='vCONFIG_VERSIONS'+vsuff, file_type='root')
    wsfile = os.path.join(dcdir, 'workspaces', 'full_analysis', wsfile)
    wsfile_new = template_filename.substitute(channel='all', subchannel='_combined', WC=dim, ScanType=ScanType+LinO_str, purpose='workspace'+suff_purp+wscopy_suff, proc=SO_lab, version='vCONFIG_VERSIONS'+vsuff, file_type='root')
    wsfile_new = os.path.join(dcdir, 'workspaces', 'full_analysis', wsfile_new)
    # copy the file and modify it
    print("Copying %s to %s for modification." % (wsfile, wsfile_new))
    shutil.copyfile(wsfile, wsfile_new)
    modify_wsfile(wsfile_new, NPs_to_promote=NPs_to_promote)


if __name__=='__main__':
    wscopy_suff = '_NPsPromote' # FIXME! Add to arguments?
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--Channel',
                        help='Which channel? ["all" (default), "0Lepton_2FJ", "0Lepton_3FJ", "2Lepton_OS", "2Lepton_SS"]')
    parser.add_argument('-d', '--Dimension',
                        help='Which dim of EFT ops to process? "dim8" (default), "dim6", "all"')
    parser.add_argument('-t', '--theLevels',
                        help='Which levels of analysis to run make workspaces for? "all" (default). Any combination in any order of the following characters will work: "b" (bin), "s" (subchannel), "c" (channel), "f" (full analysis). e.g. "bsc" will run all but the full analysis.')
    parser.add_argument('-s', '--ScanType',
                        help='What type of EFT scan was included in this file? ["_All" (default),]')
    parser.add_argument('-U', '--Unblind', help='Use datacards from unblinded private repo? "n"(default)/"y".')
    parser.add_argument('-v', '--VersionSuff',
                        help='String to append on version number, e.g. for clipping. ["" (default), "_clip_mVVV_0",...]')
    args = parser.parse_args()

    if args.Channel is None:
        args.Channel = 'all'
    if args.Channel == 'all':
        channels = datacard_dict.keys()
    else:
        channels = [args.Channel]
    if args.Dimension is None:
        args.Dimension = 'dim8'
    if args.Dimension == 'all':
        dims = ['dim6', 'dim8']
    elif args.Dimension == 'dim6':
        dims = ['dim6']
    elif args.Dimension == 'dim8':
        dims = ['dim8']
    else:
        raise ValueError('The input args.Dimension="%s" is not implemented. Please select from: ["all", "dim6", "dim8"].' % args.Dimension)
    if (args.theLevels is None) or (args.theLevels == 'all'):
        # generate_bins = True
        # generate_subch = True
        generate_ch = True
        generate_full = True
    else:
        # if 'b' in args.theLevels:
        #     generate_bins = True
        # else:
        #     generate_bins = False
        # if 's' in args.theLevels:
        #     generate_subch = True
        # else:
        #     generate_subch = False
        if 'c' in args.theLevels:
            generate_ch = True
        else:
            generate_ch = False
        if 'f' in args.theLevels:
            generate_full = True
        else:
            generate_full = False
    if args.ScanType is None:
        args.ScanType = '_All'
    if args.Unblind is None:
        args.Unblind = 'y'
    if args.Unblind == 'y':
        Unblind = True
    else:
        Unblind = False
    if args.VersionSuff is None:
        vsuff = ''
    else:
        vsuff = args.VersionSuff
    # outer loop
    for dim in dims:
        print(dim)
        NPs_to_promote = NPs_to_promote_dict[dim]
        print("Promoting %s to POIs" % NPs_to_promote)
        #########################
        # channel workspaces
        if generate_ch:
            print('Modifying channel workspaces:')
            print('=================================================')
            # for StatOnly in [False, True]:
            for StatOnly in [False]: # only makes sense to modify ws with syst
                print('Stat only? ', StatOnly)
                update_wsfile_channels(NPs_to_promote, wscopy_suff, dim, channels, datacard_dict,
                                       ScanType=args.ScanType, StatOnly=StatOnly, vsuff=vsuff, Unblind=Unblind)
            print('=================================================\n')
        #########################
        # full analysis workspace
        if generate_full:
            print('Modifying full analysis workspace:')
            print('=================================================')
            # for StatOnly in [False, True]:
            for StatOnly in [False]: # only makes sense to modify ws with syst
                print('Stat only? ', StatOnly)
                update_wsfile_full_analysis(NPs_to_promote, wscopy_suff, dim, ScanType=args.ScanType, StatOnly=StatOnly, vsuff=vsuff, Unblind=Unblind)
            print('=================================================\n')
        #########################
