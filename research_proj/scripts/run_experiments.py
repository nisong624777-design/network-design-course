# scripts/run_experiments.py
import csv
import os
import time
import yaml
from pathlib import Path

from src.netem import apply_netem, clear_netem, capture_qdisc
from src.server_control import ServerController
from src.client_runner import fetch_workload


def load_paths(path_file: str) -> list[str]:
    with open(path_file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def ensure_csv(csv_path: str) -> None:
    Path(csv_path).parent.mkdir(parents=True, exist_ok=True)
    if not Path(csv_path).exists():
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "protocol", "rtt_ms", "loss_pct", "jitter_ms", "object_mix", "run_id",
                "num_objects", "bytes_total", "completion_time_ms", "throughput_mbps",
                "negotiated_protocols", "success", "qdisc_snapshot"
            ])


def append_row(csv_path: str, row: list) -> None:
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(row)


def main():
    with open("configs/experiment.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    base_url = cfg["server"]["base_url"]
    interface = cfg["network"]["interface"]
    output_csv = cfg["experiment"]["output_csv"]
    repetitions = cfg["experiment"]["repetitions"]
    cooldown_sec = cfg["experiment"]["cooldown_sec"]
    log_dir = cfg["experiment"]["log_dir"]

    Path(log_dir).mkdir(parents=True, exist_ok=True)
    ensure_csv(output_csv)

    # server = ServerController(cfg["server"]["caddyfile"])
    # server.start()

    try:
        for object_mix, workload_cfg in cfg["workloads"].items():
            paths = load_paths(workload_cfg["object_paths_file"])
            for protocol in cfg["protocols"]:
                for rtt_ms in cfg["network"]["rtt_ms"]:
                    for loss_pct in cfg["network"]["loss_pct"]:
                        for jitter_ms in cfg["network"]["jitter_ms"]:
                            apply_netem(interface, rtt_ms, loss_pct, jitter_ms)
                            qdisc_snapshot = capture_qdisc(interface).strip().replace("\n", " | ")

                            for run_id in range(1, repetitions + 1):
                                out_dir = f"./results/tmp/{protocol}_{object_mix}_{rtt_ms}_{loss_pct}_{jitter_ms}_{run_id}"
                                os.makedirs(out_dir, exist_ok=True)

                                result = fetch_workload(base_url, paths, protocol, out_dir)
                                # result = fetch_workload(base_url, paths, protocol, out_dir, max_workers=10)

                                append_row(output_csv, [
                                    protocol,
                                    rtt_ms,
                                    loss_pct,
                                    jitter_ms,
                                    object_mix,
                                    run_id,
                                    len(paths),
                                    result["bytes_total"],
                                    result["completion_time_ms"],
                                    result["throughput_mbps"],
                                    result["negotiated_protocols"],
                                    result["success"],
                                    qdisc_snapshot,
                                ])
                                print(
                                        f"[RUN] protocol={protocol} mix={object_mix} rtt={rtt_ms} "
                                        f"loss={loss_pct} jitter={jitter_ms} run={run_id} "
                                        f"success={result['success']} time_ms={result['completion_time_ms']:.2f}",
                                        flush=True
                                    )
                                print(capture_qdisc(interface))
                                time.sleep(cooldown_sec)

                            clear_netem(interface)

    finally:
        clear_netem(interface)
        # server.stop()


if __name__ == "__main__":
    main()