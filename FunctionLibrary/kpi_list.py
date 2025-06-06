lte_parameters = ["In-Band[ant0, ant1, ant2, ant3]",
"Total-band[ant0, ant1, ant2, ant3]", 
"Tx Power(PUSCH)",
"Tx Power(PUCCH)",
"Tx Power(SRS)",
"Tx Power(AGC)",
"DL Pathloss(PUCCH)" ,
"DL Pathloss(PUSCH)", 
"Power Headroom",
"TPC Command(PUCCH)",
"TPC Command(PUSCH)",
"Serving PCI",
"Serving EARFCN",
"Serving RSRP",
"Serving RSRP[ant0, ant1, ant2, ant3]",
"Serving RSRQ",
"Serving RSRQ[ant0, ant1, ant2, ant3]",
"Serving SINR",
"Serinvg SINR[ant0, ant1, ant2, ant3]",
"Serving RSSI",
"Serving RSSI[ant0, ant1, ant2, ant3]",
"Best Neigh. PCI",
"Best Neigh. RSRP",
"Best Neigh. RSRQ",
"WB CQI[CW0, CW1]",
"Rank Index",
"WB PMI",
"DL MCS (Mode)[CW0, CW1]",
"DL MCS (Avg)[CW0, CW1]",
"DL MCS (Count)[CW0, CW1]",
"DL QPSK Rate",
"DL 16QAM Rate",
"DL 64QAM Rate",
"DL 256QAM Rate",
"DL RB Num",
"DL RB Num Inc.0",
"UL MCS(Mode)",
"UL MCS(Avg)",
"UL MCS(Count)",
"UL QPSK Rate",
"UL 16QAM Rate",
"UL 64QAM Rate",
"UL RB Num",
"UL RB Num Inc",
"PDSCH BLER",
"PUSCH BLER",
"DL PDSCH TP(Total)",
"DL MAC TP(Total)",
"DL RLC TP",
"DL PDCP TP",
"DP APP TP",
"UL PUSCH TP",
"UL MAC TP",
"UL RLC TP",
"UL PDCP TP",
"UL APP TP",
"Serving PCI / Serving Cell ID",
"NR-ARFCN",
"Frequency",
"SCS(Subcarrier Spacing)",
"SSB Idx/ID",
"SS-RSRP",
"RSRQ",
"RSSI [ant0, ant1, ant2, ant3],",
"SS-SINR [ant0, ant1, ant2, ant3],", 
"SS-SINR(Max)",
"CSI-SINR [ant0, ant1],",
"CSI-SINR(Max)",
"CSI-RSRP(Max)",
"RI",
"CQI",
"PRACH Power [ant0, ant1],",
"PUSCH Power [ant0, ant1],",
"PUCCH Power [ant0, ant1]",
"SRS Power [ant0, ant1],",
"Max PUSCH Power",
"Max PUCCH Power",
"DL MCS 0",
"DL MCS 1",
"DL MCS (Mode)", 
"DL MCS (Avg)",
"DL Mod QPSK Rate",
"DL Mod 16QAM Rate",
"DL Mod 64QAM Rate",
"DL Mod 256QAM Rate",
"DL RB Num (Avg) ",
"DL RB Num (Inc0)",
"DL RB Num (Mode) ",
"UL MCS",
"UL MCS (Mode)",
"UL MCS (Avg) ",
"UL MCS1 (Mode) ",
"UL MCS1 (Avg) ",
"UL Mod Pi/2 BPSK Rate", 
"UL Mod BPSK Rate",
"UL Mod QPSK Rate",
"UL Mod 16QAM Rate",
"UL Mod 64QAM Rate",
"UL Mod 256QAM Rate",
"UL Mod1 Pi/2 BPSK Rate",
"UL Mod1 BPSK Rate",
"UL Mod1 QPSK Rate",
"UL Mod1 16QAM Rate",
"UL Mod1 64QAM Rate",
"UL Mod1 256QAM Rate",
"UL RB Num(Avg)",
"UL RB Num(inc0) ",
"UL RB Num(Mode)",
"DL BLER(%)",
"DL Init BLER", 
"PDSCH Throughput",
"MAC DL Throughput ",
"MAC UL Throughput ",
"RLC DL Throughput ",
"RLC UL Throughput",
"PDCP DL Throughput",
"PDCP UL Throughput",
"RRCCurState"]

import numpy as np

value_id_list = {}
ts1 = np.arange(0, 56, 1).tolist()
ts2 = np.arange(97, 158, 1).tolist()
ts3 = 160

ts4 = [*ts1, *ts2, ts3]

def set_kpi_params():
    for idx, val in enumerate(ts4):
        a = str("{:02X}".format(val))
        value_id_list[a] = lte_parameters[idx]

    return value_id_list