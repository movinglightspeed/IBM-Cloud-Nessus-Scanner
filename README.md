# IBM Cloud Nessus Scanner

This is Nessus Scanner Python Project I created for IBM Cloud. It is featured on IBM.com as a feature for the IBM.com portal and not only scans any IP on the IBM Cloud Infrastructure but retrieves Nessus reports for each scan in a downloaded HTML file.

Read the technical article here on IBM.com
https://www.ibm.com/cloud/blog/an-easier-way-to-use-the-nessus-scanner

Full text below
========================================================================================================================
How to use our API to initiate scans on Windows and Linux.

IBM Cloud customers want options, and especially for those who use our tools, they want to get work done faster and without any limitations. Recently, I worked with a customer who told me that they were having errors running Nessus Vulnerability Scans through our portal.

The customer shared with me this error: "Error: An IP address is required to start a security scan request."

They had tried to initiate a Nessus vulnerability scan from the portal on their server, but they couldn’t get the scanner to initiate. My team—ACS-Security—assists customers with Nessus vulnerability scanning through the IBM Cloud portal so I started investigating this.

It turns out the reason for this error was because the customer was using a private-only server, and our portal runs and scans on the public network. If a server doesn't have a public network, they'll be presented with this error.

Now, on other occasions, I have seen customers who are in the midst of security pen tests, compliance requests, or a change management with large fleets of servers, and they need Nessus scans done quickly. Sometimes they want it done on private/secondary IPs (like our earlier example).

The easiest workaround and alternative way to initiate these scans is to use our API. When we mention API for our Nessus scans, it is not the same as the ibmcloud api that is well known, but rather a lesser-known one—the softlayer api.
Background before we start

Before we start, be sure to read our background guide on our Nessus Vulnerability Scanner. After reading the background information, make sure the vulnerability scanner IPs are first whitelisted in your firewalls:

173.192.255.232 Public IP

172.17.19.38 Private IP

Scans in Federal data centers:

100.100.1.41 Public IP

100.64.23.41 Private IP

Please visit this link to download the necessary Nessus python API files.
Start by installing Python, PIP, and Softlayer
Python

You will first need Python installed on your workstation. If you don't have it already, install it from Python.org, and during installation, make sure the Add Python to PATH option is checked. This will allow Python to be used through the Windows Powershell CLI. In the latter half of the section, we’ll cover this for Linux machines as well.
PIP

Next, you will need PIP. Unlike Python, this you may need to install. PIP is a tool that is used to the necessary Python packages, and in our case, we will need PIP to install the Softlayer Python package.

Download this file, double click to launch the Python file, and it will auto-install PIP.

Then, open up Windows Powershell. You can check the PIP is installed by typing "pip -V" in Powershell to confirm. It should look something like the following:
PS C:\Users\Home\Downloads> pip -V
pip 19.2.3 from c:\users\home\anaconda3\lib\site-packages\pip (python 3.6)
Softlayer

Next, you want to install the Softlayer Python package

To install via PIP, run the following command via Windows Powershell:
PS C:\Users\Home\Downloads> pip install softlayer
Collecting softlayer
  Downloading https://files.pythonhosted.org/packages/54/d4/f8c70fd500f68e2cdcc6d9afb271528633398b10cdf36d94d57d4fc3ebcc/SoftLayer-5.8.0-py2.py3-none-any.whl (514kB)
Successfully installed click-7.0 prompt-toolkit-2.0.9 ptable-0.9.2 requests-2.22.0 softlayer-5.8.0 urllib3-1.25.3

Once that is complete, use Powershell to navigate to the location of the downloaded Nessus py files.
Before we start using the API

The great thing about using the API is that just you need two pieces of information: the API username and API password.

You can easily find them by going to the following link: https://cloud.ibm.com/iam/apikeys > (three dots to the right) > Details.

