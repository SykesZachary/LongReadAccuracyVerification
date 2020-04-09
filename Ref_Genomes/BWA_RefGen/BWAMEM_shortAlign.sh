#!/bin/bash

for file in $(ls ../../SRS_goodPHRED); do
  bwa mem ./BWAIndex/genome.fa /home/sykes/LongReadAccuracyVerification/SRS_goodPHRED/"$file" > \
  SRS_"${file:4:11}"_MEM_align.sam
done