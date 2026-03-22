# src/metrics.py
import pandas as pd


def summarize_results(input_csv: str, output_csv: str) -> None:
    df = pd.read_csv(input_csv)

    grouped = df.groupby(["protocol", "rtt_ms", "loss_pct", "jitter_ms", "object_mix"])
    summary = grouped["completion_time_ms"].agg(
        runs="count",
        mean_ms="mean",
        median_ms="median",
        p95_ms=lambda s: s.quantile(0.95),
        p99_ms=lambda s: s.quantile(0.99),
    ).reset_index()

    throughput = grouped["throughput_mbps"].mean().reset_index(name="avg_throughput_mbps")
    summary = summary.merge(
        throughput,
        on=["protocol", "rtt_ms", "loss_pct", "jitter_ms", "object_mix"],
        how="left"
    )
    summary.to_csv(output_csv, index=False)