import requests
import datetime
import json

base_url='https://api.hubapi.com'
payload= {'hapikey':''}

def get_recent_tasks(base_url, payload,time_start):
    func_url = '/engagements/v1/engagements/recent/modified'
    payload= {'hapikey':'','since': time_start, 'count':'100'}
    url = base_url + func_url
    r = requests.get(url, params=payload)
    r.raise_for_status()
    recent_task_array=r.json()
    #print(recent_task_array)
    return recent_task_array

def get_company_name(base_url, company_id, payload):
    func_url = '/companies/v2/companies/'+str(company_id)
    url = base_url + func_url
    r = requests.get(url, params=payload)
    r.raise_for_status()
    company_details_array=r.json()
    #print(company_details.json())
    return company_details_array['properties']['name']['value']

def update_subject_with_company_name(base_url, payload,engagment_id, engagement_subject,company_name):
    func_url = '/engagements/v1/engagements/'+str(engagment_id)
    payload= {'hapikey':''}
    new_subject = company_name + " - " + engagement_subject
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    url = base_url + func_url
    r = requests.patch(url, params=payload, json={"metadata" : { "subject": new_subject}}, headers=headers)
    return r

def get_company_id_from_associated_deal(base_url, payload,deal_id):
    func_url = '/deals/v1/deal/'+str(deal_id)
    url = base_url + func_url
    r = requests.get(url, params=payload)
    r.raise_for_status()
    deal_array=r.json()
    if deal_array['associations']['associatedCompanyIds'][0]: 
        company_id = deal_array['associations']['associatedCompanyIds'][0]
    else:
        company_id = "DEAL_NOT_ASSOCIATED_COMPANY"
    return company_id


def associate_task_to_company(base_url, payload,engagement_id,company_id):
    func_url = '/engagements/v1/engagements/'+str(engagement_id)+'/associations/company/'+str(company_id)
    url = base_url + func_url
    r = requests.put(url, params=payload)
    r.raise_for_status()
    return r


def get_timestamp_minus_1_hr():
    current_time = datetime.datetime.now()  # use datetime.datetime.utcnow() for UTC time
    one_hr_ago = current_time - datetime.timedelta(hours=2)
    one_hr_ago_epoch_ts = int(one_hr_ago.timestamp() * 1000)
    return one_hr_ago_epoch_ts


def update_based_on_time(recent_task_array):
    for a in range(0, len(recent_task_array['results'])):
        try:
            status = recent_task_array['results'][a]['metadata']['status']
        except:
            status = "NULL"

        if recent_task_array['results'][a]['engagement']['type']=="TASK" and status!="COMPLETED" and not recent_task_array['results'][a]['associations']['companyIds'] and recent_task_array['results'][a]['associations']['dealIds']:
            company_id = get_company_id_from_associated_deal(base_url,payload,recent_task_array['results'][a]['associations']['dealIds'][0])
            if company_id != "DEAL_NOT_ASSOCIATED_COMPANY":
                response = associate_task_to_company(base_url, payload,recent_task_array['results'][a]['engagement']['id'],company_id)
                name_response = update_subject_with_company_name(base_url, payload,recent_task_array['results'][a]['engagement']['id'],recent_task_array['results'][a]['metadata']['subject'],get_company_name(base_url, company_id, payload))

                print(recent_task_array['results'][a]['engagement']['id'], ' :: ',recent_task_array['results'][a]['metadata']['subject'],' :: ',response,' :: ', name_response)



def update_based_on_deal_id(recent_task_array, deal_id):
    for a in range(0, len(recent_task_array['results'])):
        try:
            status = recent_task_array['results'][a]['metadata']['status']
        except:
            status = "NULL"

        if recent_task_array['results'][a]['engagement']['type']=="TASK" and status!="COMPLETED" and not recent_task_array['results'][a]['associations']['companyIds'] and recent_task_array['results'][a]['associations']['dealIds']:
            if deal_id == str(recent_task_array['results'][a]['associations']['dealIds'][0]):
                company_id = get_company_id_from_associated_deal(base_url,payload,recent_task_array['results'][a]['associations']['dealIds'][0])
                if company_id != "DEAL_NOT_ASSOCIATED_COMPANY":
                    response = associate_task_to_company(base_url, payload,recent_task_array['results'][a]['engagement']['id'],company_id)
                    name_response = update_subject_with_company_name(base_url, payload,recent_task_array['results'][a]['engagement']['id'],recent_task_array['results'][a]['metadata']['subject'],get_company_name(base_url, company_id, payload))

                    print(recent_task_array['results'][a]['engagement']['id'], ' :: ',recent_task_array['results'][a]['metadata']['subject'],' :: ',response,' :: ', name_response)

update_based_on_deal_id(get_recent_tasks(base_url,payload,get_timestamp_minus_1_hr()),deal_id)


