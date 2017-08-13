 # -*- coding: utf-8 -*-
import requests
import json
import csv


activists = {}
result = {'unknown':{}}


def load_activists():
    with open('activists.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            result[row[1]] = {}
            activists[row[0]] = {}
            act = activists[row[0]]
            act['region'] = row[1]
            act['name'] = row[2]
            act['surname'] = row[3]
            act['fathername'] = row[4]


def get_auth_hash():
    f = open('auth.txt', 'r')
    return f.readline()[:-1]


def generate_result(response):
    js_response = json.loads(response)
    items = js_response["response"]["items"]
    for item in items:
        if item["type"] != 'profile':
            continue
        act_id = str(item['id'])
        if act_id in activists:
            act = activists[act_id]
            result[act['region']][act_id] = { 'name' : act['name'], 'surname': act['surname'], 'fathername': act['fathername']}
        else:
            result['unknown'][act_id] = { 'name' : '', 'surname': '', 'fathername': ''}
            if item.get('first_name'):
                result['unknown'][act_id]['name'] = item['first_name']
            if item.get('last_name'):
                result['unknown'][act_id]['surname'] = item['last_name']
            
    

def print_result():
    for region in result:
        print region
        for act_id in result[region]:
            act = result[region][act_id]
            print  act_id, act['name'], act['surname'], act['fathername']
        print ''

load_activists()
auth_token = get_auth_hash()
group_id = raw_input('input group_id:')
item_id = raw_input('input item_id:')
url = "https://api.vk.com/method/likes.getList?type=post&owner_id=-"+group_id+"&item_id="+item_id+"&oauth=1&v=5.52&access_token="+auth_token+"&extended=true"
response = requests.get(url)
print response.text
generate_result(response.text)
print_result()


            
    



#response = requests.get("http://"+domen+"/api/v2/sender/subscribes/subscribe?token="+token+"&store_department_id="+did+"&email=d.bodunkov%2btest"+num+"%40sailplay.ru&comm_types_skus=[\"a1\",\"a2\",\"a3\",\"a4\"]")
