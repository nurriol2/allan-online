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

def plot_allan_deviation(avg_time, allan_dev):

    allan_deviation_labels = {"Averaging Time":"\u03C4 (sec)",
                                "Allan Deviation":"\u03C3(\u03C4)"}
    
    fig = px.line(data_frame={"Averaging Time":avg_time, "Allan Deviation":allan_dev},
                    x="Averaging Time",
                    y="Allan Deviation",
                    hover_name="Allan Deviation",
                    log_x=True,
                    log_y=True,
                    labels=allan_deviation_labels)

    return fig