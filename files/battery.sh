#!/bin/bash

dir=/home/surv/Documents/battery.txt

echo "time" >> $dir
date >> $dir

echo "battery" >> $dir
acpi >> $dir

echo "" >> $dir
