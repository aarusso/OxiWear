import numpy as np
import util




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
