# LongReadAccuracyVerification
Using k-mer seeds to compare the accuracy of long read alignments to that of short reads

Requirements:

The experiment within this repository requires the following:
[sra-toolkit](https://github.com/ncbi/sra-tools/wiki/01.-Downloading-SRA-Toolkit), 
[samtools](https://github.com/samtools/samtools), 
[bowtie](http://bowtie-bio.sourceforge.net/tutorial.shtml), 
[bowtie 2](http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml), 
and [bwa](http://bio-bwa.sourceforge.net/bwa.shtml)

The python scripts also require the packages:
[pysam](https://pysam.readthedocs.io/en/latest/index.html), 
[biopython](https://biopython.org/), 
and [pandas](https://pandas.pydata.org/) for the final data output


### VERY IMPOTANT ###
The shell scripts wrapped in the python will not work on Windows. 
So this can only work on Linux or Mac.
