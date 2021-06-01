from selenium import webdriver
import json
path_to_chromedriver=''#insert the path to chrome driver
browser=webdriver.Chrome(executable_path=path_to_chromedriver)

browser.get('https://cdn-api.co-vin.in/api/v2/admin/location/states')
e=browser.find_element_by_tag_name('pre')
dic=json.loads(e.text)

states={}
with open('districts.json','w') as f2:
    for state in dic["states"]:
        browser.get('https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}'.format(state['state_id']))
        e=browser.find_element_by_tag_name('pre')
        dis=json.loads(e.text)
        districts={}
        for district in dis['districts']:
            districts[district['district_name'].lower()]=district['district_id']

        states[state['state_name'].lower()]=districts
    f2.write(json.dumps(states))



browser.close()
#with open('states.json','w') as file:
