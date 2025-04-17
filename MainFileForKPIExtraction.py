from FunctionLibrary.FNC_RequestInnerHTMLContent import *
from FunctionLibrary.FNC_ParserFunctions import *
#import FunctionLibrary.FNC_ParseKPIsFromText as FNC_ParseKPIsFromText


############################################
### Saving the Modem KPIs in a TXT File ####

foldername = "./DataFolder/temporary_file_name.txt/"
############################################

methodID = 2
### 1: Access via HTML
### 2: Access via AT Commands
### 3: Access via Accuver XCAL

deviceID = 2
### 1: 5G ODU: MeiG SRT853L
### 2: 5G ODU: General Mobile OD513

############################################
### Get Access to the device #####

global_time_delay = 0.25
scene = "Metaclinic_"

if (methodID == 1):
    ############################################
    ### Opening a Chrome Webpage via Selenium ##
    executablePathForSeleniumWebdriver = "./DataFolder/SeleniumChromeDriver/v130/chromedriver.exe"
    webDriver = FNC_OpeningChromeViaSelenium.FNC_OpeningChromeViaSelenium(executablePathForSeleniumWebdriver)
    ############################################
    methodName = "HTML"
    if (deviceID == 1):
        deviceName = "MeiGSRT853L"
        URLAddress = "http://192.168.1.1/"
        webDriver = FNC_LogIn5GODUSRT853L(webDriver, URLAddress)
    elif (deviceID == 2):
        deviceName = "GMOD513"
        URLAddress = "https://192.168.128.1/"
        webDriver = FNC_LogIn5GODUGMOD513(webDriver, URLAddress)
    else:
        print("Undefined Device ID. Please Check")
elif (methodID == 2):
    methodName = "AT"
    if (deviceID == 1):
        deviceName = "MeiGSRT853L"
        COMPortID = "COM85"
        serialConnection = FNC_SerialConnect5GODUSRT853L(COMPortID)
    elif (deviceID == 2):
        deviceName = "GMOD513"

elif (methodID == 3):
    methodName = "Accuver"
    if (deviceID == 1):
        deviceName = "MeiGSRT853L"
        serialConnection = FNC_SerialConnectAccuver()

    elif (deviceID == 2):
        deviceName = "GMOD513"
        serialConnection = FNC_SerialConnectAccuver()
else:
    print("Undefined Method ID. Please Check")


############################################

### Up to this point, the InnerHTML page is accessed,
### and the code is READY for successive data reading and KPI parsing.

