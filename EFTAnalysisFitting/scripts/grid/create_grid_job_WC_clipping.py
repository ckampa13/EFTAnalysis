import os
import shutil
import subprocess
import argparse
# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from MISC_CONFIGS import (
    datacard_dir,
    template_filename,
    clip_inds,
)
from CONFIG_VERSIONS import versions_dict, WC_ALL, dim6_WCs, dim8_WCs, WCs_clip_dim6, WCs_clip_dim8, WCs_NDIM
WCs_clip = WCs_clip_dim6 + WCs_clip_dim8

sh_line_drops = [
    lambda x: 'cd /uscms_data/' in x,
]

sub_line_drops = [
]

def parse_combine_command(cmd_str):
    output_dict = {}
    output_dict['points'] = cmd_str.split('--points ')[1].split(' ')[0]
    output_dict['name'] = cmd_str.split('-n ')[1].split(' ')[0]
    # rest of "COMBINE_OPTIONS"
    #i_rest = cmd_str.find('--redefineSignalPOIs') # misses the "-t -1" for asimov
    find_str = '--alignEdges 1 '
    N = len(find_str)
    i_rest = cmd_str.find(find_str) + N
    output_dict['COMBINE_OPTIONS'] = cmd_str[i_rest:].rstrip()
    return output_dict

def make_submission_template(points, split_points, jobFlavour='workday', stdout=subprocess.PIPE, template_suff=''):
    cmd_str = "combineTool.py -d WSFILE -M MultiDimFit --algo=grid --points %s --alignEdges 1 COMBINE_OPTIONS " % (points)
    if int(split_points) > 0:
        cmd_str += "--job-mode condor --split-points %s " % (split_points)
    else:
        cmd_str += "--job-mode condor "
    cmd_str += "--sub-opts='+JobFlavour=\"%s\"' --task-name TEMPLATE_CONDOR%s --dry-run" % (jobFlavour, template_suff)
    print("Creating job submission template:\n%s\n" % cmd_str)
    proc = subprocess.call(cmd_str, stdout=stdout, shell=True)

def modify_sh_template(clip_ind, output_dict, name, CMSSW_NAME, tarfile_CMSSW, WSFILE, file_in='condor_TEMPLATE_CONDOR.sh', template_suff=''):
    # .sh template filename input
    # writes the new file
    # returns string (?)
    dir_WS = 'workspaces_clip_mVVV_%d' % clip_ind
    file_out = file_in.replace("_TEMPLATE_CONDOR%s" % template_suff, name)
    print("%s -> %s" % (file_in, file_out))
    with open(file_in, 'r') as f:
        s = f.read()
    # first make general replacements
    s = s.replace('WSFILE', '$WSFILE')
    CO = output_dict['COMBINE_OPTIONS']
    s = s.replace('COMBINE_OPTIONS', CO)
    # remove spurious -n
    s = s.replace('-n %s ' % name, '')
    # update -n with points range in the name
    s = s.replace('-n .Test', '-n '+name)
    # then split to individual lines for further parsing
    lines = s.split('\n')
    lines_save = []
    for line in lines:
        lines_before = []
        lines_after = []
        if 'export SCRAM_ARCH' in line:
            # tar_cmd = "tar -xf %s.tgz" % CMSSW_NAME
            tar_cmd = "tar -xf %s" % tarfile_CMSSW
            lines_after.append(tar_cmd)
            tarfile_WS = dir_WS + '.tgz'
            tar_cmd_WS = "tar -xf %s" % tarfile_WS
            lines_after.append(tar_cmd_WS)
        if 'cmsset_default.sh' in line:
            # go into CMSSW
            lines_after.append('cd %s/src' % CMSSW_NAME)
            # linking command
            lines_after.append('scramv1 b ProjectRename')
        if 'scramv1 runtime -sh' in line: # "cmsenv"
            lines_after.append('cd ../../')
            lines_after.append('')
            lines_after.append('WSFILE="%s/%s"' % (dir_WS, WSFILE))
        skip = False
        for drop_func in sh_line_drops:
            if drop_func(line):
                skip = True
                break
        if skip:
            continue
        for l in lines_before:
            lines_save.append(l)
        lines_save.append(line)
        for l in lines_after:
            lines_save.append(l)

    # create output file
    lines_save = [l+'\n' for l in lines_save]
    with open(file_out, 'w') as f:
        f.writelines(lines_save)
    # make output file executable
    os.chmod(file_out, 0o755)
    return lines_save

