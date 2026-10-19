# AUTOSAR ADAPTIVE PLATFORM SPECIFICATION
## High-Level Design (HLD) & Interface Control Document
### Next-Generation Electric Powertrain Domain Controller (ePDC)
> **SYNTHETIC ACADEMIC SPECIFICATION — FOR BENCHMARK EVALUATION ONLY**

---

<!-- Page 1 -->
## Page 1: Title & Document Metadata

# AUTOSAR ADAPTIVE PLATFORM SPECIFICATION

### High-Level Design Specification (HLD) & Interface Control Document

| Metadata Attribute | Specification Value |
| :--- | :--- |
| **Document Identifier** | HLD-AUTOSAR-EPDC-2026-V1.0 |
| **Document Revision** | Version 1.0 (Comprehensive Release) |
| **Standard Baseline** | AUTOSAR Adaptive Platform Release 22-11 (Synthetic Interpretation) |
| **Safety Integrity Level** | ISO 26262 ASIL-D (Powertrain Safety Envelope) |
| **Security Level** | ISO/SAE 21434 / CAL-4 (Cryptographic Security Level) |
| **Target Architecture** | Dual Heterogeneous Multicore (ARM Cortex-A78AE + Cortex-R52) |
| **Author / Engineering Group** | Automotive Systems Architecture & RAG Research Group |
| **Academic Institution** | SASTRA Deemed University — School of Computing |
| **Publication Date** | October 2026 |
| **Verification Status** | Approved for AI Document Intelligence & RAG Evaluation |

> **Academic & Synthetic Integrity Notice**: This document is a synthetic, illustrative High-Level Design (HLD) engineering document created strictly for academic research, document intelligence benchmarking, and AI evaluation of the AUTOSAR AI platform. It is NOT an authentic OEM or commercial automotive document and does NOT claim official compliance with any commercial vehicle platform. All requirements, component architectures, port mappings, and performance budgets are simulated engineering assumptions.


---

<!-- Page 2 -->
## Page 2: Document Control, Revisions & Sign-Offs

### Document Management & Governance

This High-Level Design specification governs the architectural decomposition, software component interfaces, scheduling paradigms, functional safety mechanisms, and execution profiles for the synthetic AUTOSAR Adaptive Platform Electric Powertrain Domain Controller (ePDC). All updates must follow strict document change governance.

#### Revision History

| Rev | Date | Primary Author | Description of Changes | Approval |
| :--- | :--- | :--- | :--- | :--- |
| 0.1 | 2026-01-15 | Arch Team | Initial draft of powertrain component decomposition and interfaces | Internal |
| 0.5 | 2026-03-20 | Safety Eng | Incorporated ISO 26262 ASIL-D torque safety envelope and interlocks | Reviewed |
| 0.8 | 2026-06-10 | Comms Team | Integrated SOME/IP serialization and Service Discovery definitions | Reviewed |
| 0.9 | 2026-08-05 | Sec Specialist | Added SecOC message authentication and TARA threat mitigations | Validated |
| 1.0 | 2026-10-18 | Lead Architect | Final comprehensive 101-page baseline for AI evaluation benchmarks | APPROVED |

#### Engineering Authority Sign-Off Table

| Role | Name | Department / Affiliation | Signature / Status | Sign-Off Date |
| :--- | :--- | :--- | :--- | :--- |
| Lead Systems Architect | Dr. K. S. Ramanathan | Automotive Embedded Systems Division | APPROVED | 2026-10-18 |
| Functional Safety Manager | M. V. Janardhanan | Vehicle Safety & Reliability Engineering | APPROVED (ASIL-D) | 2026-10-18 |
| Cybersecurity Architect | S. Anand | Automotive Cybersecurity Group | APPROVED (CAL-4) | 2026-10-18 |
| Software Release Lead | Abineswari P. | AUTOSAR AI Implementation Program | FINAL RELEASE | 2026-10-19 |

#### Target Hardware Execution Environment

The reference target hardware platform comprises an automotive-grade multi-core System-on-Chip (SoC) featuring four ARM Cortex-A78AE application cores operating at 2.0 GHz running POSIX-compliant Adaptive Autosar OS (QNX Neutrino / Real-Time Linux), paired with dual ARM Cortex-R52 real-time lockstep safety processor cores operating at 800 MHz dedicated to the ASIL-D Emergency Cutoff and Watchdog supervisor.


---

<!-- Page 3 -->
## Page 3: Comprehensive Architecture Table of Contents

### Table of Contents (Chapters 1 to 23)

| Ch. | Chapter Title | Primary Architectural Focus | Page Range |
| :--- | :--- | :--- | :--- |
| 1 | Document Scope, Purpose & Assumptions | Operational boundaries, terminology, and synthetic baseline | Pages 4–4 |
| 2 | System Overview & Powertrain Context | Electric Powertrain Domain Controller topology & high-level architecture | Pages 5–8 |
| 3 | Stakeholders, System Context & Actors | Vehicle interfaces, external ECUs, CAN-FD, FlexRay, Ethernet bus links | Pages 9–12 |
| 4 | Functional Requirements Catalog | Complete requirements catalog REQ-PWR-001 through REQ-PWR-040 | Pages 13–18 |
| 5 | Non-Functional Requirements & Performance Targets | Timing budgets, latency guarantees, availability, resource budgets | Pages 19–22 |
| 6 | AUTOSAR Adaptive Platform Architecture | Adaptive Runtime for Applications (ARA), Execution Manifests, Machine Manifests | Pages 23–26 |
| 7 | Application Design & Component Decomposition | Core SWC decomposition (PowertrainManager, TorqueArbitration, etc.) | Pages 27–32 |
| 8 | Software Component Detailed Responsibilities | State machines, torque blending algorithms, and component invariants | Pages 33–38 |
| 9 | Execution Management & Process Lifecycle | Process states, startup order, dependency graphs, and State Client APIs | Pages 39–43 |
| 10 | Runnable Entities, Scheduling & Core Pinning | Execution periods (1ms to 1000ms), priorities, CPU core affinity tables | Pages 44–48 |
| 11 | Communication Management & SOA Architecture | SOME/IP bindings, Service Discovery, Publish-Subscribe, Method Calls | Pages 49–53 |
| 12 | Interfaces, Ports & Data Type Catalog | Port prototypes, Service Interfaces, Data structures, Physical signal ranges | Pages 54–60 |
| 13 | SOME/IP Protocols & Service Discovery | Service IDs, Method IDs, Eventgroup mappings, Multicast UDP routing | Pages 61–65 |
| 14 | Data Models, Persistence & Storage Architecture | Key-Value Storage, File Storage, Flash wear-leveling, Backup pools | Pages 66–69 |
| 15 | Diagnostics, Logging & Health Monitoring | UDS on IP (DoIP), Diagnostic Trouble Codes (DTCs), DLT logging filters | Pages 70–74 |
| 16 | Error Handling, Degraded Modes & Recovery | Fault Containment Regions (FCR), Limp-Home modes, Safe states | Pages 75–78 |
| 17 | Functional Safety Concept (ISO 26262) | ASIL-D decomposition, E2E protection profiles, Safety invariants | Pages 79–83 |
| 18 | Cybersecurity Concept (ISO/SAE 21434) | TARA threat catalog, SecOC, TLS 1.3, Crypto Service (CRY), Secure Boot | Pages 84–87 |
| 19 | Performance, Latency & Resource Budgets | End-to-End latency budgets, Ethernet bandwidth, RAM and Flash budgets | Pages 88–90 |
| 20 | Startup, Shutdown, Deployment & Update (UCM) | Power states, A/B partition updates, Rollback protection, Manifest staging | Pages 91–93 |
| 21 | Verification, Validation & Testing Strategy | MIL/SIL/HIL testing, Fault injection, Acceptance criteria, Test harness | Pages 94–96 |
| 22 | Architectural Trade-Offs & Documented Omissions | Design decisions, trade-off analysis, explicit out-of-scope exclusions | Pages 97–98 |
| 23 | Appendices, Traceability Matrix & Glossary | Requirements Traceability Matrix (RTM), Interface cross-ref, Glossary | Pages 99–101 |


---

<!-- Page 4 -->
## Page 4: 1.1 Purpose, Boundaries, and Synthetic Baseline

### 1.1 Document Scope and Purpose

This document defines the High-Level Design (HLD) specification for the synthetic Electric Powertrain Domain Controller (ePDC), an advanced Electronic Control Unit (ECU) implemented on the AUTOSAR Adaptive Platform. The primary objective of this architecture is to provide a deterministic, high-assurance software environment capable of coordinating electric traction motor torque, high-voltage battery state management, multi-loop thermal regulation, and vehicle motion stability while satisfying stringent ISO 26262 ASIL-D functional safety constraints.

#### 1.2 Target Audience & Engineering Assumptions

This specification serves system architects, safety engineers, software developers, and verification teams. The software components specified herein execute within an Adaptive AUTOSAR runtime environment compliant with POSIX PSE52 profiles. Real-time safety monitors execute within a hardware-isolated lockstep companion core.

> **Explicit Architectural Boundary: Synthetic Nature**: This entire specification is an engineering synthesis created for benchmarking automated RAG systems. It is not an actual production design. Operating voltages, communication cycle times, and torque blending equations represent typical automotive figures but are non-binding outside this academic evaluation framework.

| Assumption ID | Engineering Assumption Description | Architectural Impact | Safety Relevance |
| :--- | :--- | :--- | :--- |
| ASM-GEN-001 | Dual 800V silicon carbide (SiC) traction inverter topology | Dictates dual torque command interfaces (Front/Rear motors) | ASIL-D |
| ASM-GEN-002 | Deterministic Gigabit Ethernet backbone with TSN (IEEE 802.1Q) | SOME/IP packets guaranteed < 1.0 ms network transit latency | ASIL-B |
| ASM-GEN-003 | Persistent storage hosted on automotive UFS 3.1 with SLC cache | Write cycles limited to 100k blocks; wear leveling required | QM |
| ASM-GEN-004 | External battery contactors managed by dedicated hardware interlock | Emergency cutoff signals disconnect contactors within 10 ms | ASIL-D |


---

<!-- Page 5 -->
## Page 5: 2.1 Powertrain System Architecture & Topology

### 2.1 Electric Powertrain Domain Controller Overview

The Electric Powertrain Domain Controller (ePDC) functions as the central computation hub for electric propulsion in modern high-performance battery electric vehicles (BEVs). It directly arbitrates driver acceleration and deceleration intents, interacts with advanced driver assistance systems (ADAS) via service-oriented SOME/IP interfaces, manages energy flow to and from the high-voltage battery, and coordinates dynamic cooling loops across motors, inverters, and battery cells.

#### 2.2 High-Level Physical Architecture Topology

```text
+---------------------------------------------------------------------------------------------------+
|                           ELECTRIC VEHICLE POWERTRAIN ARCHITECTURE                                |
|                                                                                                   |
|  [Driver Inputs]        [ADAS Domain Core]        [Battery Pack 800V]       [Thermal Chiller/Pump]|
|  Accel/Brake Pedals     SOME/IP Trajectory Cmd    BMS Cell Telemetry        Coolant Valve Sensors |
|         |                        |                         |                         |            |
|         v                        v                         v                         v            |
|  +---------------------------------------------------------------------------------------------+  |
|  |                 AUTOSAR ADAPTIVE PLATFORM — POWERTRAIN DOMAIN CONTROLLER (ePDC)             |  |
|  |                                                                                             |  |
|  |  +------------------------+  +--------------------------+  +-----------------------------+  |  |
|  |  | PowertrainManager_SWC  |  |   TorqueArbitration_SWC  |  |   BatteryManagement_SWC     |  |  |
|  |  | Mode Coordination & FSM|  |   Driver & ADAS Blending |  |   SOC, SOH, Power Envelope  |  |  |
|  |  +------------------------+  +--------------------------+  +-----------------------------+  |  |
|  |              ^                            ^                               ^                 |  |
|  |              |                            |                               |                 |  |
|  |  +------------------------+  +--------------------------+  +-----------------------------+  |  |
|  |  |  VehicleMotion_SWC     |  |   ThermalManagement_SWC  |  |    EmergencyCutoff_SWC      |  |  |
|  |  |  Slip & Stability Reg  |  |   Multi-Loop Heat Exch   |  |    ASIL-D Safety Supervisor |  |  |
|  |  +------------------------+  +--------------------------+  +-----------------------------+  |  |
|  +---------------------------------------------------------------------------------------------+  |
|         |                                    |                                       |            |
|         v                                    v                                       v            |
|  [Front Inverter (SiC)]             [Rear Inverter (SiC)]                 [High-Voltage Interlock]|
|  CAN-FD 5 Mbps 2ms                  CAN-FD 5 Mbps 2ms                     Direct Hardwired GPIO   |
+---------------------------------------------------------------------------------------------------+
```

The controller hosts six core Software Components (SWCs), two auxiliary controllers (InverterController_SWC, RegenerativeBraking_SWC), and an isolated ASIL-D safety monitor executing on a dedicated lockstep micro-core. The physical interfaces comprise automotive Gigabit Ethernet (1000BASE-T1) connecting to the vehicle backbone, dual CAN-FD channels connecting to motor inverters, and hardwired discrete digital pins for the high-voltage interlock line.


---

<!-- Page 6 -->
## Page 6: 2.2 Powertrain Operational Modes & Transitions

### 2.2 Operational States and System Modes

The ePDC software enforces a deterministic finite state machine governing powertrain lifecycle states. Under no circumstances may motor torque be delivered when the system is not in the RUN_ACTIVE state. Transitions between states require explicit multi-condition validation across battery pre-charge status, inverter ready flags, and safety interlock continuity.

| State Name | Entry Conditions | Allowable Actions | Exit Triggers | Target Safe State |
| :--- | :--- | :--- | :--- | :--- |
| PWR_OFF | Ignition clamp 15 OFF, HV contactors open | Low-power standby monitoring only; no actuation | Clamp 15 wake-up pulse | PWR_OFF |
| PWR_STANDBY | Clamp 15 ON, 12V bus valid, HV pre-charge initiated | Sensors initialized, self-tests executing; zero torque | Pre-charge complete or fault | PWR_OFF |
| PWR_PRECHARGE | Pre-charge resistor connected, capacitor charging | Capacitor voltage ramp verified against battery voltage | Delta V < 10V within 500ms | PWR_FAULT |
| PWR_READY | Main contactors closed, inverters initialized | Ready to drive; contactors locked; zero torque default | Driver selects D/R gear | PWR_STANDBY |
| RUN_ACTIVE | Gear engaged, brake pedal released, safety loop intact | Full torque arbitration active, motor actuation enabled | Gear to P/N or fault detect | RUN_DEGRADED |
| RUN_DEGRADED | Thermal threshold exceeded or cell imbalance detected | Torque output capped at 40% maximum; warnings active | Critical fault or ignition off | PWR_SAFE_STOP |
| PWR_SAFE_STOP | Torque violation detected (> 50Nm over command) | Inverter PWM immediately disabled, mechanical brakes primed | Vehicle speed = 0 km/h | PWR_OFF |
| PWR_FAULT | Critical ASIL-D safety violation or interlock break | Immediate pyrotechnic fuse or contactor opening | Manual service reset only | PWR_OFF |

> **Safety Requirement SR-PWR-010 (State Invariant)**: The transition from RUN_ACTIVE to PWR_SAFE_STOP must initiate inverter zero-torque control within 10 ms of fault assertion. If inverters fail to respond within 20 ms, the EmergencyCutoff_SWC shall assert the hardware interlock to physically decouple the high-voltage contactors.


---

<!-- Page 7 -->
## Page 7: 2.3 High-Voltage Power Distribution & Energy Path

### 2.3 High-Voltage Energy Architecture

The vehicle electrical architecture utilizes an 800V nominal lithium-ion battery pack with a total energy capacity of 96 kWh, constructed from 192 cells in series (2P192S configuration). The battery delivers continuous electrical power of up to 350 kW to front and rear dual-inverter traction drives, and absorbs up to 250 kW during high-deceleration regenerative braking events.

#### Power Distribution Specifications

| Subsystem Parameter | Nominal Value | Minimum Operating Limit | Maximum Continuous Limit | Overvoltage Cutoff |
| :--- | :--- | :--- | :--- | :--- |
| Pack Voltage | 800 V DC | 620 V DC (0% SOC) | 890 V DC (100% SOC) | 920 V DC (Instant Cutoff) |
| Peak Discharge Current | 500 A (10 seconds) | 0 A | 450 A (Continuous) | 600 A (Pyrofuse Trigger) |
| Peak Regenerative Current | 320 A (10 seconds) | 0 A | 250 A (Continuous) | 350 A (Software Clamp) |
| Front Motor Power | 160 kW continuous | 0 kW | 200 kW peak (5 sec) | 210 kW hard limit |
| Rear Motor Power | 220 kW continuous | 0 kW | 280 kW peak (5 sec) | 300 kW hard limit |
| DC Fast Charge Acceptance | 270 kW peak | 10 kW | 150 kW average (10-80%) | 300 kW peak pulse |

To prevent catastrophic thermal runaway and cell damage, the BatteryManagement_SWC computes continuous real-time discharge and charge power limits ($P_{discharge\_max}$, $P_{charge\_max}$) at a 10 ms cyclic rate. These limits are transmitted via SOME/IP service interfaces to the TorqueArbitration_SWC, which clips the requested motor torque accordingly.


---

<!-- Page 8 -->
## Page 8: 2.4 Dual Traction Motor Drive Topology

### 2.4 Dual Electric Drive Subsystem (Front & Rear Motors)

The powertrain implements an all-wheel-drive (AWD) torque-vectoring architecture featuring an interior permanent magnet synchronous motor (IPMSM) on the rear axle and an induction asynchronous motor (ASM) on the front axle. This combination provides high efficiency during steady cruising (by de-energizing the front induction motor with zero drag losses) and immediate high torque response during dynamic acceleration.

| Drive Attribute | Front Axle Motor (Induction) | Rear Axle Motor (Permanent Magnet) | Combined AWD System |
| :--- | :--- | :--- | :--- |
| Motor Topology | 3-phase AC Induction Motor (ASM) | 3-phase AC Permanent Magnet (IPMSM) | Hybrid Dual-Technology AWD |
| Peak Torque | 280 Nm @ 0–4500 RPM | 450 Nm @ 0–5500 RPM | 730 Nm Wheel-Equivalent |
| Continuous Torque | 180 Nm | 320 Nm | 500 Nm Continuous |
| Max Rotor Speed | 16,000 RPM | 18,000 RPM | Electronically Synchronized |
| Inverter Technology | Silicon Carbide (SiC) MOSFET | Silicon Carbide (SiC) MOSFET | Dual Inverter Control |
| Cooling Medium | Dielectric Oil Direct Spray | Dielectric Oil + Water Glycol Jacket | Integrated Multi-Loop Chiller |
| Inverter Interface | CAN-FD Bus 1 (2 ms cycle) | CAN-FD Bus 2 (2 ms cycle) | Dual Redundant Channels |

Torque distribution between the front and rear axles is calculated by VehicleMotion_SWC based on dynamic axle load transfer, steering angle, yaw rate error, and tire slip ratios. The resulting torque targets ($T_{cmd\_front}$, $T_{cmd\_rear}$) are forwarded to TorqueArbitration_SWC for safety envelope compliance checks.


---

<!-- Page 9 -->
## Page 9: 3.1 Vehicle System Context & Communication Topology

### 3.1 Vehicle System Context Diagram

The Electric Powertrain Domain Controller does not operate in isolation; it interfaces with six major vehicle electronic control units across three heterogeneous bus networks: Deterministic Automotive Ethernet (1000BASE-T1), High-Speed CAN-FD (5 Mbps), and hardwired safety-critical discrete circuits.

| Interfacing ECU / Actor | Bus Type & Protocol | Cycle Rate | Payload Description | ASIL Level |
| :--- | :--- | :--- | :--- | :--- |
| Body Control Module (BCM) | Ethernet / SOME/IP | 100 ms | Ignition clamp status, door interlocks, crash notification | ASIL-B |
| ADAS Central Computer | Ethernet / SOME/IP | 10 ms | Autonomous trajectory acceleration demand (-5.0 to +3.5 m/s2) | ASIL-D |
| Braking System ECU (ESC/EBS) | CAN-FD / SecOC | 10 ms | Wheel speeds, friction brake pressure, regen limit requests | ASIL-D |
| Steering Control Unit (EPS) | CAN-FD / SecOC | 10 ms | Steering wheel angle, pinion torque, driver hands-on detection | ASIL-B |
| Front Motor Inverter | Dedicated CAN-FD 1 | 2 ms | Actual torque feedback, rotor position, inverter temperature | ASIL-D |
| Rear Motor Inverter | Dedicated CAN-FD 2 | 2 ms | Actual torque feedback, rotor position, inverter temperature | ASIL-D |
| Charging Interface Controller | Ethernet / SOME/IP | 50 ms | Plug state, DC charge current capability, grid lock status | ASIL-C |
| Crash Pyrofuse Actuator | Hardwired Discrete | Continuous | Hardware pyrotechnic disconnect trigger pulse | ASIL-D |


---

<!-- Page 10 -->
## Page 10: 3.2 Hardware/Software Boundary & Microcontroller Map

### 3.2 Hardware-Software Interface (HSI)

The ePDC software interacts with hardware peripherals via standard AUTOSAR Adaptive Microcontroller Abstraction and POSIX IO drivers. The physical hardware provides hardware security modules (HSM) for cryptographic acceleration and hardware timers for sub-microsecond timestamping.

| Physical Resource | Hardware Specification | Mapped AUTOSAR Driver | Access Restrictions | Driver Priority |
| :--- | :--- | :--- | :--- | :--- |
| Ethernet MAC 0 | 1 Gbps RGMII / IEEE 802.1AS | EthIf / ComM Driver | Ring 0 Adaptive Kernel | High |
| CAN-FD Controller 1 | Bosch M_CAN IP / 5 Mbps | CanIf / CAN Driver | POSIX Character Device | High |
| CAN-FD Controller 2 | Bosch M_CAN IP / 5 Mbps | CanIf / CAN Driver | POSIX Character Device | High |
| Hardware Security Module | Evita Full / Secure Core | CryptoStack / ARA::CRY | Protected Secure Enclave | Critical |
| Flash Memory (eMMC/UFS) | 128 GB UFS 3.1 / SLC Pool | Persistency / ARA::PER | Encrypted Partition Only | Normal |
| Hardware Watchdog | External Windowed Watchdog | Watchdog Driver | Lockstep Core Direct Line | Real-Time |


---

<!-- Page 11 -->
## Page 11: 3.3 Stakeholder Registry & Expectations

### 3.3 Stakeholder Registry and Architectural Influence

Stakeholder needs directly shape the structural partitioning, verification criteria, and quality metrics of the ePDC software architecture. The table below formalizes primary stakeholders, their operational concerns, and architectural design mitigations.

| Stakeholder Group | Primary Concerns & Objectives | Architectural Response | Verification Standard |
| :--- | :--- | :--- | :--- |
| Vehicle End Users | Instant throttle response, smooth regenerative braking, range efficiency | Sub-10ms torque arbitration, intelligent front-axle decoupling | ISO 2631 Ride Comfort |
| Functional Safety Auditors | Zero unintended acceleration, deterministic shutdown upon fault | ASIL-D redundant torque plausibility check on independent lockstep core | ISO 26262 Part 4/6 |
| Homologation Authorities | Cybersecurity compliance, UNECE R155/R156 software update governance | SecOC message authentication, cryptographically signed UCM OTA updates | UNECE R155 / R156 |
| Fleet & Service Technicians | Accurate fault localization, comprehensive DTC snapshots, DoIP speed | AUTOSAR Diagnostic Management (DM), UDS over DoIP (ISO 13400) | ISO 14229 / ISO 13400 |
| Manufacturing / Plant | Fast end-of-line flashing, calibration parameter persistence | High-speed UDS 0x36 transfer blocks, Key-Value persistency partitions | Automotive SPICE Level 3 |


---

<!-- Page 12 -->
## Page 12: 3.4 Operating Environment & Climatic Assumptions

### 3.4 Environmental Operating Envelope

The ePDC enclosure is mounted in the vehicle under-hood powertrain bay and must operate continuously within harsh ambient thermal, mechanical, and electromagnetic environments. Software components must dynamically adjust execution profiles according to ambient environmental feedback.

| Environmental Parameter | Nominal Range | Extreme Lower Limit | Extreme Upper Limit | Software Derating Action |
| :--- | :--- | :--- | :--- | :--- |
| Ambient Enclosure Temp | -40°C to +85°C | -45°C (Cold Soak) | +105°C (Extreme Soak) | De-rate CPU clock at > 95°C; throttle torque |
| Coolant Inflow Temp | +25°C to +45°C | -30°C | +70°C | ThermalManagement_SWC commands max radiator fan at > 55°C |
| Supply Voltage (12V Bus) | 12.0 V to 14.4 V | 6.5 V (Cranking) | 18.0 V (Overvoltage) | Disable non-safety persistency writes if < 9.0 V |
| Mechanical Vibration | ISO 16750-3 Profile IV | 0 Hz | 2000 Hz random vibration | Storage writes buffered with CRC validation |
| Relative Humidity | 5% to 95% non-cond | 0% | 100% condensing | Conformal coating on PCB; no software impact |


---

<!-- Page 13 -->
## Page 13: 4.1 Functional Requirements: REQ-PWR-001 to REQ-PWR-007

### 4.1 Functional Requirements Group 1

This section formalizes functional requirements REQ-PWR-001 through REQ-PWR-007. Each requirement specifies exact operational constraints, functional safety classification, and responsible software component implementing the requirement.

| Req ID | Requirement Title | Detailed Technical Description & Invariants | ASIL | Responsible SWC |
| :--- | :--- | :--- | :--- | :--- |
| REQ-PWR-001 | Driver Acceleration Pedal Interpretation | The PowertrainManager_SWC shall read dual independent analog throttle pedal sensors every 10 ms and calculate driver requested torque with plausibility cross-check. | ASIL-D | TorqueArbitration_SWC |
| REQ-PWR-002 | Pedal Plausibility Discordance Cutoff | If pedal sensor signals differ by more than 10% for longer than 50 ms, driver request shall transition to 0 Nm and a fault DTC shall be raised. | ASIL-D | EmergencyCutoff_SWC |
| REQ-PWR-003 | Dual Axle Torque Vectoring Split | The VehicleMotion_SWC shall compute front-to-rear axle torque split ratios based on dynamic vertical tire load distribution and yaw error every 10 ms. | ASIL-B | TorqueArbitration_SWC |
| REQ-PWR-004 | Front Axle Induction Motor Disconnect | When cruising at steady speed above 60 km/h with torque demand below 80 Nm, front induction motor excitation current shall be ramped to zero. | QM | PowertrainManager_SWC |
| REQ-PWR-005 | Regenerative Braking Blending | TorqueArbitration_SWC shall blend motor negative torque with hydraulic friction braking up to a maximum deceleration of 0.35g without wheel lockup. | ASIL-D | RegenerativeBraking_SWC |
| REQ-PWR-006 | Battery Charge Power Limiting | TorqueArbitration_SWC shall strictly limit regenerative braking negative torque such that battery input current does not exceed the limit published by BatteryManagement_SWC. | ASIL-D | BatteryManagement_SWC |
| REQ-PWR-007 | Battery Over-Temperature Cutback | When battery pack temperature exceeds 52°C, maximum discharge power shall be linearly derated to zero at 60°C over a 500 ms rolling filter. | ASIL-C | ThermalManagement_SWC |

> **Requirements Verification Note for Group 1**: All requirements in Group 1 must be verified using Hardware-in-the-Loop (HIL) fault injection test suites with automated pass/fail assertion triggers recorded in the compliance database.


---

<!-- Page 14 -->
## Page 14: 4.2 Functional Requirements: REQ-PWR-008 to REQ-PWR-014

### 4.2 Functional Requirements Group 2

This section formalizes functional requirements REQ-PWR-008 through REQ-PWR-014. Each requirement specifies exact operational constraints, functional safety classification, and responsible software component implementing the requirement.

| Req ID | Requirement Title | Detailed Technical Description & Invariants | ASIL | Responsible SWC |
| :--- | :--- | :--- | :--- | :--- |
| REQ-PWR-008 | High-Voltage Pre-Charge Monitoring | The BatteryManagement_SWC shall verify pre-charge capacitor voltage reaches within 95% of pack voltage before closing the positive main contactor. | ASIL-D | BatteryManagement_SWC |
| REQ-PWR-009 | Contactor Weld Detection | The BatteryManagement_SWC shall execute contactor diagnostic checks upon vehicle shutdown to verify no contactors remain welded closed. | ASIL-D | BatteryManagement_SWC |
| REQ-PWR-010 | High-Voltage Interlock Loop (HVIL) | The EmergencyCutoff_SWC shall continuously monitor the physical HVIL circuit; open circuit detection within 10 ms shall force immediate zero-torque command. | ASIL-D | EmergencyCutoff_SWC |
| REQ-PWR-011 | Crash Signal Fuel/Power Cutoff | Upon receiving an authentic crash signal from the BCM via SOME/IP or discrete hardwire, the high-voltage system shall de-energize within 50 ms. | ASIL-D | EmergencyCutoff_SWC |
| REQ-PWR-012 | DC Fast Charge Thermal Pre-Conditioning | When navigation destination is set to a DC fast charger, ThermalManagement_SWC shall pre-condition battery temperature to 28°C to 35°C. | QM | ThermalManagement_SWC |
| REQ-PWR-013 | Inverter Silicon Carbide Overtemperature Protection | If inverter junction temperature exceeds 145°C, maximum motor phase current shall be restricted to 60% of continuous rating within 20 ms. | ASIL-C | InverterController_SWC |
| REQ-PWR-014 | Motor Stall Protection | If vehicle is stationary in gear and torque request is applied for > 5 seconds with zero rotor rotation, torque shall be limited to 50 Nm to prevent localized winding burnout. | ASIL-B | TorqueArbitration_SWC |

> **Requirements Verification Note for Group 2**: All requirements in Group 2 must be verified using Hardware-in-the-Loop (HIL) fault injection test suites with automated pass/fail assertion triggers recorded in the compliance database.


---

<!-- Page 15 -->
## Page 15: 4.3 Functional Requirements: REQ-PWR-015 to REQ-PWR-021

### 4.3 Functional Requirements Group 3

This section formalizes functional requirements REQ-PWR-015 through REQ-PWR-021. Each requirement specifies exact operational constraints, functional safety classification, and responsible software component implementing the requirement.

| Req ID | Requirement Title | Detailed Technical Description & Invariants | ASIL | Responsible SWC |
| :--- | :--- | :--- | :--- | :--- |
| REQ-PWR-015 | Electronic Differential Speed Matching | VehicleMotion_SWC shall adjust individual wheel torque requests during cornering to emulate mechanical limited-slip differential behavior. | ASIL-B | VehicleMotion_SWC |
| REQ-PWR-016 | Traction Control Anti-Slip Regulation | If driven wheel speed exceeds non-driven wheel speed by > 3 km/h during acceleration, torque shall be cut back within 10 ms. | ASIL-D | VehicleMotion_SWC |
| REQ-PWR-017 | Reverse Gear Speed Limiter | When reverse gear is engaged, vehicle velocity shall be electronically governed to a maximum speed of 25 km/h via closed-loop torque control. | ASIL-B | PowertrainManager_SWC |
| REQ-PWR-018 | Driver Hands-Off Autonomous Abort | If ADAS autonomous acceleration command is received while steering wheel hands-on sensor indicates driver absence for > 15 s, ADAS torque request shall be rejected. | ASIL-B | TorqueArbitration_SWC |
| REQ-PWR-019 | Hill Hold Automatic Brake Handover | When stationary on an incline > 3%, powertrain shall generate sufficient motor holding torque for up to 3.0 seconds until hydraulic parking brake clamps. | ASIL-C | PowertrainManager_SWC |
| REQ-PWR-020 | Acoustic Vehicle Alerting System (AVAS) Speed Broadcast | PowertrainManager_SWC shall broadcast vehicle speed on SOME/IP eventgroup 201 to trigger external pedestrian alert sounds between 0 and 30 km/h. | QM | PowertrainManager_SWC |
| REQ-PWR-021 | State of Charge (SOC) Coulomb Counting | BatteryManagement_SWC shall integrate battery current at 100 Hz combined with an Extended Kalman Filter to estimate state of charge with < 2.0% error. | ASIL-B | BatteryManagement_SWC |

> **Requirements Verification Note for Group 3**: All requirements in Group 3 must be verified using Hardware-in-the-Loop (HIL) fault injection test suites with automated pass/fail assertion triggers recorded in the compliance database.


---

<!-- Page 16 -->
## Page 16: 4.4 Functional Requirements: REQ-PWR-022 to REQ-PWR-028

### 4.4 Functional Requirements Group 4

This section formalizes functional requirements REQ-PWR-022 through REQ-PWR-028. Each requirement specifies exact operational constraints, functional safety classification, and responsible software component implementing the requirement.

| Req ID | Requirement Title | Detailed Technical Description & Invariants | ASIL | Responsible SWC |
| :--- | :--- | :--- | :--- | :--- |
| REQ-PWR-022 | High-Voltage Isolation Resistance Monitoring | BatteryManagement_SWC shall measure isolation resistance between high-voltage bus and chassis ground; warning at < 500 ohms/V, cutoff at < 100 ohms/V. | ASIL-D | BatteryManagement_SWC |
| REQ-PWR-023 | Coolant Flow Rate Validation | ThermalManagement_SWC shall monitor electric water pump RPM and feedback pressure; flow loss shall trigger degraded power mode within 2 seconds. | ASIL-B | ThermalManagement_SWC |
| REQ-PWR-024 | Regen Braking Cold Battery Lockout | If battery temperature is below -5°C, regenerative braking shall be disabled to prevent irreversible lithium plating on anode electrodes. | ASIL-C | RegenerativeBraking_SWC |
| REQ-PWR-025 | Creep Torque Control | When in Drive or Reverse gear with brake pedal released at speeds < 8 km/h, powertrain shall provide smooth creep torque between 20 Nm and 40 Nm. | QM | TorqueArbitration_SWC |
| REQ-PWR-026 | Low-Voltage 12V DC-DC Converter Coordination | BatteryManagement_SWC shall monitor 12V auxiliary battery voltage and command high-voltage DC-DC converter output between 13.2 V and 14.6 V. | ASIL-B | BatteryManagement_SWC |
| REQ-PWR-027 | Thermal Runaway Early Vent Gas Detection | Battery pack pressure sensors shall be polled at 10 ms; a pressure surge > 50 kPa/sec shall trigger emergency contactor disconnect and cabin warning. | ASIL-D | EmergencyCutoff_SWC |
| REQ-PWR-028 | One-Pedal Driving Deceleration Profile | When one-pedal drive mode is enabled, accelerator pedal release between 15% and 0% shall generate progressive regenerative deceleration up to 0.22g. | ASIL-B | TorqueArbitration_SWC |

> **Requirements Verification Note for Group 4**: All requirements in Group 4 must be verified using Hardware-in-the-Loop (HIL) fault injection test suites with automated pass/fail assertion triggers recorded in the compliance database.


---

<!-- Page 17 -->
## Page 17: 4.5 Functional Requirements: REQ-PWR-029 to REQ-PWR-034

### 4.5 Functional Requirements Group 5

This section formalizes functional requirements REQ-PWR-029 through REQ-PWR-034. Each requirement specifies exact operational constraints, functional safety classification, and responsible software component implementing the requirement.

| Req ID | Requirement Title | Detailed Technical Description & Invariants | ASIL | Responsible SWC |
| :--- | :--- | :--- | :--- | :--- |
| REQ-PWR-029 | Inverter Overvoltage Active Short Circuit (ASC) | Upon inverter DC link overvoltage > 900 V during high-speed field weakening, inverters shall trigger 3-phase Active Short Circuit within 200 microseconds. | ASIL-D | InverterController_SWC |
| REQ-PWR-030 | SOME/IP Message Freshness & Counter Validation | All incoming torque command SOME/IP messages from ADAS shall validate sequence counter increment and timestamp freshness (< 30 ms). | ASIL-D | TorqueArbitration_SWC |
| REQ-PWR-031 | Cryptographic Signature Verification on Firmware Images | The Update and Configuration Management (UCM) daemon shall verify RSA-3072 or ECDSA P-384 digital signatures on all incoming software packages. | ASIL-B | UpdateConfigManager |
| REQ-PWR-032 | Diagnostic Trouble Code (DTC) Snapshot Storage | Upon any confirmed electrical or safety fault, the Diagnostic Management stack shall persist freeze frame data with 16 parameters to non-volatile flash. | QM | DiagnosticManager |
| REQ-PWR-033 | Emergency Low Power Vehicle Sleep Mode | When vehicle clamp 15 is off for > 10 minutes, the ePDC shall power down non-essential domains and enter low-power sleep drawing < 2.5 mA from 12V bus. | QM | ExecutionManager |
| REQ-PWR-034 | Motor Saliency Angle Online Adaptation | InverterController_SWC shall track motor inductance variations online to optimize maximum torque per ampere (MTPA) trajectory over temperature. | QM | InverterController_SWC |

> **Requirements Verification Note for Group 5**: All requirements in Group 5 must be verified using Hardware-in-the-Loop (HIL) fault injection test suites with automated pass/fail assertion triggers recorded in the compliance database.


---

<!-- Page 18 -->
## Page 18: 4.6 Functional Requirements: REQ-PWR-035 to REQ-PWR-040

### 4.6 Functional Requirements Group 6

This section formalizes functional requirements REQ-PWR-035 through REQ-PWR-040. Each requirement specifies exact operational constraints, functional safety classification, and responsible software component implementing the requirement.

| Req ID | Requirement Title | Detailed Technical Description & Invariants | ASIL | Responsible SWC |
| :--- | :--- | :--- | :--- | :--- |
| REQ-PWR-035 | Gear Shift Interlock Prevention | PowertrainManager_SWC shall reject shift commands to Reverse or Park if forward vehicle speed is greater than 3.0 km/h. | ASIL-C | PowertrainManager_SWC |
| REQ-PWR-036 | Motor Rotor Temperature Estimation | ThermalManagement_SWC shall calculate rotor magnet temperature using thermal lumped-parameter model combined with stator RTD sensor readings. | ASIL-B | ThermalManagement_SWC |
| REQ-PWR-037 | High-Voltage Contactor Life Cycle Counting | BatteryManagement_SWC shall track cumulative mechanical and electrical contactor cycles and log a maintenance DTC upon reaching 80,000 cycles. | QM | BatteryManagement_SWC |
| REQ-PWR-038 | Maximum Acceleration Jerk Limiting | TorqueArbitration_SWC shall filter rapid torque transitions such that vehicle longitudinal jerk does not exceed 10.0 m/s3 during normal operation. | ASIL-B | TorqueArbitration_SWC |
| REQ-PWR-039 | Degraded Limp-Home Speed Governing | In RUN_DEGRADED state, maximum vehicle velocity shall be governed to 60 km/h with visual and acoustic instrument cluster notifications. | ASIL-C | PowertrainManager_SWC |
| REQ-PWR-040 | Watchdog Challenge-Response Servicing | All safety-critical processes shall service the hardware watchdog challenge-response register within a strict 50 ms window; failure resets ECU. | ASIL-D | EmergencyCutoff_SWC |

> **Requirements Verification Note for Group 6**: All requirements in Group 6 must be verified using Hardware-in-the-Loop (HIL) fault injection test suites with automated pass/fail assertion triggers recorded in the compliance database.


---

<!-- Page 19 -->
## Page 19: 5.1 Timing, Latency & Real-Time Performance Budgets

### 5.1 Deterministic Timing & Real-Time Deadlines