In the classic portal (https://control.softlayer.com/account/user/profile), you can find them under API Access Information.

It’s that simple. That is all we need.

Once you have that information, you have to decide which server you want to run a Nessus scan on. You can find the IP for the desired server to run a Nessus scan by using our API and simply typing slcli setup.

Fill in your API Username, API key, and the default API endpoint. For Timeout, enter a reasonable value—40.0 should be long enough for any failure. Then type slcli virtual list or slcli hardware list to get a full listing of virtual and hardware servers, respectively. You can note any IP from that list and use it in the following section.
Part 1: How to initiate Nessus scans on Windows

The Python script utilizes the Softlayer_Network_Security_Scanner_Request service on the backend to scan any IP you have on your account. You can learn more about the service on the Softlayer references and API blog.

In my opinion, the Python script we cover below is much simpler and up-to-date than the referenced REST examples in the links above.

Type in python nessus.py in Powershell—this will prompt you with several options, mainly API Username, API Key, and your server IP.
Preview of the Nessus scan initiation script

When you run the Python file, here is what you will be presented with:
PS C:\Users\Home\SLNessusScanner> python nessus.py
Is this a Federal server? (if so you need to be on DAL08 or WDC03 VPN) (y/N)
 
API Username: Not IBMid, from https://cloud.ibm.com/iam/apikeys :IBM1234567
 
API Key: from https://cloud.ibm.com/iam/apikeys :6vd9325720f2v9b28ed58aa17ffbbg1c315v4bs8dff2cg4ge28g4c2gdf1cbbcb15
 
Enter IP: (can be public or private) :10.123.456.78

This is the status of your scan initiation:
[{'createDate': '2019-09-02T11:33:03-05:00',
  'id': 1652240,
  'ipAddress': '10.123.456.78',
  'status': {'name': 'Scan Pending'}}]

If it shows 'Scan Pending' above, the scan has been initiated.
Part 2: How to initiate Nessus scans on Linux

For our Linux example, I’ll cover what ACS-Security team customers use on an everyday basis: AT&T Vyatta. The latest version (as of this post)—1801zb—is built on Debian 9.9, and the example below will work on the Linux servers. This is a neat way to use the Vyatta as a central hub to initiate Nessus scans on your network.

First, we will have to get the Softlayer API package installed on the Vyatta. Python is preinstalled on most operating systems—we just need the Python package installer and Softlayer package. If Python is not installed on your Linux machine for whatever reason, make sure that it is installed before you proceed.

    We start by first switching over to root user to install PIP and the Softlayer package. On Linux systems, this should be run as a privileged user, like root.
    su –
    To install PIP, securely download:
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    Then, run the following to have Python install the Python manager:
    python get-pip.py
    Next, install the Softlayer package:
    pip install softlayer
    Copy over the nessus.py via sftp to your server.
    Next, before you run the scan file, make sure you are the root user. Then type python python nessus.py. It would have the same prompts as we had earlier on the Windows side.
    If for whatever reason, you need to uninstall the packages you've installed in the future, you can simply run the following commands:
    pip uninstall softlayer
    python -m pip uninstall pip setuptools

Part 3: Grab Nessus scan reports via API

Next, we will cover how you can get Nessus reports using the API. This is, by far, one of the most exciting developments I am proud to share. It will give you timestamped files and an easy way to grab reports for all your recent scans, all by just using just the API username and API password.

Run the following to start the prompts to get Nessus reports:
python nessusreports.py
Preview of the Nessus scan report retrieval script
Here is what it looks like when you run nessusreports file via shell:
PS C:\Users\Home\SLNessusScanner> python nessusreports.py
Is this a Federal server? (if so you need to be on DAL08 or WDC03 VPN) (y/N)
 
API Username: Not IBMid, from https://cloud.ibm.com/iam/apikeys :IBM1234567
 
API Key: from https://cloud.ibm.com/iam/apikeys :6vd9325720f2v9b28ed58aa17ffbbg1c315v4bs8dff2cg4ge28g4c2gdf1cbbcb15
 
Enter IP: (can be public or private) :10.123.456.78
 
 
 
Here are all Nessus Scans for your account
…
 
Please enter a Scan ID from above to retrieve its report:1234567
 
 
The report was retrieved.

A scan report is then opened in your default browser. If you have Linux, I recommend a nifty browser like eLinks to view the downloaded .html files properly. A screenshot of what that looks like is shown below:
Nessus Scan Report

What is great about this export is that this is the original report and all original HTML from Nessus is preserved. This allows you to collapse and expand sections as necessary for presentation. You can use your browser to save as a PDF from there. In addition, the files are named in a unique way that makes them easy to identify and organize.  
The benefits of Nessus API

Both files will have similar prompts to input necessary information to get what you need to get done.

If you are doing multiple scans and reports, I recommend editing the Python files (.py) files to make some small adjustments to reduce the amount of time involved. To do that, it is very simple to open the files and use the commented lines—there are instructions inside the file. This will make it so that instead of being prompted for the API username and API key every time you run the py files, it is already set in the files for you, allowing you to run scans more quickly, especially when you are running the vulnerability scans on a fleet of servers.

Speaking of Python, any errors you might encounter running these files will likely be because of issues related to your Python installation, whether its missing or corrupted libraries or just a very old version. Reinstalling Python- and PIP-related packages and upgrading installed packages should solve most problems. The Python scripts were written with cross-compatibility in mind for Python 2.x and 3.x versions, which should make it possible for them to be run on a variety of different environments that may contain the older Python versions, like our AT&T Vyatta 5600 product environment.
Learn more about Nessus on IBM Cloud

I hope this article was helpful in learning to use our Nessus API. If you’d like to learn more, visit the IBM Cloud documentation. You can also consult the Softlayer documentation or get in contact with us by opening a ticket from the portal.

I hope that this article makes it easier for our customers who are not familiar with our APIs to get a hold of and utilize the simple commands to initiate and provide a new way to quickly get the Nessus scan reports. 
