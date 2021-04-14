max=1
for i in `seq 1 $max`
do
    bash submitCondorJob.sh  $i
done
