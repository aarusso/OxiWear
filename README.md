OxiWear Power Optimization Code
===========================================

This repo contains analysis and plotting code written for optimizing power consumption while retaining signal fidelity for blood oxygenation (SpO2) data.

Contact:\
**Abigail Russo**\
russoaa@gmail.com\
June 2021

## Code
Here is a brief, high-level description of each function included in this repo. 

`demo.ipynb`: a Jupyter Notebook containing complete didactic documentation and use examples for all code.

### utility

- `fetchDff`: a utility a function for fetching and formatting DF/F mesoscope data via the DataJoint U19 Imaging pipeline at Princeton University.  It fetches data from a single primary key corresponding to a particular FOV and returns data formatted as an Neuron x Time x Trial tensor and a 1 x Trial structure that contains behavior information for each trial. The data are binned (see meso_analysis.BinnedBehavior for binning strategy details).
- `fetchDff_sessions`: a utility a function for fetching and formatting dF/F mesoscope data.  It fetches data from one or more primary key corresponding to a mesoscope imaging session and returns data formatted as a F x K cell array where K is the number of sessions and F is the number of FOVs. Each element of the cell array is an Neuron x Time x Trial tensor (see `fetchDff` for more information on how this tensor is formatted). This function also returns a behav_data 1 x K cell array where each element is a structure that contains behavioral info for each trial. 
- `format_NxTC`: a utility a function for formatting DF/F mesoscope data in a useful format for population analyses and a corresponding mask for handy data selection. It is intended for use with NxTxTr and behavior_mask, the outputs of `fetchDff`.
- `getDffFilters`: a utility a function for generating behavior filters dF/F mesoscope data. It is intended for use with NxTxTr and behavior_mask, the outputs of `fetchDff`.


### plotting

- `cluster_across_fovs`: This analysis clusters trial-averaged data across FOVs and then plots the data sorted by cluster or by other meaningful criteria (FOV, direction or task selectivity). The intention is to observe whether meaningful clusters are extracted and whether they align with other meaningful criteria. It is intended for use with fovsXsessions and behav_data, the outputs of `fetchDff_sessions`.

### analysis
- `samplingFq_vs_HR`: Analysis regarding how the sampling frequency impacts error in calculating heart rate across heart rate amplitude
- `samplingDur_vs_HR`: Analysis regarding how the sample duration impacts error in calculating heart rate across heart rate amplitude
- `get_hr_distribution`:  meaured HR will differ somewhat depending on the starting index. This function measures that distribution for comparison across parameter settings.
- `get_hr_distribution_chunks`:  Similarly, this function extracts random segmnets of a prescribed sample duration to get a distribution of heart rate estimates across segments. 


## Required Packages
- numpy
- scipy
- pandas
- matploblib
