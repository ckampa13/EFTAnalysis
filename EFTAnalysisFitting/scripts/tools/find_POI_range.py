# runs with "python" (python2) on LPC, since pyROOT is only in python 2.
# scan a ROOT file output from combine, and print the min and max that should
# be used s.t. deltaNLL >= some threshold. Given some desired step size, the
# appropriate number of steps is also calculated.
import os
import argparse
import numpy as np
import ROOT


def check_file_threshold(rootfile, WC, NLL_threshold, stepsize, stepsize_coarse):
    # read file
    inFile = ROOT.TFile.Open(rootfile, "READ")
    limit = inFile.Get("limit")
    # loop over tree, skipping the first entry
    cs = []
    nlls = []
    for entryNum in range(1, limit.GetEntries()):
        limit.GetEntry(entryNum);
        cs.append(getattr(limit, 'k_'+WC))
        nlls.append(getattr(limit, 'deltaNLL'))
    cs = np.array(cs)
    nlls = np.array(nlls)
    nlls[np.isnan(nlls)] = 1000.
    # using a mask, find LL and UL (to be adjusted)
    below_thresh = nlls < NLL_threshold
    ilow = np.arange(len(nlls))[below_thresh][0] - 1
    ihigh = np.arange(len(nlls))[below_thresh][-1] + 1
    if ilow < 0:
        ilow = 0
    if ihigh > len(nlls) -1:
        ihigh = len(nlls)-1
    LL = cs[ilow]
    UL = cs[ihigh]
    # calculate number of steps and adjust UL
    range_ = UL - LL
    if range_ > 10:
        stepsize_ = stepsize_coarse
    else:
        stepsize_ = stepsize
    steps = int((UL-LL)/stepsize_) + 2
    UL = LL + (steps-1) * stepsize_
    # print in a way that can be easily parsed
    # check if threshold is reached...if not throws an error (in the parsing function)
    # if (nlls[ilow] < NLL_threshold) or (nlls[ihigh] < NLL_threshold):
    #     print 'ERROR: Either low end or high end does not get above NLL_threshold. Try again with a wider range.'
    # else:
    #     print 'LL:{0:0.4f};UL:{1:0.4f};steps:{2:d}'.format(LL, UL, steps)
    # use range regardless...using +-100 is a sort of nonsense range already.
    print 'LL:{0:0.4f};UL:{1:0.4f};steps:{2:d}'.format(LL, UL, steps)

    return LL, UL, steps


if __name__=='__main__':
    # directories
    datacard_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                '..')
    # absolute paths
    datacard_dir = os.path.abspath(datacard_dir)
    # parse commmand line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--File',
                        help='Name of ROOT file (including full path!).')
    parser.add_argument('-w', '--WC',
                        help='Which Wilson Coefficient to study for 1D limits? ["cW" (default),]')
    parser.add_argument('-T', '--ThresholdDeltaNLL',
                        help='What is the deltaNLL threshold? e.g. "4.0" (default) works well for 95% CL.')
    parser.add_argument('-s', '--StepSize',
                        help='What is the desired precision / step size for limit setting? e.g. "0.001" (default)')
    parser.add_argument('-sc', '--StepSizeCoarse',
                        help='What is the desired precision / step size for limit setting when range of POI > 10? e.g. "0.01" (default)')
    args = parser.parse_args()
    # fill defauls if necessary
    if args.WC is None:
        args.WC = 'cW'
    if args.ThresholdDeltaNLL is None:
        args.ThresholdDeltaNLL = 4.0
    else:
        args.ThresholdDeltaNLL = float(args.ThresholdDeltaNLL)
    if args.StepSize is None:
        args.StepSize = 0.001
    else:
        args.StepSize = float(args.StepSize)
    if args.StepSizeCoarse is None:
        args.StepSizeCoarse = 0.01
    else:
        args.StepSizeCoarse = float(args.StepSizeCoarse)
    ### check file
    # note that driving script will parse the information as printed in the function
    # so the return values are not strictly necessary here.
    LL, UL, steps = check_file_threshold(args.File, args.WC, args.ThresholdDeltaNLL, args.StepSize, args.StepSizeCoarse)
