#!/bin/bash

conda create -n graphaf python=3.7
conda activate graphaf

conda install pytorch==1.6.0 torchvision==0.7.0 cudatoolkit=10.1 -c pytorch
conda install -c conda-forge rdkit
pip install texttable tdqm cairosvg networkx notebook
