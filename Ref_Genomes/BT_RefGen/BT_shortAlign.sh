#!/bin/bash

for file in $(ls ../../SRS_goodPHRED); do
  # Change these PATHs to reflect your own system
  /home/sykes/bowtie-1.2.3-linux-x86_64/bowtie -t GCA_000001405.15_GRCh38_no_alt_analysis_set \
  /home/sykes/LongReadAccuracyVerification/SRS_goodPHRED/"$file" \
  --sam-nohead SRS_"${file:4:11}"_BT1_align.sam
done