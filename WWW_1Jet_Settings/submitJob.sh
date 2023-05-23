max=100

for i in `seq 1 $max`
do
    bash submitCondorJob.sh $i 10 20 run
    bash submitCondorJob.sh $i 10 25 run
    bash submitCondorJob.sh $i 10 30 run
    bash submitCondorJob.sh $i 10 35 run
    bash submitCondorJob.sh $i 15 25 run
    bash submitCondorJob.sh $i 15 30 run
    bash submitCondorJob.sh $i 15 35 run
    bash submitCondorJob.sh $i 15 40 run
    bash submitCondorJob.sh $i 20 30 run
    bash submitCondorJob.sh $i 20 35 run
    bash submitCondorJob.sh $i 20 40 run
    bash submitCondorJob.sh $i 20 45 run
#    bash submitCondorJob.sh $i 25 35 run
#    bash submitCondorJob.sh $i 25 40 run
#    bash submitCondorJob.sh $i 25 45 run
#    bash submitCondorJob.sh $i 25 50 run
#    bash submitCondorJob.sh $i 30 40 run
#    bash submitCondorJob.sh $i 30 45 run
#    bash submitCondorJob.sh $i 30 50 run
#    bash submitCondorJob.sh $i 30 55 run
#    bash submitCondorJob.sh $i 35 45 run
#    bash submitCondorJob.sh $i 35 50 run
#    bash submitCondorJob.sh $i 35 55 run
#    bash submitCondorJob.sh $i 35 60 run
#    bash submitCondorJob.sh $i 40 50 run
#    bash submitCondorJob.sh $i 40 55 run
#    bash submitCondorJob.sh $i 40 60 run
#    bash submitCondorJob.sh $i 40 65 run
#    bash submitCondorJob.sh $i 45 55 run
#    bash submitCondorJob.sh $i 45 60 run
#    bash submitCondorJob.sh $i 45 65 run
#    bash submitCondorJob.sh $i 45 70 run
#    bash submitCondorJob.sh $i 50 60 run
#    bash submitCondorJob.sh $i 50 65 run
#    bash submitCondorJob.sh $i 50 70 run
#    bash submitCondorJob.sh $i 50 75 run
done
