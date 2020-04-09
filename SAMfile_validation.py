### Using pysam to pull necessary data from sam files
### 01.04.2020

import os
import subprocess
import re
import shutil
import pysam
import pandas as pd

# from SeqAligner import sam_output

# CHANGE PATH FOR YOUR MACHINE
topLevelPATH = '/home/sykes/LongReadAccuracyVerification/'
SAM_files_loc = 'SAM_Files/'
BAM_files_loc = 'Sorted_BAM_BAI_Files'

# Ensures in top directory
if os.getcwd() is not topLevelPATH:
    os.chdir(topLevelPATH)

# Align cleaned FASTQ files with bowtie 1, bowtie 2, bwa mem, and bwa sw for analysis
# sam_output()

# Creating dir to eventually move BAM files
if os.path.isdir(f'{topLevelPATH}Sorted_BAM_BAI_Files/') is not True:
    os.mkdir(f'{topLevelPATH}Sorted_BAM_BAI_Files/')

# Change dir to SAM file location
# and converts SAM into sorted BAM
os.chdir(f'{topLevelPATH}{SAM_files_loc}')
subprocess.call('./SAM_to_BAM.sh')

# Moves sorted BAM to ./Sorted_BAM_BAI_Files/
for file in os.listdir(f'{topLevelPATH}{SAM_files_loc}'):

    pattern = '.*(.bam)'
    search_string = file
    BAM_tag = re.match(pattern, search_string)

    if BAM_tag is not None and BAM_tag.group(0) in file:
        shutil.move(f'{topLevelPATH}{SAM_files_loc}{file}',
                    f'{topLevelPATH}Sorted_BAM_BAI_Files/{file}')

# Indexes Sorted BAM files
os.chdir(f'{topLevelPATH}{BAM_files_loc}')
subprocess.call('./bam_indexing.sh')

df_values = {
    'SRR File Name': [],
    'SRS/LRS': [],
    'Alignment Software': [],
    'Mapped Reads': [],
    'Average Mapping Quality': [],
    'Map Qualities Above phred20': []
}


for file in os.listdir(f'{topLevelPATH}{BAM_files_loc}'):
    total_qual_vals = 0
    count = 0
    count_abv20 = 0
    pattern = '.*(.bam)$'
    search_string = file
    BAM_tag = re.match(pattern, search_string)

    if BAM_tag is not None and BAM_tag.group(0) in file:
        df_values['SRR File Name'].append(file[4:15])
        df_values['SRS/LRS'].append(file[0:3])

        if file[16:19] == 'BT2':
            df_values['Alignment Software'].append('Bowtie 2')
        elif file[16:19] == 'MEM':
            df_values['Alignment Software'].append('BWA-MEM')
        elif file[16:18] == 'SW':
            df_values['Alignment Software'].append('BWA-SW')
        else:
            df_values['Alignment Software'].append('Bowtie')

        opened_bam = pysam.AlignmentFile(file, 'rb', check_sq=False)  # bam file read in by pysam

        for read in opened_bam.fetch():
            count += 1
            total_qual_vals += read.mapping_quality
            if read.mapping_quality >= 20:
                count_abv20 += 1
        if count > 0:
            df_values['Mapped Reads'].append(count)
            df_values['Average Mapping Quality'].append(total_qual_vals / count)
            df_values['Map Qualities Above phred20'].append(count_abv20)
        else:
            df_values['Mapped Reads'].append('NA')
            df_values['Average Mapping Quality'].append('NA')
            df_values['Map Qualities Above phred20'].append('NA')

final_data_report = pd.DataFrame(data=df_values)
final_data_report.to_csv(f'{topLevelPATH}LongReadAccuracy_FinalDataReport.csv')
print('\n', final_data_report)
