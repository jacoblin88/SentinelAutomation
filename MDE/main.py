import json
from operator import ne
import os
import msal
from dotenv import load_dotenv
import logging
import requests
import urllib.request
import urllib.parse
import csv
from multiprocessing import Process

graph_url = "https://graph.microsoft.com/beta/"
Auth_headers = {}

machines_url = "https://api.securitycenter.microsoft.com/api/machines"
offboard_url = "https://api.securitycenter.microsoft.com/api/machines/{}/offboard"

def GetToken():
    tenantId = '09699c26-c01b-41ea-a9f7-262f877323be' # Paste your own tenant ID here
    appId = '7453a10e-aa11-4c49-b012-86eb0005e0bb' # Paste your own app ID here
    appSecret = 'JGd8Q~8UrHYiW5K.4P3wctx7HRddOSE9MgoCiaBP' # Paste your own app secret here

    url = "https://login.microsoftonline.com/%s/oauth2/token" % (tenantId)

    resourceAppIdUri = 'https://api.securitycenter.microsoft.com'

    body = {
        'resource' : resourceAppIdUri,
        'client_id' : appId,
        'client_secret' : appSecret,
        'grant_type' : 'client_credentials'
    }

    data = urllib.parse.urlencode(body).encode("utf-8")

    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    jsonResponse = json.loads(response.read())
    aadToken = jsonResponse["access_token"]
    return aadToken


def MakeHeaders(token):
    Auth_headers['Authorization'] = 'Bearer ' + token
    Auth_headers['Content-Type'] = 'application/json'


def ListMachines():
    res = requests.get(machines_url,headers=Auth_headers)
    json_raw = json.loads(res.text)
    return json_raw['value']

def OffboardMachine(id):
    comment_json = {'Comment': "Offboard 2022-07-14"}
    id_url = offboard_url.format(id)
    # print(id_url)
    res = requests.post(id_url,json=comment_json,headers=Auth_headers)
    print(res.text)
    print(res.status_code)

def OffboardMachineFromFile(csv_file):
    machine_csv = open(csv_file)
    csvreader = csv.DictReader(machine_csv)
    for row in csvreader:
        OffboardMachine(row['id'])

def GetMachineInfo(id):
    url = "https://api.securitycenter.microsoft.com/api/machines/{}"
    id_url = url.format(id)
    res = requests.get(id_url,headers=Auth_headers)
    return json.loads(res.text)

def GetMachineInfoFromFile(csv_file):
    machine_csv = open(csv_file)
    csvreader = csv.DictReader(machine_csv)
    dict_array = []

    for row in csvreader:
        json_item = GetMachineInfo(row['id'])
        if 'id' not in json_item:
            continue
        dict_array.append(json_item)
    return dict_array



def MakeCsvFile(filename,Csv_Headers,resultDict_Array):
    Csv_Array = []
    for arr_item in resultDict_Array:
        row = []
        for header in Csv_Headers:
            row.append(arr_item[header])
        Csv_Array.append(row)

    with open(filename,'w',encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow(Csv_Headers)
        for row in Csv_Array:
            writer.writerow(row)


def main():
    token = GetToken()
    MakeHeaders(token)

    # header = ['id','computerDnsName','onboardingStatus','ipAddresses']
    # machines_dict_array = ListMachines()
    # MakeCsvFile("machines_newstatus.csv",header,machines_dict_array)
    #OffboardMachine("1234")
    # OffboardMachineFromFile("fail_offboard_machine_status.csv")
    dict_array =  GetMachineInfoFromFile("offboard_failed_1.csv")
    header = ['id','osPlatform','computerDnsName','lastIpAddress']
    MakeCsvFile("fail_offboard_machine_status_1.csv",header,dict_array)

    



if __name__ == "__main__":
    main()