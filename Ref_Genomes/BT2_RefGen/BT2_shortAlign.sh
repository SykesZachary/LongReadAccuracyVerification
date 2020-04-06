#!/bin/bash

for file in $(ls ../../SRS_goodPHRED); do
  # Change these PATHs to reflect your own system
  /home/sykes/bowtie2-2.4.1-linux-x86_64/bowtie2 -p 4 -t -x \
   GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.bowtie_index -U \
  /home/sykes/LongReadAccuracyVerification/SRS_goodPHRED/"$file" \
  -S SRS_"${file:4:11}"_BT2_align.sam
done