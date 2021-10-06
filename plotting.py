from coefficient_fitting import fit_rate_random_walk_line, fit_random_walk_line, fit_bias_instability_line, find_index_of_closest_slope
from plotly import graph_objects as go
import plotly.express as px
import numpy as np

def get_x_axis(sim_time, fs):
    return np.linspace(0, int(sim_time), int(sim_time*fs))

def plot_time_series(time, y):

    time_series_labels = {"Time":"Time (sec)",
                        "Noise Amplitude": "Noise Amplitude (units)"}

    fig = px.line(data_frame={"Time":time, "Noise Amplitude":y},
                    x="Time",
                    y="Noise Amplitude",
                    hover_name="Noise Amplitude",
                    labels=time_series_labels)

    return fig

def plot_allan_deviation(avg_time, allan_dev, noise_model, verbose):

    allan_deviation_labels = {"Averaging Time":"\u03C4 (sec)",
                                "Allan Deviation":"\u03C3(\u03C4)"}
    
    fig = px.line(data_frame={"Averaging Time":avg_time, "Allan Deviation":allan_dev},
                    x="Averaging Time",
                    y="Allan Deviation",
                    hover_name="Allan Deviation",
                    log_x=True,
                    log_y=True,
                    labels=allan_deviation_labels)
    
    if verbose:
        if noise_model:
            rw_line = fit_random_walk_line(avg_time, allan_dev)
            fig.add_trace(go.Scatter(x=avg_time, y=rw_line[0], name=f"Random Walk", line=dict(dash="dash")))
            fig.add_annotation(xref="paper", yref="paper", x=1, y=0.2, text=f"Calculated Random Walk Coefficient: {rw_line[1]:.3}...", showarrow=False)

        if noise_model[3]:
            rrw_line = fit_rate_random_walk_line(avg_time, allan_dev)
            fig.add_trace(go.Scatter(x=avg_time, y=rrw_line[0], name="Rate Random Walk", line=dict(dash="dash")))
            fig.add_annotation(xref="paper", yref="paper", x=1, y=0.1, text=f"Calculated Rate Random Walk Coefficient: {rrw_line[1]:.3}...", showarrow=False)

        if (noise_model[1] or noise_model[2]):
            bi_line = fit_bias_instability_line(avg_time, allan_dev)
            fig.add_trace(go.Scatter(x=avg_time, y=bi_line[0], name="Bias Instability", line=dict(dash="dash")))
            fig.add_annotation(xref="paper", yref="paper", x=1, y=0.0, text=f"Calculated Bias Instability Coefficient: {bi_line[1]:.3}...", showarrow=False)

    return fig