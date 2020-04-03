### Script to wrap two bash scripts for dumping FASTQ files
### 26.03.2020

import subprocess
import os

# CHANGE PATH FOR YOUR MACHINE
topLevelPATH = '/home/sykes/LongReadAccuracyVerification/'
shortRead_GZ_loc = f'{topLevelPATH}SRRshortReads_Files_GZ/'
longRead_GZ_loc = f'{topLevelPATH}SRRlongReads_Files_GZ/'


def unpack_fastq():
    # This wraps the shell script below
    os.chdir(shortRead_GZ_loc)
    subprocess.call('./srr_unpacker_shortReads.sh')
    os.chdir(longRead_GZ_loc)
    subprocess.call('./srr_unpacker_longReads.sh')

    shortRead_dir = os.listdir(f'{topLevelPATH}SRRshortReads_Files_GZ')
    longRead_dir = os.listdir(f'{topLevelPATH}SRRlongReads_Files_GZ')

    if len(shortRead_dir) != 0:
        print('Short read fastq files pulled successfully')

    if len(longRead_dir) != 0:
        print('Long read fastq files pulled successfully')

    # Return to topLevelPATH
    os.chdir(topLevelPATH)