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
)
from CONFIG_VERSIONS import versions_dict, WC_ALL, dim6_WCs, dim8_WCs, WCs_clip_dim6, WCs_clip_dim8, WCs_NDIM

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

def make_submission_template(points, split_points, jobFlavour='workday', stdout=subprocess.PIPE):
    cmd_str = "combineTool.py -d WSFILE -M MultiDimFit --algo=grid --points %s --alignEdges 1 COMBINE_OPTIONS " % (points)
    cmd_str += "--job-mode condor --split-points %s " % (split_points)
    cmd_str += "--sub-opts='+JobFlavour=\"%s\"' --task-name TEMPLATE_CONDOR --dry-run" % (jobFlavour)
    print("Creating job submission template:\n%s\n" % cmd_str)
    proc = subprocess.call(cmd_str, stdout=stdout, shell=True)

def modify_sh_template(output_dict, name, CMSSW_NAME, tarfile, WSFILE, file_in='condor_TEMPLATE_CONDOR.sh'):
    # .sh template filename input
    # writes the new file
    # returns string (?)
    file_out = file_in.replace("_TEMPLATE_CONDOR", name)
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
            tar_cmd = "tar -xf %s" % tarfile
            lines_after.append(tar_cmd)
        if 'cmsset_default.sh' in line:
            # go into CMSSW
            lines_after.append('cd %s/src' % CMSSW_NAME)
            # linking command
            lines_after.append('scramv1 b ProjectRename')
        if 'scramv1 runtime -sh' in line: # "cmsenv"
            lines_after.append('cd ../../')
            lines_after.append('')
            lines_after.append('WSFILE="%s/%s"' % (CMSSW_NAME, WSFILE))
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

def modify_sub_template(output_dict, name, CMSSW_NAME, tarfile, file_in='condor_TEMPLATE_CONDOR.sub'):
    # .sh template filename input
    # writes the new file
    # returns string (?)
    name_ = name.lstrip('_')
    file_out = file_in.replace("TEMPLATE_CONDOR", name_)
    print("%s -> %s" % (file_in, file_out))
    with open(file_in, 'r') as f:
        s = f.read()
    # first make general replacements
    s = s.replace('TEMPLATE_CONDOR', name_)
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
            lines_after.append('transfer_input_files = %s' % tarfile)
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
    Unblind=True
    start_dir = os.getcwd()
    stdout = subprocess.PIPE
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--WC',
                        help='Which Wilson Coefficient to study for 1D limits? ["NDIM" (default), "dim6", "cW", ...]')
    parser.add_argument('-a', '--Asimov', help='Use Asimov? "y"(default)/"n".')
    parser.add_argument('-S', '--Syst', help='Include Syst? "y"(default)/"n".')
    parser.add_argument('-PRP', '--PointsRandProf',
                        help='How many random initializations of profiled params per point? "49" (default), "0", "1", "2", ..., "49"')
    parser.add_argument('-SP', '--SplitPoints', help='Split points for grid job? "10"(default), "5", "100", ...')
    parser.add_argument('-PNP', '--PromoteNPs',
                        help='Use the workspaces with some NPs promoted to POIs? Useful e.g. to use --pointsRandProf on NPs, or limiting NP ranges. "y" (default) / "n"')
    args = parser.parse_args()
    if args.WC is None:
        args.WC = 'NDIM'
    if args.WC == 'dim6':
        WCs_loop = dim6_WCs
    elif args.WC == 'NDIM':
        WCs_loop = WCs_NDIM
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
        PointsRandProf = '49'
    else:
        PointsRandProf = args.PointsRandProf
    if args.SplitPoints is None:
        args.SplitPoints = '10'
    if args.PromoteNPs is None:
        PromoteNPs = 'y'
    else:
        PromoteNPs = args.PromoteNPs
    PromoteNPs_bool = PromoteNPs == 'y'
    if PromoteNPs_bool:
        ws_suff='_NPsPromote'
    else:
        ws_suff = ''
    # CMSSW stuff
    CMSSW_DIR0 = os.environ.get("CMSSW_BASE")
    CMSSW_DIR = os.path.join(os.environ.get("CMSSW_BASE"), '')
    CMSSW_NAME = os.environ.get("CMSSW_VERSION")
    BASE_DIR = CMSSW_DIR0.replace(CMSSW_NAME, "")
    tarfile = CMSSW_NAME + ws_suff + ".tgz"
    # where to save?
    # fpath = os.path.dirname(os.path.realpath(__file__))
    outdir = os.path.join(os.path.abspath(os.path.join(fpath, '..', '..', 'unblind', 'output', 'grid', 'profile')), '')
    # scripts dir
    scripts_dir = os.path.join(os.path.abspath(os.path.join(fpath, '..')), '')
    print("Going to output dir: %s" % outdir)
    os.chdir(outdir)
    # loop through WCs
    for WC in WCs_loop:
        # run_combine_1D.py with "JustPrint" option --> dump to temp file
        cmd_str = "python3 %s1D_scan/run_combine_1D.py -w %s -t f -s _All -U y -a %s -T y -v _NDIM -J y -UP y -PRP %s -PNP %s > dump.txt" % (scripts_dir, WC, asi, PointsRandProf, PromoteNPs)
        print(cmd_str)
        proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
        # parse the output
        print("Parsing combine strings to find syst: %s" % syst_str)
        with open('dump.txt', 'r') as f:
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
            jf = 'tomorrow'
        else:
            jf = 'longlunch'
        make_submission_template(cmd_dict['points'], args.SplitPoints, jobFlavour=jf, stdout=stdout)
        # modify .sh
        print("Making modifications to .sh and .sub files:")
        sname_ch = 'all'
        sname_sch = '_combined'
        version = 'vCONFIG_VERSIONS_NDIM'
        dim = 'dim6'
        ScanTypeWS = '_All'
        if syst_bool:
            SO_lab = '' # with syst
            ws_suff_ = ws_suff
        else:
            SO_lab = '_StatOnly' # stat only
            ws_suff_ = ''
        wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS, purpose='workspace'+ws_suff_, proc=SO_lab, version=version, file_type='root')
        lines_sh = modify_sh_template(cmd_dict, cmd_dict['name'], CMSSW_NAME, tarfile, wsfile, file_in='condor_TEMPLATE_CONDOR.sh')
        lines_sub = modify_sub_template(cmd_dict, cmd_dict['name'], CMSSW_NAME, tarfile, file_in='condor_TEMPLATE_CONDOR.sub')

    # cleanup
    # remove temporary files?
    # os.remove("condor_TEMPLATE_CONDOR.sh")
    # os.remove("condor_TEMPLATE_CONDOR.sub")
    print("Going back to original dir: %s" % start_dir)
    os.chdir(start_dir)
    print('Done.\n')
