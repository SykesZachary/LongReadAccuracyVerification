#!/bin/bash

for SRR in $(cat SRR_longReads_AccList.txt); do
  # -X 20000 added to limit the amount of reads dumped for testing
  # Organism: H.sapien
  fastq-dump -X 20000 --split-files --gzip -I -O \
  "/home/sykes/LongReadAccuracyVerification/SRRlongReads_Files_GZ/" $SRR
done