The Electric Powertrain Domain Controller executes hard and soft real-time software tasks. Hard real-time tasks (such as torque arbitration, battery safety cutoffs, and inverter communication) must never miss a single scheduling deadline. The table below formalizes worst-case execution time (WCET) limits, scheduling jitter, and end-to-end latency targets.

| Timing Metric ID | Description of Timing Constraint | Nominal Period | Max Allowable Jitter | Max Allowable WCET | End-to-End Budget |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TIM-PWR-001 | Driver throttle pedal sampling to torque command dispatch | 10 ms cyclic | ± 0.25 ms | 1.8 ms | 10.0 ms maximum |
| TIM-PWR-002 | Emergency safety cutoff signal to contactor de-energize | Interrupt driven | < 0.05 ms | 0.4 ms | 10.0 ms hard limit |
| TIM-PWR-003 | ADAS trajectory acceleration demand to motor torque output | 10 ms cyclic | ± 0.50 ms | 2.2 ms | 15.0 ms maximum |
| TIM-PWR-004 | Battery pack voltage and current sensor sampling rate | 1 ms cyclic | ± 0.02 ms | 0.15 ms | 2.0 ms maximum |
| TIM-PWR-005 | Thermal management coolant valve regulation loop | 100 ms cyclic | ± 5.0 ms | 8.5 ms | 200.0 ms maximum |
| TIM-PWR-006 | Diagnostic Trouble Code (DTC) snapshot persistence to flash | Asynchronous | N/A | 15.0 ms | 50.0 ms maximum |


---

<!-- Page 20 -->
## Page 20: 5.2 Functional Safety, Reliability & Availability Targets

### 5.2 Safety Integrity Levels & Reliability Metrics

In compliance with ISO 26262:2018 Road Vehicles — Functional Safety, the overall powertrain safety goal 'Prevention of Unintended Vehicle Acceleration or Deceleration' is assigned the highest safety integrity level: ASIL-D. Software components directly controlling torque arbitration and high-voltage power paths inherit ASIL-D development rigor.

| Safety / Reliability Metric | Target Metric Value | Applicable Standard | Design Mitigation Mechanism |
| :--- | :--- | :--- | :--- |
| Random Hardware Failure Rate | < 10 FIT (10^-8 failures/hour) | ISO 26262 ASIL-D Target | Lockstep dual-core execution with parity check |
| Single Point Fault Metric (SPFM) | >= 99.0% | ISO 26262 ASIL-D Target | Hardware BIST and periodic memory sweep tests |
| Latent Fault Metric (LFM) | >= 90.0% | ISO 26262 ASIL-D Target | Startup and shutdown self-test diagnostics |
| Mean Time Between Failures (MTBF) | > 150,000 operating hours | Automotive SPICE Level 3 | Component derating and automotive-grade silicon |
| Flash Data Retention | 15 years @ 85°C ambient | JEDEC JESD22-A117 | Wear-leveling and daily ECC scrubbing |
| Safety Loop Diagnostic Coverage | >= 99.5% | ISO 26262 ASIL-D Target | Plausibility monitors on independent micro-core |


---

<!-- Page 21 -->
## Page 21: 5.3 CPU Utilization, Memory & Storage Budgets

### 5.3 Computational Resource Allocation Budgets

To prevent resource starvation, CPU core saturation, and memory overflow, strict static resource quotas are assigned to each Software Component and platform service. Under peak operating conditions (including simultaneous CAN-FD bursts, SOME/IP service discovery, and rapid torque transient calculations), aggregate CPU utilization must remain below 70%.

| Software Component / Subsystem | CPU Core Affinity | Max CPU Budget | RAM Budget (SRAM) | Flash ROM Budget | Stack Reserve |
| :--- | :--- | :--- | :--- | :--- | :--- |
| PowertrainManager_SWC | Core 0 (Cortex-A78AE) | 12.0% | 8.0 MB | 16.0 MB | 256 KB |
| TorqueArbitration_SWC | Core 1 (Cortex-A78AE) | 18.5% | 12.0 MB | 24.0 MB | 512 KB |
| BatteryManagement_SWC | Core 0 (Cortex-A78AE) | 10.0% | 6.0 MB | 12.0 MB | 256 KB |
| ThermalManagement_SWC | Core 2 (Cortex-A78AE) | 6.0% | 4.0 MB | 8.0 MB | 128 KB |
| VehicleMotion_SWC | Core 1 (Cortex-A78AE) | 14.0% | 10.0 MB | 18.0 MB | 512 KB |
| EmergencyCutoff_SWC | Core 3 (Cortex-A78AE) + R52 | 4.0% | 2.0 MB | 4.0 MB | 128 KB |
| ARA Platform Daemon Stack | Core 2 & Core 3 | 15.0% | 32.0 MB | 64.0 MB | 1024 KB |
| Total Allocated Headroom | All Cores Available | 69.5% Peak | 74.0 MB / 256 MB | 146 MB / 512 MB | Healthy Safety Margin |


---

<!-- Page 22 -->
## Page 22: 5.4 Electromagnetic Compatibility (EMC) & Cyber Resilience

### 5.4 EMC Resilience & Cybersecurity Performance

High-voltage silicon carbide switching in nearby traction inverters introduces substantial high-frequency electromagnetic interference (EMI). The ePDC communication architecture incorporates hardware shielding and digital packet filtering to maintain zero bit-error rates during 200 A/microsecond switching events.

| Standard / Threat Model | Testing Requirement | Acceptance Criteria | Software Countermeasure |
| :--- | :--- | :--- | :--- |
| CISPR 25 Class 5 | Radiated and conducted emissions | No spurious interrupt generation | Input Schmitt-trigger filtering & debounce |
| ISO 11452-2 / ISO 11452-4 | RF immunity 200 V/m (10 kHz - 18 GHz) | Zero frame corruption on Ethernet/CAN | CRC-32 checksums and packet drop counters |
| ISO 7637-2 / ISO 16750-2 | Transient electrical conduction | Zero reset on power dip to 6.5V | Brownout detect interrupt saves critical state |
| ISO/SAE 21434 CAL-4 | Cyberattack resistance against bus spoofing | 100% rejection of unauthenticated commands | SecOC AES-CMAC message verification |
| Fuzzing Stress Testing | 100M malformed SOME/IP packets | Zero kernel crash or buffer overflow | Strict schema bounds checking in deserializer |


---

<!-- Page 23 -->
## Page 23: 6.1 Adaptive Platform Foundations & ARA Architecture

### 6.1 AUTOSAR Adaptive Runtime for Applications (ARA)

The AUTOSAR Adaptive Platform is engineered for compute-intensive distributed automotive domains requiring dynamic configuration and high-bandwidth service-oriented communication. Unlike the static OSEK/AUTOSAR Classic environment, Adaptive AUTOSAR applications run as isolated POSIX processes utilizing C++14/C++17 standard libraries and interacting with the system through Adaptive Foundation APIs (ara::core, ara::com, ara::exec, ara::per, ara::diag, ara::log, and ara::crypto).

| ARA Functional Cluster | Standard Namespace | Primary Service Provided | Implementation Paradigm |
| :--- | :--- | :--- | :--- |
| Communication Management | ara::com | Service-oriented IPC, SOME/IP, Publish-Subscribe, RPC | Proxy-Skeleton abstraction pattern |
| Execution Management | ara::exec | Deterministic process lifecycle, state control, watchdog | Systemd-like daemon managing cgroups |
| Persistency Management | ara::per | Crash-safe Key-Value and File storage on non-volatile media | Atomic multi-block write with journal |
| Diagnostic Management | ara::diag | UDS on IP (ISO 14229 / ISO 13400 DoIP), DTC event handling | Diagnostic service router and handler |
| Logging & Tracing | ara::log | Diagnostic Log and Trace (DLT) standardized logging | Zero-copy shared memory lock-free ring |
| Cryptography Service | ara::crypto | Hardware Security Module interface, AES, RSA, ECDSA | PKCS#11 compatible secure keystore |
| Update & Config Manager | ara::ucm | Over-The-Air software package installation, A/B partition | Atomic image verification and commit |


---

<!-- Page 24 -->
## Page 24: 6.2 Manifest Hierarchy & Machine Deployment

### 6.2 Manifests, Software Modeling & Machine Deployment

Adaptive AUTOSAR strictly decouples application software design from physical deployment through standardized ARXML manifest files. The deployment workflow involves three distinct manifest tiers: Execution Manifests, Service Instance Manifests, and Machine Manifests.

| Manifest Category | File Format & Extension | Governed Configuration Properties | Validation Tooling |
| :--- | :--- | :--- | :--- |
| Execution Manifest | application_exec.arxml | Process startup parameters, core affinity, resource limits, environment vars | AUTOSAR Manifest Validator |
| Service Instance Manifest | service_instance.arxml | SOME/IP Service IDs, Instance IDs, Eventgroups, VLAN assignments | Network Design Tool Suite |
| Machine Manifest | machine_manifest.arxml | Network endpoints, IP addresses, POSIX user IDs, hardware timers | Platform Integration Tool |
| Software Package Manifest | sw_package.arxml | Package version, cryptographic hash, dependencies, install hooks | UCM Packaging Utility |


---

<!-- Page 25 -->
## Page 25: 6.3 Operating System Interface & POSIX PSE52 Profile

### 6.3 POSIX PSE52 Compliance & Kernel Separation

The underlying operating system provides POSIX PSE52 (Real-Time Controller) conformance with multi-threading, memory protection (MMU), real-time priority-preemptive scheduling (SCHED_FIFO), and process isolation. Software Components execute entirely within user-space memory partitions with no direct access to physical memory addresses.

| POSIX Feature Set | Standard Reference | Kernel Implementation | Safety / Security Impact |
| :--- | :--- | :--- | :--- |
| Memory Management | POSIX mman.h / mprotect() | Hardware MMU page table enforcement | Zero cross-process memory corruption possible |
| Thread Scheduling | POSIX pthread / SCHED_FIFO | 128 real-time scheduling priority levels | Deterministic high-priority task preemption |
| Inter-Process Comms | POSIX shm_open() / mmap() | Zero-copy shared memory ring buffers | High throughput, low latency IPC (< 50 us) |
| Timers and Clocks | CLOCK_MONOTONIC_RAW | Sub-microsecond hardware counter sync | Accurate jitter-free cyclic task triggering |
| Signal Handling | POSIX sigaction() | Restricted to SIGTERM, SIGUSR1, SIGSEGV | Immediate safe cleanup on process termination |


---

<!-- Page 26 -->
## Page 26: 6.4 Identity & Access Management (IAM)

### 6.4 Identity & Access Management (IAM) and Process Sandboxing

The Adaptive Platform enforces Identity and Access Management (IAM) to verify whether a given application process possesses authorization to offer or consume a specific service interface, open a communication socket, or access a persistency file. Permissions are evaluated statically at deployment time and verified dynamically at runtime.

| Process Name | Assigned POSIX UID | Authorized Services (Offer) | Authorized Services (Find/Consume) | File System Access Rights |
| :--- | :--- | :--- | :--- | :--- |
| PowertrainManager | uid: 1001 (powertrain) | IPowertrainCoordination (Svc 0x1001) | IBatteryStatus, ITorqueCommand | rw: /var/data/pwr_mgr/ |
| TorqueArbitration | uid: 1002 (torque) | ITorqueCommand (Svc 0x1002) | IPowertrainCoordination, IVehicleDynamics | rw: /var/data/torque/ |
| BatteryManagement | uid: 1003 (bms) | IBatteryStatus (Svc 0x1003) | None (Independent Provider) | rw: /var/data/bms/ |
| ThermalManagement | uid: 1004 (thermal) | IThermalTelemetry (Svc 0x1004) | IBatteryStatus, IPowertrainCoordination | rw: /var/data/thermal/ |
| VehicleMotion | uid: 1005 (motion) | IVehicleDynamics (Svc 0x1005) | IPowertrainCoordination | rw: /var/data/motion/ |
| EmergencyCutoff | uid: 1000 (safety_root) | IEmergencySafety (Svc 0x1000) | All Services (Global Safety Supervisor) | r: /proc/, rw: /dev/safety_io |


---

<!-- Page 27 -->
## Page 27: 7.1 PowertrainManager_SWC Architectural Design

### 7.1 PowertrainManager_SWC

Coordinates high-level vehicle drive modes, ignition clamp states, driver gear selections, and cruise control interfaces. It arbitrates the operational mode of the vehicle and coordinates auxiliary controllers during startup and shutdown.

#### Component Interfaces & Port Catalog

| Port Name | Port Direction | Interface Type | Transport Binding | Update Rate |
| :--- | :--- | :--- | :--- | :--- |
| PPort_PowertrainManagerStatus | Provided (PPort) | IPowertrainManagerStatus | SOME/IP Broadcast | 10 ms cyclic |
| RPort_VehicleBusData | Required (RPort) | IVehicleBusSignals | SOME/IP Consume | 10 ms cyclic |
| PPort_DiagnosticEvents | Provided (PPort) | IDiagnosticEventReport | ara::diag Direct | On Event |
| RPort_SafetyInterlocks | Required (RPort) | IEmergencySafetyLoop | Shared Memory / Direct | 1 ms cyclic |

#### Component Structural Invariants

| Invariant ID | Invariant Mathematical Condition | Enforcement Action | Safety Class |
| :--- | :--- | :--- | :--- |
| INV-POW-001 | Execution time < 2.0 ms per cycle | Raise timing violation warning to OS | ASIL-B |
| INV-POW-002 | Output values strictly within physical range | Clamp value to boundary and log error | ASIL-D |
| INV-POW-003 | Shared memory pointers non-null and valid | Trigger graceful recovery routine | ASIL-D |


---

<!-- Page 28 -->
## Page 28: 7.2 TorqueArbitration_SWC Architectural Design

### 7.2 TorqueArbitration_SWC

Performs deterministic blending and arbitration between driver accelerator pedal requests, ADAS autonomous driving commands, traction control cutbacks, and stability interventions. Ensures total commanded torque does not exceed battery or motor limits.

#### Component Interfaces & Port Catalog

| Port Name | Port Direction | Interface Type | Transport Binding | Update Rate |
| :--- | :--- | :--- | :--- | :--- |
| PPort_TorqueArbitrationStatus | Provided (PPort) | ITorqueArbitrationStatus | SOME/IP Broadcast | 10 ms cyclic |
| RPort_VehicleBusData | Required (RPort) | IVehicleBusSignals | SOME/IP Consume | 10 ms cyclic |
| PPort_DiagnosticEvents | Provided (PPort) | IDiagnosticEventReport | ara::diag Direct | On Event |
| RPort_SafetyInterlocks | Required (RPort) | IEmergencySafetyLoop | Shared Memory / Direct | 1 ms cyclic |

#### Component Structural Invariants

| Invariant ID | Invariant Mathematical Condition | Enforcement Action | Safety Class |
| :--- | :--- | :--- | :--- |
| INV-TOR-001 | Execution time < 2.0 ms per cycle | Raise timing violation warning to OS | ASIL-B |
| INV-TOR-002 | Output values strictly within physical range | Clamp value to boundary and log error | ASIL-D |
| INV-TOR-003 | Shared memory pointers non-null and valid | Trigger graceful recovery routine | ASIL-D |


---

<!-- Page 29 -->
## Page 29: 7.3 BatteryManagement_SWC Architectural Design

### 7.3 BatteryManagement_SWC

Calculates state of charge (SOC), state of health (SOH), maximum continuous discharge power, and maximum regenerative charge acceptance. Monitors individual cell voltages and temperatures, controlling pre-charge sequences and contactors.

#### Component Interfaces & Port Catalog

| Port Name | Port Direction | Interface Type | Transport Binding | Update Rate |
| :--- | :--- | :--- | :--- | :--- |
| PPort_BatteryManagementStatus | Provided (PPort) | IBatteryManagementStatus | SOME/IP Broadcast | 10 ms cyclic |
| RPort_VehicleBusData | Required (RPort) | IVehicleBusSignals | SOME/IP Consume | 10 ms cyclic |
| PPort_DiagnosticEvents | Provided (PPort) | IDiagnosticEventReport | ara::diag Direct | On Event |
| RPort_SafetyInterlocks | Required (RPort) | IEmergencySafetyLoop | Shared Memory / Direct | 1 ms cyclic |

#### Component Structural Invariants

| Invariant ID | Invariant Mathematical Condition | Enforcement Action | Safety Class |
| :--- | :--- | :--- | :--- |
| INV-BAT-001 | Execution time < 2.0 ms per cycle | Raise timing violation warning to OS | ASIL-B |
| INV-BAT-002 | Output values strictly within physical range | Clamp value to boundary and log error | ASIL-D |
| INV-BAT-003 | Shared memory pointers non-null and valid | Trigger graceful recovery routine | ASIL-D |


---

<!-- Page 30 -->
## Page 30: 7.4 ThermalManagement_SWC Architectural Design

### 7.4 ThermalManagement_SWC

Controls electric coolant pumps, proportional flow valves, front radiator shutters, and air conditioning refrigerant chillers to regulate battery, motor, and inverter temperatures within optimal thermal efficiency bands.

#### Component Interfaces & Port Catalog

| Port Name | Port Direction | Interface Type | Transport Binding | Update Rate |
| :--- | :--- | :--- | :--- | :--- |
| PPort_ThermalManagementStatus | Provided (PPort) | IThermalManagementStatus | SOME/IP Broadcast | 10 ms cyclic |
| RPort_VehicleBusData | Required (RPort) | IVehicleBusSignals | SOME/IP Consume | 10 ms cyclic |
| PPort_DiagnosticEvents | Provided (PPort) | IDiagnosticEventReport | ara::diag Direct | On Event |
| RPort_SafetyInterlocks | Required (RPort) | IEmergencySafetyLoop | Shared Memory / Direct | 1 ms cyclic |

#### Component Structural Invariants

| Invariant ID | Invariant Mathematical Condition | Enforcement Action | Safety Class |
| :--- | :--- | :--- | :--- |
| INV-THE-001 | Execution time < 2.0 ms per cycle | Raise timing violation warning to OS | ASIL-B |
| INV-THE-002 | Output values strictly within physical range | Clamp value to boundary and log error | ASIL-D |
| INV-THE-003 | Shared memory pointers non-null and valid | Trigger graceful recovery routine | ASIL-D |


---

<!-- Page 31 -->
## Page 31: 7.5 VehicleMotion_SWC Architectural Design

### 7.5 VehicleMotion_SWC

Evaluates steering angle, wheel speed sensors, lateral acceleration, and yaw rate to optimize torque split between front and rear axles. Mitigates understeer and oversteer through active torque vectoring.

#### Component Interfaces & Port Catalog

| Port Name | Port Direction | Interface Type | Transport Binding | Update Rate |
| :--- | :--- | :--- | :--- | :--- |
| PPort_VehicleMotionStatus | Provided (PPort) | IVehicleMotionStatus | SOME/IP Broadcast | 10 ms cyclic |
| RPort_VehicleBusData | Required (RPort) | IVehicleBusSignals | SOME/IP Consume | 10 ms cyclic |
| PPort_DiagnosticEvents | Provided (PPort) | IDiagnosticEventReport | ara::diag Direct | On Event |
| RPort_SafetyInterlocks | Required (RPort) | IEmergencySafetyLoop | Shared Memory / Direct | 1 ms cyclic |

#### Component Structural Invariants

| Invariant ID | Invariant Mathematical Condition | Enforcement Action | Safety Class |
| :--- | :--- | :--- | :--- |
| INV-VEH-001 | Execution time < 2.0 ms per cycle | Raise timing violation warning to OS | ASIL-B |
| INV-VEH-002 | Output values strictly within physical range | Clamp value to boundary and log error | ASIL-D |
| INV-VEH-003 | Shared memory pointers non-null and valid | Trigger graceful recovery routine | ASIL-D |


---

<!-- Page 32 -->
## Page 32: 7.6 EmergencyCutoff_SWC Architectural Design

### 7.6 EmergencyCutoff_SWC

Executes isolated plausibility monitoring on a companion lockstep core. Monitors commanded versus actual torque, accelerator versus brake conflicts, and HVIL continuity. Triggers hardware cutoff if hazardous torque is detected.

