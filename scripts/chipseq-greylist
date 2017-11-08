import subprocess
import os

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.discrete.discrete_model import NegativeBinomial as NB
import statsmodels.api as sm
from argparse import ArgumentParser

def load_sambamba_depth(filename):
    return pd.read_csv(filename, sep="\t")

def sample_counts(df, n=30000):
    return df.sample(n)["readCount"]

def estimate_nb_parameters(depth):
    counts = sample_counts(depth)
    x = list(counts)
    y = np.ones(len(counts))
    loglike_method = "nb1"
    fit = NB(x, y, loglike_method=loglike_method).fit(start_params=[0.1, 0.1])
    if loglike_method == 'nb1':
        Q = 1
    elif loglike_method == 'nb2':
        Q = 0
    mu = np.exp(fit.params[0])
    alpha = fit.params[1]
    size = 1. / alpha * mu**Q
    prob = size / (size + mu)
    return {"size": size, "prob": prob}

def estimate_threshold(depth, nreps=100, cutoff=0.99):
    parameters = [estimate_nb_parameters(depth) for x in range(nreps)]
    sizes = [x["size"] for x in parameters]
    probs = [x["prob"] for x in parameters]
    size_sd = np.std(sizes)
    size_mean = np.mean(sizes)
    prob_sd = np.std(probs)
    prob_mean = np.mean(probs)
    dist = stats.nbinom(size_mean, prob_mean)
    threshold = dist.ppf(0.99)
    return {"size_sd": size_sd,
            "size_mean": size_mean,
            "prob_sd": prob_sd,
            "prob_mean": prob_mean,
            "threshold": threshold}

def run_sambamba_depth(bamfile, outdir):
    cmd = ("sambamba depth window --window-size=1024 --overlap=512 "
           "{bamfile} > {outfile}")
    bambase = os.path.splitext(os.path.basename(bamfile))[0]
    outfile = os.path.join(outdir, bambase + "-greydepth.tsv")
    if os.path.exists(outfile):
        return outfile
    subprocess.check_call(cmd.format(**locals()), shell=True)
    return outfile

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("bamfile")
    parser.add_argument("--outdir", default=".")
    args = parser.parse_args()

    depthfile = run_sambamba_depth(args.bamfile, args.outdir)
    depth = load_sambamba_depth(depthfile)
    threshold = estimate_threshold(depth)

    bambase = os.path.splitext(os.path.basename(args.bamfile))[0]
    statsfile = os.path.join(args.outdir, bambase + "-greystats.csv")
    with open(statsfile, "w") as out_file:
        out_file.write(",".join(["stat", "value"]) + "\n")
        out_file.write(",".join(["size_sd", str(threshold["size_sd"])]) + "\n")
        out_file.write(",".join(["size_mean", str(threshold["size_mean"])]) + "\n")
        out_file.write(",".join(["prob_sd", str(threshold["prob_sd"])]) + "\n")
        out_file.write(",".join(["prob_mean", str(threshold["prob_mean"])]) + "\n")
        out_file.write(",".join(["threshold", str(threshold["threshold"])]) + "\n")

    bedfile = os.path.join(args.outdir, bambase + "-grey.bed")
    depth = depth[depth['readCount'] > threshold["threshold"]].ix[:, range(4)]
    depth.to_csv(bedfile, sep="\t", header=False, index=False)
