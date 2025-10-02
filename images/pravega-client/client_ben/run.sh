#!/bin/bash

SECURE="UNSECURE"

mkdir results
echo "Test_Case,Tool,Time,Messages" >> results/times.csv

while IFS="," read -r Test_Case Production_Rate Environment Payload Size Messages Time
do
    echo -e "Executing $Test_Case in OMB"
    python3 config_omb.py $Test_Case $Production_Rate $Payload $Size > workload_var.yaml
    cd omb
    for i in {1..10}
    do
        echo "\tExecuting $i for $Test_Case in OMB"
        START_TIME=$(date +%s)
        ./bin/benchmark ../workload_var.yaml --drivers ./dell/driver.yaml > output.txt
        END_TIME=$(date +%s)
        EXECUTION_TIME=$((END_TIME - START_TIME - 60))
        result_file=$(ls *.json)
        echo -e "\tGet Messages Sent"
        MESSAGES=$(python3 ../messages.py $result_file)
        
        echo -e "\tMove config file to ../results/$Test_Case-$i-OMB-$SECURE.yaml"
        mv ../workload_var.yaml "../results/$Test_Case-$i-OMB-$SECURE.yaml"
        echo -e "\tMove result file to ../results/$Test_Case-$i-OMB-$SECURE.json"
        mv $result_file "../results/$Test_Case-$i-OMB-$SECURE.json"
        echo "$Test_Case,OMB,$EXECUTION_TIME,$MESSAGES" >> ../results/times.csv
    done
    cd ../
    
    sleep 60
done < <(tail -n +2 test_case.csv)

