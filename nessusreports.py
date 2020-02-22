"""
API Nessus Reports
Author: Stanley Soman - IBM Cloud
Acknowledgement: SoftLayer Technologies, Inc. https://stackoverflow.com/questions/41720472/conversion-of-html-string-to-html-page-of-report-nessus-security-scanner/57918842
"""
import webbrowser
import SoftLayer
import time
import six
import io
from pprint import pprint as pp

#Let's start by setting the right environment
# Sets to simplify if/else in determining correct answers.
yesChoice = ['yes', 'y']
noChoice = ['no', 'n']

# Prompt the user with a message and get their input.
# Convert their input to lowercase.
fedqtn = six.moves.input("Is this for a Federal server report? (if so you need to be on DAL08 or WDC03 VPN) (y/N) ").lower()

# Check if our answer is in one of two sets.
if fedqtn in yesChoice:
    # call method
    ENDPOINT="https://api.service.usgov.softlayer.com/rest/v3.1/"
elif fedqtn in noChoice:
    ENDPOINT="https://api.softlayer.com/rest/v3.1/"
else:
    print("Please respond with 'y' or 'N'")
#Ask the user for SL Username, API key and the ScanID
USERNAME=six.moves.input("API Username: Not IBMid, from https://cloud.ibm.com/iam/apikeys :" )
APIKEY=six.moves.input("API Key: from https://cloud.ibm.com/iam/apikeys :" )

#For batch scan report exports, REPLACE the USERNAME & APIKEY lines found above
#with the lines below this requires only the SCANID to be inputted so no time is wasted
#USERNAME = 'Enter API Username here from https://cloud.ibm.com/iam/apikeys'
#APIKEY = 'Enter API Key here from https://cloud.ibm.com/iam/apikeys'

#Create client
client = SoftLayer.create_client_from_env(
    username=USERNAME,
    api_key=APIKEY,
    endpoint_url=ENDPOINT
)

#Find all Scans and grab a report
print("\n Here are all Nessus Scans for your account")
#listofscanids = client['Account'].getSecurityScanRequests(mask="mask[createDate, ipAddress, id, status[name]]")
#pp(listofscanids)

## Retrieve all requests and their status
object_mask = 'mask[createDate, ipAddress, id, status[name]]'

# Retrieve a list of requests and pull their object/status individually
requests = client['Account'].getSecurityScanRequests(mask='mask[id]')
for request in requests:
    request_object = client['SoftLayer_Network_Security_Scanner_Request'].getObject(id=request['id'], mask=object_mask)
    pp(request_object)


SCANID=input("\nPlease enter a Scan ID from above to retrieve its report: ")

#Create Service
scanner = client['Network_Security_Scanner_Request']

#Grab timestamp useful to prevent latter scans from overwriting earlier reports
time = time.strftime("%I%M%p")

# Export file name
file = 'NessusReport%sfrom%s.html' %(SCANID,time)
#Grab the report make sure it is encoded properly when written
f = io.open(file, 'w',encoding='utf8')

#Using try to check for errors
try:
    report = scanner.getReport(id=SCANID)
    f.write(report)
    f.close()
    webbrowser.open_new_tab(file)
    print("\nThe report was retrieved.\n")
except SoftLayer.SoftLayerAPIError as e:
    print("\nUnable to get report. faultCode=%s, faultString=%s\n" % (e.faultCode, e.faultString))
