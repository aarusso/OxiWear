import numpy as np
import util
from scipy import signal, interpolate


##########---------------------------Heart Rate-------------------------------##############
def samplingFq_vs_HR(original_hr, original_fq, target_HRs, resampled_rates):
    '''
    Determine how changing the sampling frequency impacts error in calculating heart rate across heart rate amplitude
    '''
    
    
    #  synthesize data for each target HR with same temporal duration
    synth_hr = util.synth_HR(original_hr, original_fq, target_HRs);
    
    # there will be some error between the 'target' heart rate of synthetic data and what can be estimated due to the discrete nature of peak counting
    # Thus, Use this estimated HR (rather than target HR) as a benchmark for good performance
    estim_HRs, estim_std = get_hr_distribution(synth_hr, original_fq)
    
    results_means = np.zeros((len(target_HRs), len(resampled_rates)))
    results_error = np.zeros((len(target_HRs), len(resampled_rates)))
    results_stds = np.zeros((len(target_HRs), len(resampled_rates)))
    
    for idx, new_fq in enumerate(resampled_rates):
        hr_signal_resampled = util.resample_hr(original_hr, original_fq, new_fq)
        hr_synth_resampled = util.synth_HR(hr_signal_resampled, new_fq, target_HRs); # 1 min synth data for each target HR

        estim_HRs_resampled, estim_std_resampled = get_hr_distribution(hr_synth_resampled, new_fq)
        results_means[:,idx] = estim_HRs_resampled
        results_stds[:,idx] = estim_std_resampled
        results_error[:,idx] = np.abs(np.subtract(estim_HRs, estim_HRs_resampled))
    
    return results_error, results_means, results_stds
    
    
    
def samplingDur_vs_HR(original_hr, fq, target_HRs, sample_durs):
    
    '''
    Determine how changing the sampling duration impacts error in calculating heart rate across heart rate amplitude
    '''
    
    #  synthesize data for each target HR with same temporal duration
    synth_hr = util.synth_HR(original_hr, fq, target_HRs);
    
    # there will be some error between the 'target' heart rate of synthetic data and what can be estimated due to the discrete nature of peak counting
    # Thus, Use this estimated HR (rather than target HR) as a benchmark for good performance
    estim_HRs, estim_std = get_hr_distribution(synth_hr, fq)
    
    results_means = np.zeros((len(target_HRs), len(sample_durs)))
    results_error = np.zeros((len(target_HRs), len(sample_durs)))
    results_stds = np.zeros((len(target_HRs), len(sample_durs)))
    
    for idx, dur in enumerate(sample_durs):
        estim_HRs_chunk, estim_std_chunk = get_hr_distribution_chunks(synth_hr, fq, dur)
        results_means[:,idx] = estim_HRs_chunk
        results_stds[:,idx] = estim_std_chunk
        results_error[:,idx] = np.abs(np.subtract(estim_HRs, estim_HRs_chunk))
    
    return results_error, results_means, results_stds

######------------ Estimate heart rate error distributions----------------######


def get_hr_distribution(hr_synth, fq):
    '''
    Meaured HR will differ somewhat depending on the starting index, get distributions for comparison
    '''
    min_hr = 30
    min_BPS = min_hr/60
    max_btw_samples = int(np.ceil(fq/min_BPS))

    num_iterations = max_btw_samples*10

    std = []
    mean = []
    for this_hr in hr_synth.keys():
        HR_iterations = []
        hr_signal = hr_synth[this_hr]
        for i in range(num_iterations):
            start_idx = np.random.randint(max_btw_samples)
            HR_i,_ = util.get_HR(hr_signal[start_idx:],  fq)
            HR_iterations.append(HR_i)
        std.append(np.nanstd(HR_iterations))
        mean.append(np.nanmean(HR_iterations))
        
    return mean, std

