#!/bin/bash

set -eux
DOCKER_CMD="docker run -t --rm  -v $PWD:/data/ vericocotb bash -c "
COMMON_ARGS="PYTHONDONTWRITEBYTECODE=1 COCOTB_REDUCED_LOG_FMT=true"
VERI_ARGS="SIM=verilator VERILATOR_TRACE=1 CMD=/build/env/bin/verilator $COMMON_ARGS"
ICARUS_ARGS="SIM=icarus $COMMON_ARGS"

LOG_TO_FILE="2>&1 | tee "

docker build -f dockerfiles/Dockerfile.verilator -t vericocotb .

function run_verilator {
    OUTPUT=tests/$1/verilator/
    mkdir -p $OUTPUT
    $DOCKER_CMD ". ./env/bin/activate && \
                 make -C cocotb/examples/$1/tests $VERI_ARGS \
                 $LOG_TO_FILE /data/$OUTPUT/console.log && \
                 cp cocotb/examples/$1/tests/dump.vcd /data/$OUTPUT/dump.vcd"
}

function run_icarus {
    OUTPUT=tests/$1/icarus/
    mkdir -p tests/$1/icarus/
    $DOCKER_CMD ". ./env/bin/activate && \
                 make -C cocotb/examples/$1/tests $ICARUS_ARGS \
                 $LOG_TO_FILE /data/$OUTPUT/console.log && \
                 cp cocotb/examples/$1/tests/dump.vcd /data/$OUTPUT/dump.vcd"
}

run_verilator adder
run_icarus adder


