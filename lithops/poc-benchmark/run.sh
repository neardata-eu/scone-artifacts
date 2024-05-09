#!/bin/bash

. /python/env.sh 

BENCH=${1:=simpler}

python3 /python/benchmark.py $BENCH 2>&1 |tee exe_bench_$BENCH.out

