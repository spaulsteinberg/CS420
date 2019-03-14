# Samuel Steinberg
# March 13th, 2019
# CS420 Project 4 


#!/bin/bash

set -e  # stop script at first error

make -f makefile

./GenAlgorithm 20 30 10 0.033 0.6 5 #Base case
echo Simulation 1 Complete

# ------- Testing crossover -------
./GenAlgorithm 20 30 10 0.06 0.6 5
echo Simulation 2 Complete

./GenAlgorithm 20 30 10 0.1 0.6 5
echo Simulation 3 Complete

./GenAlgorithm 20 30 10 0.8 0.6 5
echo Simulation 4 Complete

#----- Testing Mutation ------
./GenAlgorithm 20 30 10 0.033 0.2 5
echo Simulation 5 Complete

./GenAlgorithm 20 30 10 0.033 0.5 5
echo Simulation 6 Complete

./GenAlgorithm 20 30 10 0.033 0.8 5
echo Simulation 7 Complete

#------- Testing Population Size --------
./GenAlgorithm 20 10 10 0.033 0.6 5
echo Simulation 8 Complete

./GenAlgorithm 20 20 10 0.033 0.6 5
echo Simulation 9 Complete

./GenAlgorithm 20 40 10 0.033 0.6 5
echo Simulation 10 Complete

./GenAlgorithm 20 100 10 0.033 0.6 5
echo Simulation 11 Complete

#-------- Testing Gene Length ----------
./GenAlgorithm 8 30 10 0.033 0.6 5
echo Simulation 12 Complete

./GenAlgorithm 15 30 10 0.033 0.6 5
echo Simulation 13 Complete

./GenAlgorithm 30 30 10 0.033 0.6 5
echo Simulation 14 Complete

#------- Testing Generational Difference
./GenAlgorithm 20 30 5 0.033 0.6 5
echo Simulation 15 Complete

./GenAlgorithm 20 30 15 0.033 0.6 5
echo Simulation 16 Complete

./GenAlgorithm 20 30 30 0.033 0.6 5
echo Simulation 17 Complete
