import numpy as np

def find_index_of_closest_slope(x, y, slope):
    
    # Tansform x and y into log space
    logx = np.log10(x)
    logy = np.log10(y)

    # Calculate the derivative of the curve y(x) in log space
    dlogy = np.divide(np.diff(logy), np.diff(logx))

    # Calculate the index where value of derivative is closest to desired slope
    target_index = np.abs(dlogy-slope).argmin()

    return target_index

def calculate_log_space_y_intercept(x, y, slope, target_index):
    
    # Transform x and y into log space
    logx = np.log10(x)
    logy = np.log10(y)

    # Calculate the y intercept in log space
    intercept = logy[target_index] - slope*logx[target_index]

    return intercept

def calculate_coeff_from_line(slope, tau_star, intercept):
    
    coeff = None

    # For noise coefficient different than Bias Instability
    if slope!=0:

        # Compute coefficient in log space
        logCoeff = slope*np.log10(tau_star) + intercept

        # Undo log base 10
        coeff = 10**logCoeff
    
    # For Bias Instability noise coefficient
    else:

        # Bias Instability coefficient is always scaled by ~0.664
        SCALE_FACTOR = (2*np.log(2)/np.pi)**0.5
        
        # Undo log base 10
        coeff = 10**(intercept - np.log10(SCALE_FACTOR))

    return coeff


def fit_random_walk_line(rw_coeff, tau_array):
    t = np.power(tau_array, 0.5)
    
    return np.divide(rw_coeff, t)

def fit_rate_random_walk_line(rrw_coeff, tau_array):
    
    t = np.power(np.divide(tau_array,3), 0.5)
    
    return rrw_coeff * t

def fit_bias_instability_line(bi_coeff, tau_array):
    
    product = bi_coeff * (2*np.log(2)/np.pi)**0.5
    
    return product * np.ones(len(tau_array))