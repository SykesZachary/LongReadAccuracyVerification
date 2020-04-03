### Script to parse reads from SRR files
### 17.03.2020

import os
import gzip
import shutil
import re
from Bio import SeqIO
from SRR_AccUnpacker import unpack_fastq

# CHANGE PATH FOR YOUR MACHINE
topLevelPATH = '/home/sykes/LongReadAccuracyVerification/'

SRRshort_initial_loc = 'SRRshortReads_Files_GZ/'
SRRlong_initial_loc = 'SRRlongReads_Files_GZ/'
Unzip_SRRshort_dest = 'SRRshortReads_Files_Unzipped/'
Unzip_SRRlong_dest = 'SRRlongReads_Files_Unzipped/'
FinalShort_goodPHRED_dest = 'SRS_goodPHRED/'
FinalLong_goodPHRED_dest = 'LRS_goodPHRED/'


def data_return():
    # loads in our fastq files from accessions using fastq-dump in bash
    unpack_fastq()

    # Change back to correct PATH if not already in
    if os.getcwd() is not topLevelPATH:
        os.chdir(topLevelPATH)

    # UNZIP THE .GZ FILES HERE
    for file in os.listdir(SRRshort_initial_loc):  # Short Reads
        # Regex to build file_out name
        pattern = '^SRR[0-9]+'
        search_string = file
        SRR_tag = re.match(pattern, search_string)
        # print(SRR_tag.group(0)) # Output test
        if SRR_tag is not None:
            with gzip.open(f'{SRRshort_initial_loc}{file}', 'rb') as file_in, \
                    open(f'{Unzip_SRRshort_dest}{SRR_tag.group(0)}_shortRead.fastq', 'wb') as file_out:
                shutil.copyfileobj(file_in, file_out)

    for file in os.listdir(SRRlong_initial_loc):
        pattern = '^SRR[0-9]+'
        search_string = file
        SRR_tag = re.match(pattern, search_string)
        if SRR_tag is not None:
            with gzip.open(f'{SRRlong_initial_loc}{file}', 'rb') as file_in, \
                    open(f'{Unzip_SRRlong_dest}{SRR_tag.group(0)}_longRead.fastq', 'wb') as file_out:
                shutil.copyfileobj(file_in, file_out)

    # Returns avg read length for the FASTQ files
    for file in os.listdir('SRRshortReads_Files_Unzipped'):
        total_bp = 0
        count = 0
        for read in SeqIO.parse(f'{Unzip_SRRshort_dest}{file}', 'fastq'):
            total_bp += len(read)
            count += 1
        avg_readLen = int(total_bp / count)
        print(file, 'contains', count,
              'reads with an avg len of', avg_readLen)

    for file in os.listdir('SRRlongReads_Files_Unzipped'):
        total_bp = 0
        count = 0
        for read in SeqIO.parse(f'{Unzip_SRRlong_dest}{file}', 'fastq'):
            total_bp += len(read)
            count += 1
        avg_readLen = int(total_bp / count)
        print(file, 'contains', count,
              'reads with an avg len of', avg_readLen)

    # REMOVE READS WITH PHRED SCORE < 20 HERE
    good_shortReads = []
    good_longReads = []
    count_short = 0
    count_long = 0

    for file in os.listdir(Unzip_SRRshort_dest):
        pattern = '^SRR[0-9]+'
        search_string = file
        SRR_tag = re.match(pattern, search_string)
        for read in SeqIO.parse(f'{Unzip_SRRshort_dest}{file}', 'fastq'):
            if min(read.letter_annotations['phred_quality']) >= 20:
                good_shortReads.append(read)
        count_short = SeqIO.write(good_shortReads,
                                  f'SRS_{SRR_tag.group(0)}_goodPHRED.fastq', 'fastq')  # SRS = Short reads
        goodPHRED_file = f'SRS_{SRR_tag.group(0)}_goodPHRED.fastq'
        print('Saved', count_short, 'short reads from',
              SRR_tag.group(0), 'with PHRED score >= 20')
        shutil.move(f'{os.getcwd()}/{goodPHRED_file}', f'{FinalShort_goodPHRED_dest}/{goodPHRED_file}')
        good_shortReads.clear()

    for file in os.listdir(Unzip_SRRlong_dest):
        pattern = '^SRR[0-9]+'
        search_string = file
        SRR_tag = re.match(pattern, search_string)
        for read in SeqIO.parse(f'{Unzip_SRRlong_dest}{file}', 'fastq'):
            # print(read.letter_annotations['phred_quality'])
            if min(read.letter_annotations['phred_quality']) >= 20:
                good_longReads.append(read)
        count_long = SeqIO.write(good_longReads,
                                 f'LRS_{SRR_tag.group(0)}_goodPHRED.fastq', 'fastq')  # LRS = Long Reads
        goodPHRED_file = f'LRS_{SRR_tag.group(0)}_goodPHRED.fastq'
        print('Saved', count_long, 'long reads from',
              SRR_tag.group(0), 'with PHRED score >= 20')
        shutil.move(f'{os.getcwd()}/{goodPHRED_file}', f'{FinalLong_goodPHRED_dest}/{goodPHRED_file}')
        good_longReads.clear()

