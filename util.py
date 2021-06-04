import numpy as np
import pandas as pd
from scipy import signal, interpolate




def decompose_ACDC(red, infrared, sampling_rate):
    
    N = len(red)
    min_max = min(np.max(red), np.max(infrared))
    red = red/min_max
    infrared = infrared/min_max
    
    #  create high/low pass filters
    high_cut = 20  # anything lower than 20 Hz is not heart rate
    low_cut = 2

    nyq = sampling_rate*.5

    high_pass = signal.butter(1, high_cut/nyq, 'highpass', fs=sampling_rate, output='sos')
    low_pass  = signal.butter(2, low_cut/nyq, 'lowpass',  fs=sampling_rate, output='sos')
    

    # extract AC & DC components
    red_AC = signal.sosfilt(high_pass, red-np.mean(red))
    red_DC = signal.sosfilt(low_pass, red-np.mean(red))+ np.mean(red)

    IR_AC = signal.sosfilt(high_pass, infrared-np.mean(infrared))
    IR_DC = signal.sosfilt(low_pass, infrared-np.mean(infrared)) + np.mean(infrared)
    
    data = dict()
    data['red'] = red
    data['IR'] = infrared
    data['red_AC'] = red_AC
    data['red_DC'] = red_DC
    data['IR_AC'] = IR_AC
    data['IR_DC'] = IR_DC
    data['sampling_rate'] = sampling_rate
    data['high_pass'] = high_pass
    data['low_pass'] = low_pass
    data['time_min'] = np.linspace(0,N/data['sampling_rate'],N)/60
    
    return data


def getSpO2(h, sec_to_avg = 3, ratio = 1):
    red_AC = h['red_AC']
    red_DC = h['red_DC']
    
    IR_AC = h['IR_AC']
    IR_DC = h['IR_DC']
    
    sampling_rate = h['sampling_rate']
    
    #  calculate R
    R = (red_AC/red_DC)/(IR_AC/IR_DC)

    # clean data
    R[R>2] = float('nan')
    R[R<0] = float('nan')
    R_avg = pd.Series(R).rolling(int(sampling_rate*sec_to_avg), min_periods=2).mean()
    
    #  Spo2 conversion
    Spo2 = 120-(40*R_avg)
    
    h['ratio'] = np.array(R)
    h['spo2'] = np.array(Spo2)
    
    return h

#######--------------------- Calculate heart rate ----------------------#########

def get_HR(hr_signal, sampling_rate):
    max_HR = 250 # for calculating the minimum number of samples between peaks
    mins_in_sample = (len(hr_signal)/sampling_rate)/60
    max_BPS = max_HR/60
    min_btw_samples = int(np.ceil(sampling_rate/max_BPS))
    
    min_height = np.percentile(hr_signal,80)

    pks = signal.find_peaks(hr_signal, distance = min_btw_samples, height = min_height)
    pks = pks[0]
    
    # average inter-peak-interval is more reliable than a # peaks/time measure
    ipi = pks[1:] - pks[:-1]
    mean_ipi = np.mean(ipi)
    hr = (1/mean_ipi) * (sampling_rate*60)
    return hr, pks
   


#######---------------------Synthesize data----------------------#########

def synth_HR(hr_signal, fq, target_HRs):
    '''
    Synthesize 1 minute of signal at desired heart rate (target_HRs) from empirical data (hr_signal), keeping sampling rate (fq) constant.
    '''
    
    N = len(hr_signal)
    samples_per_min = int(np.ceil(fq*60))
    
    HR,_ = get_HR(hr_signal,  fq)
    t = np.linspace(0, N, N)
    interpolated = interpolate.interp1d(t, hr_signal, axis = 0, fill_value = 'extrapolate')
    
    hr_synth = dict()
    
    for target_HR in target_HRs:
        
        new_rate = HR/target_HR
        new_t = np.linspace(0, N, int(N*new_rate))
        new_hr_signal = interpolated(new_t)

        num_reps = int(np.ceil(samples_per_min/len(new_hr_signal)))
        new_hr_signal = np.tile(new_hr_signal, num_reps)
        
        new_hr_signal = new_hr_signal[:samples_per_min]
        hr_synth[target_HR] = new_hr_signal
    
    return hr_synth
    
    
# resample HR; maintain duration in seconds

def resample_hr(hr_signal, fq, resampled_fq):
    '''
    Synthesize signal at desired sampling rate (resampled_fq) from empirical data (hr_signal), keeping heart rate and sample duration in seconds constant.
    '''
    N = len(hr_signal)
    seconds_of_data = N/fq

    t = np.linspace(0, N, N)
    resampled_t = np.linspace(0, N, int(seconds_of_data*resampled_fq))

    interpolated = interpolate.interp1d(t, hr_signal, axis = 0, fill_value = 'extrapolate')
    resampled_hr_signal = interpolated(resampled_t)

    return resampled_hr_signal
