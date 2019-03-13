# Samuel Steinberg
# March 13th, 2019
# CS420 Project 4 


#!/bin/bash

set -e  # stop script at first error

make -f makefile

./GenAlgorithm 20 30 10 0.033 0.6 5

echo Simulation Complete