NUMBER_OF_RUNS = 600//global_time_delay
#NUMBER_OF_RUNS = 25//global_time_delay
numberOfCompletedRuns = 1
RSRPArray = []
RSSIArray = []
RSRQArray = []
SINRArray = []
TIMESTAMPS = []
while (numberOfCompletedRuns <= NUMBER_OF_RUNS):
    t0 = time.time()
    print("********** RUNNING: " + str(numberOfCompletedRuns) + "/" + str(NUMBER_OF_RUNS) + " **********")

    KPIFilename = "5GODU_InstantKPIs_" + deviceName + "_" + str(numberOfCompletedRuns) + "temp.txt"
    fileAddress = foldername + KPIFilename

    if (methodID == 1):
        ### (4) - Lastly Accessing the inner content of the table "RF Parameters"
        if (deviceID == 1):
            coarseKPIContent, webDriver = FNC_RequestInnerHTMLContentFromSRT853L(webDriver, URLAddress, executablePathForSeleniumWebdriver, global_time_delay)
            KPIs = FNC_ParseKPIsMeiGSRT853LfromHTML(coarseKPIContent)
        elif (deviceID == 2):
            coarseKPIContent, webDriver = FNC_RequestInnerHTMLContentFromGMOD513(webDriver, URLAddress, executablePathForSeleniumWebdriver, global_time_delay)
            KPIs = FNC_ParseKPIsGMOD513fromHTML(coarseKPIContent)
    elif (methodID == 2):
        if (deviceID == 1):
            coarseKPIContent = FNC_RequestCellInfoFromSRT853L(serialConnection, COMPortID, global_time_delay)
            KPIs = FNC_ParseKPIsMeiGSRT853LfromAT(coarseKPIContent)
        elif (deviceID == 2):

            coarseKPIContent = FNC_RequestCellInfoFromGMOD513(delay=global_time_delay)
            KPIs = FNC_ParseKPIsGMOD513fromAT(coarseKPIContent)


    elif (methodID == 3):
        if (deviceID == 1):
            coarseKPIContent = FNC_RequestCellInfowithAccuver(serialConnection, delay=global_time_delay)
            KPIs = FNC_Accuver_Parser(coarseKPIContent)
        elif (deviceID == 2):
            coarseKPIContent = FNC_RequestCellInfowithAccuver(serialConnection, delay=global_time_delay)
            KPIs = FNC_Accuver_Parser(coarseKPIContent)
    else:
        print("Undefined Connection Method ID. Please Check.")


    ### (6) - Writing the extracted KPIs to TXT file
    #textFile = open(fileAddress, 'w')

    RSSI = KPIs[0]
    RSRP = KPIs[1]
    RSRQ = KPIs[2]
    SINR = KPIs[3]
    overallTime = time.time() - t0
    print(KPIFilename + " | End-to-End Computation Time : " + str(overallTime))


    datafound = 0

    if (len(RSSI) == 0):
        RSSIStr = "RSSI [dBm]: NaN"
        newRSSI = 999
        RSSIStr = "RSSI [dBm]: " + str(newRSSI)
        print(RSSIStr)
        RSSIArray.append(newRSSI)
    else:
        datafound = 1
        indexdBm = RSSI.find("dBm")
        if (indexdBm == -1):
            newRSSI = float(RSSI)
        else:
            newRSSI = float(RSSI[0:indexdBm])

        RSSIStr = "RSSI [dBm]: " + str(newRSSI)
        print(RSSIStr)
        RSSIArray.append(newRSSI)

    if (len(RSRP) == 0):
        RSRPStr = "RSRP [dBm]: NaN"
        newRSRP = 999
        RSRPStr = "RSRP [dBm]: " + str(newRSRP)
        print(RSRPStr)
        RSRPArray.append(newRSRP)
    else:
        datafound = 1
        indexdBm = RSRP.find("dBm")
        if (indexdBm == -1):
            newRSRP = float(RSRP)
        else:
            newRSRP = float(RSRP[0:indexdBm])

        RSRPStr = "RSRP [dBm]: " + str(newRSRP)
        print(RSRPStr)
        RSRPArray.append(newRSRP)

    if (len(RSRQ) == 0):
        RSRQStr = "RSRQ [dB]: NaN"
        newRSRQ = 999
        RSRQStr = "RSRQ [dB]: " + str(newRSRQ)
        print(RSRQStr)
        RSRQArray.append(newRSRQ)
    else:
        datafound = 1
        indexdB = RSRQ.find("dB")
        if (indexdB == -1):
            newRSRQ = float(RSRQ)
        else:
            newRSRQ = float(RSRQ[0:indexdB])

        RSRQStr = "RSRQ [dB]: " + str(newRSRQ)
        print(RSRQStr)
        RSRQArray.append(newRSRQ)

    if (len(SINR) == 0):
        SINRStr = "SINR [dB]: NaN"
        newSINR = 999
        SINRStr = "SINR [dB]: " + str(newSINR)
        print(SINRStr)
        SINRArray.append(newSINR)
    else:
        datafound = 1
        indexdB = SINR.find("dB")
        if (indexdB == -1):
            newSINR = float(SINR)
        else:
            newSINR = float(SINR[0:indexdB])

        SINRStr = "SINR [dB]: " + str(newSINR)
        print(SINRStr)
        SINRArray.append(newSINR)

    TIMESTAMPS.append(time.time()) #datetime.datetime.now()\

    #textFile.close()
    numberOfCompletedRuns = numberOfCompletedRuns + 1

if (methodID == 1):
    webDriver.quit()
elif (methodID == 2):
    # Close the serial connection when done
    # serialConnection.close()
    print("Connection closed.")
else:
    print("Undefined Method ID. Please Check")

### Saving the collected KPIs ###
KPIFilename = "5GODU_" + scene + deviceName + methodName + "_InstantKPIs_RSRP.txt"
fileAddress = foldername + KPIFilename
textFile = open(fileAddress, 'w')
for lineID in range(len(RSRPArray)):
    textFile.write(str(TIMESTAMPS[lineID]) + "," + str(RSRPArray[lineID]) + "\n")

textFile.close()

KPIFilename = "5GODU_" + scene + deviceName + methodName + "_InstantKPIs_RSSI.txt"
fileAddress = foldername + KPIFilename
textFile = open(fileAddress, 'w')
for lineID in range(len(RSSIArray)):
    textFile.write(str(TIMESTAMPS[lineID]) + "," + str(RSSIArray[lineID]) + "\n")

textFile.close()

KPIFilename = "5GODU_" + scene +deviceName + methodName +  "_InstantKPIs_RSRQ.txt"
fileAddress = foldername + KPIFilename
textFile = open(fileAddress, 'w')
for lineID in range(len(RSRQArray)):
    textFile.write(str(TIMESTAMPS[lineID]) + "," + str(RSRQArray[lineID]) + "\n")

textFile.close()

KPIFilename = "5GODU_" + scene +deviceName + methodName + "_InstantKPIs_SINR.txt"
fileAddress = foldername + KPIFilename
textFile = open(fileAddress, 'w')
for lineID in range(len(SINRArray)):
    textFile.write(str(TIMESTAMPS[lineID]) + "," + str(SINRArray[lineID])+ "\n")

textFile.close()

print("********** RUN COMPLETED **********")
