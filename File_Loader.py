import requests
from flask import Flask, json


def file_from_url(url):

    try:
        u_response = requests.get(url)
    except requests.ConnectionError:
        return "Connection Error"
    data = json.loads(u_response.text)
    return data

def load_file_from_upload(file):
    try:
        data = file.read()
    except:
        return "Connection Error"
    data = json.loads(data)
    return data




def add_data_to_result_to_show(result_to_show, param):
    print "adding value to result to show"
    result_to_show.insert(len(result_to_show), str(param))


def scoop_json(data, index_of_data, attrs):

    if isinstance(data,dict):
        attrs = attrs.split(".")
        for att in attrs:
            data = data[att]
        return data
    else:
        if len(attrs) > 0:
            attrs = attrs.split(".")
            data = data[int(index_of_data)]
            for att in attrs:
                data = data[att]
            return data
        else:
            return data


def convert_list_to_dic_and_filter(data, key_attr, appender, service):

    dictionary = {}
    for value in data:
        if len(service) > 0:
            if (value[key_attr].lower()).find(service.lower()) != -1:
                key = generate_key(value[key_attr], appender)
                dictionary[key] = value
        else:
            key = generate_key(value[key_attr], appender)
            dictionary[key] = value

    return dictionary


def generate_key(value, appender):
    if appender == 'REM_AFTER_LAST_UNDERSCORE':
        value = value[0:value.rindex("_")]
        return value.lower()
    if appender == 'NOTHING':
        return value.lower()


def elements_of_same_instance(element_1, element_2):
    if type(element_1) == type(element_2):
        return True
    else:
        return False
