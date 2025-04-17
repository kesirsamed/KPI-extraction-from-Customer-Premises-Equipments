import re
def FNC_ParseKPIsMeiGSRT853LfromHTML(readLine):
    KEYWORD_A = "rfparam_tr"
    KEYWORD_B = "content_option"
    KEYWORD_C = "</div>"
    KEYWORD_1 = "CA Info:"
    KEYWORD_2 = "RSRP:"
    KEYWORD_3 = "RSSI:"
    KEYWORD_4 = "RSRQ:"
    KEYWORD_5 = "SINR:"
    KEYWORD_6 = "Band:"
    KEYWORD_7 = "PCI:"
    #-----------------------------------
    KPIData = [[] for _ in range(4)]
    CarrierAggreInfo = []
    RSRP = []
    RSSI = []
    RSRQ = []
    SINR = []
    Band = []
    PCI = []
    if readLine != "":
        if not readLine.find(KEYWORD_A) == -1:
            ### CA Info.
            indexS = readLine.find(KEYWORD_1)
            if not indexS == -1:
                indexKPIS = readLine.find(KEYWORD_B) + len(KEYWORD_B) + 2
                indexKPIE = indexKPIS + readLine[indexKPIS:].find(KEYWORD_C)
                CarrierAggreInfo = readLine[indexKPIS:indexKPIE]
                readLine = readLine[indexKPIE+1:]

            ### RSRP
            indexS = readLine.find(KEYWORD_2)
            if not indexS == -1:
                indexKPIS = readLine.find(KEYWORD_B) + len(KEYWORD_B) + 2
                indexKPIE = indexKPIS + readLine[indexKPIS:].find(KEYWORD_C)
                RSRP = readLine[indexKPIS:indexKPIE]
                readLine = readLine[indexKPIE + 1:]

            ### RSSI
            indexS = readLine.find(KEYWORD_3)
            if not indexS == -1:
                indexKPIS = readLine.find(KEYWORD_B) + len(KEYWORD_B) + 2
                indexKPIE = indexKPIS + readLine[indexKPIS:].find(KEYWORD_C)
                RSSI = readLine[indexKPIS:indexKPIE]
                readLine = readLine[indexKPIE + 1:]

            ### RSRQ
            indexS = readLine.find(KEYWORD_4)
            if not indexS == -1:
                indexKPIS = readLine.find(KEYWORD_B) + len(KEYWORD_B) + 2
                indexKPIE = indexKPIS + readLine[indexKPIS:].find(KEYWORD_C)
                RSRQ = readLine[indexKPIS:indexKPIE]
                readLine = readLine[indexKPIE + 1:]

            ### SINR
            indexS = readLine.find(KEYWORD_5)
            if not indexS == -1:
                indexKPIS = readLine.find(KEYWORD_B) + len(KEYWORD_B) + 2
                indexKPIE = indexKPIS + readLine[indexKPIS:].find(KEYWORD_C)
                SINR = readLine[indexKPIS:indexKPIE]
                readLine = readLine[indexKPIE + 1:]
                indexdB = SINR.find("dB")
                SINRValue = (float(SINR[0:indexdB]))/10
                SINR = str(SINRValue) + "dB"

            ### Band
            indexS = readLine.find(KEYWORD_6)
            if not indexS == -1:
                indexKPIS = readLine.find(KEYWORD_B) + len(KEYWORD_B) + 2
                indexKPIE = indexKPIS + readLine[indexKPIS:].find(KEYWORD_C)
                Band = readLine[indexKPIS:indexKPIE]
                readLine = readLine[indexKPIE + 1:]

            ### PCI
            indexS = readLine.find(KEYWORD_7)
            if not indexS == -1:
                indexKPIS = readLine.find(KEYWORD_B) + len(KEYWORD_B) + 2
                indexKPIE = indexKPIS + readLine[indexKPIS:].find(KEYWORD_C)
                PCI = readLine[indexKPIS:indexKPIE]
                readLine = readLine[indexKPIE + 1:]

            else:
                pass

    KPIData[0] = RSSI
    KPIData[1] = RSRP
    KPIData[2] = RSRQ
    KPIData[3] = SINR
    return KPIData

