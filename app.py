import streamlit as st
import numpy as np
from plotting import plot_log_scale
from allan_variance import overlapping_allan_deviation as oadev
from noise_synthesis import make_angle_random_walk_series, make_bias_instability_series, make_rate_random_walk_series

#TODO:  Validate parameter types to reduce the number of type conversions
#TODO:  Set boundaries on params; e.g. sim_time >= 0
#TODO:  Handle an empty (all 0s) simulation
#TODO:  Include other noise sources e.g. Rate Ramp, Quantization noise
#TODO:  Refactor Allan deviation plotting to use Altair
#TODO:  Add axis labels for Altair type plot

# Sidebar 

# Initialize simulation parameters
st.sidebar.title("Simulation Parameters")
sim_time = st.sidebar.text_input(
    label="Simulation Time (sec)",
    value=100
)

fs = st.sidebar.text_input(
    label="Sampling Rate (Hz)",
    value=10
)

st.sidebar.markdown("Generating {} data points".format(int(float(sim_time)*float(fs))))


# Initialize noise parameters
st.sidebar.title("Noise Parameters")

incl_arw = st.sidebar.checkbox("Angle Random Walk (ARW)", value=True)
arw_coeff = st.sidebar.text_input(
    label="ARW Coefficient (\u00B0/\u221Asec)",
    value=0.25
)

incl_bi = st.sidebar.checkbox("Bias Instability (BI)", value=True)
bi_coeff = st.sidebar.text_input(
    label="BI Coefficient (\u00B0/\u221Asec)",
    value=10
)

corr_time = st.sidebar.text_input(
    label="Correlation Time (units)",
    value = 1000

)

incl_rrw = st.sidebar.checkbox("Rate Random Walk (RRW)", value=True)
rrw_coeff = st.sidebar.text_input(
    label="RRW Coefficient (units/sec\u2022\u221Asec)",
    value=0.01
)


# Main app body
st.title("Allan Online")
st.markdown("""
**Allan Online** is an open source tool for simulating gyroscopes and accelerometers found on inertial measurement units (IMU). 
**Allan Online** gives users everywhere the power to characterize their navigation hardware in software!

## How to use **Allan Online**
Open the sidebar to reveal the simulation parameters. Choose how long the simulation should run and set the sampling rate in the *Simulation Parameters* section.
A dataset will be generated on screen immediately. The number of samples in this dataset can be seen below the sampling rate.

Under *Noise Parameters*, choose the noise sources affecting the IMU by checking the boxes. By default, all noise sources are included.

After setting all of the parameters, a simulated hardware signal and its corresponding Allan deviation are updated on screen.
""")


# Containerize the sections of the main app
gyro_time_series = st.beta_container()
allan_deviation = st.beta_container()

# Simulated gyro signal section
with gyro_time_series:

    # Convert input parameters str -> float
    sim_time = float(sim_time)
    fs = float(fs)
    num_samples = int(float(sim_time)*float(fs))

    arw_coeff = float(arw_coeff)
    bi_coeff = float(bi_coeff)
    rrw_coeff = float(rrw_coeff)

    # Gyro/Accel signal
    combined_noise = np.zeros(shape=(num_samples, ))

    # Include noise source iff include variable is `True`
    if incl_arw:
        combined_noise += make_angle_random_walk_series(arw_coeff, fs, sim_time)
    if incl_bi:
        corr_time = float(corr_time)
        combined_noise += make_bias_instability_series(bi_coeff, corr_time, fs, sim_time)
    if incl_rrw:
        combined_noise += make_rate_random_walk_series(rrw_coeff, fs, sim_time)

    
    st.title("Stationary IMU Signal")
    st.write("""
    The following plot is a simulation of the data captured by the on-board computer of the IMU.

    Although the virtual IMU is completely stationary, this plot shows that the sources of noise in the system are introducing error to the measurement. 

    The plot is interactive so users can probe and investigate their results, as well as save them.
    """)

    # Plot the simulated signal
    st.line_chart(combined_noise)



# Calculated Allan deviation section
with allan_deviation:

    st.title("The Allan Deviation")
    st.write("""
    The following plot is shows the Allan deviation that corresponds to the above IMU signal.

    The Allan deviation is a clever mathematical tool that is used to identify the noise sources polluting the IMU signal. 
    The Allan deviation has further uses in quantifying the impact of those same noise sources.
    """)

    taus, allan_values = oadev(combined_noise, fs)

    log_plot = plot_log_scale(taus, allan_values)
    st.pyplot(log_plot)



        
        