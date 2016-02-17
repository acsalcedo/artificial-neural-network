#!/bin/sh

for i in 1 2 3 4 5
do
    echo "Loop $i"
    echo "Training alpha = 0.2"
    python main.py -i datos_P1_RN_EM2016_n2000.txt -n 10 -t 1 -r 0.2
    echo "Training alpha = 0.1"
    python main.py -i datos_P1_RN_EM2016_n2000.txt -n 10 -t 1 -r 0.1
    echo "Training alpha = 0.5"
    python main.py -i datos_P1_RN_EM2016_n2000.txt -n 10 -t 1 -r 0.05
    echo "Training alpha = 0.01"
    python main.py -i datos_P1_RN_EM2016_n2000.txt -n 10 -t 1 -r 0.01
done

echo "DONE WITH FIRST TRAINING"

for i in 1 2 3 4 5
do
    echo "Loop $i"
    echo "Our Training alpha = 0.5"
    python main.py -i generated2000.txt -n 10 -t 1 -r 0.5
    echo "Our Training alpha = 0.3"
    python main.py -i generated2000.txt -n 10 -t 1 -r 0.3
    echo "Our Training alpha = 0.2"
    python main.py -i generated2000.txt -n 10 -t 1 -r 0.2
    echo "Our Training alpha = 0.1"
    python main.py -i generated2000.txt -n 10 -t 1 -r 0.1
    echo "Our Training alpha = 0.05"
    python main.py -i generated2000.txt -n 10 -t 1 -r 0.05
    echo "Our Training alpha = 0.01"
    python main.py -i generated2000.txt -n 10 -t 1 -r 0.01
done
