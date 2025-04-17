from FunctionLibrary.FNC_LogInNetworkDevices import *
import FunctionLibrary.FNC_OpeningChromeViaSelenium as FNC_OpeningChromeViaSelenium
import subprocess
import time
import FunctionLibrary.ReadData_Hex as rex

def FNC_RequestInnerHTMLContentFromSRT853L(driver, URLAddress, executablePathForSeleniumWebdriver, time_delay):

    try:
        innerHTMLContent = driver.find_element(By.ID, 'rfparam').get_property("innerHTML")
    except:
        print("Connection lost (probably due to modem time-out). Trying to re-connect.")
        ### First check whether the driver exists ###
        try:
            driver = FNC_LogIn5GODUSRT853L(driver, URLAddress)
        except:
            ### The Chrome page cannot be accessed, hence a new one should be generated
            ### Clearing the existing but corrupted web driver ###
            driver.quit()
            driver = FNC_OpeningChromeViaSelenium.FNC_OpeningChromeViaSelenium(executablePathForSeleniumWebdriver)
            driver = FNC_LogIn5GODUSRT853L(driver, URLAddress)

        innerHTMLContent = driver.find_element(By.ID, 'rfparam').get_property("innerHTML")

    time.sleep(time_delay)
    return innerHTMLContent, driver

def FNC_RequestInnerHTMLContentFromGMOD513(driver, URLAddress, executablePathForSeleniumWebdriver, time_delay):

    try:
        innerHTMLContent = driver.find_element(By.XPATH, "//*[@id='staticTable']").text
    except:

        print("Connection lost (probably due to modem time-out). Trying to re-connect.")
        ### First check whether the driver exists ###
        try:
            driver = FNC_LogIn5GODUGMOD513(driver, URLAddress)
        except:
            ### The Chrome page cannot be accessed, hence a new one should be generated
            ### Clearing the existing but corrupted web driver ###
            driver.quit()
            driver = FNC_OpeningChromeViaSelenium.FNC_OpeningChromeViaSelenium(executablePathForSeleniumWebdriver)
            driver = FNC_LogIn5GODUGMOD513(driver, URLAddress)

        innerHTMLContent = driver.find_element(By.XPATH, "//*[@id='staticTable']").text

    time.sleep(time_delay)
    return innerHTMLContent, driver


def FNC_RequestCellInfoFromSRT853L(serialConnection, COMPortID, time_delay):
    ### This method uses AT commands
    try:
        KPIContent = FNC_SendATCommand(serialConnection, "AT+SGCELLINFOEX?", delay=time_delay)
    except:
        print("Connection lost (probably due to modem time-out). Trying to re-connect.")
        try:
            serialConnection = FNC_SerialConnect5GODUSRT853L(COMPortID)
            KPIContent = FNC_SendATCommand(serialConnection, "AT+SGCELLINFOEX?", delay=time_delay)
        except:
            response = FNC_SendATCommand(serialConnection, "AT", delay=time_delay)
            numberOfTrials = 0
            maxNumberOfTrials = 30
            while ((response != "OK") and (numberOfTrials < maxNumberOfTrials)):
                numberOfTrials = numberOfTrials + 1
                response = FNC_SendATCommand(serialConnection, "AT", delay=time_delay)

            if (response != "OK"):
                return []
            else:
                KPIContent = FNC_SendATCommand(serialConnection, "AT+SGCELLINFOEX?", delay=1)


    return KPIContent


def FNC_RequestCellInfoFromGMOD513(delay):

    adb_path = r"C:\ADBSHELL\adb.exe"

    try:
        # Run the ADB command using subprocess and capture the output
        result = subprocess.run(
            [adb_path, "shell", "fx-at-cm at^debug?"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,  # Use universal_newlines instead of text
            check=True  # Raise an exception if the command fails
        )
        time.sleep(delay)
        # Return the standard output from the command
        return result.stdout
    except subprocess.CalledProcessError as e:
        # If there is an error executing the command, capture it
        print(f"Error executing ADB command: {e}")
        return e.stderr
    except FileNotFoundError:
        print("ADB executable not found. Make sure ADB is installed and the path is correct.")
        return ""




def FNC_SendATCommand(serialConnection, command, delay=1):
    serialConnection.write((command + '\r').encode())  # Send command
    time.sleep(delay)  # Wait for response
    response = serialConnection.read_all().decode(errors='ignore')  # Read response
    return response

def FNC_RequestCellInfowithAccuver(sock,delay):
    msg = bytearray(b'\x16\x00\x00\x00\xa3\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    sock.sendall(msg)
    time.sleep(delay)
    response = sock.recv(1024)
    kpi_list = rex.main(response)
    return kpi_list