### THIS SCRIPT IS USED TO GET REQUEST HISTORY EVENTS OF LAST 30 DAYS FROM ANY vRA TENANT

### SCRIPT IS WRITTEN IN PYTHON WHICH CALLS vRA CATALOG-SERVICE API TO
### PROVIDE TASK/EVENT DETAILS LIKE RECONFIGURE , POWER ON/OFF , LEASE EXPIRE , REQUESTED BY ETC.

### PLEASE CONTACT SAURABH SHAH IF ANY CHANGES / ENHANCMENT REQUIRED

import requests
import json
import getpass
import webbrowser
from datetime import date
from datetime import datetime  
from datetime import timedelta
import pandas as pd

fqdn = input("Please enter vRA Server FQDN Here: ")
tenant = input("Enter Your tenant Here: ")
username = input("Enter Your username@domain name Here: ")
password= getpass.getpass("Enter Your Password Here: ")

url1 = "https://{}/identity/api/tokens".format(fqdn)
payload = '{' + '\r\n  "username": "{}",\r\n  "password": "{}",\r\n  "tenant": "{}"\r\n'.format(username,password,tenant) + '}'

headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
	  }

response1 = requests.request("POST", url1, data=payload, headers=headers)
key1 = json.loads(response1.text)

deltadays = "'" + str(date.today() - timedelta(days=30)) + "'"
url2 = "https://{}/catalog-service/api/consumer/requests?limit=100&$orderby=dateSubmitted%20desc&$filter=dateCreated%20ge%20".format(fqdn)+deltadays
payload = ""

headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    'Authorization': "Bearer " + key1['id']
         }         

response2 = requests.request("GET", url2, data=payload, headers=headers)
key2 = json.loads(response2.text)
finallist = key2['content']
keylength = len(finallist)

row1 = ['requestNumber','state','requestedItemName','description','reasons','requestedFor','requestedBy','dateCreated']
row2 = ['requestCompletionState','completionDetails']
finaldata = {'requestNumber':[],'state':[],'requestedItemName':[],'description':[],'reasons':[],'requestedFor':[],'requestedBy':[],'dateCreated':[],'requestCompletionState':[],'completionDetails':[] }

print ("***Getting Request history logs of last 30 days from vRA***")  

for number in range(keylength):
    
    for each1 in row1 :
        finaldata[each1].append(finallist[number][each1])
    
    keylist = finallist[number]['requestCompletion']
    
    if keylist == None:
        for each2 in row2 : 
            finaldata[each2].append('null')
    else:
        for each2 in row2 : 
            finaldata[each2].append(keylist[each2])
                         
df = pd.DataFrame(finaldata, index = list(range(keylength)))
website = 'vRA-result.html'

print ("***Opening vRA-Result.html***") 
df.to_html(website)
webbrowser.open(website, new=2)