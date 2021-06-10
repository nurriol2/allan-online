import streamlit as st
import numpy as np
from plotting import plot_log_scale
from allan_variance import overlapping_allan_deviation as oadev
from noise_synthesis import make_angle_random_walk_series, make_bias_instability_series, make_rate_random_walk_series



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


# Containerize the sections of the main app
gyro_time_series = st.beta_container()
allan_deviation = st.beta_container()

with gyro_time_series:
    sim_time = float(sim_time)
    fs = float(fs)
    num_samples = int(float(sim_time)*float(fs))

    arw_coeff = float(arw_coeff)
    bi_coeff = float(bi_coeff)
    rrw_coeff = float(rrw_coeff)

    combined_noise = np.zeros(shape=(num_samples, ))

    if incl_arw:
        combined_noise += make_angle_random_walk_series(arw_coeff, fs, sim_time)
    if incl_bi:
        corr_time = float(corr_time)
        combined_noise += make_bias_instability_series(bi_coeff, corr_time, fs, sim_time)
    if incl_rrw:
        combined_noise += make_rate_random_walk_series(rrw_coeff, fs, sim_time)

    st.line_chart(combined_noise)

with allan_deviation:
    taus, allan_values = oadev(combined_noise, fs)

    log_plot = plot_log_scale(taus, allan_values)
    st.pyplot(log_plot)



        
        