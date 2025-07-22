# FIXME should handle not only floats but also floats with slashes 1.0/1.0
# FIXME should check 1.0 for all values instead of at least 1.0 in values for lnN
import fnmatch
import os
import re
from copy import deepcopy
from optparse import OptionParser
from shutil import copyfile
from typing import List
import numpy as np

import numpy as np
import uproot
from HiggsAnalysis.CombinedLimit.DatacardParser import *


class datacardHelper:
    @staticmethod
    def loadDatacard(dcpath: str, parser=None) -> Datacard:
        if parser == None:
            # create an empty parser
            parser = OptionParser()

        # add specific options that may not be present in the
        # command line and are specific for the parsing of
        # datacard

        addDatacardParserOptions(parser)

        # parse argument (and command line options)
        # if parser was created then we cannot parse
        # command line options

        if parser == None:
            (options, args) = parser.parse_args(args=[])
        else:
            (options, args) = parser.parse_args(args=[])

        # allow no signals
        options.allowNoSignal = True

        # read original datacard
        file = open(dcpath, "r")
        DC = parseCard(file, options)
        DC.path = "/".join(dcpath.split("/")[:-1]) + "/"
        if DC.path == "/":
            DC.path = "./"
        if not DC.hasShapes:
            DC.hasShapes = True

        return DC

    @staticmethod
    def createBundle(dcpath: str, outdir: str) -> None:
        """
        Create a copy of current datacard and all of its shapes
        inside a direcotry. Will modifify new datacard paths in order to be compliant
        with new structure
        """

        print("Creating bundle")

        if os.path.isdir(outdir):
            os.system("rm -rf " + outdir)
        os.mkdir(outdir)

        # Make new dc name
        dcname = os.path.basename(dcpath)
        newdc = os.path.join(outdir, dcname)

        # Open the base datacard and retrieve the shapes path
        # then copy the shapes into the bundle

        DC = datacardHelper.loadDatacard(dcpath)

        # keys of fileBinMap are the root shape files
        fileBinMap = datacardHelper.createfileBinMap(DC, onlyMC=False)
        # copy the original file bin map and change file paths
        new_fileBinMap = fileBinMap.copy()

        # now copy the shapes in the new directory
        # and fill new_fileBinMap
        for idx, key in enumerate(fileBinMap.keys()):
            # copy shape files side by side in the same bundle
            # easier to modify the datacard header

            # handle the case where file_name is already present 
            # in the output bundled folder by appending an index
            file_name = os.path.basename(key) + "_" + str(idx)

            copyfile(key, os.path.join(outdir, file_name))

            # change name of the dictionary key with relative
            # path that will appear in the new datacard
            new_fileBinMap[file_name] = new_fileBinMap.pop(key)

        # revert the file bin map to be compatible with
        # a DC.shapeMap object so we can write the dc out of the box
        DC.shapeMap = datacardHelper.revertFileBinMap(new_fileBinMap)

        # now write the datacard object to the bundle directory
        datacardHelper.writeDatacard(DC, newdc)

        return

    @staticmethod
    def getShapeNuisancesForSample(DC: Datacard, sample: str):
        nuis = {}
        for lsyst, nofloat, pdf0, args0, errline0 in DC.systs[:]:
            if pdf0 not in ["shape", "shapeN"]:
                continue
            for dcbin, binerrors in errline0.items():
                if sample in binerrors.keys() and binerrors[sample] > 0:
                    if lsyst not in nuis.keys():
                        nuis[lsyst] = [dcbin]
                    else:
                        nuis[lsyst].append(dcbin)
        return nuis

    @staticmethod
    def revertFileBinMap(fileBinMap) -> dict:
        revertedBinMap = {}
        for file__ in fileBinMap.keys():
            for idx in range(len(fileBinMap[file__]["nominalShapes"])):
                nomS = fileBinMap[file__]["nominalShapes"][idx]
                nuisS = fileBinMap[file__]["nuisShapes"][idx]
                dcBin = fileBinMap[file__]["datacardBin"][idx]
                key = fileBinMap[file__]["key"][idx]

                if dcBin not in revertedBinMap.keys():
                    revertedBinMap[dcBin] = {}

                if key not in revertedBinMap[dcBin].keys():
                    revertedBinMap[dcBin][key] = [file__]
                    # nominal shape present also for data
                    revertedBinMap[dcBin][key].append(nomS)
                    # in data we have no nuis
                    if nuisS != "":
                        revertedBinMap[dcBin][key].append(nuisS)
        return revertedBinMap

    @staticmethod
    def createfileBinMap(DC: Datacard, onlyMC=True, onlyData=False) -> dict:
        # to optimally retrieve shapes need to minimize file opening
        # problem is that datacard bins (in txt file) might not coincide
        # with shape root file subdirectory (if any...)
        # so we revert the dict in fileBinMap
        # key is the root file path
        # subkeys are list of paired datacard bin and corresponding shape file dir

        fileBinMap = {}

        # cycle on datacard bins to retrieve the bin shape file
        # and eventually the bin subdirectory containing the shapes
        for bin__ in DC.bins:
            # We suppose this is either "*" for mc or "data_obs" for data
            # other cases need attention

            b__ = bin__
            # handle the case where for all dc bins we only have one root file
            if b__ not in DC.shapeMap.keys() and "*" in DC.shapeMap.keys():
                b__ = "*"
            for key in DC.shapeMap[b__]:
                # We are only interested in MC as we are retrieving the EFT shapes
                if key != "data_obs" and onlyData:
                    continue
                elif key == "data_obs" and onlyMC:
                    continue

                # first entry should be the relative file path
                file__ = DC.path + DC.shapeMap[b__][key][0]
                # subdir can be empty or jusy $PROCESS
                dir__ = ""
                nuis__ = ""
                for entry in DC.shapeMap[b__][key][1:]:
                    # we could have $PROCESS or $PROCESS_$SYSTEMATIC,
                    # selecting the former as contains nominal templates
                    if entry.endswith("$PROCESS"):
                        dir__ = entry
                    elif "$SYSTEMATIC" in entry:
                        nuis__ = entry
                    else:
                        # data case
                        dir__ = entry

                if file__ not in fileBinMap.keys():
                    fileBinMap[file__] = {
                        "nominalShapes": [dir__],
                        "nuisShapes": [nuis__],
                        "datacardBin": [bin__],
                        "key": [key],
                    }
                else:
                    fileBinMap[file__]["nominalShapes"].append(dir__)
                    fileBinMap[file__]["nuisShapes"].append(nuis__)
                    fileBinMap[file__]["datacardBin"].append(bin__)
                    fileBinMap[file__]["key"].append(key)

        return fileBinMap

    @staticmethod
    def getDCEFTsamples(DC: Datacard) -> list:
        eft_signals = []
        if "sm" in DC.processes:
            eft_signals.append("sm")
        for sample in DC.processes:
            if sample.startswith("quad_") or "_quad_" in sample:
                eft_signals.append(sample)
            elif sample.startswith("lin_") or "_lin_" in sample:
                eft_signals.append(sample)
            elif sample.startswith("sm_lin_quad") or "_sm_lin_quad_" in sample:
                eft_signals.append(sample)

        return np.unique(eft_signals)

    @staticmethod
    def setSamplesAsSignals(DC: Datacard, new_signals: list) -> None:
        for sample in new_signals:
            if sample not in DC.processes:
                print(f"[ERROR] sample {sample} not in datacard samples {DC.processes}")
                return

            if sample not in DC.signals:
                DC.signals.append(sample)
                DC.isSignal[sample] = True

        return


    @staticmethod
    def remove_sample(
        DC: Datacard,
        name: str,
        channel_list=[],
    ) -> None:

        if channel_list == []:
            channel_list = DC.bins
        
        # sanitycheck, is this sample in the datacard?
        if name not in DC.processes:
            print(
                f"[ERROR] {name} not in list of processes"
                f" for current datacard: {DC.processes}"
            )
            return None
        
        DC.processes.pop(DC.processes.index(name))
        if name in DC.signals: 
            DC.signals.pop(DC.signals.index(name))
            del DC.isSignal[name]
        
        delete_idx = []
        for idx in range(len(DC.keyline)):
            if DC.keyline[idx][1] == name: delete_idx.append(idx)

        for index in sorted(delete_idx, reverse=True):
            del DC.keyline[index]

        for dcbin in DC.exp.keys():
            if name in list(DC.exp[dcbin].keys()):
                DC.exp[dcbin].pop(name)

        # renaming nusiances
        for idx in range(len(DC.systs)):
            for dcbin in DC.systs[idx][4].keys():
                if name in list(DC.systs[idx][4][dcbin].keys()):
                    DC.systs[idx][4][dcbin].pop(name)

        for (syst_name, bin, oldprocess), val in list(DC.systematicsShapeMap.items()):
            if oldprocess == name: del DC.systematicsShapeMap[(syst_name, bin, oldprocess)]

        for bin__, procs__ in DC.shapeMap.items():
            for proc in list(procs__.keys()):
                if name == proc:
                    DC.shapeMap[bin__].pop(name)

        return
                

    @staticmethod
    def renameSample(DC: Datacard, oldname=None, newname=None) -> None:
        if getattr(DC, "sampleShapeMap", None) is None:
            DC.sampleShapeMap = {}
        DC.sampleShapeMap[newname] = oldname

        # need to modify every attribute of DC object
        # in order to fully propagate the changes

        # sanitycheck, is this sample in the datacard?
        if oldname not in DC.processes:
            print(
                f"[ERROR] {oldname} not in list of processes"
                f" for current datacard: {DC.processes}"
            )
            return None

        DC.processes[DC.processes.index(oldname)] = newname
        if oldname in DC.signals:
            DC.signals[DC.signals.index(oldname)] = newname
            DC.isSignal[newname] = DC.isSignal.pop(oldname)

        for idx in range(len(DC.keyline)):
            if DC.keyline[idx][1] == oldname:
                tmp__ = list(DC.keyline[idx])
                tmp__[1] = newname
                DC.keyline[idx] = tuple(tmp__)

        for dcbin in DC.exp.keys():
            if oldname in DC.exp[dcbin].keys():
                DC.exp[dcbin][newname] = DC.exp[dcbin].pop(oldname)

        # renaming nusiances
        for idx in range(len(DC.systs)):
            for dcbin in DC.systs[idx][4].keys():
                if oldname in DC.systs[idx][4][dcbin].keys():
                    DC.systs[idx][4][dcbin][newname] = DC.systs[idx][4][dcbin].pop(
                        oldname
                    )
        # list of tuples, first is new, second is old and to delete
        swap_and_dels = []
        for (syst_name, bin, oldprocess), val in DC.systematicsShapeMap.items():
            if oldprocess == oldname:
                swap_and_dels.append(
                    ((syst_name, bin, newname), (syst_name, bin, oldname))
                )
                # DC.systematicsShapeMap[(syst_name, bin, newname)] = val
                # to_del.append((syst_name, bin, oldname))
        for swap_and_del in swap_and_dels:
            DC.systematicsShapeMap[swap_and_del[0]] = DC.systematicsShapeMap[
                swap_and_del[1]
            ]
            del DC.systematicsShapeMap[swap_and_del[1]]

        for bin__, procs__ in DC.shapeMap.items():
            for proc in procs__.keys():
                if oldname == proc:
                    DC.shapeMap[bin__][newname] = DC.shapeMap[bin__].pop(oldname)

        return

    @staticmethod
    def writeDatacard(DC: Datacard, out: str) -> None:
        fo = open(out, "w")
        fo.write(f"imax {len(DC.bins)} number of bins\n")
        fo.write(f"jmax {len(DC.processes)-1} number of processes minus 1\n")

        # as we are skipping nuisances later need to compute the empty ones
        nnuis = 0
        for nuisance_item in DC.systs:
            for b in nuisance_item[4]: 
                if all(i==0 for _, i in nuisance_item[4][b].items()): 
                    continue 
                else: 
                    nnuis += 1
                    break

        fo.write(f"kmax {nnuis} number of nuisance parameters\n")

        fo.write(f'\n{"".join(["-"]*130)}\n')

        # writing shape files
        if DC.hasShapes:
            for bin_name, values in DC.shapeMap.items():
                # key here should be for MC and data we don't know the order
                for key, shapes_pattern in values.items():
                    fo.write(
                        f"shapes {key}".ljust(20, " ")
                        + bin_name.ljust(
                            20 + len(bin_name) if len(bin_name) >= 20 else 20, " "
                        )
                        + "".join(
                            i.ljust(20 + len(i) if len(i) >= 20 else 20, " ")
                            for i in shapes_pattern
                        )
                        + "\n"
                    )

        fo.write(f'\n{"".join(["-"]*130)}\n')

        # observations

        fo.write(
            "bin".ljust(20, " ")
            + "".join(
                i.ljust(20 + len(i) if len(i) >= 20 else 20, " ") for i in DC.bins
            )
            + "\n"
        )
        fo.write(
            "observation".ljust(20, " ")
            + "".join(
                i.ljust(20 + len(i) if len(i) >= 20 else 20, " ")
                for i in [str(DC.obs[b]) for b in DC.bins]
            )
            + "\n"
        )

        fo.write(f'\n{"".join(["-"]*130)}\n')

        # dc bins
        # dc bins = number of analyses * processes in bin
        fo.write(
            "bin".ljust(20, " ")
            + "".join(
                i[0].ljust(20 + len(i[0]) if len(i[0]) >= 20 else 20, " ")
                for i in DC.keyline
            )
            + "\n"
        )
        # process
        fo.write(
            "process".ljust(20, " ")
            + "".join(
                i[1].ljust(20 + len(i[1]) if len(i[1]) >= 20 else 20, " ")
                for i in DC.keyline
            )
            + "\n"
        )

        # build a dict for signal and backgrounds indices
        start_signal = -len(DC.signals) + 1  # because 0 is still a signal
        start_bkg = 1
        proc_idx = {}
        for proc, isS in DC.isSignal.items():
            if isS:
                proc_idx[proc] = str(start_signal)
                start_signal += 1
            else:
                proc_idx[proc] = str(start_bkg)
                start_bkg += 1

        # process indices
        fo.write(
            "process".ljust(20, " ")
            + "".join(proc_idx[i[1]].ljust(20, " ") for i in DC.keyline)
            + "\n"
        )

        fo.write(f'\n{"".join(["-"]*130)}\n')

        # rate
        fo.write(
            "rate".ljust(20, " ")
            + "".join(str(DC.exp[i[0]][i[1]]).ljust(20, " ") for i in DC.keyline)
            + "\n"
        )

        fo.write(f'\n{"".join(["-"]*130)}\n')

        # nuisances

        for nuisance_item in DC.systs:
            # Prune empty systs
            emtpy = True
            for b in nuisance_item[4]:
                for p in nuisance_item[4][b]:
                    if nuisance_item[4][b][p] != 0:
                        emtpy = False
                        break
            if emtpy:
                continue
            nuisance_name = nuisance_item[0]
            nuisance_type = nuisance_item[2]
            nuisance_additional = " ".join(nuisance_item[3])
            nuisance_keys = nuisance_item[4]

            # for shape this is ok
            nuisance_values = [
                str(nuisance_keys[i[0]][i[1]]).ljust(20, " ") for i in DC.keyline
            ]
            # for lnN wee need modification
            if nuisance_type == "lnN" or nuisance_type == "shape?":
                nuisance_values = []
                for i in DC.keyline:
                    v = nuisance_keys[i[0]][i[1]]
                    if isinstance(v, float):
                        nuisance_values.append(str(v).ljust(20, " "))
                    elif isinstance(v, list):
                        nuisance_values.append(f"{v[0]}/{v[1]}".ljust(20, " "))

                # nuisance_values = [f"{str(nuisance_keys[i[0]][i[1]][0])}/{nuisance_keys[i[0]][i[1]][1]}".ljust(20, " ") for i in DC.keyline]

            fo.write(
                f"{nuisance_name}".ljust(
                    20 + len(nuisance_name) if len(nuisance_name) >= 20 else 20, " "
                )
                + f"{nuisance_type}".ljust(20, " ")
                + f"{nuisance_additional}".ljust(
                    20 if nuisance_additional != "" else 0, " "
                )
                + "".join(nuisance_values)
                + "\n"
            )

        fo.write(f'\n{"".join(["-"]*130)}\n')

        # rateParam

        for rp, rv in DC.rateParams.items():
            bin_name, process_name = rp.split("AND")
            # I don't know why they designed the value
            # this way
            for outer_cycle in rv:
                # interesting_values = ['TTest_electron_2016M', '1', 0]
                interesting_values = outer_cycle[0]
                fo.write(
                    f"{interesting_values[0]}".ljust(
                        20 + len(interesting_values[0])
                        if len(interesting_values[0]) >= 20
                        else 20,
                        " ",
                    )
                    + "rateParam".ljust(20, " ")
                    + f"{bin_name}".ljust(
                        20 + len(bin_name) if len(bin_name) >= 20 else 20, " "
                    )
                    + f"{process_name}".ljust(
                        20 + len(process_name) if len(process_name) >= 20 else 20, " "
                    )
                    + f"{interesting_values[1]}".ljust(20, " ")
                    + "\n"
                )

        # autoMCstat
        for bin_name, values in DC.binParFlags.items():
            fo.write(
                f"{bin_name}".ljust(
                    20 + len(bin_name) if len(bin_name) >= 20 else 20, " "
                )
                + "autoMCStats".ljust(20, " ")
                + f"{values[0]}".ljust(20, " ")
                + f"{str(int(values[1]))}".ljust(20, " ")
                + f"{values[2]}".ljust(20, " ")
                + "\n"
            )

        return

    @staticmethod
    def renameNuisanceParameter(
        DC: Datacard, oldname: str, newname: str, process_list=[], channel_list=[]
    ):
        """
        This is a copy and paste of the original method in the Datacard object because it does not
        work. It tries to assign values to self.systs entries (tuple). We just modify the
        code slightly to make it work.
        This function will disappear when the fix is propagated in combine official code

        https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/issues/999
        """
        existingclashes = {}
        for lsyst, nofloat, pdf0, args0, errline0 in DC.systs[:]:
            if lsyst == newname:  # found the nuisance exists
                existingclashes[lsyst] = (nofloat, pdf0, args0, errline0)

        found = False
        nuisanceID = i = -1

        if process_list == []:
            process_list = DC.processes
        if channel_list == []:
            channel_list = DC.bins

        for lsyst, nofloat, pdf0, args0, errline0 in DC.systs[:]:
            i += 1
            if lsyst == oldname:  # found the nuisance
                nuisanceID = i
                found = True
                # check if the new name exists
                if lsyst in list(existingclashes.keys()):
                    nofloat1, pdf1, args1, errline1 = existingclashes[lsyst]

                else:
                    pass
                # allow to modify this
                if process_list != DC.processes:
                    nuis_entry_backup = deepcopy(list(DC.systs[nuisanceID]))
                    nuis_entry = list(DC.systs[nuisanceID])
                    for b in channel_list:
                        for p, v in nuis_entry[4][b].items():
                            if p in process_list:
                                nuis_entry[4][b][p] = 0.0

                    DC.systs[nuisanceID] = tuple(nuis_entry)

                    nuis_entry = nuis_entry_backup
                    nuis_entry[0] = newname
                    for b in channel_list:
                        for p, v in nuis_entry[4][b].items():
                            if p not in process_list:
                                nuis_entry[4][b][p] = 0.0
                    DC.systs.append(tuple(nuis_entry))
                    DC.systIDMap[newname] = [len(DC.systs) - 1]
                else:
                    nuis_entry = list(DC.systs[nuisanceID])
                    nuis_entry[0] = newname
                    DC.systs[nuisanceID] = tuple(nuis_entry)

                # where do we need to change this if it is a shape
                # uncertainty?
                if "shape" in pdf0:
                    for b in channel_list:
                        for p in process_list:
                            # so apparently "-" is converted into 0.0 at some point
                            if (
                                p in nuis_entry[4][b].keys()
                                and nuis_entry[4][b][p] != 0
                            ):
                                DC.systematicsShapeMap[newname, b, p] = oldname
                if "param" in pdf0:
                    DC.systematicsParamMap[oldname] = newname
                break

        if not found:
            # raise RuntimeError("Error: no parameter found with = %s\n" % oldname)
            print("Error: no parameter found with = %s\n" % oldname)
        return 0



    # FIXME @jack
    @staticmethod
    def remove(
        DC: Datacard,
        name: str,
        process_list=[],
        channel_list=[],
    ) -> None:
        if process_list == []:
            process_list = DC.processes
        if channel_list == []:
            channel_list = DC.bins

        for nuisance_id, (lsyst, nofloat, pdf0, args0, errline0) in enumerate(
            DC.systs[:]
        ):
            if lsyst == name:  # found the nuisance
                nuis_entry = DC.systs[nuisance_id]
                for b in nuis_entry[4]:
                    if b not in channel_list:
                        continue
                    for p in nuis_entry[4][b]:
                        if p in process_list:
                            nuis_entry[4][b][p] = 0.0
                break

        # # cycle on regexp and pop nuisances if they match by name
        # for expression in regexp:
        #     prog = re.compile(expression)
        #     DC.systs = [i for i in DC.systs if not prog.match(i[0])]
        #     DC.systIDMap = {
        #         key: item for key, item in DC.systIDMap.items() if not prog.match(key)
        #     }

        # # remove nuisances if they match the type
        # removetype = [i for i in DC.systs if i[2] in types]
        # DC.systs = [i for i in DC.systs if i[0] not in removetype]
        # DC.systIDMap = {
        #     key: item for key, item in DC.systIDMap.items() if key not in removetype
        # }

        # # Need to resort the systIDMap after the removal (?)
        # DC.systIDMap = {key: [index] for index, key in enumerate(DC.systIDMap)}

        return None

    @staticmethod
    def convert_nuis_type(
        DC: Datacard,
        name: str,
        convert: str,
        process_list=[],
        channel_list=[],
    ) -> None:
        """Convert syst unc. to the type specified in convert

        Args:
            DC (Datacard): _description_
            name (str): _description_
        """

        allowed_conversions = {
            "shape": ["shapeN", "lnN"],
            "lnN": ["shape", "shapeN"],
            "shapeN": ["shape", "lnN"],
        }

        if process_list == []:
            process_list = DC.processes
        if channel_list == []:
            channel_list = DC.bins

        # allowed
        # shape -> lnN
        # shapeN -> lnN
        # lnN -> shape
        # lnN -> shapeN
        # shape -> shapeN

        # DC.shapeMap is:
        # list of [{bin : {process : [input file, path to shape,\
        # path to shape for uncertainty]}}]
        # create a correct shape map

        found = False

        for i_syst, syst in enumerate(DC.systs):
            if syst[0] == name:
                syst_type = DC.systs[i_syst][2]
                if syst_type == convert:
                    print("Nothing to do!\n\n")
                    return
                # if syst_type != "shape":
                #     raise Exception(
                #         "Can only convert a shape to lnN," f"not from {syst_type}"
                #     )
                if convert not in allowed_conversions[syst_type]:
                    raise ValueError(
                        f"Cannot convert nuisance {name} of type {syst_type} "
                        f"into type {convert}, "
                        f"allowed conversions {allowed_conversions}"
                    )
                new_syst_dict = {}
                # found the syst to change
                found = True
                filled = False
                for bin in DC.systs[i_syst][4]:
                    if bin not in channel_list:
                        continue
                    new_syst_dict[bin] = {}
                    shape_keys = list(DC.shapeMap[bin].keys())
                    for sample_name in DC.systs[i_syst][4][bin]:
                        if sample_name not in process_list:
                            continue

                        # skip if it has no impact
                        val = DC.systs[i_syst][4][bin][sample_name]
                        if isinstance(val, float):
                            if ("shape" in syst_type and val == 0.0) or (
                                syst_type == "lnN" and (val == 0.0 or val == 1.0)
                            ):
                                new_syst_dict[bin][sample_name] = 0.0
                                continue
                        if isinstance(val, list):
                            if syst_type == "lnN" and (0.0 in val or 1.0 in val):
                                new_syst_dict[bin][sample_name] = 0.0
                                continue

                        key = -1
                        for shape_key in shape_keys:
                            if fnmatch.fnmatch(sample_name, shape_key):
                                key = shape_key
                                break
                        if key == -1:
                            raise Exception(
                                "Could not find path to shape in root file"
                                f" for sample {sample_name} in bin {bin}"
                            )
                        filename, path_to_nominal, path_to_syst = DC.shapeMap[bin][key]
                        filename = DC.path + filename
                        f = uproot.update(filename)
                        actual_path_to_nominal = path_to_nominal.replace(
                            "$PROCESS", sample_name
                        )

                        if (
                            syst_type == "shape" or syst_type == "shapeN"
                        ) and convert == "lnN":
                            filled = True
                            actual_path_to_syst = path_to_syst.replace(
                                "$PROCESS", sample_name
                            ).replace("$SYSTEMATIC", name)
                            # times val accounts for the fact that shape unc
                            # can be defined as 1, 2, ... N sigma variations.
                            # we convert it to the 1 sigma to lnN
                            nom = np.sum(f[actual_path_to_nominal].values()) * val
                            if nom == 0:
                                new_syst_dict[bin][sample_name] = 0.0
                                continue
                            values = []
                            for tag in ["Down", "Up"]:
                                values.append(
                                    round(
                                        np.sum(
                                            f[f"{actual_path_to_syst}{tag}"].values()
                                        )
                                        / nom,
                                        4,
                                    )
                                )

                            if all(i == 1 for i in values):
                                new_syst_dict[bin][sample_name] = 0.0
                                continue

                            new_syst_dict[bin][sample_name] = values

                        # elif (syst_type == "shape" and convert == "shapeN") or (
                        #     syst_type == "shapeN" and convert == "shape"
                        # ):
                        #     new_syst_dict[bin][sample_name]

                        elif syst_type == "lnN" and (
                            convert == "shape" or convert == "shapeN"
                        ):
                            filled = True
                            actual_path_to_syst = path_to_syst.replace(
                                "$PROCESS", sample_name
                            ).replace("$SYSTEMATIC", name)

                            bins = f[actual_path_to_nominal].axis().edges()
                            nom = f[actual_path_to_nominal].values()
                            # can be a number for symmetric lnN or a list for asymmetric one
                            value = DC.systs[i_syst][4][bin][sample_name]
                            d = {}
                            if isinstance(value, list):
                                # if 0.0 in value or 1.0 in value:
                                #     new_syst_dict[bin][sample_name] = 0.0
                                #     continue
                                d["Down"], d["Up"] = nom * value[0], nom * value[1]
                            elif isinstance(value, float):
                                # if value == 0.0 or value == 1.0:
                                #     new_syst_dict[bin][sample_name] = 0.0
                                #     continue
                                d["Down"], d["Up"] = nom * (1.0 / value), nom * value

                            new_syst_dict[bin][sample_name] = 1.0

                            actual_path_to_syst = path_to_syst.replace(
                                "$PROCESS", sample_name
                            ).replace("$SYSTEMATIC", name)

                            for tag in ["Down", "Up"]:
                                f[f"{actual_path_to_syst}{tag}"] = (d[tag], bins)

                dc_syst_list = list(DC.systs[i_syst])
                dc_syst_list[2] = convert
                if filled:
                    dc_syst_list[4] = new_syst_dict
                DC.systs[i_syst] = dc_syst_list

        if not found:
            raise Exception(f"Could not find syst name {name} to change to lnN!")
        return
