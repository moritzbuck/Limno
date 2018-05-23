
DIR=$HOME/people/0010_Pauline
cd
cd $DIR

QSCRIPT="sbatch -D $DIR -A snic2017-7-173 -t 5-00:00:00 -n 20 -p node --mail-user murumbii@gmail.com --mail-type=ALL"

all_samples=`find 0000_raws/0100_reads/* -type "d" | grep -v FASTQ | rev | cut -f1 -d"/" | rev | sed 's/^/1000_processed_reads\//' | sed 's/$/\/done/' `
snakemake  --cores 16 $all_samples
all_single_asses=`find 0000_raws/0100_reads/* -type "d" | grep -v FASTQ | rev | cut -f1 -d"/" | rev | sed 's/^/1000_processed_reads\//' | sed 's/$/\/assemblies\/megahit\/data/'`
snakemake  --cluster "$QSCRIPT" --jobs 500 --cores 20 $all_single_asses
snakemake  --cluster "$QSCRIPT" --jobs 500 --cores 20
