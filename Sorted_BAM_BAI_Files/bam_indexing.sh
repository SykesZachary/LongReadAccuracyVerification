#!/bin/bash

SKIP="bam_indexing.sh"

for file in $(ls); do
	if [ "$file" != $SKIP ]; then
	    samtools index "$file"
	fi
done
