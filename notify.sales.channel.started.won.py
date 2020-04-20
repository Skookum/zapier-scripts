#===============================
# STEP 1 - Get Hubspot Details
#===============================




#INPUT
# HubspotOwnerID
# LOBownerID
# companyId

#COMBINED ALL HUBSPOT SEARCH INTO SINGLE PYTHON ACTION

#The below script does the following from a new deal entering stage in HubSpot:
#INPUTS: Company ID, LOB Owner ID, HubSpot Owner ID

import requests

#ENVIRONMENT VALUES

base_url='https://api.hubapi.com'
hapikey=''

#CONFIGURATIONS FOR INPUTS AND PAYLOADS
input_companyId = input_data['companyId']
input_HubSpotOwnerId = int(input_data['HubspotOwnerID'])

try:
    input_LOBownerId = int(input_data['LOBownerId'])
except:
    input_LOBownerId = input_HubSpotOwnerId

payload_companyId= {'hapikey':hapikey}
payload_ownerId = {'hapikey':hapikey,'includeInactive':'false'}


def getHubSpotCompanyName(base_url, companyId, payload):
    func_url = '/companies/v2/companies/'+ companyId
    url = base_url + func_url
    r = requests.get(url, params=payload)
    r.raise_for_status()
    company_details_array=r.json()
    return company_details_array['properties']['name']['value']

def getHubSpotLOBOwnerEmail(base_url,ownerId,payload):
    func_url = '/owners/v2/owners/'
    url = base_url + func_url
    r = requests.get(url, params=payload)
    r.raise_for_status()
    owners=r.json()
    return fmtHubSpotLOBOwnerEmail(owners,ownerId)

def fmtHubSpotLOBOwnerEmail(owner_details_array,ownerId):
    for a in range(0, len(owner_details_array)):
        if owner_details_array[a]['ownerId']==ownerId:
            return owner_details_array[a]['email']


hubspot_companyName=getHubSpotCompanyName(base_url,input_companyId,payload_companyId)
hubspot_LOBownerEmail = getHubSpotLOBOwnerEmail(base_url,input_LOBownerId,payload_ownerId)
hubspot_HubSpotownerEmail = getHubSpotLOBOwnerEmail(base_url,input_HubSpotOwnerId,payload_ownerId)


output = [{'companyId': 123, 'companyName': hubspot_companyName , 'LOBownerEmail': hubspot_LOBownerEmail, 'HubSpotOwnerEmail': hubspot_HubSpotownerEmail}]

#===============================
# STEP 2 - Get Slack User IDs
#===============================

#INPUT
# HubspotOwnerID
# LOBownerID


import requests

base_url='https://slack.com'
payload1= {'token':'','email':input_data['hubspotOwner']}
payload2= {'token':'','email':input_data['lobOwner']}


func_url = '/api/users.lookupByEmail'
url = base_url + func_url
h = requests.post(url, params=payload1)
h.raise_for_status()
hubspot=h.json()

l = requests.post(url, params=payload2)
l.raise_for_status()
lob=l.json()


hubspotOwner= hubspot['user']['id']
lobOwner= lob['user']['id']


output = [{'hubspotOwner': hubspotOwner, 'lobOwner': lobOwner }]