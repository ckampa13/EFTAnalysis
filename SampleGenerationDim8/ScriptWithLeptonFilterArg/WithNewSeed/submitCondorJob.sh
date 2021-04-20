#!/bin/bash
echo $PWD

echo ${1} 

cat>Job_${1}.sh<<EOF
#!/bin/bash
tar -xf CMSSW_10_2_22.tar.gz
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc820 
cd CMSSW_10_2_22/src
scramv1 b ProjectRename
cmsenv
export SCRAM_ARCH="slc7_amd64_gcc820";
scramv1 b
cd -
sh triboson_production.sh -p pileup_files.txt -s WWZ_ScaleST -c -o $PWD -a ${1} -n 10 -l DileptonFilter -b \${2}\${3}
EOF

chmod 775 Job_${1}.sh


cat>condor_${1}.jdl<<EOF
universe = vanilla
Executable = Job_${1}.sh
Arguments = \${1} \$(Cluster) \$(Process)
Requirements = OpSys == "LINUX" && (Arch != "DUMMY" )
request_disk = 10000000
request_memory = 4000
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
transfer_input_files = Job_${1}.sh, triboson_production.sh, pileup_files.txt, CMSSW_10_2_22.tar.gz 
notification = Never
Output = CondorJobs/STDOUT_\$(Cluster)\$(Process)${1}.stdout
Error = CondorJobs/STDERR_\$(Cluster)\$(Process)${1}.stderr
Log = CondorJobs/LOG_\$(Cluster)\$(Process)${1}.log
x509userproxy = ${X509_USER_PROXY}
Queue 1
EOF

condor_submit condor_${1}.jdl
