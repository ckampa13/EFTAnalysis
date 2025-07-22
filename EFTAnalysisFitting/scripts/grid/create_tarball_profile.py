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

if __name__=='__main__':
    Unblind=True
    NP_promote=False
    # NP_promote=True
    if NP_promote:
        ws_suff='_NPsPromote'
    else:
        ws_suff=''
    start_dir = os.getcwd()
    stdout = subprocess.PIPE
    # CMSSW stuff
    CMSSW_DIR0 = os.environ.get("CMSSW_BASE")
    CMSSW_DIR = os.path.join(os.environ.get("CMSSW_BASE"), '')
    CMSSW_NAME = os.environ.get("CMSSW_VERSION")
    BASE_DIR = CMSSW_DIR0.replace(CMSSW_NAME, "")
    tarfile = CMSSW_NAME + ws_suff + ".tgz"
    # where to save?
    # fpath = os.path.dirname(os.path.realpath(__file__))
    outdir = os.path.join(os.path.abspath(os.path.join(fpath, '..', '..', 'unblind', 'output', 'grid', 'profile')), '')
    print("Going to output dir: %s" % outdir)
    os.chdir(outdir)
    # get the wsfiles and copy them
    sname_ch = 'all'
    sname_sch = '_combined'
    version = 'vCONFIG_VERSIONS_NDIM'
    dim = 'dim6'
    ScanTypeWS = '_All'
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    wsdir = os.path.join(dcdir, 'workspaces', 'full_analysis')
    # syst
    SO_lab = '' # with syst
    wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS, purpose='workspace'+ws_suff, proc=SO_lab, version=version, file_type='root')
    wsfile = os.path.join(wsdir, wsfile)
    print("Copying workspace file (syst) to CMSSW dir: %s -> %s" % (wsfile, CMSSW_DIR))
    shutil.copy(wsfile, CMSSW_DIR)
    # stat only
    SO_lab = '_StatOnly' # stat only
    wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS, purpose='workspace', proc=SO_lab, version=version, file_type='root')
    wsfile = os.path.join(wsdir, wsfile)
    print("Copying workspace file (stat only) to CMSSW dir: %s -> %s" % (wsfile, CMSSW_DIR))
    shutil.copy(wsfile, CMSSW_DIR)
    # make the tarball
    print("Making tarball of CMSSW (with workspace files):")
    cmd_str = "tar -zcf %s -C %s %s" % (tarfile, BASE_DIR, CMSSW_NAME)
    print(cmd_str)
    proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
    # cleanup
    print("Going back to original dir: %s" % start_dir)
    os.chdir(start_dir)
    print('Done.\n')
