import numpy as np
import math


# Simulate angle random walk from given parameters
def make_angle_random_walk_series(coeff, fs, sim_time):
    num_samples = int(sim_time*fs)

    arw_psd = coeff**2
    sigma_arw = math.sqrt(arw_psd*fs)
    arw_series = sigma_arw*np.random.randn(num_samples)

    return arw_series


# Simulate bias instability noise from given parameters
def make_bias_instability_series(coeff, corr_time, fs, sim_time):
    num_samples = int(sim_time*fs)

    bi_series = np.zeros(shape=(num_samples,))

    for i in range(1, num_samples):
        eta = (1/corr_time)*coeff*np.random.randn(1)
        bdot = (-1/corr_time)*bi_series[i-1] + eta
        bi_series[i] = bi_series[i-1] + bdot

    return bi_series


# Simulate rate random walk noise from given parameters
def make_rate_random_walk_series(coeff, fs, sim_time):
    num_samples = int(sim_time*fs)

    rrw_psd = coeff**2
    sigma_rrw = math.sqrt(rrw_psd*fs)
    white_noise_series = sigma_rrw*np.random.randn(num_samples)
    rrw_series = (1/fs)*np.cumsum(white_noise_series)

    return rrw_series