def modify_sub_template(clip_ind, output_dict, name, CMSSW_NAME, tarfile_CMSSW, file_in='condor_TEMPLATE_CONDOR.sub', template_suff=''):
    # .sh template filename input
    # writes the new file
    # returns string (?)
    dir_WS = 'workspaces_clip_mVVV_%d' % clip_ind
    tarfile_WS = dir_WS + '.tgz'
    name_ = name.lstrip('_')
    file_out = file_in.replace("_TEMPLATE_CONDOR%s" % template_suff, name)
    print("%s -> %s" % (file_in, file_out))
    with open(file_in, 'r') as f:
        s = f.read()
    # first make general replacements
    s = s.replace('TEMPLATE_CONDOR', name_)
    s = s.replace(template_suff, '')
    # then split to individual lines for further parsing
    lines = s.split('\n')
    lines_save = []
    for line in lines:
        lines_before = []
        lines_after = []
        if line[:3] == 'log':
            lines_after.append('')
            lines_after.append('should_transfer_files = yes')
            # lines_after.append('transfer_input_files = %s.tgz' % CMSSW_NAME)
            lines_after.append('transfer_input_files = %s, %s' % (tarfile_CMSSW, tarfile_WS))
            lines_after.append('when_to_transfer_output = on_exit')
        skip = False
        for drop_func in sub_line_drops:
            if drop_func(line):
                skip = True
                break
        if skip:
            continue
        for l in lines_before:
            lines_save.append(l)
        lines_save.append(line)
        for l in lines_after:
            lines_save.append(l)

    # create output file
    lines_save = [l+'\n' for l in lines_save]
    with open(file_out, 'w') as f:
        f.writelines(lines_save)
    return lines_save


