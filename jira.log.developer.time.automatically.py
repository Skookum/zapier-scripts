# INPUTS:
# Issue Key


import requests
import json

#CONFIGURATIONS FOR INPUTS AND PAYLOADS
input_issueKey = input_data['issueKey']
base_url = "https://skookum3.atlassian.net"

headers = {
   "Accept": "application/json",
   "Content-Type": "application/json"
}

auth=('google_account', 'password')

def getOriginalEstimate(base_url, issueID, headers, auth):
    func_url = "/rest/api/3/issue/"+issueID
    url = base_url + func_url
    r = requests.get(url, headers=headers, auth=auth)
    r.raise_for_status()
    issue_details_array=r.json()
    return issue_details_array['fields']

def getIssueIDValue(array, property_name):
    return array[property_name]

def logTimeTracking(base_url, issueID, headers, auth, payload):
    func_url = "/rest/api/3/issue/"+issueID+"/worklog"
    url = base_url + func_url
    r = requests.post(url, headers=headers, auth=auth, data=payload)
    r.raise_for_status()

original_estimate = getIssueIDValue(getOriginalEstimate(base_url,input_issueKey,headers,auth),'timeoriginalestimate')
change_date = getIssueIDValue(getOriginalEstimate(base_url,input_issueKey,headers,auth),'updated')

payload = json.dumps( {
  "timeSpentSeconds": original_estimate,
  "comment": {
    "type": "doc",
    "version": 1,
    "content": [
      {
        "type": "paragraph",
        "content": [
          {
            "text": "development",
            "type": "text"
          }
        ]
      }
    ]
  },
  "started": change_date
} )

logTimeTracking(base_url,input_issueKey,headers,auth,payload)
