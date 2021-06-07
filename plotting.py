import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import util


'''
For Mimic Sun et al Plots, use the following parameter settings:

Figure 1

#  control
params_ctrl = dict()
params_ctrl['baseline_spo2'] = 98
params_ctrl['drop_time_sec'] = 6*60
params_ctrl['recover_time_sec'] = 20*60
params_ctrl['drop_frac'] = 0.85


#  no-shunt-PPH
params_pph_noshunt = dict()
params_pph_noshunt['baseline_spo2'] = 94
params_pph_noshunt['drop_time_sec'] = 14*60
params_pph_noshunt['recover_time_sec'] = 20*60
params_pph_noshunt['drop_frac'] = 0.80


#  shunt PPH case average
params_pph_avg = dict()
params_pph_avg['baseline_spo2'] = 94
params_pph_avg['drop_time_sec'] = 2*60
params_pph_avg['recover_time_sec'] = 90*60
params_pph_avg['drop_frac'] = 0.75

Figure 2

#  control individual
params_ctrl_indi = dict()
params_ctrl_indi['baseline_spo2'] = 98.5
params_ctrl_indi['drop_time_sec'] = 10
params_ctrl_indi['recover_time_sec'] = 20*60
params_ctrl_indi['drop_frac'] = 0.95

#  no-shunt-PPH
params_pph_noshunt_indi = dict()
params_pph_noshunt_indi['baseline_spo2'] = 97
params_pph_noshunt_indi['drop_time_sec'] = 30
params_pph_noshunt_indi['recover_time_sec'] = 20*60
params_pph_noshunt_indi['drop_frac'] = 0.90

#  shunt PPH case individual
params_pph_indi = dict()
params_pph_indi['baseline_spo2'] = 94
params_pph_indi['drop_time_sec'] = 45
params_pph_indi['recover_time_sec'] = 20*60
params_pph_indi['drop_frac'] = 0.82

Figure 3

#  quick-recovery
params_quick_recov = dict()
params_quick_recov['baseline_spo2'] = 98
params_quick_recov['drop_time_sec'] = 60
params_quick_recov['recover_time_sec'] = 6*60
params_quick_recov['drop_frac'] = 0.60


'''


##########---------------------------Simple plots-------------------------------##############
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

##########---------------------------Mimic Sun et al Plots-------------------------------##############
def plot_synth_spo2(data, params, marker, data_label='', plot_line = True):

    data_synth = util.synthesize_SpO2(data, params)
    t = data_synth['time_min'] - data_synth['time_min'][data_synth['drop_idx']]
    time2plot = t<30
    if plot_line:
        plt.plot(t[time2plot][1::500], data_synth['spo2'][time2plot][1::500],'k')
    plt.plot(t[time2plot][1::500], data_synth['spo2'][time2plot][1::500], marker, label = data_label)
    
    
def plot_fig_1(data, params_ctrl, params_pph_avg, params_pph_noshunt):
    plt.figure()
    plot_synth_spo2(data, params_ctrl,'ko',data_label = 'Control')
    plot_synth_spo2(data, params_pph_avg,'ks',data_label = 'Shunt-PPH')
    plot_synth_spo2(data, params_pph_noshunt,'kx',data_label = 'No-Shunt-PPH')
    plt.legend()
    ax = plt.gca()
    ax.set_xlim(-3,6)
    ax.set_ylim(80,100)
    ax.set_yticks(np.arange(80,101,5))
    ax.set_xticks(np.arange(-3,18,3))
    ax.set_xticklabels(np.arange(0,19,3))
    ax.axvline(color = 'k',linestyle = '--',x=0)
    ax.axvline(color = 'k',linestyle = '--',x=3)
    plt.xlabel('Time (min)')
    plt.ylabel('SpO2 (%)')
    plt.title('Average across participants')


    plt.show()
    
    
