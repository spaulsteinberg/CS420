# Samuel Steinberg
# March 13th, 2019
# CS420 Project 4 


#!/bin/bash

set -e  # stop script at first error

make -f makefile
declare -i id=1

./GenAlgorithm 20 30 10 0.033 0.6 5 $id #Base case
echo Simulation 1 Complete
id=2
# ------- Testing crossover -------
./GenAlgorithm 20 30 10 0.06 0.6 5 $id
echo Simulation 2 Complete
id=3

./GenAlgorithm 20 30 10 0.1 0.6 5 $id
echo Simulation 3 Complete
id=4

./GenAlgorithm 20 30 10 0.8 0.6 5 $id
echo Simulation 4 Complete
id=5

#----- Testing Mutation ------
./GenAlgorithm 20 30 10 0.033 0.2 5 $id
echo Simulation 5 Complete

id=6
./GenAlgorithm 20 30 10 0.033 0.5 5 $id
echo Simulation 6 Complete
id=7
./GenAlgorithm 20 30 10 0.033 0.8 5 $id
echo Simulation 7 Complete
id=8
#------- Testing Population Size --------
./GenAlgorithm 20 10 10 0.033 0.6 5 $id
echo Simulation 8 Complete
id=9
./GenAlgorithm 20 20 10 0.033 0.6 5 $id
echo Simulation 9 Complete
id=10
./GenAlgorithm 20 40 10 0.033 0.6 5 $id
echo Simulation 10 Complete
id=11
./GenAlgorithm 20 100 10 0.033 0.6 5 $id
echo Simulation 11 Complete
id=12
#-------- Testing Gene Length ----------
./GenAlgorithm 8 30 10 0.033 0.6 5 $id
echo Simulation 12 Complete
id=13
./GenAlgorithm 15 30 10 0.033 0.6 5 $id
echo Simulation 13 Complete
id=14
./GenAlgorithm 30 30 10 0.033 0.6 5 $id
echo Simulation 14 Complete
id=15
#------- Testing Generational Difference
./GenAlgorithm 20 30 5 0.033 0.6 5 $id
echo Simulation 15 Complete
id=16
./GenAlgorithm 20 30 15 0.033 0.6 5 $id
echo Simulation 16 Complete
id=17
./GenAlgorithm 20 30 30 0.033 0.6 5 $id
echo Simulation 17 Complete
