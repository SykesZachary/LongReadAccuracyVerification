#!/bin/bash

SKIP="SAM_to_BAM.sh"

for file in $(ls "$PWD"); do
  if [ "${file:18:1}" == 2 ]; then
    samtools view -S -b "$file" > "${file:0:25}".bam
  elif [ "$file" == "$SKIP" ]; then
    continue
  elif [ "${file:18}" != 2 ]; then
    samtools view -S -b "$file" > "${file:0:24}".bam
  fi
done