def plot_fig_2(data, params_ctrl_indi, params_pph_noshunt_indi, params_pph_indi):
    plt.figure()
    plot_synth_spo2(data, params_ctrl_indi,'k:', data_label = 'Control',plot_line = False)
    plot_synth_spo2(data, params_pph_noshunt_indi,'k--', data_label = 'No-Shunt-PPH',plot_line = False)
    plot_synth_spo2(data, params_pph_indi,'k', data_label = 'Shunt-PPH',plot_line = False)
    ax = plt.gca()
    ax.set_xlim(-1,4)
    ax.set_ylim(85,100)
    ax.set_yticks(np.arange(85,101,5))
    ax.set_xticks(np.arange(-1,4,1))
    # ax.set_xticklabels(np.arange(0,19,3))
    ax.axvline(color = 'k',linestyle = '--',x=0)
    ax.axvline(color = 'k',linestyle = '--',x=3)
    plt.xlabel('Time (min)')
    plt.ylabel('SpO2 (%)')
    plt.title('Individual participants')
    plt.legend()
    plt.show()

def plot_fig_3(data, params_quick_recov):
    plt.figure()
    plot_synth_spo2(data, params_quick_recov,'ks')
    ax = plt.gca()
    ax.set_xlim(-3,3)
    ax.set_ylim(80,100)
    ax.set_yticks(np.arange(80,101,5))
    ax.set_xticks(np.arange(-10.5,2,3))
    ax.set_xticklabels(np.arange(0,13,3))
    ax.axvline(color = 'k',linestyle = '--', x=3-10.5)
    ax.axvline(color = 'k',linestyle = '--', x=6-10.5)
    ax.axvline(color = 'k',linestyle = '--', x=12-10.5)
    plt.xlabel('Time (min)')
    plt.ylabel('SpO2 (%)')
    plt.title('Late-developing, quick recovery')

    plt.show()


def plot_color_range(data, params, data_rate_green_sec, green_range, orange_range, red_thresh):
    ax = plt.gca()
    data_synth = util.synthesize_SpO2(data, params)
    t = data_synth['time_min'] - data_synth['time_min'][data_synth['drop_idx']]

    spo2 = data_synth['spo2']
    time2plot = t<15
    t = t[time2plot]
    spo2 =spo2[time2plot]
    plt.plot(t, spo2,'k')

    green = t[spo2>green_range[0]]
    green_spo2 = spo2[spo2>green_range[0]]
    sampling_period = int(data_synth['sampling_rate']*data_rate_green_sec*60)
    plt.plot(green[::sampling_period], green_spo2[::sampling_period], 'gx')

    orange = t[spo2<green_range[0]]
    orange_spo2 = spo2[spo2<green_range[0]]
    plt.plot(orange, orange_spo2, color = '#FCA103',marker = 'x')
    
    t_lims = [-5,6]
    ymin = 85
    ax.set_xlim(t_lims[0],t_lims[1])
    ax.set_xticks(np.arange(t_lims[0],t_lims[1],5))
    ax.set_ylim(ymin,100)
    ax.set_yticks(np.arange(ymin,101,5))

    # ax.set_xticklabels(np.arange(0,19,3))
    ax.axhline(color = 'r', y=red_thresh)

    plt.xlabel('Time (min)')
    plt.ylabel('SpO2 (%)')
    plt.title('Individual participant: Shunt-PPH')
    
    ax.fill_between(t_lims,[green_range[0], green_range[0]], [green_range[1],green_range[1]],color = 'g',alpha = .2)
    ax.fill_between(t_lims,[orange_range[0], orange_range[0]], [orange_range[1],orange_range[1]],color = '#FCA103',alpha = .3)
    ax.fill_between(t_lims,[red_thresh, red_thresh], [ymin,ymin],color = 'r',alpha = .2)
    
    
    plt.show()


##########---------------------------analysis plots-------------------------------##############

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
    
    mn = np.mean(pct_error,axis = 1 )
    std = np.std(pct_error,axis = 1 )
    axs[0].plot(target_HRs, mn, color = 'k',linewidth = 2)
    axs[0].fill_between(target_HRs, mn+std, mn-std,color = 'k',alpha = .3)
    axs[0].set_ylabel('mean error (%)')
    axs[0].set_ylim(0,20)
    axs[0].set_yticks(np.arange(0,21,5))
