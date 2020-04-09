#!/bin/bash

for file in $(ls ../../LRS_goodPHRED); do
  bwa mem ./BWAIndex/genome.fa /home/sykes/LongReadAccuracyVerification/LRS_goodPHRED/"$file" > \
  LRS_"${file:4:11}"_MEM_align.sam
done