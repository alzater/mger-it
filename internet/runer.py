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
            
    
class ResultPrinter:
    def __init__(self, is_wide):
        self.is_wide = is_wide  


    def print_result(self, result):
        for region in result:
            self.print_region(region)
            if self.is_wide:
                self.print_activists(result[region])

    def print_region(self, region):
        print region
    
    def print_activists(self, activists):
        for act_id in activists:
            act = activists[act_id]
            print  '    ', act_id, act['name'], act['surname'], act['fathername']

    

result_printer = ResultPrinter(True)
load_activists()
auth_token = get_auth_hash()
#group_id = raw_input('input group_id:')
#item_id = raw_input('input item_id:')
group_id = '120214657'
item_id = '275'
url = "https://api.vk.com/method/likes.getList?type=post&owner_id=-"+group_id+"&item_id="+item_id+"&oauth=1&v=5.52&access_token="+auth_token+"&extended=true"
response = requests.get(url)
generate_result(response.text)
result_printer.print_result(result)


            
    



#response = requests.get("http://"+domen+"/api/v2/sender/subscribes/subscribe?token="+token+"&store_department_id="+did+"&email=d.bodunkov%2btest"+num+"%40sailplay.ru&comm_types_skus=[\"a1\",\"a2\",\"a3\",\"a4\"]")