def FNC_ParseKPIsGMOD513fromHTML(readLine):
    KEYWORD_1 = "CA Info"
    KEYWORD_2 = "RSRP"
    KEYWORD_3 = "RSSI"
    KEYWORD_4 = "RSRQ"
    KEYWORD_5 = "SINR"
    KEYWORD_6 = "Band/Bandwidth"
    KEYWORD_7 = "PCI"

    KPIData = [[] for _ in range(4)]
    number_of_feature = 12
    temp = readLine.replace('\n', ' ').replace('/ ', '/').split(" ")

    for idx in range(len(temp)):
        if temp[idx] == "PCell":
            pcell_flag = idx
            break
        else:
            pcell_flag = 99

    if pcell_flag != 99:
        Pcell_info = temp[pcell_flag:pcell_flag + number_of_feature]

    # check feature index is lower than 5 or not because of the band/bandwidth info is separated

    ### CA Info.
    if KEYWORD_1 in temp:
        idx = temp.index(KEYWORD_1)
        if idx < 5:
            CarrierAggreInfo = Pcell_info[idx]
        else:
            CarrierAggreInfo = Pcell_info[idx + 1]
    else:
        CarrierAggreInfo = []

    ### RSRP
    if KEYWORD_2 in temp:
        idx = temp.index(KEYWORD_2)
        if idx < 5:
            RSRP = Pcell_info[idx]
        else:
            RSRP = Pcell_info[idx + 1]
    else:
        RSRP = []

    ### RSSI
    if KEYWORD_3 in temp:
        idx = temp.index(KEYWORD_3)
        if idx < 5:
            RSSI = Pcell_info[idx]
        else:
            RSSI = Pcell_info[idx + 1]
    else:
        RSSI = []

    ### RSRQ
    if KEYWORD_4 in temp:
        idx = temp.index(KEYWORD_4)
        if idx < 5:
            RSRQ = Pcell_info[idx]
        else:
            RSRQ = Pcell_info[idx + 1]
    else:
        RSRQ = []

    ### SINR
    if KEYWORD_5 in temp:
        idx = temp.index(KEYWORD_5)
        if idx < 5:
            SINR = Pcell_info[idx]
        else:
            SINR = Pcell_info[idx + 1]
    else:
        SINR = []

    ### Band/Bandwidth
    if KEYWORD_6 in temp:
        idx = temp.index(KEYWORD_6)
        Band = Pcell_info[idx] + " " + Pcell_info[idx + 1]
    else:
        Band = []

    ### SINR
    if KEYWORD_7 in temp:
        idx = temp.index(KEYWORD_7)
        if idx < 5:
            PCI = Pcell_info[idx]
        else:
            PCI = Pcell_info[idx + 1]
    else:
        PCI = []

    KPIData[0] = RSSI
    KPIData[1] = RSRP
    KPIData[2] = RSRQ
    KPIData[3] = SINR
    return KPIData