#### Component Interfaces & Port Catalog

| Port Name | Port Direction | Interface Type | Transport Binding | Update Rate |
| :--- | :--- | :--- | :--- | :--- |
| PPort_EmergencyCutoffStatus | Provided (PPort) | IEmergencyCutoffStatus | SOME/IP Broadcast | 10 ms cyclic |
| RPort_VehicleBusData | Required (RPort) | IVehicleBusSignals | SOME/IP Consume | 10 ms cyclic |
| PPort_DiagnosticEvents | Provided (PPort) | IDiagnosticEventReport | ara::diag Direct | On Event |
| RPort_SafetyInterlocks | Required (RPort) | IEmergencySafetyLoop | Shared Memory / Direct | 1 ms cyclic |

#### Component Structural Invariants

| Invariant ID | Invariant Mathematical Condition | Enforcement Action | Safety Class |
| :--- | :--- | :--- | :--- |
| INV-EME-001 | Execution time < 2.0 ms per cycle | Raise timing violation warning to OS | ASIL-B |
| INV-EME-002 | Output values strictly within physical range | Clamp value to boundary and log error | ASIL-D |
| INV-EME-003 | Shared memory pointers non-null and valid | Trigger graceful recovery routine | ASIL-D |


---

<!-- Page 33 -->
## Page 33: 8.1 PowertrainManager_SWC State Machine

### 8.1 PowertrainManager_SWC State Machine

This section documents the formal mathematical formulations, internal state machine definitions, and execution invariants governing PowertrainManager_SWC State Machine. All equations are executed cyclically by the component's internal runnable entities.

#### Detailed Algorithmic Specification

Torque request calculation combines driver pedal mapping, cruise control PID output, and speed limit governor commands: T_raw = (Pedal_Ratio * T_max_curve(RPM)) + T_cruise_delta. The result is clipped against the battery power envelope: T_clipped = min(T_raw, (P_battery_discharge_limit / Motor_Angular_Velocity)). When friction braking is active, regenerative torque is blended smoothly: T_final = T_clipped - T_regen_target.

| Algorithmic Step | Mathematical Equation / Logic Rule | Execution Frequency | Expected Output Range |
| :--- | :--- | :--- | :--- |
| Step 1: Input Conditioning | Throttle_Filtered = LowPassFilter(Pedal_Raw, tau=15ms) | 10 ms | 0.0% to 100.0% |
| Step 2: Base Torque Lookup | T_driver = LookupTable2D(Throttle_Filtered, Motor_RPM) | 10 ms | -150 Nm to +730 Nm |
| Step 3: Power Limit Clamp | T_allowable = min(T_driver, P_bat_lim / omega) | 10 ms | -250 Nm to +730 Nm |
| Step 4: Stability Adjustment | T_front, T_rear = YawDistribution(T_allowable, Yaw_Error) | 10 ms | Front: 0-280Nm, Rear: 0-450Nm |
| Step 5: Safety Verification | assert |T_commanded - T_actual| < 50Nm for 20ms | 2 ms | Boolean Invariant Check |

> **Safety Invariant Verification**: Any violation of Step 5 where commanded torque exceeds actual motor torque capability by more than 50 Nm for longer than 20 ms triggers immediate ASIL-D safe stop initiation.


---

<!-- Page 34 -->
## Page 34: 8.2 TorqueArbitration_SWC Blending Math

### 8.2 TorqueArbitration_SWC Blending Math

This section documents the formal mathematical formulations, internal state machine definitions, and execution invariants governing TorqueArbitration_SWC Blending Math. All equations are executed cyclically by the component's internal runnable entities.

#### Detailed Algorithmic Specification

Torque request calculation combines driver pedal mapping, cruise control PID output, and speed limit governor commands: T_raw = (Pedal_Ratio * T_max_curve(RPM)) + T_cruise_delta. The result is clipped against the battery power envelope: T_clipped = min(T_raw, (P_battery_discharge_limit / Motor_Angular_Velocity)). When friction braking is active, regenerative torque is blended smoothly: T_final = T_clipped - T_regen_target.

| Algorithmic Step | Mathematical Equation / Logic Rule | Execution Frequency | Expected Output Range |
| :--- | :--- | :--- | :--- |
| Step 1: Input Conditioning | Throttle_Filtered = LowPassFilter(Pedal_Raw, tau=15ms) | 10 ms | 0.0% to 100.0% |
| Step 2: Base Torque Lookup | T_driver = LookupTable2D(Throttle_Filtered, Motor_RPM) | 10 ms | -150 Nm to +730 Nm |
| Step 3: Power Limit Clamp | T_allowable = min(T_driver, P_bat_lim / omega) | 10 ms | -250 Nm to +730 Nm |
| Step 4: Stability Adjustment | T_front, T_rear = YawDistribution(T_allowable, Yaw_Error) | 10 ms | Front: 0-280Nm, Rear: 0-450Nm |
| Step 5: Safety Verification | assert |T_commanded - T_actual| < 50Nm for 20ms | 2 ms | Boolean Invariant Check |

> **Safety Invariant Verification**: Any violation of Step 5 where commanded torque exceeds actual motor torque capability by more than 50 Nm for longer than 20 ms triggers immediate ASIL-D safe stop initiation.


---

<!-- Page 35 -->
## Page 35: 8.3 BatteryManagement_SWC State Estimation

### 8.3 BatteryManagement_SWC State Estimation

This section documents the formal mathematical formulations, internal state machine definitions, and execution invariants governing BatteryManagement_SWC State Estimation. All equations are executed cyclically by the component's internal runnable entities.

#### Detailed Algorithmic Specification

Torque request calculation combines driver pedal mapping, cruise control PID output, and speed limit governor commands: T_raw = (Pedal_Ratio * T_max_curve(RPM)) + T_cruise_delta. The result is clipped against the battery power envelope: T_clipped = min(T_raw, (P_battery_discharge_limit / Motor_Angular_Velocity)). When friction braking is active, regenerative torque is blended smoothly: T_final = T_clipped - T_regen_target.

| Algorithmic Step | Mathematical Equation / Logic Rule | Execution Frequency | Expected Output Range |
| :--- | :--- | :--- | :--- |
| Step 1: Input Conditioning | Throttle_Filtered = LowPassFilter(Pedal_Raw, tau=15ms) | 10 ms | 0.0% to 100.0% |
| Step 2: Base Torque Lookup | T_driver = LookupTable2D(Throttle_Filtered, Motor_RPM) | 10 ms | -150 Nm to +730 Nm |
| Step 3: Power Limit Clamp | T_allowable = min(T_driver, P_bat_lim / omega) | 10 ms | -250 Nm to +730 Nm |
| Step 4: Stability Adjustment | T_front, T_rear = YawDistribution(T_allowable, Yaw_Error) | 10 ms | Front: 0-280Nm, Rear: 0-450Nm |
| Step 5: Safety Verification | assert |T_commanded - T_actual| < 50Nm for 20ms | 2 ms | Boolean Invariant Check |

> **Safety Invariant Verification**: Any violation of Step 5 where commanded torque exceeds actual motor torque capability by more than 50 Nm for longer than 20 ms triggers immediate ASIL-D safe stop initiation.


---

<!-- Page 36 -->
## Page 36: 8.4 ThermalManagement_SWC Control Loops

### 8.4 ThermalManagement_SWC Control Loops

This section documents the formal mathematical formulations, internal state machine definitions, and execution invariants governing ThermalManagement_SWC Control Loops. All equations are executed cyclically by the component's internal runnable entities.

#### Detailed Algorithmic Specification

Torque request calculation combines driver pedal mapping, cruise control PID output, and speed limit governor commands: T_raw = (Pedal_Ratio * T_max_curve(RPM)) + T_cruise_delta. The result is clipped against the battery power envelope: T_clipped = min(T_raw, (P_battery_discharge_limit / Motor_Angular_Velocity)). When friction braking is active, regenerative torque is blended smoothly: T_final = T_clipped - T_regen_target.

| Algorithmic Step | Mathematical Equation / Logic Rule | Execution Frequency | Expected Output Range |
| :--- | :--- | :--- | :--- |
| Step 1: Input Conditioning | Throttle_Filtered = LowPassFilter(Pedal_Raw, tau=15ms) | 10 ms | 0.0% to 100.0% |
| Step 2: Base Torque Lookup | T_driver = LookupTable2D(Throttle_Filtered, Motor_RPM) | 10 ms | -150 Nm to +730 Nm |
| Step 3: Power Limit Clamp | T_allowable = min(T_driver, P_bat_lim / omega) | 10 ms | -250 Nm to +730 Nm |
| Step 4: Stability Adjustment | T_front, T_rear = YawDistribution(T_allowable, Yaw_Error) | 10 ms | Front: 0-280Nm, Rear: 0-450Nm |
| Step 5: Safety Verification | assert |T_commanded - T_actual| < 50Nm for 20ms | 2 ms | Boolean Invariant Check |

> **Safety Invariant Verification**: Any violation of Step 5 where commanded torque exceeds actual motor torque capability by more than 50 Nm for longer than 20 ms triggers immediate ASIL-D safe stop initiation.


---

<!-- Page 37 -->
## Page 37: 8.5 VehicleMotion_SWC Vectoring Algorithm

### 8.5 VehicleMotion_SWC Vectoring Algorithm

This section documents the formal mathematical formulations, internal state machine definitions, and execution invariants governing VehicleMotion_SWC Vectoring Algorithm. All equations are executed cyclically by the component's internal runnable entities.

#### Detailed Algorithmic Specification

Torque request calculation combines driver pedal mapping, cruise control PID output, and speed limit governor commands: T_raw = (Pedal_Ratio * T_max_curve(RPM)) + T_cruise_delta. The result is clipped against the battery power envelope: T_clipped = min(T_raw, (P_battery_discharge_limit / Motor_Angular_Velocity)). When friction braking is active, regenerative torque is blended smoothly: T_final = T_clipped - T_regen_target.

| Algorithmic Step | Mathematical Equation / Logic Rule | Execution Frequency | Expected Output Range |
| :--- | :--- | :--- | :--- |
| Step 1: Input Conditioning | Throttle_Filtered = LowPassFilter(Pedal_Raw, tau=15ms) | 10 ms | 0.0% to 100.0% |
| Step 2: Base Torque Lookup | T_driver = LookupTable2D(Throttle_Filtered, Motor_RPM) | 10 ms | -150 Nm to +730 Nm |
| Step 3: Power Limit Clamp | T_allowable = min(T_driver, P_bat_lim / omega) | 10 ms | -250 Nm to +730 Nm |
| Step 4: Stability Adjustment | T_front, T_rear = YawDistribution(T_allowable, Yaw_Error) | 10 ms | Front: 0-280Nm, Rear: 0-450Nm |
| Step 5: Safety Verification | assert |T_commanded - T_actual| < 50Nm for 20ms | 2 ms | Boolean Invariant Check |

> **Safety Invariant Verification**: Any violation of Step 5 where commanded torque exceeds actual motor torque capability by more than 50 Nm for longer than 20 ms triggers immediate ASIL-D safe stop initiation.


---

<!-- Page 38 -->
## Page 38: 8.6 EmergencyCutoff_SWC Plausibility Logic

### 8.6 EmergencyCutoff_SWC Plausibility Logic

This section documents the formal mathematical formulations, internal state machine definitions, and execution invariants governing EmergencyCutoff_SWC Plausibility Logic. All equations are executed cyclically by the component's internal runnable entities.

#### Detailed Algorithmic Specification

Torque request calculation combines driver pedal mapping, cruise control PID output, and speed limit governor commands: T_raw = (Pedal_Ratio * T_max_curve(RPM)) + T_cruise_delta. The result is clipped against the battery power envelope: T_clipped = min(T_raw, (P_battery_discharge_limit / Motor_Angular_Velocity)). When friction braking is active, regenerative torque is blended smoothly: T_final = T_clipped - T_regen_target.

| Algorithmic Step | Mathematical Equation / Logic Rule | Execution Frequency | Expected Output Range |
| :--- | :--- | :--- | :--- |
| Step 1: Input Conditioning | Throttle_Filtered = LowPassFilter(Pedal_Raw, tau=15ms) | 10 ms | 0.0% to 100.0% |
| Step 2: Base Torque Lookup | T_driver = LookupTable2D(Throttle_Filtered, Motor_RPM) | 10 ms | -150 Nm to +730 Nm |
| Step 3: Power Limit Clamp | T_allowable = min(T_driver, P_bat_lim / omega) | 10 ms | -250 Nm to +730 Nm |
| Step 4: Stability Adjustment | T_front, T_rear = YawDistribution(T_allowable, Yaw_Error) | 10 ms | Front: 0-280Nm, Rear: 0-450Nm |
| Step 5: Safety Verification | assert |T_commanded - T_actual| < 50Nm for 20ms | 2 ms | Boolean Invariant Check |

> **Safety Invariant Verification**: Any violation of Step 5 where commanded torque exceeds actual motor torque capability by more than 50 Nm for longer than 20 ms triggers immediate ASIL-D safe stop initiation.


---

<!-- Page 39 -->
## Page 39: 9.1 Adaptive Execution Management Overview

### 9.1 Adaptive Execution Management Overview

Execution Management (ara::exec) is responsible for the structured startup, shutdown, deterministic execution, and operational state supervision of all software processes within the Adaptive Platform.

| Process Identifier | Binary Executable Path | Startup Order Phase | Function Group Binding | Recovery Action on Crash |
| :--- | :--- | :--- | :--- | :--- |
| Proc_PowertrainMgr | /opt/autosar/bin/powertrain_manager | Phase 3 (Applications) | MachineState::Running | Restart Process (Max 3 attempts) |
| Proc_TorqueArbiter | /opt/autosar/bin/torque_arbitration | Phase 3 (Applications) | MachineState::Running | Restart Process; if fail -> Limp Home |
| Proc_BatteryMgr | /opt/autosar/bin/battery_management | Phase 2 (Device Services) | MachineState::Running | Lock High-Voltage Safety Mode |
| Proc_ThermalMgr | /opt/autosar/bin/thermal_management | Phase 3 (Applications) | MachineState::Running | Run Pumps at 100% Fallback |
| Proc_VehicleMotion | /opt/autosar/bin/vehicle_motion | Phase 3 (Applications) | MachineState::Running | Fallback to 50:50 Fixed Split |
| Proc_EmergencyCutoff | /opt/autosar/bin/emergency_cutoff | Phase 1 (Safety Core) | Always Active | Hardware System Reset |


---

<!-- Page 40 -->
## Page 40: 9.2 Process Startup Sequencing & Dependencies

### 9.2 Process Startup Sequencing & Dependencies

Execution Management (ara::exec) is responsible for the structured startup, shutdown, deterministic execution, and operational state supervision of all software processes within the Adaptive Platform.

| Process Identifier | Binary Executable Path | Startup Order Phase | Function Group Binding | Recovery Action on Crash |
| :--- | :--- | :--- | :--- | :--- |
| Proc_PowertrainMgr | /opt/autosar/bin/powertrain_manager | Phase 3 (Applications) | MachineState::Running | Restart Process (Max 3 attempts) |
| Proc_TorqueArbiter | /opt/autosar/bin/torque_arbitration | Phase 3 (Applications) | MachineState::Running | Restart Process; if fail -> Limp Home |
| Proc_BatteryMgr | /opt/autosar/bin/battery_management | Phase 2 (Device Services) | MachineState::Running | Lock High-Voltage Safety Mode |
| Proc_ThermalMgr | /opt/autosar/bin/thermal_management | Phase 3 (Applications) | MachineState::Running | Run Pumps at 100% Fallback |
| Proc_VehicleMotion | /opt/autosar/bin/vehicle_motion | Phase 3 (Applications) | MachineState::Running | Fallback to 50:50 Fixed Split |
| Proc_EmergencyCutoff | /opt/autosar/bin/emergency_cutoff | Phase 1 (Safety Core) | Always Active | Hardware System Reset |


---

<!-- Page 41 -->
## Page 41: 9.3 State Management & Function Groups

### 9.3 State Management & Function Groups

Execution Management (ara::exec) is responsible for the structured startup, shutdown, deterministic execution, and operational state supervision of all software processes within the Adaptive Platform.

| Process Identifier | Binary Executable Path | Startup Order Phase | Function Group Binding | Recovery Action on Crash |
| :--- | :--- | :--- | :--- | :--- |
| Proc_PowertrainMgr | /opt/autosar/bin/powertrain_manager | Phase 3 (Applications) | MachineState::Running | Restart Process (Max 3 attempts) |
| Proc_TorqueArbiter | /opt/autosar/bin/torque_arbitration | Phase 3 (Applications) | MachineState::Running | Restart Process; if fail -> Limp Home |
| Proc_BatteryMgr | /opt/autosar/bin/battery_management | Phase 2 (Device Services) | MachineState::Running | Lock High-Voltage Safety Mode |
| Proc_ThermalMgr | /opt/autosar/bin/thermal_management | Phase 3 (Applications) | MachineState::Running | Run Pumps at 100% Fallback |
| Proc_VehicleMotion | /opt/autosar/bin/vehicle_motion | Phase 3 (Applications) | MachineState::Running | Fallback to 50:50 Fixed Split |
| Proc_EmergencyCutoff | /opt/autosar/bin/emergency_cutoff | Phase 1 (Safety Core) | Always Active | Hardware System Reset |


---

<!-- Page 42 -->
## Page 42: 9.4 Execution Client API & Process Health Reporting

### 9.4 Execution Client API & Process Health Reporting

Execution Management (ara::exec) is responsible for the structured startup, shutdown, deterministic execution, and operational state supervision of all software processes within the Adaptive Platform.

| Process Identifier | Binary Executable Path | Startup Order Phase | Function Group Binding | Recovery Action on Crash |
| :--- | :--- | :--- | :--- | :--- |
| Proc_PowertrainMgr | /opt/autosar/bin/powertrain_manager | Phase 3 (Applications) | MachineState::Running | Restart Process (Max 3 attempts) |
| Proc_TorqueArbiter | /opt/autosar/bin/torque_arbitration | Phase 3 (Applications) | MachineState::Running | Restart Process; if fail -> Limp Home |
| Proc_BatteryMgr | /opt/autosar/bin/battery_management | Phase 2 (Device Services) | MachineState::Running | Lock High-Voltage Safety Mode |
| Proc_ThermalMgr | /opt/autosar/bin/thermal_management | Phase 3 (Applications) | MachineState::Running | Run Pumps at 100% Fallback |
| Proc_VehicleMotion | /opt/autosar/bin/vehicle_motion | Phase 3 (Applications) | MachineState::Running | Fallback to 50:50 Fixed Split |
| Proc_EmergencyCutoff | /opt/autosar/bin/emergency_cutoff | Phase 1 (Safety Core) | Always Active | Hardware System Reset |


---

<!-- Page 43 -->
## Page 43: 9.5 Process Failure Containment & Core Recovery

### 9.5 Process Failure Containment & Core Recovery

Execution Management (ara::exec) is responsible for the structured startup, shutdown, deterministic execution, and operational state supervision of all software processes within the Adaptive Platform.

| Process Identifier | Binary Executable Path | Startup Order Phase | Function Group Binding | Recovery Action on Crash |
| :--- | :--- | :--- | :--- | :--- |
| Proc_PowertrainMgr | /opt/autosar/bin/powertrain_manager | Phase 3 (Applications) | MachineState::Running | Restart Process (Max 3 attempts) |
| Proc_TorqueArbiter | /opt/autosar/bin/torque_arbitration | Phase 3 (Applications) | MachineState::Running | Restart Process; if fail -> Limp Home |
| Proc_BatteryMgr | /opt/autosar/bin/battery_management | Phase 2 (Device Services) | MachineState::Running | Lock High-Voltage Safety Mode |
| Proc_ThermalMgr | /opt/autosar/bin/thermal_management | Phase 3 (Applications) | MachineState::Running | Run Pumps at 100% Fallback |
| Proc_VehicleMotion | /opt/autosar/bin/vehicle_motion | Phase 3 (Applications) | MachineState::Running | Fallback to 50:50 Fixed Split |
| Proc_EmergencyCutoff | /opt/autosar/bin/emergency_cutoff | Phase 1 (Safety Core) | Always Active | Hardware System Reset |


