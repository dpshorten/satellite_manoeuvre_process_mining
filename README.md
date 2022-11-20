# TLE Satellite Observation Data

This repository contains a dataset with TLE data for 15 satellites. Its purpose is to serve as a benchmark dataset for 
studies examining changes in satellite orbits over larger time scales. It also contains the ground-truth manoeuvre timestamps
for these satellites. Highly-accurate positional data from DORIS ground beacons is also included for some satellites.

Please see the paper: *Wide-scale Monitoring of Satellite Lifetimes: Pitfalls and a Benchmark Dataset* for a detailed 
description of the dataset.

The directory `plotting` contains the scripts for creating the plots in that paper.
- `plotting_TLE_propagation_residuals.py` creates the plots in figures 2, 11, 12 and 13.
- `plotting_osculating_mean_and_DORIS.py` creates the plots in figure 3.
- `plotting_osculating_and_mean_diffs_distribution.py` creates the plots in figure 4.
- `plotting_osculating_propagation_to_mean_diff.py` creates the plots in figure 5.
- `plot_satellite_liftimes_gantt.py` creates the plot in figure 6.
- `plotting_propagation_accuracy_TLE_to_SP3.py` creates the plots in figure 7.
- `plotting_DORIS_fourier_analysis.py` creates the plots in figures 8, 9 and 10.

you will need to change the file paths in params.py

The directory `dataset_formatting` contains scripts for manipulating the raw data into the compiled files.