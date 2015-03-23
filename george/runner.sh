#! /bin/bash

rm ./err/* # Flush error logs
rm ./out/* # Flush output logs

bsub -W 6000 -n 4 -o ./out/runner.out.%J -e ./err/runner.err.%J tcsh klazzifiers.sh &