---

<!-- Page 44 -->
## Page 44: 10.1 Runnable Catalog: High-Frequency 1ms & 2ms Tasks

### 10.1 Runnable Catalog: High-Frequency 1ms & 2ms Tasks

Every Adaptive software component organizes its internal computation into discrete runnable entities triggered by periodic timers or asynchronous events.

| Runnable Entity Symbol | Parent Software Component | Trigger Type & Period | SCHED_FIFO Priority | Target Core Affinity |
| :--- | :--- | :--- | :--- | :--- |
| Runnable_EmergencyCutoff_1ms | EmergencyCutoff_SWC | Periodic 1.0 ms | Priority 99 (Max) | Core 3 (Isolated) |
| Runnable_InverterComm_2ms | InverterController_SWC | Periodic 2.0 ms | Priority 90 | Core 1 |
| Runnable_BatterySafety_5ms | BatteryManagement_SWC | Periodic 5.0 ms | Priority 85 | Core 0 |
| Runnable_ArbitrateTorque_10ms | TorqueArbitration_SWC | Periodic 10.0 ms | Priority 80 | Core 1 |
| Runnable_EvaluateDriverDemand_10ms | PowertrainManager_SWC | Periodic 10.0 ms | Priority 75 | Core 0 |
| Runnable_VehicleStability_10ms | VehicleMotion_SWC | Periodic 10.0 ms | Priority 70 | Core 1 |
| Runnable_MonitorThermal_100ms | ThermalManagement_SWC | Periodic 100.0 ms | Priority 40 | Core 2 |
| Runnable_DiagnosticHealth_1000ms | DiagnosticManager | Periodic 1000.0 ms | Priority 10 (Lowest) | Core 2 |


---

<!-- Page 45 -->
## Page 45: 10.2 Runnable Catalog: Real-Time 5ms & 10ms Tasks

### 10.2 Runnable Catalog: Real-Time 5ms & 10ms Tasks

Every Adaptive software component organizes its internal computation into discrete runnable entities triggered by periodic timers or asynchronous events.

| Runnable Entity Symbol | Parent Software Component | Trigger Type & Period | SCHED_FIFO Priority | Target Core Affinity |
| :--- | :--- | :--- | :--- | :--- |
| Runnable_EmergencyCutoff_1ms | EmergencyCutoff_SWC | Periodic 1.0 ms | Priority 99 (Max) | Core 3 (Isolated) |
| Runnable_InverterComm_2ms | InverterController_SWC | Periodic 2.0 ms | Priority 90 | Core 1 |
| Runnable_BatterySafety_5ms | BatteryManagement_SWC | Periodic 5.0 ms | Priority 85 | Core 0 |
| Runnable_ArbitrateTorque_10ms | TorqueArbitration_SWC | Periodic 10.0 ms | Priority 80 | Core 1 |
| Runnable_EvaluateDriverDemand_10ms | PowertrainManager_SWC | Periodic 10.0 ms | Priority 75 | Core 0 |
| Runnable_VehicleStability_10ms | VehicleMotion_SWC | Periodic 10.0 ms | Priority 70 | Core 1 |
| Runnable_MonitorThermal_100ms | ThermalManagement_SWC | Periodic 100.0 ms | Priority 40 | Core 2 |
| Runnable_DiagnosticHealth_1000ms | DiagnosticManager | Periodic 1000.0 ms | Priority 10 (Lowest) | Core 2 |


---

<!-- Page 46 -->
## Page 46: 10.3 Runnable Catalog: Mid-Frequency 20ms & 50ms Tasks

### 10.3 Runnable Catalog: Mid-Frequency 20ms & 50ms Tasks

Every Adaptive software component organizes its internal computation into discrete runnable entities triggered by periodic timers or asynchronous events.

| Runnable Entity Symbol | Parent Software Component | Trigger Type & Period | SCHED_FIFO Priority | Target Core Affinity |
| :--- | :--- | :--- | :--- | :--- |
| Runnable_EmergencyCutoff_1ms | EmergencyCutoff_SWC | Periodic 1.0 ms | Priority 99 (Max) | Core 3 (Isolated) |
| Runnable_InverterComm_2ms | InverterController_SWC | Periodic 2.0 ms | Priority 90 | Core 1 |
| Runnable_BatterySafety_5ms | BatteryManagement_SWC | Periodic 5.0 ms | Priority 85 | Core 0 |
| Runnable_ArbitrateTorque_10ms | TorqueArbitration_SWC | Periodic 10.0 ms | Priority 80 | Core 1 |
| Runnable_EvaluateDriverDemand_10ms | PowertrainManager_SWC | Periodic 10.0 ms | Priority 75 | Core 0 |
| Runnable_VehicleStability_10ms | VehicleMotion_SWC | Periodic 10.0 ms | Priority 70 | Core 1 |
| Runnable_MonitorThermal_100ms | ThermalManagement_SWC | Periodic 100.0 ms | Priority 40 | Core 2 |
| Runnable_DiagnosticHealth_1000ms | DiagnosticManager | Periodic 1000.0 ms | Priority 10 (Lowest) | Core 2 |


---

<!-- Page 47 -->
## Page 47: 10.4 Runnable Catalog: Low-Frequency 100ms & 1000ms Tasks

### 10.4 Runnable Catalog: Low-Frequency 100ms & 1000ms Tasks

Every Adaptive software component organizes its internal computation into discrete runnable entities triggered by periodic timers or asynchronous events.

| Runnable Entity Symbol | Parent Software Component | Trigger Type & Period | SCHED_FIFO Priority | Target Core Affinity |
| :--- | :--- | :--- | :--- | :--- |
| Runnable_EmergencyCutoff_1ms | EmergencyCutoff_SWC | Periodic 1.0 ms | Priority 99 (Max) | Core 3 (Isolated) |
| Runnable_InverterComm_2ms | InverterController_SWC | Periodic 2.0 ms | Priority 90 | Core 1 |
| Runnable_BatterySafety_5ms | BatteryManagement_SWC | Periodic 5.0 ms | Priority 85 | Core 0 |
| Runnable_ArbitrateTorque_10ms | TorqueArbitration_SWC | Periodic 10.0 ms | Priority 80 | Core 1 |
| Runnable_EvaluateDriverDemand_10ms | PowertrainManager_SWC | Periodic 10.0 ms | Priority 75 | Core 0 |
| Runnable_VehicleStability_10ms | VehicleMotion_SWC | Periodic 10.0 ms | Priority 70 | Core 1 |
| Runnable_MonitorThermal_100ms | ThermalManagement_SWC | Periodic 100.0 ms | Priority 40 | Core 2 |
| Runnable_DiagnosticHealth_1000ms | DiagnosticManager | Periodic 1000.0 ms | Priority 10 (Lowest) | Core 2 |


---

<!-- Page 48 -->
## Page 48: 10.5 CPU Core Affinity & Scheduling Priority Allocation

### 10.5 CPU Core Affinity & Scheduling Priority Allocation

Every Adaptive software component organizes its internal computation into discrete runnable entities triggered by periodic timers or asynchronous events.

| Runnable Entity Symbol | Parent Software Component | Trigger Type & Period | SCHED_FIFO Priority | Target Core Affinity |
| :--- | :--- | :--- | :--- | :--- |
| Runnable_EmergencyCutoff_1ms | EmergencyCutoff_SWC | Periodic 1.0 ms | Priority 99 (Max) | Core 3 (Isolated) |
| Runnable_InverterComm_2ms | InverterController_SWC | Periodic 2.0 ms | Priority 90 | Core 1 |
| Runnable_BatterySafety_5ms | BatteryManagement_SWC | Periodic 5.0 ms | Priority 85 | Core 0 |
| Runnable_ArbitrateTorque_10ms | TorqueArbitration_SWC | Periodic 10.0 ms | Priority 80 | Core 1 |
| Runnable_EvaluateDriverDemand_10ms | PowertrainManager_SWC | Periodic 10.0 ms | Priority 75 | Core 0 |
| Runnable_VehicleStability_10ms | VehicleMotion_SWC | Periodic 10.0 ms | Priority 70 | Core 1 |
| Runnable_MonitorThermal_100ms | ThermalManagement_SWC | Periodic 100.0 ms | Priority 40 | Core 2 |
| Runnable_DiagnosticHealth_1000ms | DiagnosticManager | Periodic 1000.0 ms | Priority 10 (Lowest) | Core 2 |


---

<!-- Page 49 -->
## Page 49: 11.1 Service-Oriented Architecture (SOA) Foundations

### 11.1 Service-Oriented Architecture (SOA) Foundations

Communication Management (ara::com) provides a unified, location-transparent communication abstraction for intra-machine IPC and inter-ECU SOME/IP network traffic.

| Service Interface Symbol | Service ID | Communication Pattern | Transport Binding | E2E Protection Profile |
| :--- | :--- | :--- | :--- | :--- |
| IPowertrainCoordination | 0x1001 | Publish-Subscribe Events + Methods | SOME/IP over UDP | E2E Profile 11 (CRC-32) |
| ITorqueCommand | 0x1002 | Publish-Subscribe Events | SOME/IP over UDP | E2E Profile 11 (CRC-32) |
| IBatteryStatus | 0x1003 | Publish-Subscribe Events | SOME/IP over UDP | E2E Profile 4 (CRC-16) |
| IThermalTelemetry | 0x1004 | Publish-Subscribe Events | SOME/IP over TCP | None (Standard CRC) |
| IVehicleDynamics | 0x1005 | Publish-Subscribe Events | SOME/IP over UDP | E2E Profile 11 (CRC-32) |
| IEmergencySafetyCutoff | 0x1000 | Direct IPC / Shared Memory | ara::com Zero-Copy | E2E Profile 11 (Double Hash) |


---

<!-- Page 50 -->
## Page 50: 11.2 Publish-Subscribe Event Communication Patterns

### 11.2 Publish-Subscribe Event Communication Patterns

Communication Management (ara::com) provides a unified, location-transparent communication abstraction for intra-machine IPC and inter-ECU SOME/IP network traffic.

| Service Interface Symbol | Service ID | Communication Pattern | Transport Binding | E2E Protection Profile |
| :--- | :--- | :--- | :--- | :--- |
| IPowertrainCoordination | 0x1001 | Publish-Subscribe Events + Methods | SOME/IP over UDP | E2E Profile 11 (CRC-32) |
| ITorqueCommand | 0x1002 | Publish-Subscribe Events | SOME/IP over UDP | E2E Profile 11 (CRC-32) |
| IBatteryStatus | 0x1003 | Publish-Subscribe Events | SOME/IP over UDP | E2E Profile 4 (CRC-16) |
| IThermalTelemetry | 0x1004 | Publish-Subscribe Events | SOME/IP over TCP | None (Standard CRC) |
| IVehicleDynamics | 0x1005 | Publish-Subscribe Events | SOME/IP over UDP | E2E Profile 11 (CRC-32) |
| IEmergencySafetyCutoff | 0x1000 | Direct IPC / Shared Memory | ara::com Zero-Copy | E2E Profile 11 (Double Hash) |


---

<!-- Page 51 -->
## Page 51: 11.3 Request-Response Method RPC Architectures

### 11.3 Request-Response Method RPC Architectures

Communication Management (ara::com) provides a unified, location-transparent communication abstraction for intra-machine IPC and inter-ECU SOME/IP network traffic.

| Service Interface Symbol | Service ID | Communication Pattern | Transport Binding | E2E Protection Profile |
| :--- | :--- | :--- | :--- | :--- |
| IPowertrainCoordination | 0x1001 | Publish-Subscribe Events + Methods | SOME/IP over UDP | E2E Profile 11 (CRC-32) |
| ITorqueCommand | 0x1002 | Publish-Subscribe Events | SOME/IP over UDP | E2E Profile 11 (CRC-32) |
| IBatteryStatus | 0x1003 | Publish-Subscribe Events | SOME/IP over UDP | E2E Profile 4 (CRC-16) |
| IThermalTelemetry | 0x1004 | Publish-Subscribe Events | SOME/IP over TCP | None (Standard CRC) |
| IVehicleDynamics | 0x1005 | Publish-Subscribe Events | SOME/IP over UDP | E2E Profile 11 (CRC-32) |
| IEmergencySafetyCutoff | 0x1000 | Direct IPC / Shared Memory | ara::com Zero-Copy | E2E Profile 11 (Double Hash) |


---

<!-- Page 52 -->
## Page 52: 11.4 End-to-End (E2E) Communication Protection

### 11.4 End-to-End (E2E) Communication Protection

Communication Management (ara::com) provides a unified, location-transparent communication abstraction for intra-machine IPC and inter-ECU SOME/IP network traffic.

| Service Interface Symbol | Service ID | Communication Pattern | Transport Binding | E2E Protection Profile |
| :--- | :--- | :--- | :--- | :--- |
| IPowertrainCoordination | 0x1001 | Publish-Subscribe Events + Methods | SOME/IP over UDP | E2E Profile 11 (CRC-32) |
| ITorqueCommand | 0x1002 | Publish-Subscribe Events | SOME/IP over UDP | E2E Profile 11 (CRC-32) |
| IBatteryStatus | 0x1003 | Publish-Subscribe Events | SOME/IP over UDP | E2E Profile 4 (CRC-16) |
| IThermalTelemetry | 0x1004 | Publish-Subscribe Events | SOME/IP over TCP | None (Standard CRC) |
| IVehicleDynamics | 0x1005 | Publish-Subscribe Events | SOME/IP over UDP | E2E Profile 11 (CRC-32) |
| IEmergencySafetyCutoff | 0x1000 | Direct IPC / Shared Memory | ara::com Zero-Copy | E2E Profile 11 (Double Hash) |


---

<!-- Page 53 -->
## Page 53: 11.5 Network Serialization & Zero-Copy IPC Optimization

### 11.5 Network Serialization & Zero-Copy IPC Optimization

Communication Management (ara::com) provides a unified, location-transparent communication abstraction for intra-machine IPC and inter-ECU SOME/IP network traffic.

| Service Interface Symbol | Service ID | Communication Pattern | Transport Binding | E2E Protection Profile |
| :--- | :--- | :--- | :--- | :--- |
| IPowertrainCoordination | 0x1001 | Publish-Subscribe Events + Methods | SOME/IP over UDP | E2E Profile 11 (CRC-32) |
| ITorqueCommand | 0x1002 | Publish-Subscribe Events | SOME/IP over UDP | E2E Profile 11 (CRC-32) |
| IBatteryStatus | 0x1003 | Publish-Subscribe Events | SOME/IP over UDP | E2E Profile 4 (CRC-16) |
| IThermalTelemetry | 0x1004 | Publish-Subscribe Events | SOME/IP over TCP | None (Standard CRC) |
| IVehicleDynamics | 0x1005 | Publish-Subscribe Events | SOME/IP over UDP | E2E Profile 11 (CRC-32) |
| IEmergencySafetyCutoff | 0x1000 | Direct IPC / Shared Memory | ara::com Zero-Copy | E2E Profile 11 (Double Hash) |


---

<!-- Page 54 -->
## Page 54: 12.1 Service Interface: IPowertrainCoordination (0x1001)

### 12.1 Service Interface: IPowertrainCoordination (0x1001)

This section formalizes the exact data structures, member types, scaling equations, physical boundaries, and invalid value indicators for this interface.

| Field / Member Name | Data Type | Scaling Factor | Physical Range | Invalid Value Indicator |
| :--- | :--- | :--- | :--- | :--- |
| TargetTorque_Front | int16_t | 0.1 Nm / LSB | -300.0 to +300.0 Nm | 0x7FFF (Invalid) |
| TargetTorque_Rear | int16_t | 0.1 Nm / LSB | -500.0 to +500.0 Nm | 0x7FFF (Invalid) |
| TorqueLimit_Discharge | uint16_t | 0.1 Nm / LSB | 0.0 to +800.0 Nm | 0xFFFF (Invalid) |
| TorqueLimit_Regen | uint16_t | 0.1 Nm / LSB | 0.0 to +400.0 Nm | 0xFFFF (Invalid) |
| SequenceCounter | uint8_t | 1 unit / LSB | 0 to 255 (Rolling) | No Invalid State |
| SafetyCRC | uint32_t | Bitmask | 0x00000000 - 0xFFFFFFFF | 0x00000000 |


---

<!-- Page 55 -->
## Page 55: 12.2 Service Interface: ITorqueCommand (0x1002)

### 12.2 Service Interface: ITorqueCommand (0x1002)

This section formalizes the exact data structures, member types, scaling equations, physical boundaries, and invalid value indicators for this interface.

| Field / Member Name | Data Type | Scaling Factor | Physical Range | Invalid Value Indicator |
| :--- | :--- | :--- | :--- | :--- |
| TargetTorque_Front | int16_t | 0.1 Nm / LSB | -300.0 to +300.0 Nm | 0x7FFF (Invalid) |
| TargetTorque_Rear | int16_t | 0.1 Nm / LSB | -500.0 to +500.0 Nm | 0x7FFF (Invalid) |
| TorqueLimit_Discharge | uint16_t | 0.1 Nm / LSB | 0.0 to +800.0 Nm | 0xFFFF (Invalid) |
| TorqueLimit_Regen | uint16_t | 0.1 Nm / LSB | 0.0 to +400.0 Nm | 0xFFFF (Invalid) |
| SequenceCounter | uint8_t | 1 unit / LSB | 0 to 255 (Rolling) | No Invalid State |
| SafetyCRC | uint32_t | Bitmask | 0x00000000 - 0xFFFFFFFF | 0x00000000 |


---

<!-- Page 56 -->
## Page 56: 12.3 Service Interface: IBatteryStatus (0x1003)

### 12.3 Service Interface: IBatteryStatus (0x1003)

This section formalizes the exact data structures, member types, scaling equations, physical boundaries, and invalid value indicators for this interface.

| Field / Member Name | Data Type | Scaling Factor | Physical Range | Invalid Value Indicator |
| :--- | :--- | :--- | :--- | :--- |
| TargetTorque_Front | int16_t | 0.1 Nm / LSB | -300.0 to +300.0 Nm | 0x7FFF (Invalid) |
| TargetTorque_Rear | int16_t | 0.1 Nm / LSB | -500.0 to +500.0 Nm | 0x7FFF (Invalid) |
| TorqueLimit_Discharge | uint16_t | 0.1 Nm / LSB | 0.0 to +800.0 Nm | 0xFFFF (Invalid) |
| TorqueLimit_Regen | uint16_t | 0.1 Nm / LSB | 0.0 to +400.0 Nm | 0xFFFF (Invalid) |
| SequenceCounter | uint8_t | 1 unit / LSB | 0 to 255 (Rolling) | No Invalid State |
| SafetyCRC | uint32_t | Bitmask | 0x00000000 - 0xFFFFFFFF | 0x00000000 |


---

<!-- Page 57 -->
## Page 57: 12.4 Service Interface: IThermalTelemetry (0x1004)

### 12.4 Service Interface: IThermalTelemetry (0x1004)

This section formalizes the exact data structures, member types, scaling equations, physical boundaries, and invalid value indicators for this interface.

| Field / Member Name | Data Type | Scaling Factor | Physical Range | Invalid Value Indicator |
| :--- | :--- | :--- | :--- | :--- |
| TargetTorque_Front | int16_t | 0.1 Nm / LSB | -300.0 to +300.0 Nm | 0x7FFF (Invalid) |
| TargetTorque_Rear | int16_t | 0.1 Nm / LSB | -500.0 to +500.0 Nm | 0x7FFF (Invalid) |
| TorqueLimit_Discharge | uint16_t | 0.1 Nm / LSB | 0.0 to +800.0 Nm | 0xFFFF (Invalid) |
| TorqueLimit_Regen | uint16_t | 0.1 Nm / LSB | 0.0 to +400.0 Nm | 0xFFFF (Invalid) |
| SequenceCounter | uint8_t | 1 unit / LSB | 0 to 255 (Rolling) | No Invalid State |
| SafetyCRC | uint32_t | Bitmask | 0x00000000 - 0xFFFFFFFF | 0x00000000 |