#    axs[0].set_xlabel('heart rate (BPM)')
    axs[0].set_ylabel('mean error (%)')

    mn = np.mean(pct_error,axis = 0 )
    std = np.std(pct_error,axis = 0 )
    axs[1].plot(resampled_rates, mn, color = 'k',linewidth = 2)
    axs[1].fill_between(resampled_rates, mn+std, mn-std,color = 'k',alpha = .3)
    axs[1].set_ylim(0,20)
    axs[1].set_yticks(np.arange(0,21,5))
    axs[1].set_xlabel('sampling frequency (Hz)')
    axs[1].set_ylabel('mean error (%)')
    axs[1].axhline(color = 'k',linestyle = '--', y=2.4)
    axs[1].axvline(color = 'k',linestyle = '--', x=18)
    
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
    mn = np.mean(pct_error,axis = 1 )
    std = np.std(pct_error,axis = 1 )
    axs[0].plot(target_HRs, mn, color = 'k',linewidth = 2)
    axs[0].fill_between(target_HRs, mn+std, mn-std,color = 'k',alpha = .3)
    axs[0].set_ylim(0,20)
    axs[0].set_yticks(np.arange(0,21,5))
    axs[0].set_xlabel('heart rate (BPM)')
    axs[0].set_ylabel('mean error (%)')

    mn = np.mean(pct_error,axis = 0 )
    std = np.std(pct_error,axis = 0 )
    axs[1].plot(sample_durs, mn, color = 'k',linewidth = 2)
    axs[1].fill_between(sample_durs, mn+std, mn-std,color = 'k',alpha = .3)
    axs[1].set_xlabel('sample duration (sec)')
    axs[1].set_ylabel('mean error (%)')
    axs[1].set_ylim(0,20)
    axs[1].set_yticks(np.arange(0,21,5))
    axs[1].axhline(color = 'k',linestyle = '--', y=1)
    axs[1].axvline(color = 'k',linestyle = '--', x=5)
#    plt.show()


def plot_rate_vs_alarm_time(alarm_times_sec,alarm_times_stds, inter_sample_sec, spo2_thresh):
    plt.imshow(alarm_times_sec)

    locs, labels = plt.xticks()
    ax = plt.gca()
    x_idx = np.arange(0,len(inter_sample_sec),2)
    ax.set_xticks(x_idx)
    ax.set_xticklabels(inter_sample_sec[x_idx])

    y_idx = np.arange(0,len(spo2_thresh),2)
    ax.set_yticks(y_idx)
    ax.set_yticklabels([int(s) for s in spo2_thresh[y_idx]])

    plt.colorbar(label='warning delay (sec)')
    plt.xlabel('inter sample space (sec)')
    plt.ylabel('trigger threshold')
    plt.show()

    plt.figure()
    times = np.nanmean(alarm_times_sec,0)
    stds = np.nanmean(alarm_times_stds,0)
    plt.plot(inter_sample_sec, times, 'k',linewidth = 2)
    plt.fill_between(inter_sample_sec, times+stds, times-stds,color = 'k',alpha = .3)

    plt.plot([0,140],[0,140],'b')
    ax = plt.gca()
    plt.xlabel('inter sample space (sec)')
    x_idx = np.arange(0,len(inter_sample_sec),2)
    ax.set_xticks(inter_sample_sec[x_idx])
    ax.set_xticklabels(inter_sample_sec[x_idx])
    ax.axvline(color = 'k',linestyle = '--', x=30)
    ax.axhline(color = 'k',linestyle = '--', y=30)
    plt.ylabel('warning time delay (sec)')
    plt.show()


