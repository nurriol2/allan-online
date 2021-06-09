import streamlit as st
import numpy as np



# Initialize simulation parameters
st.sidebar.title("Simulation Parameters")
experiment_length = st.sidebar.text_input(
    label="Simulation Length (sec)",
    value=100
)

fs = st.sidebar.text_input(
    label="Sampling Rate (Hz)",
    value=10
)

num_samples = int(float(experiment_length)*float(fs))
st.sidebar.markdown(f"Generating {num_samples} data points")



# Initialize noise parameters
st.sidebar.title("Noise Parameters")
st.sidebar.header("Angle Random Walk (ARW)")
arw_coeff = st.sidebar.text_input(
    label="ARW Coefficient (\u00B0/\u221Asec)",
    value=0.25
)

st.sidebar.header("Bias Instability (BI)")
bi_coeff = st.sidebar.text_input(
    label="BI Coefficient (\u00B0/\u221Asec)",
    value=10
)

corr_time = st.sidebar.text_input(
    label="Correlation Time (units)",
    value = 1000

)

st.sidebar.header("Rate Random Walk (RRW)")
rrw_coeff = st.sidebar.text_input(
    label="RRW Coefficient (units/sec\u2022\u221Asec)",
    value=0.01
)


# Containerize the sections of the main app
simulation_time_series = st.beta_container()
allan_deviation = st.beta_container()