---

<!-- Page 58 -->
## Page 58: 12.5 Service Interface: IVehicleDynamics (0x1005)

### 12.5 Service Interface: IVehicleDynamics (0x1005)

This section formalizes the exact data structures, member types, scaling equations, physical boundaries, and invalid value indicators for this interface.

| Field / Member Name | Data Type | Scaling Factor | Physical Range | Invalid Value Indicator |
| :--- | :--- | :--- | :--- | :--- |
| TargetTorque_Front | int16_t | 0.1 Nm / LSB | -300.0 to +300.0 Nm | 0x7FFF (Invalid) |
| TargetTorque_Rear | int16_t | 0.1 Nm / LSB | -500.0 to +500.0 Nm | 0x7FFF (Invalid) |
| TorqueLimit_Discharge | uint16_t | 0.1 Nm / LSB | 0.0 to +800.0 Nm | 0xFFFF (Invalid) |
| TorqueLimit_Regen | uint16_t | 0.1 Nm / LSB | 0.0 to +400.0 Nm | 0xFFFF (Invalid) |
| SequenceCounter | uint8_t | 1 unit / LSB | 0 to 255 (Rolling) | No Invalid State |
| SafetyCRC | uint32_t | Bitmask | 0x00000000 - 0xFFFFFFFF | 0x00000000 |


---

<!-- Page 59 -->
## Page 59: 12.6 Service Interface: IEmergencySafetyCutoff (0x1000)

### 12.6 Service Interface: IEmergencySafetyCutoff (0x1000)

This section formalizes the exact data structures, member types, scaling equations, physical boundaries, and invalid value indicators for this interface.

| Field / Member Name | Data Type | Scaling Factor | Physical Range | Invalid Value Indicator |
| :--- | :--- | :--- | :--- | :--- |
| TargetTorque_Front | int16_t | 0.1 Nm / LSB | -300.0 to +300.0 Nm | 0x7FFF (Invalid) |
| TargetTorque_Rear | int16_t | 0.1 Nm / LSB | -500.0 to +500.0 Nm | 0x7FFF (Invalid) |
| TorqueLimit_Discharge | uint16_t | 0.1 Nm / LSB | 0.0 to +800.0 Nm | 0xFFFF (Invalid) |
| TorqueLimit_Regen | uint16_t | 0.1 Nm / LSB | 0.0 to +400.0 Nm | 0xFFFF (Invalid) |
| SequenceCounter | uint8_t | 1 unit / LSB | 0 to 255 (Rolling) | No Invalid State |
| SafetyCRC | uint32_t | Bitmask | 0x00000000 - 0xFFFFFFFF | 0x00000000 |


---

<!-- Page 60 -->
## Page 60: 12.7 Complete Signal Dictionary & Physical Unit Mapping

### 12.7 Complete Signal Dictionary & Physical Unit Mapping

This section formalizes the exact data structures, member types, scaling equations, physical boundaries, and invalid value indicators for this interface.

| Field / Member Name | Data Type | Scaling Factor | Physical Range | Invalid Value Indicator |
| :--- | :--- | :--- | :--- | :--- |
| TargetTorque_Front | int16_t | 0.1 Nm / LSB | -300.0 to +300.0 Nm | 0x7FFF (Invalid) |
| TargetTorque_Rear | int16_t | 0.1 Nm / LSB | -500.0 to +500.0 Nm | 0x7FFF (Invalid) |
| TorqueLimit_Discharge | uint16_t | 0.1 Nm / LSB | 0.0 to +800.0 Nm | 0xFFFF (Invalid) |
| TorqueLimit_Regen | uint16_t | 0.1 Nm / LSB | 0.0 to +400.0 Nm | 0xFFFF (Invalid) |
| SequenceCounter | uint8_t | 1 unit / LSB | 0 to 255 (Rolling) | No Invalid State |
| SafetyCRC | uint32_t | Bitmask | 0x00000000 - 0xFFFFFFFF | 0x00000000 |


---

<!-- Page 61 -->
## Page 61: 13.1 SOME/IP Header Format & Serialization Standard

### 13.1 SOME/IP Header Format & Serialization Standard

Scalable service-Oriented MiddlewarE over IP (SOME/IP) is the automotive standard transport protocol for high-bandwidth Adaptive AUTOSAR communication.

| Network Parameter | Configured Value | Protocol Reference | Network Architecture Impact |
| :--- | :--- | :--- | :--- |
| ePDC IP Address | 192.168.10.15 / 24 | IPv4 Static Host | Primary powertrain controller address |
| SOME/IP-SD Multicast IP | 239.255.0.1 | IETF RFC 2365 | All powertrain nodes listen on this address |
| SOME/IP-SD UDP Port | 30490 | AUTOSAR SD Specification | Standardized service discovery port |
| Real-Time VLAN ID | VLAN 100 (Priority 6) | IEEE 802.1Q | Guaranteed bandwidth for torque messages |
| Diagnostic VLAN ID | VLAN 200 (Priority 2) | IEEE 802.1Q | DoIP diagnostic communication traffic |


---

<!-- Page 62 -->
## Page 62: 13.2 Service Discovery (SOME/IP-SD) Entry Formats

### 13.2 Service Discovery (SOME/IP-SD) Entry Formats

Scalable service-Oriented MiddlewarE over IP (SOME/IP) is the automotive standard transport protocol for high-bandwidth Adaptive AUTOSAR communication.

| Network Parameter | Configured Value | Protocol Reference | Network Architecture Impact |
| :--- | :--- | :--- | :--- |
| ePDC IP Address | 192.168.10.15 / 24 | IPv4 Static Host | Primary powertrain controller address |
| SOME/IP-SD Multicast IP | 239.255.0.1 | IETF RFC 2365 | All powertrain nodes listen on this address |
| SOME/IP-SD UDP Port | 30490 | AUTOSAR SD Specification | Standardized service discovery port |
| Real-Time VLAN ID | VLAN 100 (Priority 6) | IEEE 802.1Q | Guaranteed bandwidth for torque messages |
| Diagnostic VLAN ID | VLAN 200 (Priority 2) | IEEE 802.1Q | DoIP diagnostic communication traffic |


---

<!-- Page 63 -->
## Page 63: 13.3 Network Topology: IP Endpoints & VLAN Partitioning

### 13.3 Network Topology: IP Endpoints & VLAN Partitioning

Scalable service-Oriented MiddlewarE over IP (SOME/IP) is the automotive standard transport protocol for high-bandwidth Adaptive AUTOSAR communication.

| Network Parameter | Configured Value | Protocol Reference | Network Architecture Impact |
| :--- | :--- | :--- | :--- |
| ePDC IP Address | 192.168.10.15 / 24 | IPv4 Static Host | Primary powertrain controller address |
| SOME/IP-SD Multicast IP | 239.255.0.1 | IETF RFC 2365 | All powertrain nodes listen on this address |
| SOME/IP-SD UDP Port | 30490 | AUTOSAR SD Specification | Standardized service discovery port |
| Real-Time VLAN ID | VLAN 100 (Priority 6) | IEEE 802.1Q | Guaranteed bandwidth for torque messages |
| Diagnostic VLAN ID | VLAN 200 (Priority 2) | IEEE 802.1Q | DoIP diagnostic communication traffic |


---

<!-- Page 64 -->
## Page 64: 13.4 Eventgroup Subscription & Multicast Routing

### 13.4 Eventgroup Subscription & Multicast Routing

Scalable service-Oriented MiddlewarE over IP (SOME/IP) is the automotive standard transport protocol for high-bandwidth Adaptive AUTOSAR communication.

| Network Parameter | Configured Value | Protocol Reference | Network Architecture Impact |
| :--- | :--- | :--- | :--- |
| ePDC IP Address | 192.168.10.15 / 24 | IPv4 Static Host | Primary powertrain controller address |
| SOME/IP-SD Multicast IP | 239.255.0.1 | IETF RFC 2365 | All powertrain nodes listen on this address |
| SOME/IP-SD UDP Port | 30490 | AUTOSAR SD Specification | Standardized service discovery port |
| Real-Time VLAN ID | VLAN 100 (Priority 6) | IEEE 802.1Q | Guaranteed bandwidth for torque messages |
| Diagnostic VLAN ID | VLAN 200 (Priority 2) | IEEE 802.1Q | DoIP diagnostic communication traffic |


---

<!-- Page 65 -->
## Page 65: 13.5 SOME/IP Error Codes & RPC Return Codes

### 13.5 SOME/IP Error Codes & RPC Return Codes

Scalable service-Oriented MiddlewarE over IP (SOME/IP) is the automotive standard transport protocol for high-bandwidth Adaptive AUTOSAR communication.

| Network Parameter | Configured Value | Protocol Reference | Network Architecture Impact |
| :--- | :--- | :--- | :--- |
| ePDC IP Address | 192.168.10.15 / 24 | IPv4 Static Host | Primary powertrain controller address |
| SOME/IP-SD Multicast IP | 239.255.0.1 | IETF RFC 2365 | All powertrain nodes listen on this address |
| SOME/IP-SD UDP Port | 30490 | AUTOSAR SD Specification | Standardized service discovery port |
| Real-Time VLAN ID | VLAN 100 (Priority 6) | IEEE 802.1Q | Guaranteed bandwidth for torque messages |
| Diagnostic VLAN ID | VLAN 200 (Priority 2) | IEEE 802.1Q | DoIP diagnostic communication traffic |


---

<!-- Page 66 -->
## Page 66: 14.1 Persistency Management (ara::per) Architecture

### 14.1 Persistency Management (ara::per) Architecture

Persistency Management (ara::per) guarantees deterministic, atomic access to non-volatile flash storage across vehicle power loss events.

| Persisted Item Key | Data Structure Type | Max Size | Update Frequency | Integrity Protection |
| :--- | :--- | :--- | :--- | :--- |
| CFG_PedalResponseMap | Array of Float (20x2) | 320 Bytes | Manufacturing / Service | CRC-32 + Digital Signature |
| CAL_MotorThermalLimits | Struct ThermalCoeffs | 128 Bytes | Manufacturing / Service | CRC-32 |
| NV_OdometerTotalEnergy | uint64_t (Watt-hours) | 8 Bytes | Every 1.0 km traveled | Double-buffered + Journal |
| NV_ContactorCycleCount | uint32_t (Cycles) | 4 Bytes | On vehicle shutdown | Atomic Flash Write |
| DTC_FreezeFrameStore | Array of Snapshots (64) | 16.0 KB | On diagnostic event | Crash-safe File Storage |


---

<!-- Page 67 -->
## Page 67: 14.2 Non-Volatile Calibration Parameter Catalog

### 14.2 Non-Volatile Calibration Parameter Catalog

Persistency Management (ara::per) guarantees deterministic, atomic access to non-volatile flash storage across vehicle power loss events.

| Persisted Item Key | Data Structure Type | Max Size | Update Frequency | Integrity Protection |
| :--- | :--- | :--- | :--- | :--- |
| CFG_PedalResponseMap | Array of Float (20x2) | 320 Bytes | Manufacturing / Service | CRC-32 + Digital Signature |
| CAL_MotorThermalLimits | Struct ThermalCoeffs | 128 Bytes | Manufacturing / Service | CRC-32 |
| NV_OdometerTotalEnergy | uint64_t (Watt-hours) | 8 Bytes | Every 1.0 km traveled | Double-buffered + Journal |
| NV_ContactorCycleCount | uint32_t (Cycles) | 4 Bytes | On vehicle shutdown | Atomic Flash Write |
| DTC_FreezeFrameStore | Array of Snapshots (64) | 16.0 KB | On diagnostic event | Crash-safe File Storage |


---

<!-- Page 68 -->
## Page 68: 14.3 Flash Wear-Leveling & Redundancy Pools

### 14.3 Flash Wear-Leveling & Redundancy Pools

Persistency Management (ara::per) guarantees deterministic, atomic access to non-volatile flash storage across vehicle power loss events.

| Persisted Item Key | Data Structure Type | Max Size | Update Frequency | Integrity Protection |
| :--- | :--- | :--- | :--- | :--- |
| CFG_PedalResponseMap | Array of Float (20x2) | 320 Bytes | Manufacturing / Service | CRC-32 + Digital Signature |
| CAL_MotorThermalLimits | Struct ThermalCoeffs | 128 Bytes | Manufacturing / Service | CRC-32 |
| NV_OdometerTotalEnergy | uint64_t (Watt-hours) | 8 Bytes | Every 1.0 km traveled | Double-buffered + Journal |
| NV_ContactorCycleCount | uint32_t (Cycles) | 4 Bytes | On vehicle shutdown | Atomic Flash Write |
| DTC_FreezeFrameStore | Array of Snapshots (64) | 16.0 KB | On diagnostic event | Crash-safe File Storage |


---

<!-- Page 69 -->
## Page 69: 14.4 Crash-Safe Transactional Persistence Strategy

### 14.4 Crash-Safe Transactional Persistence Strategy

Persistency Management (ara::per) guarantees deterministic, atomic access to non-volatile flash storage across vehicle power loss events.

| Persisted Item Key | Data Structure Type | Max Size | Update Frequency | Integrity Protection |
| :--- | :--- | :--- | :--- | :--- |
| CFG_PedalResponseMap | Array of Float (20x2) | 320 Bytes | Manufacturing / Service | CRC-32 + Digital Signature |
| CAL_MotorThermalLimits | Struct ThermalCoeffs | 128 Bytes | Manufacturing / Service | CRC-32 |
| NV_OdometerTotalEnergy | uint64_t (Watt-hours) | 8 Bytes | Every 1.0 km traveled | Double-buffered + Journal |
| NV_ContactorCycleCount | uint32_t (Cycles) | 4 Bytes | On vehicle shutdown | Atomic Flash Write |
| DTC_FreezeFrameStore | Array of Snapshots (64) | 16.0 KB | On diagnostic event | Crash-safe File Storage |


---

<!-- Page 70 -->
## Page 70: 15.1 Diagnostic Management (ara::diag) & DoIP Architecture

### 15.1 Diagnostic Management (ara::diag) & DoIP Architecture

Diagnostic Management (ara::diag) provides standardized UDS service routing over Ethernet DoIP (ISO 13400) for offboard scan tools.

| DTC Identifier | Diagnostic Trouble Description | Fault Trigger Condition | Debounce Filter | Primary System Action |
| :--- | :--- | :--- | :--- | :--- |
| DTC_P0A1F | Battery Management System Internal Error | BMS microcontroller self-test failure | Immediate (0ms) | Inhibit fast charge, alert driver |
| DTC_P0A80 | Replace Hybrid/EV Battery Pack | Cell capacity delta > 25% across modules | 10 drive cycles | Limp home mode, illuminated MIL |
| DTC_P0C00 | Drive Motor Phase U Current Imbalance | Motor current sensor mismatch > 15A | 20 ms continuous | Inverter 3-phase Active Short Circuit |
| DTC_U0100 | Lost Communication With ECM/PCM | SOME/IP heartbeat missing for > 100 ms | 100 ms timeout | Autonomous driving abort to safe stop |
| DTC_P0A0D | High Voltage System Interlock Circuit Open | HVIL continuity signal lost | 10 ms immediate | Open main contactors within 10 ms |


---

<!-- Page 71 -->
## Page 71: 15.2 Diagnostic Trouble Code (DTC) Master Catalog

### 15.2 Diagnostic Trouble Code (DTC) Master Catalog

Diagnostic Management (ara::diag) provides standardized UDS service routing over Ethernet DoIP (ISO 13400) for offboard scan tools.

| DTC Identifier | Diagnostic Trouble Description | Fault Trigger Condition | Debounce Filter | Primary System Action |
| :--- | :--- | :--- | :--- | :--- |
| DTC_P0A1F | Battery Management System Internal Error | BMS microcontroller self-test failure | Immediate (0ms) | Inhibit fast charge, alert driver |
| DTC_P0A80 | Replace Hybrid/EV Battery Pack | Cell capacity delta > 25% across modules | 10 drive cycles | Limp home mode, illuminated MIL |
| DTC_P0C00 | Drive Motor Phase U Current Imbalance | Motor current sensor mismatch > 15A | 20 ms continuous | Inverter 3-phase Active Short Circuit |
| DTC_U0100 | Lost Communication With ECM/PCM | SOME/IP heartbeat missing for > 100 ms | 100 ms timeout | Autonomous driving abort to safe stop |
| DTC_P0A0D | High Voltage System Interlock Circuit Open | HVIL continuity signal lost | 10 ms immediate | Open main contactors within 10 ms |


---

<!-- Page 72 -->
## Page 72: 15.3 Freeze Frame Data Definitions & Trigger Conditions

### 15.3 Freeze Frame Data Definitions & Trigger Conditions

Diagnostic Management (ara::diag) provides standardized UDS service routing over Ethernet DoIP (ISO 13400) for offboard scan tools.

| DTC Identifier | Diagnostic Trouble Description | Fault Trigger Condition | Debounce Filter | Primary System Action |
| :--- | :--- | :--- | :--- | :--- |
| DTC_P0A1F | Battery Management System Internal Error | BMS microcontroller self-test failure | Immediate (0ms) | Inhibit fast charge, alert driver |
| DTC_P0A80 | Replace Hybrid/EV Battery Pack | Cell capacity delta > 25% across modules | 10 drive cycles | Limp home mode, illuminated MIL |
| DTC_P0C00 | Drive Motor Phase U Current Imbalance | Motor current sensor mismatch > 15A | 20 ms continuous | Inverter 3-phase Active Short Circuit |
| DTC_U0100 | Lost Communication With ECM/PCM | SOME/IP heartbeat missing for > 100 ms | 100 ms timeout | Autonomous driving abort to safe stop |
| DTC_P0A0D | High Voltage System Interlock Circuit Open | HVIL continuity signal lost | 10 ms immediate | Open main contactors within 10 ms |


---

<!-- Page 73 -->
## Page 73: 15.4 Diagnostic Log and Trace (DLT) Logging Framework

### 15.4 Diagnostic Log and Trace (DLT) Logging Framework

Diagnostic Management (ara::diag) provides standardized UDS service routing over Ethernet DoIP (ISO 13400) for offboard scan tools.

| DTC Identifier | Diagnostic Trouble Description | Fault Trigger Condition | Debounce Filter | Primary System Action |
| :--- | :--- | :--- | :--- | :--- |
| DTC_P0A1F | Battery Management System Internal Error | BMS microcontroller self-test failure | Immediate (0ms) | Inhibit fast charge, alert driver |
| DTC_P0A80 | Replace Hybrid/EV Battery Pack | Cell capacity delta > 25% across modules | 10 drive cycles | Limp home mode, illuminated MIL |
| DTC_P0C00 | Drive Motor Phase U Current Imbalance | Motor current sensor mismatch > 15A | 20 ms continuous | Inverter 3-phase Active Short Circuit |
| DTC_U0100 | Lost Communication With ECM/PCM | SOME/IP heartbeat missing for > 100 ms | 100 ms timeout | Autonomous driving abort to safe stop |
| DTC_P0A0D | High Voltage System Interlock Circuit Open | HVIL continuity signal lost | 10 ms immediate | Open main contactors within 10 ms |


---

<!-- Page 74 -->
## Page 74: 15.5 Supervised Entity Health Monitoring & Watchdog Integration

### 15.5 Supervised Entity Health Monitoring & Watchdog Integration

Diagnostic Management (ara::diag) provides standardized UDS service routing over Ethernet DoIP (ISO 13400) for offboard scan tools.

