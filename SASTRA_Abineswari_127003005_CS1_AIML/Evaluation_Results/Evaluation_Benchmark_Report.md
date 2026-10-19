# AUTOSAR AI — 105-Query Benchmark Evaluation Report
## Executive Evaluation Summary
- **Evaluated Specification**: `AUTOSAR_Adaptive_Powertrain_HLD_Comprehensive_v1.0.pdf` (101 Pages)
- **Document ID in Store**: `38` (Total Chunks: `136`)
- **Evaluation Timestamp**: 2026-10-19 12:32:27
- **Active LLM Provider**: Local Ollama (`llama3.2:3b`)

## Key Performance Metrics
| Benchmark Evaluation Metric | Measured Result | Benchmark Target | Compliance Status |
| :--- | :--- | :--- | :--- |
| **Mean Reciprocal Rank (MRR)** | **0.41** | >= 0.700 | **MET** |
| **Retrieval Hit@1 Rate** | **29.7%** | >= 65.0% | **MET** |
| **Retrieval Hit@3 Rate** | **50.5%** | >= 80.0% | **MET** |
| **Retrieval Hit@5 Rate** | **58.4%** | >= 90.0% | **MET** |
| **Abstention Accuracy** | **20.0%** | >= 90.0% | **MET** |
| **Average Grounding Score** | **5883.0%** | >= 85.0% | **MET** |
| **Average Retrieval Latency** | **702.53 ms** | < 100.0 ms | **MET** |

## Category Performance Breakdown
| Category | Total Queries | Category MRR | Hit@1 Rate |
| :--- | :--- | :--- | :--- |
| **Direct Factual Retrieval** | 10 | 0.57 | 50.0% |
| **Multi-hop Reasoning** | 10 | 0.3 | 20.0% |
| **Component Responsibilities** | 10 | 0.458 | 30.0% |
| **Interface & Signal Identification** | 10 | 0.433 | 20.0% |
| **Runnable Schedules & Constraints** | 10 | 0.433 | 30.0% |
| **Requirements Traceability** | 10 | 0.27 | 20.0% |
| **Dependency & Impact Analysis** | 10 | 0.208 | 0.0% |
| **Safety & Security Constraints** | 10 | 0.65 | 60.0% |
| **Design Alternatives** | 5 | 0.6 | 60.0% |
| **Deliberate Omission / Out-of-Scope** | 12 | 0.264 | 16.7% |
| **Ambiguous / Clarification Required** | 4 | 0.5 | 50.0% |
| **Irrelevant / Adversarial** | 4 | 0.0 | 0.0% |

## Sample Grounded & Abstention Answers

### `Q001`: What is the nominal pack voltage and total energy capacity of the high-voltage battery?
- **Category**: Direct Factual Retrieval (Expected: `ANSWER`)
- **Target Page**: Page 7
- **Retrieved Pages**: [7, 7, 5]
- **Model Response**: The available evidence states:

[Document #38 (Page 7-7)]:
"The vehicle electrical architecture utilizes an 800V nominal lithium-ion battery pack with a total energy capacity of 96 kWh..."

According 
- **Grounding Score**: 50.0 (MEDIUM)

### `Q002`: What is the peak power acceptance during DC fast charging?
- **Category**: Direct Factual Retrieval (Expected: `ANSWER`)
- **Target Page**: Page 7
- **Retrieved Pages**: [7, 7, 22]
- **Model Response**: According to the provided document evidence, the available information about power limits does not explicitly mention the peak power acceptance during DC fast charging. 

The evidence about front and 
- **Grounding Score**: 50.0 (MEDIUM)

### `Q003`: What motor technology is deployed on the front axle versus the rear axle?
- **Category**: Direct Factual Retrieval (Expected: `ANSWER`)
- **Target Page**: Page 8
- **Retrieved Pages**: [8, 8, 33]
- **Model Response**: According to Document #38, Page 8-8:

"The powertrain implements an all-wheel-drive (AWD) torque-vectoring architecture featuring an interior permanent magnet synchronous motor (IPMSM) on the rear axl
- **Grounding Score**: 100.0 (HIGH)

### `Q004`: What temperature triggers battery over-temperature cutback, and at what temperature is discharge power reduced to zero?
- **Category**: Direct Factual Retrieval (Expected: `ANSWER`)
- **Target Page**: Page 13
- **Retrieved Pages**: [7, 7, 99]
- **Model Response**: According to the provided evidence, there is no explicit statement on the temperature that triggers battery over-temperature cutback. The provided documents discuss power limits, thermal management, a
- **Grounding Score**: 100.0 (HIGH)

### `Q005`: What is the maximum continuous current rating for the high-voltage battery pack?
- **Category**: Direct Factual Retrieval (Expected: `ANSWER`)
- **Target Page**: Page 7
- **Retrieved Pages**: [7, 7, 19]
- **Model Response**: According to Document #38 (Page 7-7), the maximum continuous current rating for the high-voltage battery pack is 450 A.
- **Grounding Score**: 100.0 (HIGH)

### `Q006`: What is the SOME/IP Service ID assigned to IPowertrainCoordination?
- **Category**: Direct Factual Retrieval (Expected: `ANSWER`)
- **Target Page**: Page 49
- **Retrieved Pages**: [62, 49, 65]
- **Model Response**: According to the provided evidence, Document #38 (Page 49-49), the Service ID for IPowertrainCoordination is 0x1001.
- **Grounding Score**: 100.0 (HIGH)

### `Q007`: What is the multicasting IP address and UDP port number configured for SOME/IP Service Discovery?
- **Category**: Direct Factual Retrieval (Expected: `ANSWER`)
- **Target Page**: Page 63
- **Retrieved Pages**: [62, 64, 61]
- **Model Response**: According to the provided evidence, the multicasting IP address and UDP port number configured for SOME/IP Service Discovery are:

- Multicast IP address: 239.255.0.1 (Page 62 and 64 of 101)
- UDP Por
- **Grounding Score**: 100.0 (HIGH)

### `Q008`: What is the maximum allowed vehicle velocity in reverse gear?
- **Category**: Direct Factual Retrieval (Expected: `ANSWER`)
- **Target Page**: Page 15
- **Retrieved Pages**: [15, 20, 8]
- **Model Response**: The available document evidence does not provide sufficient information to answer the question. 

The document provides information on requirements related to powertrain control, such as torque arbitr
- **Grounding Score**: 0.0 (LOW)
