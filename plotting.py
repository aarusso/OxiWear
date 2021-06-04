import numpy as np
import matplotlib.pyplot as plt


def plot_raw_data(data):
    fig, axs = plt.subplots(3, 1)
    plt.rcParams['font.size'] = '12'
    fig.set_figheight(10)
    axs[0].plot(data['time_min'], data['IR'])
    axs[0].set_ylabel('infrared signal (normalized)')


    axs[1].plot(data['time_min'], data['IR_AC'])
    axs[1].set_ylabel('AC component')


    axs[2].plot(data['time_min'], data['IR_DC'])
    axs[2].set_xlabel('time (minutes)')
    axs[2].set_ylabel('DC component')


    plt.show()

def plot_nyquest(fq_of_interest, data_label):
    min_sampling_Hz = (2*fq_of_interest)/60
    plt.plot(fq_of_interest, min_sampling_Hz)
    plt.ylabel('minimum sampling rate (Hz)')
    plt.xlabel(data_label)
    plt.show()


def plot_fq_vs_HR(pct_error, target_HRs, resampled_rates):
    plt.imshow(pct_error.T)
    locs, labels = plt.xticks()
    ax = plt.gca()
    x_idx = np.arange(0,len(target_HRs),3)
    ax.set_xticks(x_idx)
    ax.set_xticklabels(target_HRs[x_idx])

    y_idx = np.arange(0,len(resampled_rates),2)

    plt.rcParams['font.size'] = '12'
    ax.set_yticks(y_idx)
    ax.set_yticklabels(resampled_rates[y_idx].T)
    plt.colorbar(label='percent error (%)')
    plt.xlabel('heart rate (BPM)')
    plt.ylabel('sampling frequency (Hz)')
    plt.clim(0,10)

    plt.show()
    
    fig, axs = plt.subplots(2, 1)
    plt.rcParams['font.size'] = '12'
    fig.set_figheight(8)
    axs[0].plot(target_HRs, np.mean(pct_error,axis = 1 ))
    axs[0].set_xlabel('heart rate (BPM)')
    axs[0].set_ylabel('mean error (%)')


    axs[1].plot(resampled_rates, np.mean(pct_error,axis = 0 ))
    axs[1].set_xlabel('sampling frequency (Hz)')
    axs[1].set_ylabel('mean error (%)')
    plt.show()

def plot_dur_vs_HR(pct_error, target_HRs, sample_durs):
    plt.imshow(pct_error.T)
    locs, labels = plt.xticks()
    ax = plt.gca()
    x_idx = np.arange(0,len(target_HRs),2)
    ax.set_xticks(x_idx)
    ax.set_xticklabels(target_HRs[x_idx])

    y_idx = np.arange(0,len(sample_durs),1)
    ax.set_yticks(y_idx)
    ax.set_yticklabels(np.array(sample_durs)[y_idx].T)
    # plt.colorbar()


    plt.colorbar(label='percent error (%)')
    plt.clim(0,10)
    plt.xlabel('heart rate (BPM)')
    plt.ylabel('sample duration (sec)')
    plt.show()

    fig, axs = plt.subplots(2, 1)
    plt.rcParams['font.size'] = '12'
    fig.set_figheight(8)
    axs[0].plot(target_HRs, np.mean(pct_error,axis = 1 ))
    axs[0].set_xlabel('heart rate (BPM)')
    axs[0].set_ylabel('mean error (%)')


    axs[1].plot(sample_durs, np.mean(pct_error,axis = 0 ))
    axs[1].set_xlabel('sample duration (sec)')
    axs[1].set_ylabel('mean error (%)')
    plt.show()
