import streamlit as st
from plotting import get_x_axis, plot_time_series, plot_allan_deviation
from allan_variance import overlapping_allan_deviation as oadev
from noise_synthesis import make_angle_random_walk_series, make_rate_random_walk_series, simulate_flicker_noise, simulate_quantization_noise, simulate_rate_ramp, make_bias_instability_series

# TODO:  Implement checks for minimum number of noise samples (AOTC streaming data)

# Sidebar 

# Initialize simulation parameters
st.sidebar.title("Simulation Parameters")

sim_time = st.sidebar.number_input(
    label="Simulation Time (sec)",
    min_value=1.0,
    value=3_000.0,
    format="%.2f"
)

fs = st.sidebar.number_input(
    label="Sampling Rate (Hz)",
    min_value=1.0,
    value=20.0,
    format="%.2f"
)

st.sidebar.markdown("Generating {} data points".format(int(float(sim_time)*float(fs))))


# Initialize error coefficients
st.sidebar.title("Error Coefficients")

# Angle random walk
incl_arw = st.sidebar.checkbox("Angle Random Walk (ARW)", value=True)
arw_coeff = st.sidebar.number_input(
    label="ARW Coefficient (\u00B0/\u221Asec)",
    min_value=0.000_000_001,
    value=0.025,
    format="%f"
)

# First Order Markov Model of Bias Instability
use_first_order_markov = st.sidebar.checkbox("Bias Instability (BI) - First Order Markov Model", value=True) # For simplicity, omit this noise source by default
first_order_markov_bi_coeff = st.sidebar.number_input(
    label="BI Coefficient (\u00B0/sec)",
    min_value=0.000_000_001,
    value=0.005,
    format="%f",
    key="first order markov model coefficient"
)

corr_time = st.sidebar.number_input(
    label="Correlation Time (sec)",
    min_value=0.0,
    value=10.0,
    format="%f"
)


# Filter Model of Bias instability
use_filter_model = st.sidebar.checkbox("Bias Instability (BI) - Filter Model", value=False) # For simplicity, omit this noise source by default
filter_model_bi_coeff = st.sidebar.number_input(
    label="BI Coefficient (\u00B0/sec)",
    min_value=0.000_000_001,
    value=0.005,
    format="%f",
    key="filter model coefficient"
)

trunc_limit = st.sidebar.number_input(
    label="Number of IIR Filter Coefficients",
    min_value=1,
    value=500
)


# Rate random walk
incl_rrw = st.sidebar.checkbox("Rate Random Walk (RRW)", value=True)
rrw_coeff = st.sidebar.number_input(
    label="RRW Coefficient (units/sec\u2022\u221Asec)",
    min_value=0.000_000_001,
    value=0.001,
    format="%f"
)

# Quantization noise
incl_qn = st.sidebar.checkbox("Quantization Noise (QN)", value=False) # For simplicity, omit this noise source by default
qn_coeff = st.sidebar.number_input(
    label="QN Coefficient (\u00B0)",
    min_value = 0.000_000_001,
    value=0.0025,
    format="%f"
)

# Rate ramp
incl_rr = st.sidebar.checkbox("Rate Ramp (RR)", value=False) # For simplicity, omit this noise source by default
rr_coeff = st.sidebar.number_input(
    label="Rate Ramp (\u00B0/sec\u00b2)",
    min_value=0.000_000_001,
    value=1e-8,
    format="%f"
)


# Text in the main body of the app
st.title("Allan Online")
st.markdown("""
**Allan Online** is an open source tool for simulating the error characteristics of gyroscopes and accelerometers found on inertial measurement units (IMU). 
**Allan Online** gives users everywhere the power to characterize their navigation hardware in software!

## How to use **Allan Online**
Open the sidebar to reveal the simulation parameters. Choose how long the simulation should run and set the sampling rate in the *Simulation Parameters* section.
A dataset will be generated on screen immediately. The number of samples in this dataset can be seen below the sampling rate.

Under *Error Coefficients*, choose which noise type should be simulated by checking the boxes. 
By default, only *Angle Random Walk*, *Bias Instability*, and *Rate Random Walk* are included.
Then, provide the necessary data for each noise type.

After setting all of the parameters, a simulated signal of a single axis gyroscope and the corresponding Allan deviation are updated on screen.
""")


# Containerize the remaining sections of the app
gyro_time_series = st.beta_container()
allan_deviation = st.beta_container()

# Simulated gyro signal section
with gyro_time_series:

    st.title("Single Stationary Gyroscope Signal")

    st.write("""
    The following plot is a simulation of stationary gyroscope data captured by the on-board computer of the IMU.

    Although the virtual device is completely stationary, this plot shows that sources of noise in the system are introducing error to the measurement. 

    The plot is interactive so users can probe and investigate their results. Plots can also be saved as a png.
    """)


    # Convert input parameters str -> float
    num_samples = int(sim_time*fs)


    # Boolean array indicating which noise sources to include
    noise_model = [incl_arw, use_first_order_markov, use_filter_model, incl_rrw, incl_qn, incl_rr]
    
    # If user is trying to use both Filter model and First Order Markov model simultaneously...
    if (use_filter_model==True) and (use_first_order_markov==True):
        # Use only the First Order Markov model for Bias instability
        noise_model = [incl_arw, True, False, incl_rrw, incl_qn, incl_rr]
        st.header("""Only one Bias Instability model can be used at a time. Using First Order Markov Model.""")

    # All possible noise sources [ARW, 1st order BI, filter BI, RRW, QN, RR]
    noise_sources = [
        make_angle_random_walk_series(arw_coeff, fs, sim_time),
        make_bias_instability_series(first_order_markov_bi_coeff, corr_time, fs, sim_time),
        simulate_flicker_noise(filter_model_bi_coeff, fs, sim_time, trunc_limit),
        make_rate_random_walk_series(rrw_coeff, fs, sim_time),
        simulate_quantization_noise(qn_coeff, fs, sim_time),
        simulate_rate_ramp(rr_coeff, fs, sim_time)
    ]

    # Calculate the time stamps (x-axis values)
    timestamps = get_x_axis(sim_time, fs)

    # Add noise source series together according to the noise model
    combined_noise = sum([noise*include for noise, include in zip(noise_sources, noise_model)])

    # Create a figure for the time series
    combined_noise_plot = plot_time_series(timestamps, combined_noise)
    
    # Plot the combined noise time series
    st.plotly_chart(combined_noise_plot)
    


# Allan deviation section 
with allan_deviation:

    st.title("The Allan Deviation")
    st.write("""
    The following plot is shows the Allan deviation that corresponds to the above gyroscope signal.

    The Allan deviation is a clever mathematical tool that is used to identify the noise sources polluting a time series. 
    The Allan deviation has further uses in quantifying the impact of those same noise sources.
    """)

    # Compute the Allan deviation of the combined noise series
    taus, allan_values = oadev(combined_noise, fs)

    # Create a figure for the Allan deviation
    allan_plot = plot_allan_deviation(taus, allan_values)

    # Plot the Allan deviation
    st.plotly_chart(allan_plot)
     