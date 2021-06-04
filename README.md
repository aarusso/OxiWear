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

- `decompose_ACDC`: Decomposes the red or infrared sensor data into AC and DC components, using high-pass and low-pass Butterworth filters, respectively. 
- `getSpO2`: Calculates SpO2 based on the ratio between red and infrared AC/DC components. Typically this is done with a look-up table. Here, we approximated the relationship between the ratio and SpO2 with a linear function.
- `get_HR`: Calculates heart rate from the AC component of the red sensor data. Peaks in the data are identified and heart rate is calculated from the inter-peak interval, which was found to be more accurate than dividing the total number of peaks by the sample duration.
- `synth_HR`: Simulates 1 minute of signal at desired heart rates from empirical data, keeping sampling rate constant.
- `resample_hr`: Simulates signal at a desired sampling rate from empirical data, keeping heart rate and sample duration in seconds constant.

### analysis
- `samplingFq_vs_HR`: Analysis regarding how the sampling frequency impacts error in calculating heart rate across heart rate amplitude
- `samplingDur_vs_HR`: Analysis regarding how the sample duration impacts error in calculating heart rate across heart rate amplitude
- `get_hr_distribution`:  meaured HR will differ somewhat depending on the starting index. This function measures that distribution for comparison across parameter settings.
- `get_hr_distribution_chunks`:  Similarly, this function extracts random segmnets of a prescribed sample duration to get a distribution of heart rate estimates across segments. 

### plotting

- `plot_raw_data`: plots the sensor data from the infrared channel in three versions: raw, AC component, and DC component.
- `plot_nyquest`: plots the theoretically minimum viable sampling rate as a function of heart rate according to the Nyquest-Shannon theorem.
- `plot_fq_vs_HR`: plots the results of `samplingFq_vs_HR` as both a 2 dimensional heat plot and marginalized across either sampling frequency or heart rate.
- `plot_dur_vs_HR`: plots the results of `samplingDur_vs_HR` as both a 2 dimensional heat plot and marginalized across either sample duration or heart rate.


## Required Packages
- numpy
- scipy
- pandas
- matploblib
