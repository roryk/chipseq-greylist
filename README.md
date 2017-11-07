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
