import re
import csv
import sys
import os
from .string_subs import *
import pandas as pd
from pathlib import Path
import requests

global global_dic
global_dic = {}
global functions_pool
functions_pool = {"falcon_wikipedia_function":"","falcon_dbpedia_function":"","falcon_UMLS_CUI_function":"",
                "falcon_wikipedia_description_function":"","falcon_dbpedia_description_function":"",
                "falcon_UMLS_CUI_description_function":"","concat2":""}


########################################################
################## Falcon Functions ####################
########################################################

headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

def falcon_wikipedia_function():
    value = global_dic["value"]
    output = ""
    url = 'http://node3.research.tib.eu:5005/falcon2/api?mode=short'
    entities=[]
    text = str(value).replace("_"," ")
    payload = '{"text":"'+text+'"}'
    r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
    if r.status_code == 200:
        response=r.json()
        for result in response['entities']:
            entities.append(result[0])
    else:
        r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
        if r.status_code == 200:
            response=r.json()
            for result in response['entities_wikidata']:
                entities.append(result[0])
    if len(entities) >= 1:
        return entities[0].replace('<','').replace('>','')
    else:
        return ""           

def falcon_dbpedia_function():
    value = global_dic["value"]
    output = ""
    url = 'http://node3.research.tib.eu:5005/api?mode=short'
    entities=[]
    text = str(value).replace("_"," ")
    payload = '{"text":"'+text+'"}'
    r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
    if r.status_code == 200:
        response=r.json()
        for result in response['entities']:
            entities.append(result[0])
    else:
        r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
        if r.status_code == 200:
            response=r.json()
            for result in response['entities']:
                entities.append(result[0])
    if len(entities) >= 1:
        return entities[0]
    else:
        return ""          

def falcon_UMLS_CUI_function():
    value = global_dic["value"]
    output = ""
    url = 'https://labs.tib.eu/sdm/biofalcon/api?mode=short'
    text = str(value).replace("_"," ")
    payload = '{"text":"'+text+'"}'
    r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
    if r.status_code == 200:
        response=r.json()
        return response['entities'][1][0]
    else:
        return ""

def falcon_wikipedia_description_function():
    value = global_dic["value"]
    output = ""
    url = 'http://node3.research.tib.eu:5005/falcon2/api?mode=long'
    entities=[]
    text = str(value).replace("_"," ")
    payload = '{"text":"'+text+'"}'
    r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
    if r.status_code == 200:
        response=r.json()
        for result in response['entities_wikidata']:
            entities.append(result[0])
    else:
        r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
        if r.status_code == 200:
            response=r.json()
            for result in response['entities_wikidata']:
                entities.append(result[0])
    if len(entities) >= 1:
        return list(str(entities[i]).replace('<','').replace('>','') for i in range (0, len(entities)))
    else:
        return ""           

def falcon_dbpedia_description_function():
    value = global_dic["value"]
    output = ""
    url = 'http://node3.research.tib.eu:5005/api?mode=long'
    entities=[]
    text = str(value).replace("_"," ")
    payload = '{"text":"'+str(text)+'"}'
    r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
    if r.status_code == 200:
        response=r.json()
        for result in response['entities']:
            entities.append(result[0])
    else:
        r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
        if r.status_code == 200:
            response=r.json()
            for result in response['entities']:
                entities.append(result[0])
    if len(entities) >= 1:
        return entities
    else:
        return ""            

def falcon_UMLS_CUI_description_function():
    value = global_dic["value"]
    output = ""
    url = 'http://node3.research.tib.eu:5005/api_umls?mode=long&type=cui'
    text = str(value).replace("_"," ")
    payload = '{"data":"'+text+'"}'
    r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
    if r.status_code == 200:
        response=r.json()
        entity_list = response['entities']
        return list(entity_list[i][0][1] for i in range (0, len(entity_list)))
    else:
        return ""

########################################################

def concat2():
    value1 = global_dic["value1"]
    value2 = global_dic["value2"]
    if bool(value1) and bool(value2):
        result = str(str(value1)+str(value2))
    else:
        result = ""  
    return(result)

################################################################################################
############################ Static (Do NOT change this code) ##################################
################################################################################################

def execute_function(row,header,dic):
    if "#" in dic["function"]:
        func = dic["function"].split("#")[1]
    else:
        func = dic["function"].split("/")[len(dic["function"].split("/"))-1]
    #print(dic)
    if func in functions_pool:
        global global_dic
        global_dic = execution_dic(row,header,dic)
        return eval(func + "()")             
    else:
        print("Invalid function")
        print("Aborting...")
        sys.exit(1)

def execution_dic(row,header,dic):
    output = {}
    for inputs in dic["inputs"]:
        if "constant" not in inputs:
            if "reference" in inputs[1]:
                if isinstance(row,dict):
                    output[inputs[2]] = row[inputs[0]]
                else:
                    output[inputs[2]] = row[header.index(inputs[0])]
            elif "template" in inputs:
                if isinstance(row,dict):
                    output[inputs[2]] = string_substitution(inputs[0], "{(.+?)}", row, "subject", "yes", "None")
                else:
                    output[inputs[2]] = string_substitution_array(inputs[0], "{(.+?)}", row, header, "subject", "yes")
        else:
            output[inputs[2]] = inputs[0]
    return output