def FNC_ParseKPIsMeiGSRT853LfromAT(readLine):
    KEYWORD_A = "\r\n"
    #KEYWORD_1 = "CURR_MODE:"
    #KEYWORD_2 = "DUPLEX MODE:"
    #KEYWORD_3 = "MCC:"
    #KEYWORD_4 = "MNC:"
    #KEYWORD_5 = "NR CELL ID:"
    #KEYWORD_6 = "PHYSICAL_CELL_ID:"
    #KEYWORD_7 = "TAC_ID:"
    #KEYWORD_8 = "BAND:"
    #KEYWORD_9 = "BANDWIDTH:"
    #KEYWORD_10 = "SUB_CARRIER_SPACING:"
    #KEYWORD_11 = "FR_TYPE:"
    #KEYWORD_12 = "DL CHANNEL:"
    #KEYWORD_13 = "UL CHANNEL:"
    KEYWORD_14 = "RSSI:"
    KEYWORD_15 = "RSRP:"
    KEYWORD_16 = "RSRQ:"
    KEYWORD_17 = "SINR:"
    #KEYWORD_18 = "VONR:"

    #-----------------------------------
    KPIData = [[] for _ in range(4)]
    RSSI = []
    RSRP = []
    RSRQ = []
    SINR = []
    if readLine != "":
        if not readLine.find(KEYWORD_A) == -1:
            indexS = readLine.find(KEYWORD_14)
            if not indexS == -1:
                indexKPIS = readLine[indexS:].find(":") + 1
                indexKPIE = readLine[indexS:].find(KEYWORD_A) - 1
                RSSI = readLine[indexS+indexKPIS:indexS+indexKPIE+1]
            else:
                pass

            indexS = readLine.find(KEYWORD_15)
            if not indexS == -1:
                indexKPIS = readLine[indexS:].find(":") + 1
                indexKPIE = readLine[indexS:].find(KEYWORD_A) - 1
                RSRP = readLine[indexS + indexKPIS:indexS + indexKPIE + 1]
            else:
                pass

            indexS = readLine.find(KEYWORD_16)
            if not indexS == -1:
                indexKPIS = readLine[indexS:].find(":") + 1
                indexKPIE = readLine[indexS:].find(KEYWORD_A) - 1
                RSRQ = readLine[indexS + indexKPIS:indexS + indexKPIE + 1]
            else:
                pass

            indexS = readLine.find(KEYWORD_17)
            if not indexS == -1:
                indexKPIS = readLine[indexS:].find(":") + 1
                indexKPIE = readLine[indexS:].find(KEYWORD_A) - 1
                SINR = readLine[indexS + indexKPIS:indexS + indexKPIE + 1]
            else:
                pass

    KPIData[0] = RSSI
    KPIData[1] = RSRP
    KPIData[2] = RSRQ
    KPIData[3] = str(float(SINR)/10)
    return KPIData


def FNC_ParseKPIsGMOD513fromAT(readLine):
    """
        Parses the KPI information from the response text.
        """
    # Define regex patterns
    patterns = {
        "RSRP": r'nr_rsrp:\s*([-\+]?[\d\.]+)dBm',
        "RSRQ": r'nr_rsrq:\s*([-\+]?[\d\.]+)dB',
        "SNR": r'nr_snr:\s*([-\+]?[\d\.]+)dB',
        "RSSI": r'rx_diversity:\s*\d+\s*\(([-\d\.]+)dBm,([-+\d\.]+)dBm'
    }

    # Search for matches
    matches = {key: re.search(pattern, readLine) for key, pattern in patterns.items()}

    KPIData = [[] for _ in range(4)]

    if matches["RSSI"] is None:
        print("RSSI NA")
    else:
        KPIData[0] = (f"{matches['RSSI'].group(1)}dBm")

    if matches["RSRP"] is None:
        print("RSRP NA")
    else:
        KPIData[1] = (f"{matches['RSRP'].group(1)}dBm")

    if matches["RSRQ"] is None:
        print("RSRQ NA")
    else:
        KPIData[2] = (f"{matches['RSRQ'].group(1)}dB")

    if matches["SNR"] is None:
        print("SNR NA")
    else:
        KPIData[3] = (f"{matches['SNR'].group(1)}dB")

    # kpis_for_optimization = float(matches["RSSI"].group(1)) if matches["RSSI"] else "N/A"

    return KPIData

def FNC_Accuver_Parser(kpi_list):
    KPIData = [[] for _ in range(4)]

    KPIData[1] = f"{kpi_list['SS-RSRP']}dBm"
    KPIData[2] = f"{kpi_list['RSRQ']}dB"

    # KPIData[3] = 999
    # KPIData[0] = 999
    return KPIData
