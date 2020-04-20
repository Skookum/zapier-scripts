import requests

base_url='https://api.hubapi.com'
payload= {'hapikey':''}

def prompt_company_id():
    print ('')
    print ("enter company id")
    print ('')
    env = input("company id: ")
    return env

def get_company_details(base_url, company_id, payload):
    func_url = '/companies/v2/companies/'+company_id
    url = base_url + func_url
    r = requests.get(url, params=payload)
    r.raise_for_status()
    company_details_array=r.json()
    #print(company_details.json())
    return company_details_array

def fmt_company_details(company_details_array):
    #for a in range(0, len(company_details_array['properties'])):
    #    portalId = company_details_array['channel'][a]['portalId']
    #    print (portalId)
    print(company_details_array['properties']['name']['value'])


fmt_company_details(get_company_details(base_url,prompt_company_id(),payload))


