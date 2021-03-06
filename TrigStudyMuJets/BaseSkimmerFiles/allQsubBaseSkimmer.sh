#!/bin/bash


echo " "
counter=1
setERA=$3
#ERA_ARRAY=("17B" "17C" "17DEF")
for f in ${1}*; do
#for setERA in ${ERA_ARRAY[*]};do
# SUBSTRING=$(echo $f| cut -d'/' -f 10); 
logDESCRIPTOR=${2}${setERA}_${counter}

if [[ $f == *".root" ]]; then
echo " "
echo "qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=$f,ERA=${setERA} runBaseSkim.sh"
sleep 1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=$f,ERA=${setERA} runBaseSkim.sh

#done

# sleep 5

((counter++))
fi
done