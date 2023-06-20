#!/bin/bash
echo $PWD

echo ${1} 

# this is used for transfer the out put, should be consistant with the output name in the triboson_production.sh
#SAMPLE=WWW
SAMPLE=WWW_Dim6_cW_cHd_cHWB_cHW_4F
CAMPAIGN=RunIISummer20UL18
NPART=${1}
STEP5_NAME=${SAMPLE}-${CAMPAIGN}MiniAODv2_${NPART}.root
STEP6_NAME=${SAMPLE}-${CAMPAIGN}NanoAODv9_${NPART}.root

OUTPUTDIR=$PWD

LogDir=CondorJobs
[ -d $LogDir ] || mkdir ${LogDir};


Nevents=1000
   
# if run on the cmsplc, can not use remap, use -f options here to copy the file
cat>Job_${1}.sh<<EOF
#!/bin/bash
sh triboson_production.sh -p pileup_files.txt -s ${SAMPLE} -c -o $PWD -a ${1} -n ${Nevents} -b \${2}\${3} -l DileptonFilter -f
EOF

chmod 775 Job_${1}.sh

# x509up_u100637, ${X509_USER_PROXY} doesn't work on cms connect 

cat>condor_${1}.jdl<<EOF
universe = vanilla
Executable = Job_${1}.sh
Arguments = ${1} \$(Cluster) \$(Process)
Requirements = OpSys == "LINUX" && (Arch != "DUMMY" )
request_disk = 10000000
request_memory = 6000
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
transfer_input_files = Job_${1}.sh, triboson_production.sh, pileup_files.txt
notification = Never
Output = ${LogDir}/STDOUT_\$(Cluster)\$(Process)${1}.stdout
Error = ${LogDir}/STDERR_\$(Cluster)\$(Process)${1}.stderr
Log = ${LogDir}/LOG_\$(Cluster)\$(Process)${1}.log
x509userproxy = ${X509_USER_PROXY}
+MaxRuntime           = 86400
Queue 1
EOF

if [ "${2}" = "run" ]; then
   condor_submit condor_${1}.jdl
   echo "submit condor job"
else
   echo 'dry run'
fi
#condor_submit condor_${1}.jdl
