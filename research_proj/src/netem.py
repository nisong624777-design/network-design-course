# src/netem.py
import subprocess


def run_cmd(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def apply_netem(interface: str, rtt_ms: int, loss_pct: float, jitter_ms: int = 0) -> None:
    cmd = [
        "sudo", "tc", "qdisc", "replace", "dev", interface, "root", "netem",
        "delay", f"{rtt_ms}ms", f"{jitter_ms}ms",
        "loss", f"{loss_pct}%"
    ]
    run_cmd(cmd)


def clear_netem(interface: str) -> None:
    subprocess.run(
        ["sudo", "tc", "qdisc", "del", "dev", interface, "root"],
        capture_output=True,
        text=True
    )


def capture_qdisc(interface: str) -> str:
    result = run_cmd(["tc", "qdisc", "show", "dev", interface])
    return result.stdout