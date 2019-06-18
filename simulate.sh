#!/bin/bash

set -eux
DOCKER_CMD="docker run -t --rm  -v $PWD:/data/ vericocotb bash -c "
COMMON_ARGS="PYTHONDONTWRITEBYTECODE=1 COCOTB_REDUCED_LOG_FMT=true RANDOM_SEED=123"
VERI_ARGS="SIM=verilator VERILATOR_TRACE=1 CMD=/build/env/bin/verilator $COMMON_ARGS"
ICARUS_ARGS="SIM=icarus $COMMON_ARGS"

LOG_TO_FILE="2>&1 | tee "

docker build -f dockerfiles/Dockerfile.verilator -t vericocotb .

function run_verilator {
    OUTPUT=results/$1/verilator/
    mkdir -p $OUTPUT
    $DOCKER_CMD ". ./env/bin/activate && \
                 make -C cocotb/examples/$1/tests $VERI_ARGS \
                 $LOG_TO_FILE /data/$OUTPUT/console.log && \
                 cp cocotb/examples/$1/tests/*.vcd /data/$OUTPUT/dump.vcd"
}

function run_icarus {
    OUTPUT=results/$1/icarus/
    mkdir -p $OUTPUT
    $DOCKER_CMD ". ./env/bin/activate && \
                 make -C cocotb/examples/$1/tests $ICARUS_ARGS \
                 $LOG_TO_FILE /data/$OUTPUT/console.log && \
                 cp cocotb/examples/$1/tests/*.vcd /data/$OUTPUT/dump.vcd"
}

set +e

for TEST in adder axi_lite_slave dff # endian_swapper Makefile mean mixed_language ping_tun_tap
do
    run_verilator $TEST
    run_icarus $TEST
    python3 compare.py $TEST
done


