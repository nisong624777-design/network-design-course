import os
import pandas as pd
import matplotlib.pyplot as plt


def p95(series):
    return series.quantile(0.95)


def main():
    df = pd.read_csv("./results/raw_results.csv")
    os.makedirs("./results/figures", exist_ok=True)

    # 只保留成功的实验
    df = df[df["success"] == True].copy()

    # -----------------------------
    # Figure 1: completion time vs RTT
    # Fix loss=0, jitter=0
    # -----------------------------
    rtt_df = df[
        (df["loss_pct"] == 0) &
        (df["jitter_ms"] == 0)
    ]

    fig1_df = (
        rtt_df.groupby(["protocol", "rtt_ms", "object_mix"])["completion_time_ms"]
        .median()
        .reset_index()
        .sort_values(["protocol", "object_mix", "rtt_ms"])
    )

    for object_mix in fig1_df["object_mix"].unique():
        subset = fig1_df[fig1_df["object_mix"] == object_mix]

        plt.figure(figsize=(7, 5))
        for protocol in subset["protocol"].unique():
            p = subset[subset["protocol"] == protocol]
            plt.plot(p["rtt_ms"], p["completion_time_ms"], marker="o", label=protocol)

        plt.xlabel("RTT (ms)")
        plt.ylabel("Median Completion Time (ms)")
        plt.title(f"Completion Time vs RTT ({object_mix}, loss=0%, jitter=0ms)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"./results/figures/fig_completion_vs_rtt_{object_mix}.png")
        plt.close()

    # -----------------------------
    # Figure 2: p95 completion time vs loss
    # Fix rtt=50, jitter=0
    # -----------------------------
    loss_df = df[
        (df["rtt_ms"] == 50) &
        (df["jitter_ms"] == 0)
    ]

    fig2_df = (
        loss_df.groupby(["protocol", "loss_pct", "object_mix"])["completion_time_ms"]
        .apply(p95)
        .reset_index()
        .sort_values(["protocol", "object_mix", "loss_pct"])
    )

    for object_mix in fig2_df["object_mix"].unique():
        subset = fig2_df[fig2_df["object_mix"] == object_mix]

        plt.figure(figsize=(7, 5))
        for protocol in subset["protocol"].unique():
            p = subset[subset["protocol"] == protocol]
            plt.plot(p["loss_pct"], p["completion_time_ms"], marker="o", label=protocol)

        plt.xlabel("Loss (%)")
        plt.ylabel("p95 Completion Time (ms)")
        plt.title(f"p95 Completion Time vs Loss ({object_mix}, RTT=50ms, jitter=0ms)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"./results/figures/fig_p95_vs_loss_{object_mix}.png")
        plt.close()


if __name__ == "__main__":
    main()