if __name__=='__main__':
    date = '07-13-25' # where to save the jobs
    Unblind=True
    start_dir = os.getcwd()
    stdout = subprocess.PIPE
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--ClipInd',
                        help='Which clip index to use? "all" (default), "0", "1",...')
    parser.add_argument('-w', '--WC',
                        help='Which Wilson Coefficient to study for 1D limits? ["all" (default), "dim6", "dim8", "cW", ...]')
    parser.add_argument('-a', '--Asimov', help='Use Asimov? "y"(default)/"n".')
    parser.add_argument('-S', '--Syst', help='Include Syst? "y"(default)/"n".')
    parser.add_argument('-PRP', '--PointsRandProf',
                        help='How many random initializations of profiled params per point? "4" (default), "0", "1", "2", ..., "49"')
    parser.add_argument('-SP', '--SplitPoints', help='Split points for grid job? Note zero will not split. "0" (default), "10", "5", "100", ...')
    # parser.add_argument('-PNP', '--PromoteNPs',
    #                     help='Use the workspaces with some NPs promoted to POIs? Useful e.g. to use --pointsRandProf on NPs, or limiting NP ranges. "y" (default) / "n"')
    args = parser.parse_args()
    if args.ClipInd is None:
        args.ClipInd = 'all'
    if args.ClipInd == 'all':
        clip_inds_loop = clip_inds
    else:
        clip_inds_loop = [int(args.ClipInd)]
    if args.WC is None:
        args.WC = 'all'
    if args.WC == 'all':
        WCs_loop = WCs_clip
    elif args.WC == 'dim6':
        WCs_loop = WCs_clip_dim6
    elif args.WC == 'dim8':
        WCs_loop = WCs_clip_dim8
    else:
        WCs_loop = [args.WC]
    if args.Asimov is None:
        asi = 'y'
    else:
        asi = args.Asimov
    if args.Syst is None:
        syst = 'y'
    else:
        syst = args.Syst
    syst_bool = syst == 'y'
    if syst_bool:
        syst_str = 'syst'
    else:
        syst_str = 'nosyst'
    if args.PointsRandProf is None:
        PointsRandProf = '4'
    else:
        PointsRandProf = args.PointsRandProf
    if args.SplitPoints is None:
        args.SplitPoints = '0'
    # if args.PromoteNPs is None:
    #     PromoteNPs = 'y'
    # else:
    #     PromoteNPs = args.PromoteNPs
    # PromoteNPs_bool = PromoteNPs == 'y'
    # if PromoteNPs_bool:
    #     ws_suff='_NPsPromote'
    # else:
    #     ws_suff = ''
    # CMSSW stuff
    CMSSW_DIR0 = os.environ.get("CMSSW_BASE")
    CMSSW_DIR = os.path.join(os.environ.get("CMSSW_BASE"), '')
    CMSSW_NAME = os.environ.get("CMSSW_VERSION")
    BASE_DIR = CMSSW_DIR0.replace(CMSSW_NAME, "")
    tarfile_CMSSW = CMSSW_NAME + ".tgz"
    # where to save?
    # fpath = os.path.dirname(os.path.realpath(__file__))
    outdir = os.path.join(os.path.abspath(os.path.join(fpath, '..', '..', 'unblind', 'output', 'grid', 'clipping', date)), '')
    # scripts dir
    scripts_dir = os.path.join(os.path.abspath(os.path.join(fpath, '..')), '')
    print("Going to output dir: %s" % outdir)
    os.chdir(outdir)
    # loop through clip inds
    for clip_ind in clip_inds_loop:
        vsuff = '_clip_mVVV_%d' % clip_ind
        print('clip_ind = %d' % clip_ind)
        # loop through WCs
        for WC in WCs_loop:
            if WC in dim6_WCs:
                dim = 'dim6'
                ws_suff = ''
                PNP = 'n'
            else:
                dim = 'dim8'
                if syst_bool:
                    ws_suff = '_NPsPromote'
                    PNP = 'y'
                else:
                    ws_suff = ''
                    PNP = 'n'
            # run_combine_1D.py with "JustPrint" option --> dump to temp file
            dumpfile = 'dump_%s_asi_%s_syst_%s.txt' % (WC, asi, syst)
            print('dumpfile=%s' % dumpfile)
            cmd_str = "python3 %s1D_scan/run_combine_1D.py -w %s -t f -s _1D -U y -a %s -T y -v %s -J y -UP y -PRP %s -PNP %s > %s" % (scripts_dir, WC, asi, vsuff, PointsRandProf, PNP, dumpfile)
            print(cmd_str)
            proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
            # parse the output
            print("Parsing combine strings to find syst: %s" % syst_str)
            with open(dumpfile, 'r') as f:
                lines=f.readlines()
            lines_run = []
            for line in lines:
                if line[:22] == "combine -M MultiDimFit":
                    lines_run.append(line)
            line_corr = None
            for line in lines_run:
                if "--freezeNuisanceGroups nosyst" in line: # syst
                    if syst_bool:
                        line_corr = line
                        break
                else:
                    if not syst_bool:
                        line_corr = line
                        break
            print("Found command:\n%s\n" % line_corr)
            # parse command and create grid submission script template
            print("Parsing command:")
            cmd_dict = parse_combine_command(line_corr)
            print(cmd_dict)
            # note: workday=8hrs, tommorow=24hrs
            if syst_bool:
                if dim == 'dim6':
                    # jf = 'espresso'
                    jf = 'longlunch'
                else:
                    jf = 'longlunch'
            else:
                jf = 'espresso'
            template_suff = '_%s_asi_%s_syst_%s' % (WC, asi, syst)
            print('template_suff=%s' % template_suff)
            make_submission_template(cmd_dict['points'], args.SplitPoints, jobFlavour=jf, stdout=stdout, template_suff=template_suff)
            # modify .sh
            print("Making modifications to .sh and .sub files:")
            sname_ch = 'all'
            sname_sch = '_combined'
            version = 'vCONFIG_VERSIONS'
            version_full = version + vsuff
            ScanTypeWS = '_All'
            if syst_bool:
                SO_lab = '' # with syst
                ws_suff_ = ws_suff
            else:
                SO_lab = '_StatOnly' # stat only
                ws_suff_ = ''
            wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS, purpose='workspace'+ws_suff_, proc=SO_lab, version=version_full, file_type='root')
            lines_sh = modify_sh_template(clip_ind, cmd_dict, cmd_dict['name'], CMSSW_NAME, tarfile_CMSSW, wsfile,
                                          file_in='condor_TEMPLATE_CONDOR%s.sh' % template_suff, template_suff=template_suff)
            lines_sub = modify_sub_template(clip_ind, cmd_dict, cmd_dict['name'], CMSSW_NAME, tarfile_CMSSW,
                                            file_in='condor_TEMPLATE_CONDOR%s.sub' % template_suff, template_suff=template_suff)
            os.remove(dumpfile)
            os.remove('condor_TEMPLATE_CONDOR%s.sub' % template_suff)
            os.remove('condor_TEMPLATE_CONDOR%s.sh' % template_suff)
        print()
    # cleanup
    # remove temporary files?
    # os.remove("condor_TEMPLATE_CONDOR.sh")
    # os.remove("condor_TEMPLATE_CONDOR.sub")
    print("Going back to original dir: %s" % start_dir)
    os.chdir(start_dir)
    print('Done.\n')
