import os

# local imports
import sys
fpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fpath,'..'))
from MISC_CONFIGS import dim6_ops

def write_datacards(WCs, channel, keys_out, keys_out_dim8, filename_root_out, filename_root_out_dim8, not_bg_flags, filename_dc, use_autoMCStats=True):
    print('\nWriting DataCards...')
    # constants
    linebreak = 100*'-'+'\n'
    # get names of all background procs
    procs_bg = []
    for k in keys_out:
        k_ = '_'.join(k.split('_')[1:])
        bg = True
        for flag in not_bg_flags:
            if flag in k_:
                bg = False
                break
        if bg:
            procs_bg.append(k_)
    # rename channel (can't be a number!!)
    bin_label = 'bin_'+channel
    procs_bg = sorted(procs_bg)
    print('procs_bg=')
    print(procs_bg)
    # generate a set of datacards for each operator you wish to consider
    datacard_string_dict = {}
    for WC in WCs:
        if WC in dim6_ops:
            filename_root_ = filename_root_out
            keys_ = keys_out
        else:
            filename_root_ = filename_root_out_dim8
            keys_ = keys_out_dim8
        # rename datacard file
        filename_dc_WC = filename_dc.replace('WC', WC)
        filename_dc_WC_statonly = filename_dc_WC.replace('DataCard_Yields', 'DataCard_Yields_StatOnly')
        # fill string
        # header
        datacard_string = linebreak + 'imax    1 number of bins\n'
        datacard_string += 'jmax    * number of processes minus 1\n'
        datacard_string += 'kmax    * number of nuisance parameters\n'
        datacard_string += linebreak
        # files and format of the histogram names
        datacard_string += f'shapes * * {filename_root_} h_$PROCESS h_$PROCESS_$SYSTEMATIC\n'
        datacard_string += f'shapes data_obs * {filename_root_} h_$PROCESS\n'
        datacard_string += linebreak
        # observation line
        datacard_string += f'bin          {bin_label}\n'
        # if has_data:
        #     datacard_string += '# ROOT contained "data_obs"\n'
        # else:
        #     datacard_string += '# ROOT did not contain "data_obs". Values set to zero.\n'
        # either way just have it grab from the file (i.e. "-1)
        datacard_string += 'observation  -1\n'
        datacard_string += linebreak
        # update the processes and other yield lines
        procs_ = ['sm']
        for k in keys_:
            k_ = '_'.join(k.split('_')[1:])
            if (WC in k_) and (('quad' in k_) or ('lin' in k_)):
                # make sure to skip systematics
                if ("Up" in k_) or ("Down" in k_):
                    continue
                # skip if a longer WC string is in the key (e.g. remove 'cHWB' from 'cHW' datacard)
                has_longer_WC = False
                for WC_ in WCs:
                    if len(WC_) > len(WC):
                        if WC_ in k_:
                            has_longer_WC = True
                            break
                if has_longer_WC:
                    continue
                # if it gets to here, safe to add
                procs_.append(k_)
        # add in the bg
        procs_ = procs_ + procs_bg
        # yield lines
        datacard_string += '%-27s' % 'bin'
        bin_labels = len(procs_)*['%-30s' % bin_label]
        datacard_string += ''.join(bin_labels) + '\n'
        datacard_string += '%-27s' % 'process'
        for proc in procs_:
            datacard_string += '%-30s' % proc
        datacard_string += '\n'
        # process indices
        datacard_string += '%-27s' % 'process'
        indices = range(len(procs_))
        yield_labels = ['%-30s' % str(i) for i in indices]
        datacard_string += ''.join(yield_labels) + '\n'
        # rates
        datacard_string += '%-27s' % 'rate'
        y = "-1"
        yield_labels = len(procs_)*['%-30s' % y]
        datacard_string += ''.join(yield_labels) + '\n'
        datacard_string += linebreak
        # systematics
        # loop through processes
        all_systs = set()
        for proc in procs_:
            relevant_keys = [k for k in keys_ if proc in k]
            for rk in relevant_keys:
                if "Up" in rk:
                    # remove any of the EFT histograms (should add in a careful way!!)
                    # any_WC = False
                    # for op in ops:
                    #     if op in rk:
                    #         any_WC = True
                    # if not any_WC:
                    syst = rk.replace('h_'+proc+'_', '').replace('Up', '')
                    all_systs.add(syst)
        all_systs = sorted(list(all_systs))
        # now loop through each systematic and fill for each process appropriately
        for syst in all_systs:
            #datacard_string += f'{syst:<20} shape '
            datacard_string += '%-20s' % syst
            datacard_string += ' shape '
            for proc in procs_:
                k = 'h_%s_%sUp' % (proc, syst)
                if k in keys_:
                    #datacard_string += f'{"1":<30}'
                    datacard_string += '%-30s' % "1"
                else:
                    # datacard_string += f'{"-":<30}'
                    datacard_string += '%-30s' % "-"
            datacard_string += '\n'
        # dummy systematics line
        datacard_string += '# systematics "off" (very very small)\n'
        #datacard_string += f'{"statonly":<20}'
        datacard_string += '%-20s' % 'statonly'
        datacard_string += ' lnN   '
        #y = f'{"1.0001":<30}'
        y = '%-30s' % '1.0001'
        datacard_string += ''.join(len(procs_)*[y]) + '\n'
        # artificially add "statonly" to systematics if they are missing from the file
        if len(all_systs) < 1:
            all_systs = ['statonly2']
            datacard_string += '# systematics "off" (very very small)\n'
            #datacard_string += f'{"statonly2":<20}'
            datacard_string += '%-20s' % 'statonly2'
            datacard_string += ' lnN   '
            # y = f'{"1.0001":<30}'
            y = '%-30s' % '1.0001'
            datacard_string += ''.join(len(procs_)*[y]) + '\n'
        # add "groups" line for turning on and off systematics
        datacard_string += '# nuisance groups (for stat-only vs. with systematics)\n'
        datacard_string += 'allsyst group = '
        datacard_string += ' '.join(all_systs) + '\n'
        datacard_string += 'nosyst group = statonly\n'
        # write to file
        with open(filename_dc_WC_statonly, 'w') as file_dc:
            file_dc.write(datacard_string)
        # make a version with automcstats, if relevant for that channel, else datacard is the same
        if use_autoMCStats:
            datacard_string += '# MC stat uncertainties\n'
            # FIXME! Add tunable threshold?
            datacard_string += '* autoMCStats 0\n'
        # write to file
        with open(filename_dc_WC, 'w') as file_dc:
            file_dc.write(datacard_string)
        # add to dict for return
        datacard_string_dict[WC] = datacard_string

    return datacard_string_dict
