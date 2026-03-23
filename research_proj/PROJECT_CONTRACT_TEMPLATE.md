# Project Contract (Extra Credit Research Track)

> This document is your binding agreement for Final Waiver and Automatic A eligibility.
> If the contract requirements are met by the deadlines, the outcome is guaranteed.

**Team Name:**  \ 
**Members:** song ni    song_ni@student.uml.edu  
**Survey Topic:** Family A: HTTP/2 vs HTTP/3/QUIC behaviorunder realistic conditions
**Project Title:**  When Does HTTP/3 vs HTTP/2 Performance Degrade Under Latency and Loss? A Controlled Measurement Study.
**GitHub Repo URL:**  https://github.com/nisong624777-design/network-design-course/tree/main/research_proj
**Project Category:** Measurement 

---

## 1) Survey: open question bridge
### 1.1 Three claims from your survey sources
Write 3 claim statements you found, each with a citation.

1. Claim: HTTP/3/QUIC can mitigate the impact of TCP-level head-of-line blocking on web object retrieval in the presence of packet loss.
   - Source:
   [1]Iyengar, Jana, and Martin Thomson. "RFC 9000: QUIC: A UDP-based multiplexed and secure transport." Omtermet Emgomeeromg Task Force (2021): 4.
   [2]Langley, Adam, et al. "The quic transport protocol: Design and internet-scale deployment." Proceedings of the conference of the ACM special interest group on data communication. 2017.
2. Claim:QUIC may perform more stably than traditional TCP in wireless/highly variable networks, but the effect depends on congestion control and network conditions.
   - Source:
   [1]Kakhki, Arash Molavi, et al. "Taking a long look at QUIC: an approach for rigorous evaluation of rapidly evolving transport protocols." proceedings of the 2017 internet measurement conference. 2017
   [2]Sidhu, Jashanjot Singh, et al. "From 5G RAN Queue Dynamics to Playback: A Performance Analysis for QUIC Video Streaming." IEEE Transactions on Networking 34 (2025): 2384-2399.
3. Claim:Protocol performance cannot be judged solely by averages; tail latency (such as p95/p99) is more important under interactive workloads.
   - Source:
   [1]Dean, Jeffrey, and Luiz André Barroso. "The tail at scale." Communications of the ACM 56.2 (2013): 74-80.
   [2]Li, Jialin, et al. "Tales of the tail: Hardware, os, and application-level sources of tail latency." Proceedings of the ACM Symposium on Cloud Computing. 2014.

### 1.2 Your open question
Rewrite one claim into a measurable question: Does HTTP/3 (QUIC) significantly reduce p95 tail latency compared to HTTP/2 (TCP) when fetching a high-concurrency mix of small objects (e.g., 100+) under simulated high-loss (2%-5%) and jittered wireless conditions
- **Research question (1 sentence):**
Under what network conditions (RTT and packet loss) does HTTP/3 improve completion time and tail latency compared to HTTP/2 for high-concurrency small-object workloads?
- **Hypothesis (falsifiable, 1 sentence):**
HTTP/3 will not outperform HTTP/2 under pure RTT conditions, but will demonstrate improved tail latency and more stable performance under increasing packet loss.

### 1.3 Difference from prior work
3–5 bullets that make your project unique. Examples:
- Controlled local environment using namespace + netem

- Focus on many-small-objects scenarios, rather than large file throughput. 

- Emphasize comparing p95 tail latency, instead of only looking at average completion time. 

- Perform small-scale sweeps under controlled combinations of RTT + loss + jitter. 

- Create a locally reproducible experiment pipeline, output CSVs and graphs, and emphasize reproducibility.
- 

---

## 2) Project scope
### 2.1 In scope (what you will do)
Bullet list of concrete tasks.
1.Set up a local server that supports HTTP/2 and HTTP/3

2.Construct a fixed many-small-objects dataset

3.Use tc netem to inject RTT / loss / jitter

4.Write an automated runner to execute experiments in batches and save CSVs

5.Generate 2 core charts + 1 table

6.Compare HTTP/2 and HTTP/3 p95 completion time under various conditions
### 2.2 Out of scope (what you will NOT do)
This is critical for fairness. List what you are explicitly not attempting.
1.Do not compare multiple QUIC implementations

2.Do not study all cases of 0-RTT resumption

3.Do not perform real Internet website crawling tests

4.Do not study mobile energy consumption

5.Do not perform browser engine-level page rendering analysis, only measure the time for network/transport layer completion
---

## 3) Deliverables
To qualify for final waiver + automatic A, you must deliver **all** items below.

### 3.1 Repo deliverable
Your repo must include, at minimum:

```
config/
src/
scripts/
static/
results/
README.md
```

### 3.2 Reproducibility deliverable

### 3.2.1 System Requirements
- Linux (Ubuntu recommended)
- Python 3.10+
- Root privileges (required for `tc netem` and network namespaces)
---
### 3.2.2 Create a virtual environment:
```bash
python3 -m venv network_env
source network_env/bin/activate
pip install httpx[http2] aioquic matplotlib pyyaml
```
### 3.2.3 Network Namespace setup
Create isolated client and server environments:
```bash
sudo ip netns add ns_client
sudo ip netns add ns_server
sudo ip link add veth-client type veth peer name veth-server
sudo ip link set veth-client netns ns_client
sudo ip link set veth-server netns ns_server
### assign IP address
sudo ip netns exec ns_client ip addr add 10.0.0.1/24 dev veth-client
sudo ip netns exec ns_server ip addr add 10.0.0.2/24 dev veth-server
### Bring interfaces up
sudo ip netns exec ns_client ip link set lo up
sudo ip netns exec ns_server ip link set lo up
sudo ip netns exec ns_client ip link set veth-client up
sudo ip netns exec ns_server ip link set veth-server up
### test connectivity
sudo ip netns exec ns_client ping -c 3 10.0.0.2
```
### 3.2.4 Start server (in ns_server)
```bash
sudo ip netns exec ns_server bash
cd research_project (research_project is the code folder)
caddy run --config configs/Caddyfile #here you must keep the serve monitoring 
```
### 3.2.5 Start client (in ns_client)
```bash
sudo ip netns exec ns_client bash
cd research_project
source network_env/bin/activate
```
### 3.2.6 run experiment (in ns_client)
python -m scripts.run_experiments

