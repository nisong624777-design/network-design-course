import json
import subprocess
from pathlib import Path


def fetch_workload(
    base_url: str,
    paths: list[str],
    protocol: str,
    output_dir: str,
) -> dict:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    paths_file = out_dir / "paths.txt"
    paths_file.write_text("\n".join(paths), encoding="utf-8")

    if protocol == "h2":
        cmd = [
            "python",
            "-m",
            "src.http2_fetch",
            "--base-url",
            base_url,
            "--paths-file",
            str(paths_file),
            "--output-dir",
            str(out_dir),
        ]
    elif protocol == "h3":
        cmd = [
            "python",
            "-m",
            "src.http3_fetch",
            "--base-url",
            base_url,
            "--paths-file",
            str(paths_file),
            "--output-dir",
            str(out_dir),
        ]
    else:
        raise ValueError(f"Unsupported protocol: {protocol}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        stderr_msg = result.stderr.strip()
        if stderr_msg:
            print(f"[{protocol.upper()} ERROR] {stderr_msg}", flush=True)
        return {
            "completion_time_ms": -1,
            "bytes_total": 0,
            "throughput_mbps": 0.0,
            "success_count": 0,
            "negotiated_protocols": "error",
            "success": False,
            "per_object_median_ms": 0.0,
        }

    try:
        info = json.loads(result.stdout.strip())
    except json.JSONDecodeError:
        print(f"[{protocol.upper()} ERROR] Invalid JSON output: {result.stdout}", flush=True)
        return {
            "completion_time_ms": -1,
            "bytes_total": 0,
            "throughput_mbps": 0.0,
            "success_count": 0,
            "negotiated_protocols": "error",
            "success": False,
            "per_object_median_ms": 0.0,
        }

    total_ms = float(info["elapsed_ms"])
    total_bytes = int(info["bytes_total"])
    object_count = int(info["object_count"])
    protocol_name = str(info["protocol"])

    throughput_mbps = (total_bytes * 8 / 1_000_000) / (total_ms / 1000.0) if total_ms > 0 else 0.0

    return {
        "completion_time_ms": total_ms,
        "bytes_total": total_bytes,
        "throughput_mbps": throughput_mbps,
        "success_count": object_count,
        "negotiated_protocols": protocol_name,
        "success": bool(info["success"]),
        "per_object_median_ms": total_ms / object_count if object_count > 0 else 0.0,
    }