### Script to parse reads from SRR files
### 17.03.2020

import os
import gzip
import shutil
import re
from Bio import SeqIO
from KMer_counter import kmer_read_counter

SRR_initial_loc = 'SRR_Files_GZ/'
Unzip_SRR_dest = 'SRR_Files_Unzipped/'

# UNZIP THE .GZ FILES HERE
for file in os.listdir(SRR_initial_loc):  # This will need to be modified for multiple .gz files within the dir (regex)
    # Regex to build file_out name
    pattern = '^SRR[0-9]+'
    search_string = file
    SRR_tag = re.match(pattern, search_string)
    # print(SRR_tag.group(0)) # Output test
    with gzip.open(f'{SRR_initial_loc}{file}', 'rb') as file_in, open(f'{Unzip_SRR_dest}{SRR_tag.group(0)}.fastq',
                                                                      'wb') as file_out:
        shutil.copyfileobj(file_in, file_out)

# print(os.listdir(SRR_initial_loc)) # Output test

# COUNT TOTAL NUMBER OF READS IN FASTQ HERE
count = 0
read_lst = []
for file in os.listdir(Unzip_SRR_dest):
    for read in SeqIO.parse(f'{Unzip_SRR_dest}{file}', 'fastq'):
        read_lst.append(read)
        count += 1

# Determine average read length from fastq file here
print('%i reads' % count)

# REMOVE READS WITH PHRED SCORE < 20 HERE
good_reads = []
for file in os.listdir(Unzip_SRR_dest):
    pattern = '^SRR[0-9]+' # Start RegEx
    search_string = file
    SRR_tag = re.match(pattern, search_string) # End RegEx
    for read in SeqIO.parse(f'{Unzip_SRR_dest}{file}', 'fastq'):
        if min(read.letter_annotations['phred_quality']) >= 20:
            good_reads.append(read)
    count = SeqIO.write(good_reads, f'{SRR_tag.group(0)}_goodPHREDscores.fastq', 'fastq')
print('Saved %i reads with PHRED score >= 20' % count)

quality_seq = []
for seq in good_reads:
    seq_data = str(seq.seq)
    quality_seq.append(seq_data)

print(quality_seq) # Output test
# print(type(quality_seq[0])) # Output test

iteration = 1
for seq in quality_seq:
    read_names = ['SRR020192_read', str(iteration)] # Implement regex here too for read_names[0]
    kmer_read_counter(seq, 9, ''.join(read_names), ''.join(read_names))
    iteration += 1
