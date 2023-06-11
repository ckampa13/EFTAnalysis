#!/bin/bash
echo $PWD

echo ${1} 
echo ${2} 
echo ${3} 

# this is used for transfer the out put, should be consistant with the output name in the qcut.sh
SAMPLE=WW_2Jets
CAMPAIGN=RunIISummer20UL18
NPART=${1}
XQCUT=${2}
QCUT=${3}

OUTPUTDIR=$PWD

LogDir=CondorJobs
[ -d $LogDir ] || mkdir ${LogDir};


Nevents=1000
   
# if run on the cmsplc, can not use remap, use -f options here to copy the file
cat>Job_${1}_xqcut${2}_qcut${3}.sh<<EOF
#!/bin/bash
sh qcut.sh -s ${SAMPLE} -c -o $PWD -a ${1} -n ${Nevents} -b \${2}\${3} -x ${2} -q ${3} -l NoFilter -f 
EOF

chmod 775 Job_${1}_xqcut${2}_qcut${3}.sh

# x509up_u100637, ${X509_USER_PROXY} doesn't work on cms connect 

cat>condor_${1}_xqcut${2}_qcut${3}.jdl<<EOF
universe = vanilla
Executable = Job_${1}_xqcut${2}_qcut${3}.sh
Arguments = ${1} \$(Cluster) \$(Process)
Requirements = OpSys == "LINUX" && (Arch != "DUMMY" )
request_disk = 10000000
request_memory = 6000
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
transfer_input_files = Job_${1}_xqcut${2}_qcut${3}.sh, qcut.sh
notification = Never
Output = ${LogDir}/STDOUT_\$(Cluster)\$(Process)${1}_xqcut${2}_qcut${3}.stdout
Error = ${LogDir}/STDERR_\$(Cluster)\$(Process)${1}_xqcut${2}_qcut${3}.stderr
Log = ${LogDir}/LOG_\$(Cluster)\$(Process)${1}_xqcut${2}_qcut${3}.log
x509userproxy = ${X509_USER_PROXY}
+MaxRuntime           = 86400
Queue 1
EOF

if [ "${4}" = "run" ]; then
   condor_submit condor_${1}_xqcut${2}_qcut${3}.jdl
   echo "submit condor job"
else
   echo 'dry run'
fi
#condor_submit condor_${1}.jdl
