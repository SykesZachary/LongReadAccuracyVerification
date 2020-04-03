### Using pysam to pull necessary data from sam files
### 01.04.2020

import os
import subprocess
import re
import shutil
import pysam

# from Bowtie_seqAligner import sam_output

# CHANGE PATH FOR YOUR MACHINE
topLevelPATH = '/home/sykes/LongReadAccuracyVerification/'
SAM_files_loc = 'SAM_Files/'

# Ensures in top directory
if os.getcwd() is not topLevelPATH:
    os.chdir(topLevelPATH)

# Align cleaned FASTQ files with bowtie 1 and 2 for analysis
# sam_output()

# Creating dir to eventually move BAM files
if os.path.isdir(f'{topLevelPATH}Converted_BAM_Files/') is not True:
    os.mkdir(f'{topLevelPATH}Converted_BAM_Files/')

# Change dir to SAM file location
os.chdir(f'{topLevelPATH}{SAM_files_loc}')
subprocess.call('./SAM_to_BAM.sh')

for file in os.listdir(f'{topLevelPATH}{SAM_files_loc}'):
    pattern = '.*(.bam)'
    search_string = file
    BAM_tag = re.match(pattern, search_string)

    if BAM_tag is not None:
        if BAM_tag.group(0) in file:
            shutil.move(f'{topLevelPATH}{SAM_files_loc}{file}',
                        f'{topLevelPATH}Converted_BAM_Files/{file}')

