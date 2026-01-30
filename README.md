# Network Design Project 

## Overview
This repository implements a UDP-based file transfer protocol across **6 phases**, progressively adding reliability mechanisms and performance evaluation. Currently, **Phase 1** is complete, which establishes the foundation through basic UDP socket communication and the RDT 1.0 protocol for reliable data transfer over a perfectly reliable channel.

## Name  email 
Song Ni  song_ni@student.uml.edu

## Demo Video (Phase 1)
- **video is available in folder "video"** 
- **Timestamped outline:**
  - 00:00 → Phase 1(a): UDP Message Echo Demonstration
  - 01:15 → Phase 1(b): RDT 1.0 BMP File Transfer
  - 02:00 → Verification: MD5 Hash Integrity Check

---

## Repository Structure (Required)
The project is organized as follows to ensure reproducibility:
---

## Requirements
- **Language/runtime:** Python 3.10 
- **OS tested:** Ubuntu (WSL2) / Linux
- **Dependencies:** - Only Python standard libraries are used: `socket`, `argparse`, `struct`, `time`. 
  - No external `pip` installations are required for Phase 1.

- built virtual environment :uv venv network_env
- activate environment: source network_env/bin/activate

---
## Standard CLI Interface 
Both programs support standardized flags to ensure consistent grading and testing. 

### Receiver 
- `--port <int>`: UDP port to bind (e.g., 9000).
- `--out <path>`: Output file path to write received bytes.
- `--seed <int>`: RNG seed (default: 0).
- `--log-level <debug|info|warning|error>` (default: info).

### Sender
- `--host <ip/hostname>`: Receiver host IP (use 127.0.0.1 for local tests).
- `--port <int>`: Receiver port.
- `--file <path>`: Input file to send.
- `--seed <int>`: RNG seed (default: 0).
- `--log-level <debug|info|warning|error>` (default: info).
---
## Quick Start 

### 1. Start Receiver and sender
Open a terminal and run the receiver first and waiting, then open another terminal to send files.
```bash
python src/receiver.py --port 9000 --out results/received.bmp

python src/sender.py --host 127.0.0.1 --port 9000 --file data/sample.bmp

### 2. Verification 
md5sum data/sample.bmp
md5sum results/received.bmp