python -m scripts.plot_results

### 3.2.7 Output
1. Raw data: results/raw_results.csv
2. Figure 1: RTT vs completion time
2. Figure 2: Loss vs p95 completion time
```
```

### 3.3 Demo video
- Private YouTube link: https://youtu.be/s1jeDvK06Q8
- Timestamped outline (mm:ss what you show):
- 00:00~ 00:05  : show the clent and server terminal
- 00:06~ 00:20  : show the parameter setting
- 00:20~ 01:33  : run experiment and shwo result when setting workload being many-small file.
- 01:33~ 02:45  : run experiment and shwo result when setting workload being few-large file.


### 3.4 Two-page paper deliverable (IEEE 2-column format)
- Paper title: When Does HTTP/3 Improve Tail Latency Over HTTP/2 Under Network Impairments
- 2 pages (PDF), includes at least **one results figure/table**

---

## 4) Results plan
### 4.1 Primary metric(s)
List 1–3 metrics you will report (examples):
- completion time, throughput, goodput
- latency distribution (p50/p95/p99)
- fairness (Jain’s index), variability
- handshake time distribution
- energy proxy (bytes sent per delivered message)

### 4.2 Baselines
List at least 2 baselines (fair comparison points).

- Baseline A:
HTTP/2 over TCP/TLS 1.3 using HTTPX (http2=True)

- Baseline B:
HTTP/3 over QUIC using aioquic

- (Optional) Baseline C:
None
### 4.3 Controlled variables / sweep grid
List at least 2 variables you will sweep.


| Variable | Values |
|---|---|
| RTT (ms) | {0, 100, 200} |
| Packet Loss (%) | {0, 1, 3, 5} |

### 4.4 Required figures/plots/tables
List the **exact** outputs you promise to deliver.

| Item | X-axis | Y-axis | Sweep/conditions | Output filename |
|---|---|---|---|---|
| Figure 1 | RTT | Median completion time | many_small workload, loss=0 | fig_rtt_many_small.png |
| Figure 2 | Packet loss | p95 completion time | many_small workload, RTT=50ms | fig_loss_many_small.png |
| Figure 3 | RTT | Median completion time | few_large workload | fig_rtt_few_large.png |
| Figure 4 | Packet loss | p95 completion time | few_large workload | fig_loss_few_large.png |

---

## 5) Implementation plan
### 5.1 Architecture sketch
Flow:
Client → namespace → netem → server → response → CSV → plots

### 5.2 Key data structures
Main components:
- Caddy server (HTTP/2 + HTTP/3)
- Python client runner
- Network emulation (tc netem)
- Plotting script
---

## 6) Validation checks
You must include at least **two** checks that prove your measurements are meaningful.

| Validation check | What evidence you will record | Pass condition |
|---|---|---|
| Network impairments applied | tc qdisc snapshot per run | delay/loss matches configuration |
| Protocol negotiation | client logs (HTTP/2 vs h3) | correct protocol used |
---

## 7) Checkpoints and deadlines
Your team must meet **all** checkpoints.

### Checkpoint 0: Approval
- [ ] Contract is specific enough to approve (baselines + sweeps + outputs + commands)
- [ ] Repo created with skeleton + README stub

### Checkpoint 1: Baseline
- [ ] Baseline run works end-to-end
- [ ] At least one preliminary figure/table generated from real measurements/data
- [ ] Evidence recorded for validation checks (initial)

### Checkpoint 2: Pipelines
- [ ] Full experiment pipeline runs end-to-end
- [ ] CSV output + at least two final-quality figures (or 1 figure + 1 table)

### Checkpoint 3: Final
- [ ] Demo video complete (timestamped)
- [ ] Repo reproducible from README commands
- [ ] 2-page paper PDF submitted

---

## 8) Team plan (required)
### 8.1 Ownership
| Task | Owner | Due checkpoint | Definition of done |
|---|---|---|---|
| Literature scan + delta bullets |  |  |  |
| Harness / pipeline |  |  |  |
| Experiments + CSV |  |  |  |
| Plotting + figures |  |  |  |
| Paper draft |  |  |  |
| Demo video |  |  |  |

### 8.2 Meetings
- How often you will sync as a team:
- How you will communicate:

---

## 9) Edge cases and tests
### 9.1 Top edge cases you will test
| Edge case | Why it matters | How you will test | Expected behavior |
|---|---|---|---|
| High packet loss (5%) | stress QUIC recovery | run loss=5% | H3 more stable |
| RTT=0ms | baseline sanity check | run RTT=0 | minimal latency |

### 9.2 Minimal test plan
- Integration tests (required): e.g., “run pipeline and verify outputs exist + schema sanity”
- Unit tests (optional):

---

## 10) Instructor/TA approval notes (To be filled out after being graded)
- Decision: (Approved / Revise and resubmit)
- Notes:
