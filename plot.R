#!/usr/bin/env Rscript

library(argparse)
library(ggplot2)
library(RcppCNPy)

commandline_parser = ArgumentParser(
        description="calculate the expected absorption signal")
commandline_parser$add_argument('input',
            type='character', nargs='?', default='KO202.npy',
            help='file with the aggregated')

args = commandline_parser$parse_args()
data = npyLoad(args$input)

print(data)

invisible(readLines(con="stdin", 1))
