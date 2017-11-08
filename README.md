Python implementation of the GreyListChIP Bioconductor package.

For a ChIP-seq experiment with a paired input and ChIP sample, this will
calculate a greylist for peaks from the input for that particular pair. These
are questionable peaks for this particular input-ChIP pair.

The reason for doing this is that peak callers can sometimes have trouble in
high depth input regions even though the caller adjusts for the reads in the
input lane. It is standard practice to use the ENCODE blacklist regions for
commonly problematic regions but there can be additional, sample-specific high
depth input regions that are not covered by the blacklist regions.  This flags
peaks that falls into those sample-specific high input regions as questionable.

This implementation improves on the R implementation by not needing a separate
genome file and being easily runnable on the command line. It contains no
original ideas. 

https://bioconductor.org/packages/release/bioc/html/GreyListChIP.html is
the source of the idea and the algorithm.

## usage
Run chipseq-greylist on your **input BAM** file for each input-ChIP pair:

```bash
chipseq-greylist bamfile
```

this will produce a few files:

* **bamfile-input-greystats.csv**: bootstrapped negative binomial parameters and estimated threshold
* **bamfile-input-greydepth.tsv**: sambamba windowed depth
* **bamfile-input-grey.bed**: BED file of greylist regions exceeding coverage threshold in the input file

You can now filter out/annotate peaks falling in the greylist regions by interesecting the peaks with
the greylist file. For example:

```bash
bedtools intersect -wao -a bamfile-peaks.bed -b bamfile-input-grey.bed > bamfile-peaks-greylist-annotated.bed
```
