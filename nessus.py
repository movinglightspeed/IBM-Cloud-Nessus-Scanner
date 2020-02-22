"""
API Nessus Scanner
Author: Stanley Soman - IBM Cloud
Acknowledgement: SoftLayer Technologies, Inc. https://stackoverflow.com/questions/42143386/softlayer-vulnerability-scan-python
"""
import SoftLayer
import six
from pprint import pprint as pp

#Let's start by setting the right environment
# Sets to simplify if/else in determining correct answers.
yesChoice = ['yes', 'y']
noChoice = ['no', 'n']

# Prompt the user with a message and get their input.
# Convert their input to lowercase.
fedqtn = six.moves.input("Is this a Federal server? (if so you need to be on DAL08 or WDC03 VPN) (y/N) ").lower()

# Check if our answer is in one of two sets.
if fedqtn in yesChoice:
    # call method
    ENDPOINT="https://api.service.usgov.softlayer.com/rest/v3.1/"
elif fedqtn in noChoice:
    ENDPOINT="https://api.softlayer.com/rest/v3.1/"
else:
    print("Please respond with 'y' or 'N'")
USERNAME=six.moves.input("API Username: Not IBMid, from https://cloud.ibm.com/iam/apikeys :" )
APIKEY=six.moves.input("API Key: from https://cloud.ibm.com/iam/apikeys :" )
inputIP=six.moves.input("Enter IP: (can be public or private) :")

#For batch scan initiations, REPLACE the USERNAME & APIKEY lines found above
#with the lines below so only the IP Address has to be inputted so there is less time wasted
#Remove comments at the beginning of each of the two lines below.
#USERNAME = 'Replace this text with API Username here from https://cloud.ibm.com/iam/apikeys'
#APIKEY = 'Replace this text with API KEY from https://cloud.ibm.com/iam/apikeys'

#Create client
client = SoftLayer.create_client_from_env(
    username=USERNAME,
    api_key=APIKEY,
    endpoint_url=ENDPOINT
)

#Get account
account = client['Account'].getObject()


#IfElse Statement to cover both VSI & Baremetal HWOs based on IP
server = client['Virtual_Guest'].findByIpAddress(inputIP)
if (server):
    ipAddress = server.get("primaryIpAddress")
    if not ipAddress:
        ipAddress = server.get("primaryBackendIpAddress")
    initiatescanrequest = {
            "accountId": account["id"],
            "guestId": server["id"],
            "ipAddress": ipAddress
    }
else:
    server = client['Hardware_Server'].findByIpAddress(inputIP)
    if (server):
        ipAddress = server.get("primaryIpAddress")
        if not ipAddress:
            ipAddress = server.get("primaryBackendIpAddress")
        initiatescanrequest = {
            "accountId": account["id"],
            "hardwareId": server["id"],
            "ipAddress": ipAddress
    }
    else:
        print ("No server was found with that IP.")
        exit

#Send over details to Nessus
scanner = client['Network_Security_Scanner_Request']
scanner.createObject(initiatescanrequest)

#Huzzah
print("\nThis is the status of your scan initiation\n")
scanstatus = client['Account'].getSecurityScanRequests(filter={'securityScanRequests':{'statusId':{'operation':"101"}}},mask='mask[createDate, ipAddress, id, status[name]]')
pp(scanstatus)
print ("\nIf it shows 'Scan Pending' above, the scan has been initiated.")