def plot_fraction_batt_vs_orange_time(results, inter_sample_sec, prcile_orange):
    
    
    norm = TwoSlopeNorm(vmin=0, vcenter=.5, vmax=1)

    fig, ax = plt.subplots(figsize=(8, 6))

    cax = ax.imshow(results.T, cmap = 'bwr',norm = norm)

    locs, labels = plt.xticks()

    poriton_label = np.array([int((i)/5) for i in inter_sample_sec])
    poriton_label = inter_sample_sec
    x_idx = np.arange(0,len(poriton_label),2)
    ax.set_xticks(x_idx)
    ax.set_xticklabels(poriton_label[x_idx])

    pct_label = np.array([int(p*100) for p in prcile_orange])
    y_idx = np.arange(1,len(pct_label),2)
    ax.set_yticks(y_idx)
    ax.set_yticklabels(np.array(pct_label)[y_idx].T)


    # fig.colorbar(cax, label='est. battery life (days)')
    # plt.clim(0,4)
    plt.xlabel('inter sample space (sec)')
    plt.ylabel('% time in orange range')
    fig.colorbar(cax, label='fraction battery use', ticks = np.arange(0,1.1,.25),fraction=0.03, pad=0.04)


    plt.show()


    plt.plot(poriton_label, results[:,prcile_orange==.5],label = '50%',color = '#FCA103', linewidth = 4)
    plt.plot(poriton_label, results[:,prcile_orange==.4],label = '40%',color = '#FCA103', linewidth = 3)
    plt.plot(poriton_label, results[:,prcile_orange==.3],label = '30%',color = '#FCA103', linewidth = 2)
    plt.plot(poriton_label, results[:,prcile_orange==.2],label = '20%',color = '#FCA103', linewidth = 1)
    ax = plt.gca()
    ax.axhline(color = 'k',linestyle = '--', y=.5)
    ax.axvline(color = 'k',linestyle = '--', x=30)
    poriton_label = inter_sample_sec
    x_idx = np.arange(0,len(poriton_label),2)
    ax.set_xticks(poriton_label[x_idx])
    plt.xlabel('inter sample space in green range (sec)')
    plt.ylabel('fraction battery use')
    plt.title('Fraction battery use vs % time in orange range')
    plt.legend()
    plt.show()


def plot_battery_life_in_days(results, multiplier, inter_sample_sec, prcile_orange, plot_title):
    

    results_batty = (1/results)*multiplier

    norm = TwoSlopeNorm(vmin=0, vcenter=1, vmax=3)

    fig, ax = plt.subplots(figsize=(8, 6))

    cax = ax.imshow(results_batty.T, cmap = 'bwr_r',norm = norm)

    locs, labels = plt.xticks()

    poriton_label = np.array([int((i)/5) for i in inter_sample_sec])
    poriton_label = inter_sample_sec
    x_idx = np.arange(0,len(poriton_label),2)
    ax.set_xticks(x_idx)
    ax.set_xticklabels(poriton_label[x_idx])

    pct_label = np.array([int(p*100) for p in prcile_orange])
    y_idx = np.arange(1,len(pct_label),2)
    ax.set_yticks(y_idx)
    ax.set_yticklabels(np.array(pct_label)[y_idx].T)


    # fig.colorbar(cax, label='est. battery life (days)')
    # plt.clim(0,4)
    plt.xlabel('inter sample space (sec)')
    plt.ylabel('% time in orange range')


    cbar = fig.colorbar(cax, ticks=[0,1,2,3], label='est. battery life (days)',fraction=0.03, pad=0.04)
    cbar.ax.set_yticklabels(['0', '1', '2','>3'])  # vertically oriented colorbar

    plt.title(plot_title)
    plt.show()
    
    max_bat = np.max(results_batty[:,prcile_orange==.2])
    max_bat = np.ceil(max_bat/.5)*.5
    plt.figure()
    plt.plot(poriton_label, results_batty[:,prcile_orange==.5],label = '50%',color = '#FCA103', linewidth = 4)
    plt.plot(poriton_label, results_batty[:,prcile_orange==.4],label = '40%',color = '#FCA103', linewidth = 3)
    plt.plot(poriton_label, results_batty[:,prcile_orange==.3],label = '30%',color = '#FCA103', linewidth = 2)
    plt.plot(poriton_label, results_batty[:,prcile_orange==.2],label = '20%',color = '#FCA103', linewidth = 1)
    ax = plt.gca()
    ax.axhline(color = 'k',linestyle = '--', y=1)
    ax.axvline(color = 'k',linestyle = '--', x=30)
    ax.axvline(color = 'k',linestyle = '--', x=60)
    poriton_label = inter_sample_sec
    x_idx = np.arange(0,len(poriton_label),2)
    ax.set_xticks(poriton_label[x_idx])
    
    ax.set_yticks(np.arange(0,max_bat+.1,.5))
    plt.xlabel('inter sample space in green range (sec)')
    plt.ylabel('Battery life (days)')
    plt.title('Battery life (days) vs % time in orange range')
    plt.legend()
    plt.show()
    
