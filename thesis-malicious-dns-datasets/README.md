# Thesis - Malicious DNS datasets
Simulated DNS storage channels. All files are in the `dns.log` format of [Zeek v3.1.2](https://docs.zeek.org/en/v3.1.2/). Uncompressed total file size ~7.4GB.


## Test Subjects
**Connection Tunneling**\
*iodine* and *dns2tcp* used to perform various operations, e.g. file transfers of different sizes using *nc* and *scp*, speed tests, SSH session and simulated internet browsing. The following (combinations of) tunneling parameters were used:

|              | iodine        | dns2tcp       |
|--------------|---------------|---------------|
**Query type** |      `MX`, `NULL`, `PRIVATE`, `SRV`, `TXT` | `KEY`, `TXT` | 
**Max. query length** | 100\|150, 255 | - |
**Upstream encoding** | Base\{32, 64, 64u, 128\} | - |
**Compression** |  - | No (0), Yes (1) |


**PoS-Malware**\
*BernhardPOS*, *FrameworkPOS*, *MULTIGRAIN* and *UDPoS* credit card exfiltration simulations. Exfiltration intervals either 1 sec, 1 min or 5 min. Additional plain text exfiltration using the same exfil schedule, not based on existing malware. Code used for simulation is published [here](https://github.com/tudelft-cda-lab/dns-storage-channel-detection/tree/main/thesis-dns-malware).


## Overview

|       | Num. datasets | Num. queries (total) | Num. queries (avg) |  Duration (mean ± std.) |  Max. burst / sec.  |
|--------------|---------------|----------------------|--------------------|-------------------------|---------------------|
| **dns2tcp**      | 4             | 1,711,049              | 427,762             | 19m ± 0m                | 6814                |
| **iodine**       | 40            | 10,765,229             | 269,131             | 22m ± 3m                | 2403                |
|              |               |                      |                    |                         |                     |
| **BernhardPOS**  | 3             | 43,807                | 14,602              | 11h 57m ± 2m            | 2                   |
| **FrameworkPOS** | 3             | 43,784                | 14,595              | 12h 24m ± 2m            | 2                   |
| **MULTIGRAIN**   | 3             | 43,736                | 14,579              | 12h 24m ± 1m            | 2                   |
| **UDPoS**        | 3             | 44,153                | 14,718              | 12h 23m ± 2m            | 2                   |

The configuration is included in the file name of the respective dataset. For example, `proc_iod_TXT_32_150.log` corresponds to `iodine`, query type `TXT`, `Base32` encoding and a maximum query length of `150`.


## Reference
For more information about this dataset, see Chap.4 (pp. 27-33) and Appendix A (pp. 91-92) of the [thesis](http://resolver.tudelft.nl/uuid:df016cc5-bd42-4c01-b16d-6d4889246861).