| DTC Identifier | Diagnostic Trouble Description | Fault Trigger Condition | Debounce Filter | Primary System Action |
| :--- | :--- | :--- | :--- | :--- |
| DTC_P0A1F | Battery Management System Internal Error | BMS microcontroller self-test failure | Immediate (0ms) | Inhibit fast charge, alert driver |
| DTC_P0A80 | Replace Hybrid/EV Battery Pack | Cell capacity delta > 25% across modules | 10 drive cycles | Limp home mode, illuminated MIL |
| DTC_P0C00 | Drive Motor Phase U Current Imbalance | Motor current sensor mismatch > 15A | 20 ms continuous | Inverter 3-phase Active Short Circuit |
| DTC_U0100 | Lost Communication With ECM/PCM | SOME/IP heartbeat missing for > 100 ms | 100 ms timeout | Autonomous driving abort to safe stop |
| DTC_P0A0D | High Voltage System Interlock Circuit Open | HVIL continuity signal lost | 10 ms immediate | Open main contactors within 10 ms |


---

<!-- Page 75 -->
## Page 75: 16.1 Fault Containment Regions (FCR) Architecture

### 16.1 Fault Containment Regions (FCR) Architecture

The powertrain architecture implements layered Fault Containment Regions (FCRs) to isolate component failures before they propagate into hazard states.

| Degraded Mode Identifier | Activation Trigger | Torque Capability Limit | Vehicle Speed Cap | Driver Warning |
| :--- | :--- | :--- | :--- | :--- |
| LIMP_INVERTER_FAIL | Single motor inverter failure (Front or Rear) | Rear only: max 150 Nm; Front only: max 100 Nm | 80 km/h | Amber Powertrain Warning |
| LIMP_BATTERY_HOT | Battery pack temperature between 55°C and 60°C | Linear derating from 100% to 0% at 60°C | 100 km/h | Battery Temperature Warning |
| LIMP_COOLING_PUMP | Primary coolant loop pump failure detected | Maximum 40 kW continuous total power | 60 km/h | Red Thermal Service Warning |
| SAFE_STOP_TORQUE | Asymmetric torque violation > 50 Nm | Zero motor torque (Inverters disabled) | Coast to stop | Red Immediate Stop Warning |


---

<!-- Page 76 -->
## Page 76: 16.2 Limp-Home Degraded Operating Modes

### 16.2 Limp-Home Degraded Operating Modes

The powertrain architecture implements layered Fault Containment Regions (FCRs) to isolate component failures before they propagate into hazard states.

| Degraded Mode Identifier | Activation Trigger | Torque Capability Limit | Vehicle Speed Cap | Driver Warning |
| :--- | :--- | :--- | :--- | :--- |
| LIMP_INVERTER_FAIL | Single motor inverter failure (Front or Rear) | Rear only: max 150 Nm; Front only: max 100 Nm | 80 km/h | Amber Powertrain Warning |
| LIMP_BATTERY_HOT | Battery pack temperature between 55°C and 60°C | Linear derating from 100% to 0% at 60°C | 100 km/h | Battery Temperature Warning |
| LIMP_COOLING_PUMP | Primary coolant loop pump failure detected | Maximum 40 kW continuous total power | 60 km/h | Red Thermal Service Warning |
| SAFE_STOP_TORQUE | Asymmetric torque violation > 50 Nm | Zero motor torque (Inverters disabled) | Coast to stop | Red Immediate Stop Warning |


---

<!-- Page 77 -->
## Page 77: 16.3 Emergency Contactor Opening & Pyrofuse Deployment

### 16.3 Emergency Contactor Opening & Pyrofuse Deployment

The powertrain architecture implements layered Fault Containment Regions (FCRs) to isolate component failures before they propagate into hazard states.

| Degraded Mode Identifier | Activation Trigger | Torque Capability Limit | Vehicle Speed Cap | Driver Warning |
| :--- | :--- | :--- | :--- | :--- |
| LIMP_INVERTER_FAIL | Single motor inverter failure (Front or Rear) | Rear only: max 150 Nm; Front only: max 100 Nm | 80 km/h | Amber Powertrain Warning |
| LIMP_BATTERY_HOT | Battery pack temperature between 55°C and 60°C | Linear derating from 100% to 0% at 60°C | 100 km/h | Battery Temperature Warning |
| LIMP_COOLING_PUMP | Primary coolant loop pump failure detected | Maximum 40 kW continuous total power | 60 km/h | Red Thermal Service Warning |
| SAFE_STOP_TORQUE | Asymmetric torque violation > 50 Nm | Zero motor torque (Inverters disabled) | Coast to stop | Red Immediate Stop Warning |


---

<!-- Page 78 -->
## Page 78: 16.4 Thermal Derating Envelopes & Power Throttling

### 16.4 Thermal Derating Envelopes & Power Throttling

The powertrain architecture implements layered Fault Containment Regions (FCRs) to isolate component failures before they propagate into hazard states.

| Degraded Mode Identifier | Activation Trigger | Torque Capability Limit | Vehicle Speed Cap | Driver Warning |
| :--- | :--- | :--- | :--- | :--- |
| LIMP_INVERTER_FAIL | Single motor inverter failure (Front or Rear) | Rear only: max 150 Nm; Front only: max 100 Nm | 80 km/h | Amber Powertrain Warning |
| LIMP_BATTERY_HOT | Battery pack temperature between 55°C and 60°C | Linear derating from 100% to 0% at 60°C | 100 km/h | Battery Temperature Warning |
| LIMP_COOLING_PUMP | Primary coolant loop pump failure detected | Maximum 40 kW continuous total power | 60 km/h | Red Thermal Service Warning |
| SAFE_STOP_TORQUE | Asymmetric torque violation > 50 Nm | Zero motor torque (Inverters disabled) | Coast to stop | Red Immediate Stop Warning |


---

<!-- Page 79 -->
## Page 79: 17.1 Item Definition & Hazard Analysis and Risk Assessment (HARA)

### 17.1 Item Definition & Hazard Analysis and Risk Assessment (HARA)

In accordance with ISO 26262:2018, this chapter formalizes the functional safety concept and safety goals protecting vehicle occupants from powertrain hazards.

| Hazard ID | Hazardous Event Scenario | Severity (S) | Exposure (E) | Controllability (C) | Safety Goal & ASIL |
| :--- | :--- | :--- | :--- | :--- | :--- |
| HAZ-001 | Unintended forward acceleration while vehicle is stationary | S3 (Life threatening) | E4 (High exposure) | C3 (Difficult to control) | SG1: Prevent unintended torque (ASIL-D) |
| HAZ-002 | Unintended maximum regenerative braking on highway | S3 (Life threatening) | E3 (Moderate exposure) | C3 (Difficult to control) | SG2: Prevent unintended deceleration (ASIL-D) |
| HAZ-003 | High-voltage exposure during vehicle maintenance | S3 (Fatal shock) | E2 (Low exposure) | C3 (Uncontrollable) | SG3: Ensure HV isolation and interlock (ASIL-D) |
| HAZ-004 | Battery pack thermal runaway during DC fast charging | S3 (Fire / Explosion) | E3 (Moderate exposure) | C2 (Partial control) | SG4: Prevent overcharge & overheating (ASIL-C) |


---

<!-- Page 80 -->
## Page 80: 17.2 Functional Safety Concept (FSC) & Safety Goals

### 17.2 Functional Safety Concept (FSC) & Safety Goals

In accordance with ISO 26262:2018, this chapter formalizes the functional safety concept and safety goals protecting vehicle occupants from powertrain hazards.

| Hazard ID | Hazardous Event Scenario | Severity (S) | Exposure (E) | Controllability (C) | Safety Goal & ASIL |
| :--- | :--- | :--- | :--- | :--- | :--- |
| HAZ-001 | Unintended forward acceleration while vehicle is stationary | S3 (Life threatening) | E4 (High exposure) | C3 (Difficult to control) | SG1: Prevent unintended torque (ASIL-D) |
| HAZ-002 | Unintended maximum regenerative braking on highway | S3 (Life threatening) | E3 (Moderate exposure) | C3 (Difficult to control) | SG2: Prevent unintended deceleration (ASIL-D) |
| HAZ-003 | High-voltage exposure during vehicle maintenance | S3 (Fatal shock) | E2 (Low exposure) | C3 (Uncontrollable) | SG3: Ensure HV isolation and interlock (ASIL-D) |
| HAZ-004 | Battery pack thermal runaway during DC fast charging | S3 (Fire / Explosion) | E3 (Moderate exposure) | C2 (Partial control) | SG4: Prevent overcharge & overheating (ASIL-C) |


---

<!-- Page 81 -->
## Page 81: 17.3 Technical Safety Concept (TSC) & Architecture Decomposition

### 17.3 Technical Safety Concept (TSC) & Architecture Decomposition

In accordance with ISO 26262:2018, this chapter formalizes the functional safety concept and safety goals protecting vehicle occupants from powertrain hazards.

| Hazard ID | Hazardous Event Scenario | Severity (S) | Exposure (E) | Controllability (C) | Safety Goal & ASIL |
| :--- | :--- | :--- | :--- | :--- | :--- |
| HAZ-001 | Unintended forward acceleration while vehicle is stationary | S3 (Life threatening) | E4 (High exposure) | C3 (Difficult to control) | SG1: Prevent unintended torque (ASIL-D) |
| HAZ-002 | Unintended maximum regenerative braking on highway | S3 (Life threatening) | E3 (Moderate exposure) | C3 (Difficult to control) | SG2: Prevent unintended deceleration (ASIL-D) |
| HAZ-003 | High-voltage exposure during vehicle maintenance | S3 (Fatal shock) | E2 (Low exposure) | C3 (Uncontrollable) | SG3: Ensure HV isolation and interlock (ASIL-D) |
| HAZ-004 | Battery pack thermal runaway during DC fast charging | S3 (Fire / Explosion) | E3 (Moderate exposure) | C2 (Partial control) | SG4: Prevent overcharge & overheating (ASIL-C) |


---

<!-- Page 82 -->
## Page 82: 17.4 Hardware-Software Fault Metrics & Diagnostic Coverage

### 17.4 Hardware-Software Fault Metrics & Diagnostic Coverage

In accordance with ISO 26262:2018, this chapter formalizes the functional safety concept and safety goals protecting vehicle occupants from powertrain hazards.

| Hazard ID | Hazardous Event Scenario | Severity (S) | Exposure (E) | Controllability (C) | Safety Goal & ASIL |
| :--- | :--- | :--- | :--- | :--- | :--- |
| HAZ-001 | Unintended forward acceleration while vehicle is stationary | S3 (Life threatening) | E4 (High exposure) | C3 (Difficult to control) | SG1: Prevent unintended torque (ASIL-D) |
| HAZ-002 | Unintended maximum regenerative braking on highway | S3 (Life threatening) | E3 (Moderate exposure) | C3 (Difficult to control) | SG2: Prevent unintended deceleration (ASIL-D) |
| HAZ-003 | High-voltage exposure during vehicle maintenance | S3 (Fatal shock) | E2 (Low exposure) | C3 (Uncontrollable) | SG3: Ensure HV isolation and interlock (ASIL-D) |
| HAZ-004 | Battery pack thermal runaway during DC fast charging | S3 (Fire / Explosion) | E3 (Moderate exposure) | C2 (Partial control) | SG4: Prevent overcharge & overheating (ASIL-C) |


---

<!-- Page 83 -->
## Page 83: 17.5 Safety Mechanisms & E2E Protection Implementations

### 17.5 Safety Mechanisms & E2E Protection Implementations

In accordance with ISO 26262:2018, this chapter formalizes the functional safety concept and safety goals protecting vehicle occupants from powertrain hazards.

| Hazard ID | Hazardous Event Scenario | Severity (S) | Exposure (E) | Controllability (C) | Safety Goal & ASIL |
| :--- | :--- | :--- | :--- | :--- | :--- |
| HAZ-001 | Unintended forward acceleration while vehicle is stationary | S3 (Life threatening) | E4 (High exposure) | C3 (Difficult to control) | SG1: Prevent unintended torque (ASIL-D) |
| HAZ-002 | Unintended maximum regenerative braking on highway | S3 (Life threatening) | E3 (Moderate exposure) | C3 (Difficult to control) | SG2: Prevent unintended deceleration (ASIL-D) |
| HAZ-003 | High-voltage exposure during vehicle maintenance | S3 (Fatal shock) | E2 (Low exposure) | C3 (Uncontrollable) | SG3: Ensure HV isolation and interlock (ASIL-D) |
| HAZ-004 | Battery pack thermal runaway during DC fast charging | S3 (Fire / Explosion) | E3 (Moderate exposure) | C2 (Partial control) | SG4: Prevent overcharge & overheating (ASIL-C) |


---

<!-- Page 84 -->
## Page 84: 18.1 Threat Analysis and Risk Assessment (TARA)

### 18.1 Threat Analysis and Risk Assessment (TARA)

This chapter defines the cybersecurity architecture safeguarding the powertrain against unauthorized remote manipulation in compliance with ISO/SAE 21434 and UNECE R155.

| Threat ID | Threat Scenario (STRIDE) | Impact | Attack Feasibility | Cybersecurity Goal & Countermeasure |
| :--- | :--- | :--- | :--- | :--- |
| THR-001 | Spoofing of ADAS acceleration SOME/IP packet | Severe (Crash) | Low (Requires bus access) | CG1: Enforce SecOC authentication on all torque packets |
| THR-002 | Tampering with firmware update binary via OTA | Severe (ECU takeover) | Moderate (Network attack) | CG2: Enforce RSA-3072 signature check in secure boot |
| THR-003 | Elevation of privilege inside Adaptive user space | Moderate (Data access) | Low (Sandboxed POSIX) | CG3: POSIX cgroups and non-root execution sandboxes |
| THR-004 | Denial of service flooding on SOME/IP-SD port | Moderate (Comms loss) | Moderate (Ethernet flood) | CG4: Hardware ingress rate-limiting on Ethernet switch |


---

<!-- Page 85 -->
## Page 85: 18.2 Secure Onboard Communication (SecOC) Specifications

### 18.2 Secure Onboard Communication (SecOC) Specifications

This chapter defines the cybersecurity architecture safeguarding the powertrain against unauthorized remote manipulation in compliance with ISO/SAE 21434 and UNECE R155.

| Threat ID | Threat Scenario (STRIDE) | Impact | Attack Feasibility | Cybersecurity Goal & Countermeasure |
| :--- | :--- | :--- | :--- | :--- |
| THR-001 | Spoofing of ADAS acceleration SOME/IP packet | Severe (Crash) | Low (Requires bus access) | CG1: Enforce SecOC authentication on all torque packets |
| THR-002 | Tampering with firmware update binary via OTA | Severe (ECU takeover) | Moderate (Network attack) | CG2: Enforce RSA-3072 signature check in secure boot |
| THR-003 | Elevation of privilege inside Adaptive user space | Moderate (Data access) | Low (Sandboxed POSIX) | CG3: POSIX cgroups and non-root execution sandboxes |
| THR-004 | Denial of service flooding on SOME/IP-SD port | Moderate (Comms loss) | Moderate (Ethernet flood) | CG4: Hardware ingress rate-limiting on Ethernet switch |


---

<!-- Page 86 -->
## Page 86: 18.3 Transport Layer Security (TLS 1.3) & DoIP Encryption

### 18.3 Transport Layer Security (TLS 1.3) & DoIP Encryption

This chapter defines the cybersecurity architecture safeguarding the powertrain against unauthorized remote manipulation in compliance with ISO/SAE 21434 and UNECE R155.

| Threat ID | Threat Scenario (STRIDE) | Impact | Attack Feasibility | Cybersecurity Goal & Countermeasure |
| :--- | :--- | :--- | :--- | :--- |
| THR-001 | Spoofing of ADAS acceleration SOME/IP packet | Severe (Crash) | Low (Requires bus access) | CG1: Enforce SecOC authentication on all torque packets |
| THR-002 | Tampering with firmware update binary via OTA | Severe (ECU takeover) | Moderate (Network attack) | CG2: Enforce RSA-3072 signature check in secure boot |
| THR-003 | Elevation of privilege inside Adaptive user space | Moderate (Data access) | Low (Sandboxed POSIX) | CG3: POSIX cgroups and non-root execution sandboxes |
| THR-004 | Denial of service flooding on SOME/IP-SD port | Moderate (Comms loss) | Moderate (Ethernet flood) | CG4: Hardware ingress rate-limiting on Ethernet switch |


---

<!-- Page 87 -->
## Page 87: 18.4 Secure Boot, Crypto Stack & Key Storage Architecture

### 18.4 Secure Boot, Crypto Stack & Key Storage Architecture

This chapter defines the cybersecurity architecture safeguarding the powertrain against unauthorized remote manipulation in compliance with ISO/SAE 21434 and UNECE R155.

| Threat ID | Threat Scenario (STRIDE) | Impact | Attack Feasibility | Cybersecurity Goal & Countermeasure |
| :--- | :--- | :--- | :--- | :--- |
| THR-001 | Spoofing of ADAS acceleration SOME/IP packet | Severe (Crash) | Low (Requires bus access) | CG1: Enforce SecOC authentication on all torque packets |
| THR-002 | Tampering with firmware update binary via OTA | Severe (ECU takeover) | Moderate (Network attack) | CG2: Enforce RSA-3072 signature check in secure boot |
| THR-003 | Elevation of privilege inside Adaptive user space | Moderate (Data access) | Low (Sandboxed POSIX) | CG3: POSIX cgroups and non-root execution sandboxes |
| THR-004 | Denial of service flooding on SOME/IP-SD port | Moderate (Comms loss) | Moderate (Ethernet flood) | CG4: Hardware ingress rate-limiting on Ethernet switch |


---

<!-- Page 88 -->
## Page 88: 19.1 End-to-End Latency Profiles across Vehicle Networks

### 19.1 End-to-End Latency Profiles across Vehicle Networks

This chapter documents empirical performance measurements, network traffic shaping budgets, and memory allocation maps.

| Traffic Class / Network Path | VLAN Tag | Allocated Bandwidth | Max Burst Size | Max Queuing Delay Target |
| :--- | :--- | :--- | :--- | :--- |
| Class A: Real-Time Torque Control | VLAN 100 | 25.0 Mbps | 1500 Bytes | < 0.25 ms |
| Class B: Safety Interlock Telemetry | VLAN 100 | 10.0 Mbps | 1000 Bytes | < 0.50 ms |
| Class C: General Status Telemetry | VLAN 150 | 50.0 Mbps | 9000 Bytes | < 2.0 ms |
| Class D: Diagnostic DoIP Traffic | VLAN 200 | 150.0 Mbps | 65535 Bytes | < 10.0 ms |
| Class E: Best-Effort Logging & DLT | VLAN 250 | 50.0 Mbps | 32768 Bytes | < 50.0 ms |


---

<!-- Page 89 -->
## Page 89: 19.2 Ethernet Bandwidth Allocation & TSN Traffic Classes

### 19.2 Ethernet Bandwidth Allocation & TSN Traffic Classes

This chapter documents empirical performance measurements, network traffic shaping budgets, and memory allocation maps.

| Traffic Class / Network Path | VLAN Tag | Allocated Bandwidth | Max Burst Size | Max Queuing Delay Target |
| :--- | :--- | :--- | :--- | :--- |
| Class A: Real-Time Torque Control | VLAN 100 | 25.0 Mbps | 1500 Bytes | < 0.25 ms |
| Class B: Safety Interlock Telemetry | VLAN 100 | 10.0 Mbps | 1000 Bytes | < 0.50 ms |
| Class C: General Status Telemetry | VLAN 150 | 50.0 Mbps | 9000 Bytes | < 2.0 ms |
| Class D: Diagnostic DoIP Traffic | VLAN 200 | 150.0 Mbps | 65535 Bytes | < 10.0 ms |
| Class E: Best-Effort Logging & DLT | VLAN 250 | 50.0 Mbps | 32768 Bytes | < 50.0 ms |


---

<!-- Page 90 -->
## Page 90: 19.3 Memory Footprint & Non-Volatile Flash Allocation

### 19.3 Memory Footprint & Non-Volatile Flash Allocation

This chapter documents empirical performance measurements, network traffic shaping budgets, and memory allocation maps.

