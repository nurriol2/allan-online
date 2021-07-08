import numpy as np
import math


# Simulate angle random walk from given parameters
def make_angle_random_walk_series(coeff, fs, sim_time):
    """Generate an angle random walk noise series

    Args:
        coeff (float): Angle random walk coefficient found on a data sheet
        fs (int or float): Sampling rate in Hz
        sim_time (int or float): Length of the simulation in seconds

    Returns:
        numpy.array: Array of samples making an angle random walk noise time series
    """
    num_samples = int(sim_time*fs)

    arw_psd = coeff**2
    sigma_arw = math.sqrt(arw_psd*fs)
    arw_series = sigma_arw*np.random.randn(num_samples)

    return arw_series


# Simulate bias instability noise from given parameters
def make_bias_instability_series(coeff, corr_time, fs, sim_time):
    """Alternative method for generating a flicker noise series.
    Generate flicker noise by calculating discrete time steps of a
    stochastic differential equation.

    Args:
        coeff (float): Flicker noise coefficient
        corr_time (int or float): Correlation time parameter
        fs (int or float): Sampling rate in Hz
        sim_time (int or float): Length of the simulation in seconds

    Returns:
        numpy.array: Array of samples making a flicker noise time series
    """
    num_samples = int(sim_time*fs)

    bi_series = np.zeros(shape=(num_samples,))

    for i in range(1, num_samples):
        eta = (1/corr_time)*coeff*np.random.randn(1)
        bdot = (-1/corr_time)*bi_series[i-1] + eta
        bi_series[i] = bi_series[i-1] + bdot

    return bi_series


# Simulate flicker noise by shaping a white noise series
def simulate_flicker_noise(coeff, fs, sim_time, trunc_limit):
    """Generate flicker noise by shaping a white noise series.
    This is the preferred method for generating a flicker noise
    series.


    Args:
        coeff (float): Flicker noise coefficient found on a data sheet
        fs (int or float): Sampling rate in Hz
        sim_time (int or float): Length of the simulation in seconds
        trunc_limit (int): Number of IIR filter coefficients

    Returns:
        numpy.array: 1 by `numTerms+1` element array of samples making the flicker noise time series
    """

    # Number of terms in the final flicker noise sequence
    num_terms = int(sim_time*fs)

    ### Step 0 - Calculating the white noise scale value B ###
    # Supply flicker noise coefficient
    # Calculate the PSD from coeff
    # Supply sampling rate
    # Calculate variance of flicker noise
    # Define the exponent of 1/f^a noise
        # Set a==1 for Flicker Noise by def'n
 
    fn_psd = coeff**2
    sigma_fn = math.sqrt(fn_psd*fs)
    ALPHA = 1

    
    ### Step 1 - Initialize a white noise sequence ###
    # Define size of white noise sequence

    # White noise as a column vector
    white_noise = np.random.randn(num_terms, 1)


    ### Step 2 - Initialize the arrays to return at the end ###
    # Create containers for
        # Shaped values
        # flicker noise series
        # (opt.) integral of flicker noise series

    # Null row vector - Container for the shaped white noise series
    shape_values = np.zeros((1, num_terms+1))   

    
    ### Step 3 - Calculate IIR coeffs ###
    # Calculate a growing list of IIR coefficients
    #   There should be `trunc_limit`+1 total terms in the list 
    #   The 0th element of the list is 1

    a = [1]
    for i in range(1, trunc_limit+1):
        ith_iir_coeff = (i-1-ALPHA/2)*(a[i-1])/i
        a.append(ith_iir_coeff)
    assert (len(a)==trunc_limit+1), f"Wrong number of IIR Coefficients. Have {len(a)} Require {trunc_limit+1}"

    iir_coeffs = np.asarray(a).reshape((1, -1))
    # Require a row vector of IIR coefficients
    assert (iir_coeffs.shape[0]==1 and iir_coeffs.shape[1]!=0), f"Require a row vector. Got shape {iir_coeffs.shape}"


    ### Step 4 - DO white noise shaping ###
    # Set up accumulator pattern:
    # scale white noise by B from Step 0
    # loop 
    #   calculate single element for `shape_values` from coefficents and scaled white noise
    #       The matrix multiplication needs to be [1xN]*[Nx1]
    
    scaled_white_noise = sigma_fn*white_noise
    for count in range(trunc_limit+1, num_terms):

        iir_slice = -1*iir_coeffs[0][1:].reshape(1,-1)
        # Condition that iir_slice is also a row vector
        assert iir_slice.shape[0]==1 and iir_slice.shape[1]!=0, f"Require a row vector. Got shape {iir_slice.shape}"

        white_noise_sample = scaled_white_noise[count]

        shape_values_slice = shape_values[0][count-trunc_limit:count].reshape(1, -1)
        values_col_vec = np.transpose(np.fliplr(shape_values_slice))
        # Condition for a column vector
        assert values_col_vec.shape[1]==1 and values_col_vec.shape[0]!=0, f"Require column vector. Got shape {values_col_vec.shape}"
        # Condition for matrix multiplication
        assert iir_slice.shape[1]==values_col_vec.shape[0], f"Incompatible inner dimensions A*B = {iir_slice.shape}*{values_col_vec.shape}"
        
        single_value = np.matmul(iir_slice, values_col_vec) + white_noise_sample
        assert single_value!=0, f"Require non-zero value. Got {single_value}"

        shape_values[0][count+1] = single_value

    # Resulting array should be non-null
    assert np.any(shape_values), f"Array has no non-zero values"
    

    ### Step 5 - Return values ###
    # Do a circular shift of the `shape_values` array

    # The number of unshaped values depends on the size of `trunc_limit`
    fn_series = np.roll(shape_values, [0, -trunc_limit])


    return fn_series[0][0:-1]


