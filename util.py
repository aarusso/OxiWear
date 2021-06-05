import numpy as np
import pandas as pd
from scipy import signal, interpolate




def decompose_ACDC(red, infrared, sampling_rate):
    
    N = len(red)
    
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
    data['time_min'] = np.linspace(0,N/data['sampling_rate'],N)/60
    
    return data


def getSpO2(h, sec_to_avg = 3):
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
   


#######---------------------Synthesize data (HR) ----------------------#########

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


#######---------------------Synthesize data (SpO2) ----------------------#########


def synthesize_SpO2(h, tile_range, params):
    
    red = h['red']
    IR = h['IR']
    sampling_rate = h['sampling_rate']
    

    simulation_dur_sec = params['drop_time_sec'] + params['recover_time_sec'] + 20*60 # 20 minute buffer
    data_dur_sec = (tile_range[1]-tile_range[0])/sampling_rate
    num2tile = int(np.ceil(simulation_dur_sec/data_dur_sec))
    
    #####---------------------------------------------------####
    def synthesize_data(data_AC, data_DC, drop):
       
        data_AC = data_AC[tile_range[0]:tile_range[1]]
        AC_synth = np.tile(data_AC, num2tile)

        N = len(AC_synth)
        
        data_DC = data_DC[tile_range[0]:tile_range[1]]
        DC_synth = np.tile(data_DC, num2tile)

        # mimic spo2 drop on 'red' DC
        if drop:
            drop_time    = int(params['drop_time_sec']*sampling_rate)
            recover_time = int(params['recover_time_sec']*sampling_rate)
            kernel_duration = drop_time + recover_time

            buffer = 1000
            # 5-15 minutes into the recording = spo2 drop
            drop_idx = np.random.randint(5*60*sampling_rate, 15*60*sampling_rate)
            drop_kernel = make_kernel(sampling_rate, params)
            kernel = np.ones(N)
            kernel[drop_idx:len(drop_kernel)+drop_idx] = drop_kernel

            DC_synth = np.multiply(DC_synth,kernel)
        else:
            drop_idx = float('nan')

        
        return AC_synth, DC_synth, drop_idx
    #####---------------------------------------------------####
    
    
    # NB: this is intentional: using IR to synthesize both red and IR than artifically setting the ratio
    IR_AC_synth,  IR_DC_synth, _  = synthesize_data(h['IR_AC'],  h['IR_DC'], False)
    red_AC_synth, red_DC_synth, drop_idx = synthesize_data(h['IR_AC'], h['IR_DC'], True)
    
    synth_ratio = (params['baseline_spo2']-120)/-40
    IR_DC_synth = IR_DC_synth*synth_ratio
    
    # add noise
    noise_level = params['noise'] * np.std(IR_DC_synth) * 10
    low_pass  = signal.butter(2, .01, 'lowpass',  fs=sampling_rate, output='sos')
    noise = np.random.randn(len(IR_DC_synth))
    noise = signal.sosfilt(low_pass, noise) * noise_level
    IR_DC_synth = IR_DC_synth + noise
    
    data_synth = dict()
    data_synth['red'] = red_AC_synth + red_DC_synth
    data_synth['IR'] = IR_AC_synth + IR_DC_synth
    data_synth['red_AC'] = red_AC_synth
    data_synth['red_DC'] = red_DC_synth
    data_synth['IR_AC'] = IR_AC_synth
    data_synth['IR_DC'] = IR_DC_synth
    data_synth['sampling_rate'] = sampling_rate
    data_synth['drop_idx'] = drop_idx
    data_synth['time_min'] = np.linspace(0,len(red_AC_synth)/sampling_rate,len(red_AC_synth))/60
    
    data_synth = getSpO2(data_synth)

    return data_synth

# function to synthesze a spo2 drop
def make_kernel(sampling_rate, params):


    drop_time    = int(params['drop_time_sec']*sampling_rate)
    recover_time = int(params['recover_time_sec']*sampling_rate)
    kernel_duration = drop_time + recover_time
    
    drop_kernel = np.ones(kernel_duration)
    
    drop_kernel[:drop_time] = np.linspace(1, params['drop_frac'], drop_time)
    drop_kernel[drop_time:drop_time+recover_time]  = np.linspace(params['drop_frac'] ,1, recover_time)
    
  
    return drop_kernel

