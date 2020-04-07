### Script to call bowtie and bowtie2 to align the cleaned FASTQ files
### 31.03.2020

import os
import shutil
import subprocess
import re
from FASTQ_dataParser import data_return

# CHANGE PATH FOR YOUR MACHINE
topLevelPATH = '/home/sykes/LongReadAccuracyVerification/'

sam_file_dest = 'SAM_Files/'
BT2_subPATH = 'Ref_Genomes/BT2_RefGen/'
BT_subPATH = 'Ref_Genomes/BT_RefGen/'
BWA_subPATH = 'Ref_Genomes/BWA_RefGen/'

# Pull and clean FASTQ files to be aligned below
data_return()

# Set PATHs for alignment scripts
bt_alignment_loc = f'{topLevelPATH}{BT_subPATH}'
bt2_alignment_loc = f'{topLevelPATH}{BT2_subPATH}'
bwa_alignment_loc = f'{topLevelPATH}{BWA_subPATH}'

# Change wd and run alignments
os.chdir(bt2_alignment_loc)  # Bowtie 2
subprocess.call('./BT2_shortAlign.sh')
subprocess.call('./BT2_longAlign.sh')

os.chdir(bt_alignment_loc)  # Bowtie
subprocess.call('./BT_shortAlign.sh')
subprocess.call('./BT_longAlign.sh')

os.chdir(bwa_alignment_loc) # BWA MEM and SW
subprocess.call('./BWAMEM_shortAlign.sh')
subprocess.call('./BWAMEM_shortAlign.sh')
subprocess.call('./BWASW_shortAlign.sh')
subprocess.call('./BWASW_longAlign.sh')

# Moving the aligned sam files to specified directory
def sam_output():
    for file in os.listdir(bt2_alignment_loc):
        pattern_shortRead = '^SRS_SRR[0-9]+_BT2_align.sam'
        pattern_longRead = '^LRS_SRR[0-9]+_BT2_align.sam'
        search_string = file
        shortRead_tag = re.match(pattern_shortRead, search_string)
        longRead_tag = re.match(pattern_longRead, search_string)
        if shortRead_tag is not None:
            if file == shortRead_tag.group(0):
                shutil.move(f'{bt2_alignment_loc}{file}',
                            f'{topLevelPATH}{sam_file_dest}{file}')
        if longRead_tag is not None:
            if file == longRead_tag.group(0):
                shutil.move(f'{bt2_alignment_loc}{file}',
                            f'{topLevelPATH}{sam_file_dest}{file}')

    for file in os.listdir(bt_alignment_loc):
        pattern_shortRead = '^SRS_SRR[0-9]+_BT_align.sam'
        pattern_longRead = '^LRS_SRR[0-9]+_BT1_align.sam'
        search_string = file
        shortRead_tag = re.match(pattern_shortRead, search_string)
        longRead_tag = re.match(pattern_longRead, search_string)
        if shortRead_tag is not None:
            if file == shortRead_tag.group(0):
                shutil.move(f'{bt_alignment_loc}{file}',
                            f'{topLevelPATH}{sam_file_dest}{file}')
        if longRead_tag is not None:
            if file == longRead_tag.group(0):
                shutil.move(f'{bt_alignment_loc}{file}',
                            f'{topLevelPATH}{sam_file_dest}{file}')

    for file in os.listdir(bwa_alignment_loc):
        pattern = '^(L|S)RS_SRR[0-9]+_(MEM|SW)_align.sam'
        search_string = file
        BWA_SAM_tag = re.match(pattern, search_string)
        if BWA_SAM_tag is not None and file == BWA_SAM_tag.group(0):
            shutil.move(f'{bwa_alignment_loc}{file}',
                        f'{topLevelPATH}{sam_file_dest}{file}')

    # Return to topLevelPATH
    os.chdir(topLevelPATH)
