# UnetStack Lab – Q1 to Q5

Groovy simulation scripts and a custom agent for the five UnetStack exercises.

> **Version note:** These examples target the UnetStack v7-style handbook/API. They have not been executed against your local installation. UnetStack releases and modem profiles can differ, especially in PHY frame parameters and simulation setup paths. Run one experiment at a time and compare the shell output with the expected observations below.

## 1. Folder layout

```text
unetstack-lab/
├── README.md
├── scripts/
│   ├── q1-range.groovy
│   ├── q2-raw-frames.groovy
│   ├── q3-datagrams.groovy
│   ├── q4-echo.groovy
│   └── q5-static-routing.groovy
└── classes/
    ├── EchoAgent.groovy
    └── StaticRouteInstaller.groovy
```

## 2. Install / prepare

1. Install and extract UnetStack.
2. Open a terminal in the UnetStack installation directory (the directory containing `bin/unet`).
3. Copy this repository's `scripts/*.groovy` into a convenient folder, e.g. `scripts/lab/`.
4. Copy `classes/*.groovy` into the UnetStack installation's `classes/` directory. Create `classes/` if it does not exist.
5. Make sure the `bin/unet` launcher is executable:

```bash
chmod +x bin/unet
```

The simulation scripts use the default stack at `$home/etc/setup`. If your installation uses a different default stack file, update that path in the scripts.

## 3. Run a simulation

Run from the UnetStack installation directory:

```bash
bin/unet scripts/lab/q1-range.groovy
```

The simulator prints the web and API ports for each node. Open each node's web URL in a browser, for example:

- `http://localhost:8081/`
- `http://localhost:8082/`
- `http://localhost:8083/`

Use the shell in the node web interface. The simulation runs until you stop it with `Ctrl+C`.

**Important:** Stop the current simulation with `Ctrl+C` before starting the next script. Do not run all five scripts simultaneously because their web/API ports may overlap.

If the `bin/unet` command is not found, `cd` into the UnetStack installation directory first. On Windows, use the equivalent launcher provided by your distribution.

---

# Q1 – Communication range

## Run

```bash
bin/unet scripts/lab/q1-range.groovy
```

## Test commands

Open node 1 (`http://localhost:8081/`) and run:

```groovy
ping 2
ping 3
```

Open node 2 (`http://localhost:8082/`) and run:

```groovy
ping 1
ping 3
```

Open node 3 (`http://localhost:8083/`) and run:

```groovy
ping 1
ping 2
```

The script starts with node positions 0 m, 1200 m and 2400 m. For the second placement, stop the simulation, open `q1-range.groovy`, change node 3's x-coordinate from `2400.m` to `1800.m`, save, and run it again:

```groovy
location: [1800.m, 0.m, 0.m]
```

## Expected connectivity

| Pair | Distance (placement 1) | Reachable? |
|---|---:|---|
| 1–2 | 1200 m | Yes |
| 2–3 | 1200 m | Yes |
| 1–3 | 2400 m | No |

| Pair | Distance (placement 2) | Reachable? |
|---|---:|---|
| 1–2 | 1200 m | Yes |
| 2–3 | 600 m | Yes |
| 1–3 | 1800 m | No |

The communication range is 1500 m. Detection range (2000 m) does not mean a frame can be decoded. With `pDetection = 1` and `pDecoding = 1`, frames within communication range are decoded successfully. A frame between communication and detection range may be detected but not decoded.

---

# Q2 – Raw PHY frames

## Run

```bash
bin/unet scripts/lab/q2-raw-frames.groovy
```

Node A: `http://localhost:8081/`  
Node B: `http://localhost:8082/`

At **node B**, subscribe to PHY notifications:

```groovy
subscribe phy
```

At **node A**, inspect the channel settings:

```groovy
phy[CONTROL].frameLength
phy[CONTROL].dataRate
phy[CONTROL].frameDuration

phy[DATA].frameLength
phy[DATA].dataRate
phy[DATA].frameDuration
```

Set your roll number in the following command. Replace `YOUR_ROLL_NUMBER` with the actual value (do not leave the placeholder):

```groovy
def payload = 'YOUR_ROLL_NUMBER'.bytes as byte[]
```

Send one raw frame on CONTROL and one on DATA:

```groovy
phy << new TxFrameReq(to: 20, type: CONTROL, data: payload)
phy << new TxFrameReq(to: 20, type: DATA, data: payload)
```

At node A, you should see the request accepted and a `TxFrameNtf` after transmission. At node B, look for `RxFrameNtf` and inspect:

```groovy
new String(ntf.data)
```

To calculate the nominal full-frame time from the current channel configuration:

```groovy
(phy[CONTROL].frameLength * 8.0) / phy[CONTROL].dataRate
(phy[DATA].frameLength * 8.0) / phy[DATA].dataRate
```

These are seconds because `dataRate` is in bits/s and `frameLength` is in bytes. Compare these values with `frameDuration` and the `txDuration` in `TxFrameStartNtf` if your PHY implementation reports it. Do not copy sample frame lengths/data rates from another machine: they are modem/profile dependent.

**Note:** `frameLength` is the configured PHY frame length, not the number of payload bytes in the roll number. The modem adds framing/header overhead and may reject payloads larger than the channel MTU.

