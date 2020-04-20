#INPUT
# real_name (google_calendar_subject). Example: "Will DeLozier (2 yrs)""


import requests

base_url='https://slack.com'
payload1= {'token':''}
func_url = '/api/users.list'
input_name = input_data['real_name']
real_name = input_name.split(" (")

anniversary_year = real_name[1][:-1].replace("yrs", "year")
real_name = real_name[0]



url = base_url + func_url
h = requests.post(url, params=payload1)
h.raise_for_status()
user=h.json()
output = ""

for a in user['members']:
    slackID= a['id']
    slack_real= a['profile']['real_name']

    if slack_real == real_name:
        output = [{'slackID': "<@"+slackID+">", 'anniversary_year': anniversary_year }]
        break
    else:
        output = [{'slackID': real_name, 'anniversary_year': anniversary_year }]


print(output)