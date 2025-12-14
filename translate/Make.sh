#!/bin/bash

for i in *.txt; do
    python3 translate.py $i
done