---

# Q3 – Unicast and broadcast datagrams

## Run

```bash
bin/unet scripts/lab/q3-datagrams.groovy
```

Open all three node shells. The shell normally subscribes to datagram notifications automatically. If needed, subscribe explicitly:

```groovy
subscribe topic(Topics.DATAGRAM)
```

At node 1, replace the roll-number placeholder and send unicast to node 3:

```groovy
def payload = 'HELLO-YOUR_ROLL_NUMBER'.bytes
phy << new DatagramReq(to: 3, protocol: Protocol.USER, data: payload)
```

Then send broadcast (address `0`):

```groovy
phy << new DatagramReq(to: 0, protocol: Protocol.USER, data: payload)
```

At receiving nodes, inspect the latest notification and decode it:

```groovy
new String(ntf.data)
```

Expected:
- Unicast to 3: node 3 receives it; node 2 should not receive it as an addressed datagram.
- Broadcast to 0: nodes 2 and 3 receive it.

A broadcast is not an acknowledged reliable-delivery guarantee. The exact display format depends on the shell and stack version.

---

# Q4 – Custom EchoAgent

## Run

First make sure `classes/EchoAgent.groovy` is in the UnetStack installation's `classes/` directory. Then run:

```bash
bin/unet scripts/lab/q4-echo.groovy
```

Node 1: `http://localhost:8081/`  
Node 2: `http://localhost:8082/`

The node 2 stack closure loads `EchoAgent` at startup. At node 2, verify it is present:

```groovy
agents
```

At node 1, subscribe to datagram notifications:

```groovy
subscribe topic(Topics.DATAGRAM)
```

Send three messages (replace the sample values if desired):

```groovy
phy << new DatagramReq(to: 2, protocol: Protocol.USER, data: 'hello'.bytes)
phy << new DatagramReq(to: 2, protocol: Protocol.USER, data: 'unetstack'.bytes)
phy << new DatagramReq(to: 2, protocol: Protocol.USER, data: 'computer networks'.bytes)
```

Expected reply payloads have this form:

```text
HELLO @ <reception-time-in-milliseconds>
UNETSTACK @ <reception-time-in-milliseconds>
COMPUTER NETWORKS @ <reception-time-in-milliseconds>
```

The agent responds using `Protocol.DATA`, not `Protocol.USER`, to avoid echoing its own reply indefinitely.

---

# Q5 – Static routing

## Run

```bash
bin/unet scripts/lab/q5-static-routing.groovy
```

Node 11: `http://localhost:8081/`  
Node 12: `http://localhost:8082/`  
Node 13: `http://localhost:8083/`

The script places nodes at 0 m, 1000 m and 2000 m. Communication range is 1000 m, so 11 and 13 cannot communicate directly, while both can communicate with 12.

The script loads `StaticRouteInstaller` on each node. Its `startup()` method installs routes through that node's local router agent. Routes are:

| Node | Destination | Next hop |
|---|---:|---:|
| 11 | 13 | 12 |
| 12 | 13 | 13 |
| 12 | 11 | 11 |
| 13 | 11 | 12 |

At node 11 and node 13, display routes:

```groovy
routes
```

At node 11, send to node 13:

```groovy
router << new DatagramReq(to: 13, protocol: Protocol.USER, data: 'HELLO-ROUTING'.bytes)
```

At node 13, send the reply:

```groovy
router << new DatagramReq(to: 11, protocol: Protocol.USER, data: 'REPLY-RECEIVED'.bytes)
```

The route trace can be requested from the source router:

```groovy
router << new DatagramTraceReq(to: 13)
```

The route should be 11 → 12 → 13. The reverse route should be 13 → 12 → 11.

**Before-route comparison:** The exercise asks you to demonstrate failure before adding routes. For a clean before/after comparison, first run a copy of the topology without the `StaticRouteInstaller` agents, send the datagram, record the no-route failure, then run the supplied routed script. Do not expect a no-route failure after the static-route installer has already run.

---

## Evidence/screenshots checklist

- [ ] Q1: ping results for 1–2, 2–3 and 1–3 at both node-3 positions.
- [ ] Q2: node 10 transmit requests / `TxFrameNtf`; node 20 `RxFrameNtf`; channel parameter table.
- [ ] Q3: unicast send + only node 3 receive; broadcast send + node 2 and node 3 receive.
- [ ] Q4: `agents` output at node 2; three requests and three uppercase replies at node 1.
- [ ] Q5: failed pre-route attempt; route tables; successful request/reply; route trace through node 12.

## Official references

- [UnetStack Handbook – Simulating networks](https://unetstack.net/handbook/402_sim.html)
- [UnetStack Handbook – Protocol channel model](https://unetstack.net/handbook/402_sim.html#3481-protocol-channel-model)
- [UnetStack Handbook – Physical service](https://unetstack.net/handbook/305_phy.html)
- [UnetStack Handbook – Datagram service](https://unetstack.net/handbook/304_datagram.html)
- [UnetStack Handbook – Developing agents / echo daemon](https://unetstack.net/handbook/401_agents.html)
- [UnetStack Handbook – Router](https://unetstack.net/handbook/309_router.html)