def get_hr_distribution_chunks(hr_synth, fq, dur_sec):
    min_hr = 30
    min_BPS = min_hr/60
    max_btw_samples = int(np.ceil(fq/min_BPS))

    num_iterations = max_btw_samples*10 # just for consistency across analyses

    
    std = []
    mean = []
    for this_hr in hr_synth.keys():
        hr_signal = hr_synth[this_hr]
        N = len(hr_signal)
        seconds_of_data = N/fq
        N_desired_dur = int(dur_sec*fq)
        
        HR_iterations = []
        
        for i in range(num_iterations):
            start_idx = np.random.randint(N-N_desired_dur)
            HR_i,_ = util.get_HR(hr_signal[start_idx:start_idx+N_desired_dur],  fq)
            HR_iterations.append(HR_i)
        std.append(np.nanstd(HR_iterations))
        mean.append(np.nanmean(HR_iterations))
        
    return mean, std


##########---------------------------SpO2-------------------------------##############




def test_data_rate(data_synth, sample_dur_sec, inter_sample_sec):
#     sample_dur_sec : collect X seconds of data at a time; AVERAGE within this period = spo2 output
#     inter_sample_sec : collect a data sample every X minutes

    N = len(data_synth['spo2'])
    sampling_rate = data_synth['sampling_rate']
    tile_range = data_synth['tile_range']
    sampling_period = int((inter_sample_sec+sample_dur_sec)*sampling_rate)

    first_sample  = np.random.randint(sampling_period) # randomize starting index!
    sample_starts = np.arange(first_sample, N, sampling_period)
    sample_ends   = [i + int(sample_dur_sec*sampling_rate) for i in sample_starts]

    spo2 = []
    d = dict()
    d['sampling_rate'] = data_synth['sampling_rate']
    for iO,iN in zip(sample_starts, sample_ends):

        d['red_AC'] = data_synth['red_AC'][iO:iN]
        d['red_DC'] = data_synth['red_DC'][iO:iN]
        d['IR_AC'] = data_synth['IR_AC'][iO:iN]
        d['IR_DC'] = data_synth['IR_DC'][iO:iN]

        h = util.getSpO2(d, tile_range)
        spo2.append(np.nanmean(h['spo2']))

    return np.array(spo2), np.array(sample_ends)



def get_alarm_time_distribution(data_synth, sample_dur_sec, inter_sample_sec, spo2_thresh, num_iterations = 40):
    ''' for the same data, alarm time will depend on how the samples are shifted with respect to the drop in Spo2. Randomize the shift and measure the distribution.
    '''
    alarm_times = []
    for i in range(num_iterations):
        spo2, sample_ends = test_data_rate(data_synth, sample_dur_sec, inter_sample_sec)
        low_spo2 = sample_ends[spo2<spo2_thresh]
        try:
            alarm_times.append(low_spo2[0])
        except:
            alarm_times.append(np.float('Nan'))
    alarm_times = np.array(alarm_times)
    return np.mean(alarm_times), np.std(alarm_times)


def inter_sample_vs_alarm_time(data_synth, params, sample_dur_sec, inter_sample_sec, spo2_thresh):
    results_means = np.zeros((len(spo2_thresh), len(inter_sample_sec)))
    results_stds = np.zeros((len(spo2_thresh), len(inter_sample_sec)))
    for i1, thresh in enumerate(spo2_thresh):
        for i2, inter in enumerate(inter_sample_sec):
            mn, std = get_alarm_time_distribution(data_synth, sample_dur_sec, inter, thresh)
            results_means[i1,i2] = mn
            results_stds[i1,i2]  = std
    alarm_times_sec = np.subtract(results_means, np.reshape(results_means[:,0],(-1,1)))/data_synth['sampling_rate']
    alarm_times_stds = results_stds/data_synth['sampling_rate']
    return alarm_times_sec, alarm_times_stds


##########---------------------------Battery-------------------------------##############

def get_battery_fraction(sample_dur_sec, inter_sample_sec, prcile_orange):
    proportion_on_green = sample_dur_sec/(sample_dur_sec+inter_sample_sec)
    results = np.zeros((len(proportion_on_green),len(prcile_orange)))
    for i1, pg in enumerate(proportion_on_green):
        for i2, po in enumerate(prcile_orange):
            results[i1,i2] = pg*(1-po) + 1*po
    return results