| Traffic Class / Network Path | VLAN Tag | Allocated Bandwidth | Max Burst Size | Max Queuing Delay Target |
| :--- | :--- | :--- | :--- | :--- |
| Class A: Real-Time Torque Control | VLAN 100 | 25.0 Mbps | 1500 Bytes | < 0.25 ms |
| Class B: Safety Interlock Telemetry | VLAN 100 | 10.0 Mbps | 1000 Bytes | < 0.50 ms |
| Class C: General Status Telemetry | VLAN 150 | 50.0 Mbps | 9000 Bytes | < 2.0 ms |
| Class D: Diagnostic DoIP Traffic | VLAN 200 | 150.0 Mbps | 65535 Bytes | < 10.0 ms |
| Class E: Best-Effort Logging & DLT | VLAN 250 | 50.0 Mbps | 32768 Bytes | < 50.0 ms |


---

<!-- Page 91 -->
## Page 91: 20.1 Cold Startup & Hardware Power-On Sequencing

### 20.1 Cold Startup & Hardware Power-On Sequencing

This chapter defines the state sequence governing hardware power-up, fast cold-boot, graceful shutdown, and atomic over-the-air firmware updates via UCM.

| Startup Phase | Governing Subsystem | Execution Actions | Max Allowable Duration | Exit Criteria |
| :--- | :--- | :--- | :--- | :--- |
| Phase 0: BootROM / Pre-boot | Hardware / HSM | Hardware self-tests, verify Stage 1 signature | 25 ms | Signature Valid |
| Phase 1: OS Kernel Boot | POSIX RTOS | Initialize MMU, drivers, load Adaptive daemons | 150 ms | POSIX PSE52 Ready |
| Phase 2: Platform Services | ara::exec | Start ara::com, ara::per, ara::diag, ara::log | 200 ms | Platform Services Up |
| Phase 3: Applications | ara::exec | Spawn PowertrainManager, TorqueArbitration, etc. | 150 ms | Ready State Reached |
| Total Startup Budget | End-to-End System | Time from clamp 15 pulse to first valid torque packet | 525 ms (Budget < 600 ms) | RUN_ACTIVE Achievable |


---

<!-- Page 92 -->
## Page 92: 20.2 Graceful Shutdown & Fast Wakeup Sleep Sequencing

### 20.2 Graceful Shutdown & Fast Wakeup Sleep Sequencing

This chapter defines the state sequence governing hardware power-up, fast cold-boot, graceful shutdown, and atomic over-the-air firmware updates via UCM.

| Startup Phase | Governing Subsystem | Execution Actions | Max Allowable Duration | Exit Criteria |
| :--- | :--- | :--- | :--- | :--- |
| Phase 0: BootROM / Pre-boot | Hardware / HSM | Hardware self-tests, verify Stage 1 signature | 25 ms | Signature Valid |
| Phase 1: OS Kernel Boot | POSIX RTOS | Initialize MMU, drivers, load Adaptive daemons | 150 ms | POSIX PSE52 Ready |
| Phase 2: Platform Services | ara::exec | Start ara::com, ara::per, ara::diag, ara::log | 200 ms | Platform Services Up |
| Phase 3: Applications | ara::exec | Spawn PowertrainManager, TorqueArbitration, etc. | 150 ms | Ready State Reached |
| Total Startup Budget | End-to-End System | Time from clamp 15 pulse to first valid torque packet | 525 ms (Budget < 600 ms) | RUN_ACTIVE Achievable |


---

<!-- Page 93 -->
## Page 93: 20.3 Update and Configuration Management (UCM) & A/B Partitions

### 20.3 Update and Configuration Management (UCM) & A/B Partitions

This chapter defines the state sequence governing hardware power-up, fast cold-boot, graceful shutdown, and atomic over-the-air firmware updates via UCM.

| Startup Phase | Governing Subsystem | Execution Actions | Max Allowable Duration | Exit Criteria |
| :--- | :--- | :--- | :--- | :--- |
| Phase 0: BootROM / Pre-boot | Hardware / HSM | Hardware self-tests, verify Stage 1 signature | 25 ms | Signature Valid |
| Phase 1: OS Kernel Boot | POSIX RTOS | Initialize MMU, drivers, load Adaptive daemons | 150 ms | POSIX PSE52 Ready |
| Phase 2: Platform Services | ara::exec | Start ara::com, ara::per, ara::diag, ara::log | 200 ms | Platform Services Up |
| Phase 3: Applications | ara::exec | Spawn PowertrainManager, TorqueArbitration, etc. | 150 ms | Ready State Reached |
| Total Startup Budget | End-to-End System | Time from clamp 15 pulse to first valid torque packet | 525 ms (Budget < 600 ms) | RUN_ACTIVE Achievable |


---

<!-- Page 94 -->
## Page 94: 21.1 Verification Methodology: MIL, SIL, and HIL Levels

### 21.1 Verification Methodology: MIL, SIL, and HIL Levels

This chapter documents the multi-tier verification and validation methodology confirming that all 40 functional requirements and safety goals are satisfied.

| Test Level | Execution Platform | Target Requirement Scope | Pass / Fail Decision Criteria | Automation Framework |
| :--- | :--- | :--- | :--- | :--- |
| MIL (Model-in-the-Loop) | Simulink / MATLAB | Control algorithms (Torque split, SOC) | Model output error < 1.0% vs reference | Simulink Test |
| SIL (Software-in-the-Loop) | Linux x86 Virtual Machine | C++17 code compilation, ara::com IPC | 100% statement and branch code coverage | Google Test / CTest |
| HIL (Hardware-in-the-Loop) | dSPACE SCALEXIO Simulator | Complete ECU with electrical load simulation | Zero safety violations in 500h soak | Python / AutomationDesk |
| Vehicle Test Track | Prototype Electric Vehicle | High-speed stability, thermal stress, DC charge | Driver subjective rating >= 8.5/10 | Vector CANoe / ETAS INCA |


---

<!-- Page 95 -->
## Page 95: 21.2 Fault Injection Testing & Safety Case Validation

### 21.2 Fault Injection Testing & Safety Case Validation

This chapter documents the multi-tier verification and validation methodology confirming that all 40 functional requirements and safety goals are satisfied.

| Test Level | Execution Platform | Target Requirement Scope | Pass / Fail Decision Criteria | Automation Framework |
| :--- | :--- | :--- | :--- | :--- |
| MIL (Model-in-the-Loop) | Simulink / MATLAB | Control algorithms (Torque split, SOC) | Model output error < 1.0% vs reference | Simulink Test |
| SIL (Software-in-the-Loop) | Linux x86 Virtual Machine | C++17 code compilation, ara::com IPC | 100% statement and branch code coverage | Google Test / CTest |
| HIL (Hardware-in-the-Loop) | dSPACE SCALEXIO Simulator | Complete ECU with electrical load simulation | Zero safety violations in 500h soak | Python / AutomationDesk |
| Vehicle Test Track | Prototype Electric Vehicle | High-speed stability, thermal stress, DC charge | Driver subjective rating >= 8.5/10 | Vector CANoe / ETAS INCA |


---

<!-- Page 96 -->
## Page 96: 21.3 System Acceptance Criteria & Homologation Gates

### 21.3 System Acceptance Criteria & Homologation Gates

This chapter documents the multi-tier verification and validation methodology confirming that all 40 functional requirements and safety goals are satisfied.

| Test Level | Execution Platform | Target Requirement Scope | Pass / Fail Decision Criteria | Automation Framework |
| :--- | :--- | :--- | :--- | :--- |
| MIL (Model-in-the-Loop) | Simulink / MATLAB | Control algorithms (Torque split, SOC) | Model output error < 1.0% vs reference | Simulink Test |
| SIL (Software-in-the-Loop) | Linux x86 Virtual Machine | C++17 code compilation, ara::com IPC | 100% statement and branch code coverage | Google Test / CTest |
| HIL (Hardware-in-the-Loop) | dSPACE SCALEXIO Simulator | Complete ECU with electrical load simulation | Zero safety violations in 500h soak | Python / AutomationDesk |
| Vehicle Test Track | Prototype Electric Vehicle | High-speed stability, thermal stress, DC charge | Driver subjective rating >= 8.5/10 | Vector CANoe / ETAS INCA |


---

<!-- Page 97 -->
## Page 97: 22.1 Architectural Decision Records & Trade-Off Analysis

### 22.1 Architecture Decision Records (ADRs)

During the design of the Electric Powertrain Domain Controller, several fundamental architectural trade-offs were evaluated. The table below formalizes key design decisions, rejected alternatives, and architectural rationales.

| ADR Identifier | Design Decision Made | Rejected Alternative | Primary Engineering Rationale |
| :--- | :--- | :--- | :--- |
| ADR-001 | Adaptive AUTOSAR on POSIX OS for powertrain coordination | Classic AUTOSAR OSEK on bare metal | Enables dynamic SOME/IP service communication and high compute bandwidth |
| ADR-002 | SOME/IP over UDP with E2E CRC-32 for torque commands | Raw Ethernet Layer-2 proprietary packets | Standardized cross-ECU interoperability and SOME/IP tooling compatibility |
| ADR-003 | Silicon Carbide (SiC) dual traction inverter topology | Silicon IGBT standard inverters | Higher switching frequencies (up to 25 kHz) yielding 6.5% higher drive efficiency |
| ADR-004 | Independent companion lockstep micro-core for ASIL-D safety | Software-only monitoring on POSIX OS | Hardware independence eliminates common-cause OS kernel crash hazards |
| ADR-005 | A/B Dual-Bank Partitioning for OTA software updates | Single-partition in-place flashing | Eliminates risk of bricked ECUs during interrupted over-the-air flash updates |


---

<!-- Page 98 -->
## Page 98: 22.2 Explicitly Documented Out-of-Scope Exclusions & Omissions

### 22.2 Deliberately Documented Omissions & Out-of-Scope Items

To establish clear functional boundaries for system verification and AI evaluation benchmarks, the following domains and capabilities are EXPLICITLY EXCLUDED and documented as OUT OF SCOPE. The software components described herein contain NO implementation, logic, or interfaces for these topics.

| Omission ID | Excluded Domain / Feature | Allocated External Subsystem | Architectural Rationale for Omission |
| :--- | :--- | :--- | :--- |
| OMS-001 | Cabin HVAC temperature setpoint and blower fan control | Body Domain Controller (BDC) | Cabin comfort is non-safety; handled separately by Body ECU |
| OMS-002 | Autonomous driving camera perception and obstacle tracking | ADAS Autonomous Driving Core | Perception requires neural NPUs outside powertrain scope |
| OMS-003 | In-Vehicle Infotainment (IVI) touch screen rendering & audio | Infotainment Head Unit (IHU) | Multimedia display pipelines run on separate consumer OS |
| OMS-004 | Electro-hydraulic brake caliper hydraulic pressure modulation | Electronic Stability Control (ESC) | Mechanical friction hydraulics managed by dedicated brake ECU |
| OMS-005 | High-voltage lithium cell internal chemical degradation modeling | Offboard Cloud Fleet Analytics | Molecular degradation modeling exceeds embedded CPU budgets |
| OMS-006 | Steering rack electric motor angle PID position control | Electric Power Steering (EPS) | Steering motor actuation managed by dedicated EPS ECU |
| OMS-007 | Airbag pyrotechnic squib crash deployment firing circuits | Restraints Control Module (RCM) | Airbag deployment requires dedicated accelerometer sensor ASIC |
| OMS-008 | Tire pressure monitoring radio receiver sensor processing | Telematics Gateway Module (TGM) | RF 433 MHz tire sensor signals processed by telematics unit |
| OMS-009 | Vehicle-to-Grid (V2G) bidirectional AC power inverter logic | High-Voltage On-Board Charger (OBC) | AC grid inversion handled by dedicated bidirectional OBC |
| OMS-010 | Legacy CAN 2.0A 11-bit standard identifier bus support | None (Deprecated in architecture) | Architecture exclusively mandates CAN-FD 2.0B and SOME/IP Ethernet |

> **Evaluation Benchmark Anchor**: Queries regarding cabin air conditioning, camera object recognition, brake caliper hydraulic fluid pressure, or tire pressure RF frequencies MUST result in an honest system abstention confirming that these features are explicitly out of scope.


---

<!-- Page 99 -->
## Page 99: 23.1 Requirements Traceability Matrix (RTM - Part 1)

### 23.1 Requirements Traceability Matrix (Requirements 001-020)

The Requirements Traceability Matrix establishes bidirectional traceability between system requirements, architecture components, design sections, and verification test cases.

| Requirement ID | Requirement Title | Implementing SWC | Design Section | Verification Test Case |
| :--- | :--- | :--- | :--- | :--- |
| REQ-PWR-001 | Driver Acceleration Pedal Interpretation | PowertrainManager_SWC | Section 7.1 / 8.1 | TC-PWR-HIL-001 |
| REQ-PWR-002 | Pedal Plausibility Discordance Cutoff | EmergencyCutoff_SWC | Section 7.6 / 8.6 | TC-SAF-HIL-002 |
| REQ-PWR-003 | Dual Axle Torque Vectoring Split | VehicleMotion_SWC | Section 7.5 / 8.5 | TC-MOT-HIL-003 |
| REQ-PWR-004 | Front Axle Induction Motor Disconnect | PowertrainManager_SWC | Section 7.1 / 8.1 | TC-PWR-HIL-004 |
| REQ-PWR-005 | Regenerative Braking Blending | TorqueArbitration_SWC | Section 7.2 / 8.2 | TC-REG-HIL-005 |
| REQ-PWR-006 | Battery Charge Power Limiting | TorqueArbitration_SWC | Section 7.2 / 8.2 | TC-BAT-HIL-006 |
| REQ-PWR-007 | Battery Over-Temperature Cutback | ThermalManagement_SWC | Section 7.4 / 8.4 | TC-THM-HIL-007 |
| REQ-PWR-008 | High-Voltage Pre-Charge Monitoring | BatteryManagement_SWC | Section 7.3 / 8.3 | TC-BAT-HIL-008 |
| REQ-PWR-009 | Contactor Weld Detection | BatteryManagement_SWC | Section 7.3 / 8.3 | TC-BAT-HIL-009 |
| REQ-PWR-010 | High-Voltage Interlock Loop (HVIL) | EmergencyCutoff_SWC | Section 7.6 / 8.6 | TC-SAF-HIL-010 |
| REQ-PWR-011 | Crash Signal Power Cutoff | EmergencyCutoff_SWC | Section 7.6 / 8.6 | TC-SAF-HIL-011 |
| REQ-PWR-012 | DC Fast Charge Pre-Conditioning | ThermalManagement_SWC | Section 7.4 / 8.4 | TC-THM-HIL-012 |
| REQ-PWR-013 | Inverter SiC Overtemperature | InverterController_SWC | Section 7.2 / 8.2 | TC-INV-HIL-013 |
| REQ-PWR-014 | Motor Stall Protection | TorqueArbitration_SWC | Section 7.2 / 8.2 | TC-PWR-HIL-014 |


---

<!-- Page 100 -->
## Page 100: 23.2 Requirements Traceability Matrix (RTM - Part 2)

### 23.2 Requirements Traceability Matrix (Requirements 021-040)

Continuation of the Requirements Traceability Matrix connecting requirements 021 through 040 to software components, implementation sections, and test suites.

| Requirement ID | Requirement Title | Implementing SWC | Design Section | Verification Test Case |
| :--- | :--- | :--- | :--- | :--- |
| REQ-PWR-021 | State of Charge Coulomb Counting | BatteryManagement_SWC | Section 7.3 / 8.3 | TC-BAT-HIL-021 |
| REQ-PWR-022 | HV Isolation Resistance Monitoring | BatteryManagement_SWC | Section 7.3 / 8.3 | TC-BAT-HIL-022 |
| REQ-PWR-023 | Coolant Flow Rate Validation | ThermalManagement_SWC | Section 7.4 / 8.4 | TC-THM-HIL-023 |
| REQ-PWR-024 | Regen Braking Cold Battery Lockout | RegenerativeBraking_SWC | Section 7.2 / 8.2 | TC-REG-HIL-024 |
| REQ-PWR-025 | Creep Torque Control | TorqueArbitration_SWC | Section 7.2 / 8.2 | TC-PWR-HIL-025 |
| REQ-PWR-026 | 12V DC-DC Converter Coordination | BatteryManagement_SWC | Section 7.3 / 8.3 | TC-BAT-HIL-026 |
| REQ-PWR-027 | Thermal Runaway Pressure Detection | EmergencyCutoff_SWC | Section 7.6 / 8.6 | TC-SAF-HIL-027 |
| REQ-PWR-028 | One-Pedal Driving Deceleration | TorqueArbitration_SWC | Section 7.2 / 8.2 | TC-PWR-HIL-028 |
| REQ-PWR-029 | Inverter Active Short Circuit (ASC) | InverterController_SWC | Section 7.2 / 8.2 | TC-INV-HIL-029 |
| REQ-PWR-030 | SOME/IP Freshness Validation | TorqueArbitration_SWC | Section 11.4 / 13.1 | TC-COM-HIL-030 |
| REQ-PWR-035 | Gear Shift Interlock Prevention | PowertrainManager_SWC | Section 7.1 / 8.1 | TC-PWR-HIL-035 |
| REQ-PWR-038 | Maximum Acceleration Jerk Limiting | TorqueArbitration_SWC | Section 7.2 / 8.2 | TC-PWR-HIL-038 |
| REQ-PWR-039 | Degraded Limp-Home Speed Governing | PowertrainManager_SWC | Section 16.2 | TC-ERR-HIL-039 |
| REQ-PWR-040 | Watchdog Challenge-Response Check | EmergencyCutoff_SWC | Section 15.5 | TC-SAF-HIL-040 |


---

<!-- Page 101 -->
## Page 101: 23.3 Complete Technical Glossary & Acronym Dictionary

### 23.3 Technical Glossary & Acronym Dictionary

This glossary defines standard terminology, acronyms, and automotive architectural abbreviations utilized throughout this specification.

| Acronym / Term | Full Engineering Expansion | Standardizing Body | Architectural Definition in ePDC |
| :--- | :--- | :--- | :--- |
| ADAS | Advanced Driver Assistance Systems | SAE J3016 | Vehicle computing domain controlling autonomous trajectory |
| ARA | AUTOSAR Runtime for Applications | AUTOSAR Adaptive | User-space runtime API abstraction for adaptive software |
| ASIL | Automotive Safety Integrity Level | ISO 26262 | Risk classification scheme (ASIL A lowest, ASIL D highest) |
| AVAS | Acoustic Vehicle Alerting System | UNECE R138 | Exterior pedestrian warning sound system at low speeds |
| BMS | Battery Management System | Automotive Standard | Hardware/software controlling high-voltage battery pack |
| DoIP | Diagnostics over Internet Protocol | ISO 13400 | Transport protocol for UDS diagnostic communication over IP |
| DTC | Diagnostic Trouble Code | ISO 14229 / SAE J2012 | Alphanumeric code identifying specific vehicle fault conditions |
| E2E | End-to-End Protection | AUTOSAR Standard | Safety mechanism protecting communication against transmission errors |
| ePDC | Electric Powertrain Domain Controller | Synthetic System | Central automotive domain ECU governing electric propulsion |
| FCR | Fault Containment Region | Fault Tolerant Systems | Structural boundary preventing fault propagation across domains |
| HIL | Hardware-in-the-Loop | Testing Standard | Real-time electrical test bench interfacing real ECU hardware |
| HVIL | High-Voltage Interlock Loop | ISO 6469 | Safety circuit detecting disconnections in high-voltage wiring |
| SOME/IP | Scalable Service-Oriented Middleware over IP | AUTOSAR Standard | Automotive client-server and publish-subscribe protocol |
| SWC | Software Component | AUTOSAR Standard | Encapsulated modular software unit providing ports and runnables |
| UCM | Update and Configuration Management | AUTOSAR Adaptive | Functional cluster managing OTA software package installations |
| UDS | Unified Diagnostic Services | ISO 14229 | Diagnostic communication protocol used by offboard scan tools |

> **End of Specification Document**: This concludes the 101-page High-Level Design (HLD) Specification for the AUTOSAR Adaptive Powertrain Domain Controller (v1.0 Comprehensive Baseline).


---
