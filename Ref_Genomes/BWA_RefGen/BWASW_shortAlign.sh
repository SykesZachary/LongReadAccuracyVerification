#!/bin/bash

for file in $(ls ../../SRS_goodPHRED); do
  bwa bwasw ./BWAIndex/genome.fa /home/sykes/LongReadAccuracyVerification/SRS_goodPHRED/"$file" > \
  SRS_"${file:4:11}"_SW_align.sam
done