# Simulate rate random walk noise from given parameters
def make_rate_random_walk_series(coeff, fs, sim_time):
    """Generate rate random walk noise series by scaling
    a white noise time series.

    Args:
        coeff (float): Rate random walk coefficient
        fs (int or float): Sampling rate in Hz
        sim_time (int or float): Length of simulation in seconds

    Returns:
        numpy.array: Array of values comprising a rate random walk noise time series
    """
    num_samples = int(sim_time*fs)

    rrw_psd = coeff**2
    sigma_rrw = math.sqrt(rrw_psd*fs)
    white_noise_series = sigma_rrw*np.random.randn(num_samples)
    rrw_series = (1/fs)*np.cumsum(white_noise_series)

    return rrw_series 

def simulate_quantization_noise(K, fs, sim_time, noise_amp=3.0, noise_freq=1.0):
    """Generate a quantization noise time series by adding white noise to a
    pure tone sinewave.

    Args:
        K (float):  Quantization Noise coefficient
        fs (int or float): Sampling rate in Hz
        sim_time (int or float): Length of the simulation in seconds
        noise_amp (float, optional): Amplitude of the pure tone sinewave. Also used to scale white noise series. Defaults to 3.0.
        noise_freq (float, optional): Frequency of the pure tone sinewave. Defaults to 1.0.

    Returns:
        numpy.array: Array of values comprising a quantization noise time series
    """
    num_terms = int(sim_time*fs)
    t = np.linspace(0, sim_time, num_terms+1)

    signal = noise_amp*np.sin((2*np.pi*noise_freq)*t)
    signal = signal + 0.1*noise_amp*np.random.randn(1, num_terms+1)

    E = np.mean(fs*abs(np.diff(signal)))
    
    q = (K*E)/fs

    xq = q*np.rint(np.divide(signal, q))
    qe = signal - xq

    qe_dot = np.divide(np.diff(qe), np.diff(t))

    qn = qe_dot.flatten()

    return qn

def simulate_rate_ramp(coeff, sim_time, fs):
    """Generate a rate ramp time series

    Args:
        coeff (float): Rate ramp coefficient
        sim_time (int or float): Length of the simulation in seconds
        fs (int or float): Sampling rate in Hz

    Returns:
        numpy.array: Array of values comprising a rate ramp time series
    """
    num_terms = int(sim_time*fs)
    return coeff*np.linspace(0, sim_time, num_terms+1)