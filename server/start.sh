#!/bin/bash

screen -S DistributionStream -d -m python3 DistributionStream.py $(pwd)

sleep 1

screen -S wsInterface -d -m python3 Interfaces/wsInterface.py $(pwd)
screen -S serialInterface -d -m python3 Interfaces/serialInterface.py $(pwd)
#screen -S cliInterface -d -m python3 Interfaces/cliInterface.py $(pwd)
