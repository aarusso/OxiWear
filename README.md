OxiWear Power Optimization Code
===========================================

This repo contains analysis and plotting code written for optimizing power consumption while retaining signal fidelity for blood oxygenation (SpO2) data.

Contact:\
**Abigail Russo**\
russoaa@gmail.com\
June 2021

## Set up with Conda
We have provided a file called **environment.yml**. This YAML file will help you create a virtual environment named **oxiwear** used for activation and install necessary dependencies.

To create your environment from the YAML file please run:\
`conda env create --file environment.yml`\
Next, you will activate the created environment. To do so, you will need to
to call the following command:\
`conda activate oxiwear`\
To run the demo notebook, you will need to install the environment to Jupyter Notebook. With the environment active, install ipykernel:\
`conda install -c anaconda ipykernel`\
`ipython kernel install --user --name=oxiwear`\
Launch Jupyter notebook in the active environment:\
`jupyter notebook`\
You should now see the environment `oxiwear` as a kernel option.

## Code
Here is a brief, high-level description of each function included in this repo. 

`demo.ipynb`: a Jupyter Notebook containing complete didactic documentation and use examples for all code.

You can open this notebook in your web browser using Google Colaboratory\
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aarusso/OxiWear/blob/main/demo.ipynb)

### utility

- `decompose_ACDC`: Decomposes the red or infrared sensor data into AC and DC components, using high-pass and low-pass Butterworth filters, respectively. 
- `getSpO2`: Calculates SpO2 based on the ratio between red and infrared AC/DC components. Typically this is done with a look-up table. Here, we approximated the relationship between the ratio and SpO2 with a linear function.
- `get_HR`: Calculates heart rate from the AC component of the red sensor data. Peaks in the data are identified and heart rate is calculated from the inter-peak interval, which was found to be more accurate than dividing the total number of peaks by the sample duration.
- `synth_HR`: Simulates 1 minute of signal at desired heart rates from empirical data, keeping sampling rate constant.
- `synthesize_SpO2`: Simulates SpO2 with or without a hypoxic event, see docstring for more information.
- `make_kernel`: creates a kernel to mimic a SpO2 drop with the desired time-course and magnitude.

### analysis
- `samplingFq_vs_HR`: Analysis regarding how the sampling frequency impacts error in calculating heart rate across heart rate amplitude
- `samplingDur_vs_HR`: Analysis regarding how the sample duration impacts error in calculating heart rate across heart rate amplitude
- `get_hr_distribution`:  Measured HR will differ somewhat depending on the starting index. This function measures that distribution for comparison across parameter settings.
- `get_hr_distribution_chunks`:  Similarly, this function extracts random segments of a prescribed sample duration to get a distribution of heart rate estimates across segments. 
- `test_data_rate`:  Used by `get_alarm_time_distribution`, this function mimics a data update period strategy and outputs the corresponding SpO2 values that would have been detected.
- `get_alarm_time_distribution`: Used by `inter_sample_vs_alarm_time`,  this function determines how delays in alarm time interacts with the choice of data update period. 
- `inter_sample_vs_alarm_time`:  This function determines how alarm time delays vary with both the choice of the inter sample spacing and the choice of low-SpO2 trigger threshold.
- `get_battery_fraction`: This function calculates the proportion of battery life saved given a sampling strategy.


### plotting

- `plot_raw_data`: plots the sensor data from the infrared channel in three versions: raw, AC component, and DC component.
- `plot_nyquest`: plots the theoretically minimum viable sampling rate as a function of heart rate according to the Nyquest-Shannon theorem.
- `plot_fq_vs_HR`: plots the results of `samplingFq_vs_HR` as both a 2 dimensional heat plot and marginalized across either sampling frequency or heart rate.
- `plot_dur_vs_HR`: plots the results of `samplingDur_vs_HR` as both a 2 dimensional heat plot and marginalized across either sample duration or heart rate.
- `plot_synth_spo2`: A simple function for plotting SpO2 vs time, used by the following functions
- `plot_fig_1`, `plot_fig_2`,` plot_fig_3`: These functions plot simulated data to model the timecourse of SpO2 drops as observed in the literature (Sun et al _Gas exchange detection of exercise-induced right-to-left shunt in patients with primary pulmonary hypertension._ Circulation 2002). See docstring of plotting.py for parameter choices to simulate these empirical data.
- `plot_rate_vs_alarm_time`: plots the results of `inter_sample_vs_alarm_time` as both a 2 dimensional heat plot and marginalized across trigger threshold.
- `plot_color_range`: Plots a SpO2 trace with green, orange, and red ranges overlaid and the SpO2-aware sampling strategy indicated with x's.
- `plot_fraction_batt_vs_orange_time`:  plots the results of `get_battery_fraction` as both a 2 dimensional heat plot and a line plot with slices through % time in orange range.
- `plot_battery_life_in_days`: plots the results of `get_battery_fraction` on the scale of days as both a 2 dimensional heat plot and a line plot with slices through % time in orange range.


## Required Packages
- numpy
- scipy
- pandas
- matploblib
