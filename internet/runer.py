 # -*- coding: utf-8 -*-
import requests
import json
import csv
import re
import vk

class Report:
    def __init__(self):
        data_loader = DataLoader()
        self.api = data_loader.get_api()
        self.activists = data_loader.load_activists()
        self.region_info = data_loader.load_region_info()   
        self.result = {}

    def init_result(self):
        self.result.clear()
        self.result['unknown'] = {}
        for act in self.activists:
            self.result[self.activists[act]['region']] = {}

    def generate_result(self, users):
        for user in users:
            act_id = str(user['uid'])
            if act_id in self.activists:
                act = self.activists[act_id]
                self.result[act['region']][act_id] = { 'name' : act['name'], 'surname': act['surname'], 'fathername': act['fathername']}
            else:
                self.result['unknown'][act_id] = { 'name' : '', 'surname': '', 'fathername': ''}
                if user.get('first_name'):
                    self.result['unknown'][act_id]['name'] = user['first_name']
                if user.get('last_name'):
                    self.result['unknown'][act_id]['surname'] = user['last_name']

    def make_report_part(self, rtype):
        self.init_result()
        if rtype == 'likes':
            users = self.get_likes()
        else:
            users = self.get_reposts()
        self.generate_result(users)
        print "--------------"+rtype+"--------------"
        self.result_printer.print_result(self.result)  

    def get_likes(self):
        response = self.api.likes.getList(type="post", owner_id=self.group_id, item_id=self.item_id, extended="1")
        users = response['items']
        return users

    def get_reposts(self):
        response = self.api.wall.getReposts(type="post", owner_id=self.group_id, post_id=self.item_id)
        result = response['profiles']
        return result 

    def input_data(self):
        url = raw_input('input post url: ')
        m = re.match(r".*wall(?P<group_id>[\w-]+)_(?P<item_id>\w+)", url)
        self.group_id = m.group('group_id')
        self.item_id = m.group('item_id')

        #self.group_id = '-120214657'
        #self.item_id = '283' 
  
    def make_report(self):
        self.result_printer = ResultPrinter(self.region_info)
        self.make_report_part("likes")
        self.make_report_part("reposts")


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

    def get_api(self):
        print "start auth"
        f = open('auth.txt', 'r')
        login = f.readline()[:-1]
        password = f.readline()[:-1]
        session = vk.AuthSession(app_id='6131487', user_login=login, user_password=password)
        api = vk.API(session)
   
        print "auth OK"
        return api

    
class ResultPrinter:
    def __init__(self, region_info):
        self.region_info = region_info    
        self.is_wide = False

    def set_wide_result(self, is_wide):
        self.is_wide = is_wide      

    def print_result(self, result):
        for region in result:
            self.print_region(region, len(result[region]))
            if self.is_wide or region == 'unknown':
                self.print_activists(result[region])

    def print_region(self, region, count):
        info = ""
        if self.region_info.get(region) != None:
            info = self.region_info[region]
    
        print '('+str(count)+')', region, (' - ' + info if info != "" else "")
    
    def print_activists(self, activists):
        for act_id in activists:
            act = activists[act_id]
            print  '. . . ', act_id, act['name'], act['surname'], act['fathername']

    
report = Report()
report.input_data()
report.make_report()
