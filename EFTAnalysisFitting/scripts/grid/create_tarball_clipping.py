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

def copy_files_and_tar(wsfiles, clip_ind):
    dirname = 'workspaces_clip_mVVV_%d' % clip_ind
    if not os.path.exists(dirname):
        # print("Creating workspace tar dir: %s" % dirname)
        os.mkdir(dirname)
    # copy files into dir
    for w in wsfiles:
        shutil.copy(w, dirname)
    # tar
    tarfile = dirname + '.tgz'
    cmd_str = "tar -zcf %s %s" % (tarfile, dirname)
    print(cmd_str)
    proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
    # clean up -- remove dir
    shutil.rmtree(dirname)


if __name__=='__main__':
    date = '07-13-25' # where to save the jobs
    Unblind=True
    # NP_promote=False
    NP_promote=True
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
    # tarfile = CMSSW_NAME + ws_suff + ".tgz"
    tarfile_CMSSW = CMSSW_NAME + ".tgz"
    # where to save?
    outdir = os.path.join(os.path.abspath(os.path.join(fpath, '..', '..', 'unblind', 'output', 'grid', 'clipping', date)), '')
    if not os.path.exists(outdir):
        print("Creating output dir: %s" % outdir)
        os.mkdir(outdir)
    print("Going to output dir: %s" % outdir)
    os.chdir(outdir)
    # loop through clip indexes and make tarballs
    print('Making clipped workspace tar files:')
    sname_ch = 'all'
    sname_sch = '_combined'
    version = 'vCONFIG_VERSIONS_clip_mVVV_'
    ScanTypeWS = '_All'
    dcdir = datacard_dir
    if Unblind:
        dcdir = os.path.join(dcdir, 'unblind')
    wsdir = os.path.join(dcdir, 'workspaces', 'full_analysis')
    for clip_ind in clip_inds:
        print('clip_ind = %d: ' % clip_ind, end='')
        wsfiles = []
        version_full = version + str(clip_ind)
        for dim, dim_suff in zip(['dim6', 'dim8'], ['', '_dim8']):
            if dim == 'dim8':
                ws_suffs = [ws_suff, '']
            else:
                ws_suffs = ['', '']
            for SO_lab, ws_suff_ in zip(['', '_StatOnly'], ws_suffs):
                wsfile = template_filename.substitute(channel=sname_ch, subchannel=sname_sch, WC=dim, ScanType=ScanTypeWS, purpose='workspace'+ws_suff_, proc=SO_lab, version=version_full, file_type='root')
                wsfile = os.path.join(wsdir, wsfile)
                wsfiles.append(wsfile)
        # copy files and tar
        print('copy and tar %d wsfiles' % len(wsfiles))
        copy_files_and_tar(wsfiles, clip_ind)
    print()
    # CMSSW tarball
    print("Making tarball of CMSSW (without workspace files):")
    # make the tarball
    cmd_str = "tar -zcf %s -C %s %s" % (tarfile_CMSSW, BASE_DIR, CMSSW_NAME)
    print(cmd_str)
    proc = subprocess.call(cmd_str, stdout=stdout, shell=True)
    # cleanup
    print("Going back to original dir: %s" % start_dir)
    os.chdir(start_dir)
    print('Done.\n')
