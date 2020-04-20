import requests

base_url='https://api.hubapi.com'
payload= {'hapikey':'','includeInactive':'false'}

def prompt_owner_id():
    print ('')
    print ("enter company id")
    print ('')
    #env = input("company id: ")
    env=''
    return env

def get_owner_details(base_url, payload):
    func_url = '/owners/v2/owners/'
    url = base_url + func_url
    r = requests.get(url, params=payload)
    r.raise_for_status()
    owner_details_array=r.json()
    return owner_details_array

    

def fmt_owner_details(owner_details_array,input_owner_id):
    for a in range(0, len(owner_details_array)):
        if owner_details_array[a]['ownerId']==input_owner_id:
            print(owner_details_array[a]['email'])


fmt_owner_details(get_owner_details(base_url,payload),env)


