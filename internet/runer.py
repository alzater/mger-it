 # -*- coding: utf-8 -*-
import requests
import json
import csv



class Report:
    def __init__(self):
        data_loader = DataLoader()
        self.auth_token = data_loader.get_auth_hash()
        self.activists = data_loader.load_activists()
        self.region_info = data_loader.load_region_info()   
        self.result = {}

    def init_result(self):
        self.result.clear()
        self.result['unknown'] = {}
        for act in self.activists:
            self.result[self.activists[act]['region']] = {}

    def generate_result(self, response):
        js_response = json.loads(response)
        if js_response["response"].get("profiles") != None:
            items = js_response["response"]["profiles"]
        else:
            items = js_response["response"]["items"]

        for item in items:
            act_id = str(item['id'])
            if act_id in self.activists:
                act = self.activists[act_id]
                self.result[act['region']][act_id] = { 'name' : act['name'], 'surname': act['surname'], 'fathername': act['fathername']}
            else:
                self.result['unknown'][act_id] = { 'name' : '', 'surname': '', 'fathername': ''}
                if item.get('first_name'):
                    self.result['unknown'][act_id]['name'] = item['first_name']
                if item.get('last_name'):
                    self.result['unknown'][act_id]['surname'] = item['last_name']

    def make_report_part(self, url):
        self.init_result()
        response = requests.get(url)
        self.generate_result(response.text)
        print "--------------likes--------------"
        self.result_printer.print_result(self.result)     

    def input_data(self):
        #group_id = raw_input('input group_id:')
        #item_id = raw_input('input item_id:')
        self.group_id = '120214657'
        self.item_id = '274' 
  
    def make_report(self):
        self.result_printer = ResultPrinter(self.region_info)

        url = "https://api.vk.com/method/likes.getList?type=post&owner_id=-"+self.group_id+"&item_id="+self.item_id+"&oauth=1&v=5.52&access_token="+self.auth_token+"&extended=true"
        self.make_report_part(url)

        url = "https://api.vk.com/method/wall.getReposts?&owner_id=-"+self.group_id+"&post_id="+self.item_id+"&oauth=1&v=5.52&access_token="+ self.auth_token
        self.make_report_part(url)


class DataLoader:
    def __init__(self):
        print "init loader"

    def load_activists(self):
        activists = {}
        with open('activists.csv', 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                activists[row[0]] = {}
                act = activists[row[0]]
                act['region'] = row[1]
                act['name'] = row[2]
                act['surname'] = row[3]
                act['fathername'] = row[4]
        return activists

    def load_region_info(self):
        region_info = {}
        with open('region_info.csv', 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                region_info[row[0]] = row[1] 
        return region_info

    def get_auth_hash(self):
        f = open('auth.txt', 'r')
        return f.readline()[:-1]

    
class ResultPrinter:
    def __init__(self, region_info):
        self.region_info = region_info    
        self.is_wide = False

    def set_wide_result(self, is_wide):
        self.is_wide = is_wide      

    def print_result(self, result):
        for region in result:
            self.print_region(region, len(result[region]))
            if self.is_wide:
                self.print_activists(result[region])

    def print_region(self, region, count):
        info = ""
        if self.region_info.get(region) != None:
            info = self.region_info[region]
    
        print '('+str(count)+')', region, (' - ' + info if info != "" else "")
    
    def print_activists(self, activists):
        for act_id in activists:
            act = activists[act_id]
            print  '    ', act_id, act['name'], act['surname'], act['fathername']

    
report = Report()
report.input_data()
report.make_report()
