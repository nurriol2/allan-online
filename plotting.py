import matplotlib.pyplot as plt
import streamlit as st

def plot_log_scale(x, y):

    fig, ax = plt.subplots()

    ax.loglog(x, y)
    plt.title("Allan Deviation of Simulated Signal")
    plt.ylabel("Allan Deviation $\sigma(\\tau)$")
    plt.xlabel("Averaging Time $\\tau$ (sec)")
    plt.grid(b=True)

    return fig 