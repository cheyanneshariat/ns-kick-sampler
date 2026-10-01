"""Plot the sampled global kick-speed distribution; requires Matplotlib."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ns_kick_sampler import sample_kick_speeds


def main():
    speeds = sample_kick_speeds(1_000_000, seed=67)
    log_bins = np.linspace(np.log10(0.05), np.log10(1000), 85)
    density, edges = np.histogram(np.log10(speeds), bins=log_bins, density=True)

    plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 11})
    fig, ax = plt.subplots(figsize=(6.4, 4.2), layout="constrained")
    ax.stairs(density, 10**edges, fill=True, color="#8fbfb7", alpha=0.4, linewidth=0)
    ax.stairs(density, 10**edges, color="#222222", linewidth=1.3)
    ax.set_xscale("log")
    ax.set_xlim(1, 1000)
    ax.set_ylim(bottom=0)
    ax.set_xticks([1, 10, 100, 1000], labels=["1", "10", "100", "1000"])
    ax.set_xlabel(r"natal-kick speed [km s$^{-1}$]", fontsize=18)
    ax.set_ylabel(r"$dP/d\log_{10}(v)$", fontsize=18)
    ax.set_title("global NS kick distribution", fontsize=18, pad=10)
    ax.tick_params(which="both", direction="in", top=True, right=True)
    fig.savefig(Path(__file__).with_name("kick_distribution.png"), dpi=240)
    plt.close(fig)
    print("Saved kick_distribution.png (1,000,000 samples; seed=67)")


if __name__ == "__main__":
    main()
