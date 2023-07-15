import requests
import json
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
devices_url = "https://192.168.0.109:8443/v1/devices"
headers = {"Authorization": "Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjA3MTYzODI5NWMyYWI4Y2NlNGI2MTBhYjU1MzE4MWE5MzlhYmMwZWMwNTYyMGQzMTFlMDBhZmI5NDEzZGVjZWIifQ.eyJpc3MiOiJkN2NlY2IyZS04NTdkLTRjYzEtODhhYy0yZDNmMmRjNGY0NTAiLCJ0eXBlIjoiYWNjZXNzIiwiYXVkIjoiaG9tZXNtYXJ0LmxvY2FsIiwic3ViIjoiNjZjNDNjYzAtZTllOC00NjQ2LTk3ZjQtM2Q2NjZiMTkxZTgyIiwiaWF0IjoxNjg4NTc3MzM3LCJleHAiOjIwMDQxNTMzMzd9.hyLjh33ZpqnlZZ0izrzRipnA5W3fHVZvmkTf895fnHeYZnMUVNmMHYPGIGJUOROt0MWQuf7e-TX2_ngWCdKW2w"}


def get_raw_json_data(verbose):
    response = requests.get(devices_url, headers=headers, verify=False)
    if (verbose): print(json.dumps(response.json(), indent=2))


#get_raw_json_data(True)


def get_device_attributes(name, verbose):
    response = requests.get(devices_url, headers=headers, verify=False)
    devices = response.json()
    for device in devices:
        device_name = device["attributes"]["customName"].lower()
        device_attributes = device["attributes"]
        if (f"{device_name}" == name.lower()):
            if (verbose):
                print(device_attributes)
            return device_attributes


def get_device_info(name, verbose):
    response = requests.get(devices_url, headers=headers, verify=False)
    devices = response.json()
    for device in devices:
        device_id = device["id"]
        device_name = device["attributes"]["customName"].lower()
        device_type = device["type"]
        if (f"{device_name}" == name.lower()):
            if (verbose):
                print('{"device_name": "'+device_name+'", "device_id": "' +
                      device_id+'", "device_type": "'+device_type+'"}')
            return '{"device_name": "'+device_name+'", "device_id": "'+device_id+'", "device_type": "'+device_type+'"}'


def list_type(verbose, data_type):
    response = requests.get(devices_url, headers=headers, verify=False)
    devices = response.json()
    data = []
    for device in devices:
        device_id = device["id"]
        device_name = device["attributes"]["customName"].lower()
        device_type = device["type"]
        if (device_name != "home"):

            if (data_type == "name" or data_type == 1):
                if (verbose):
                    print(f'{device_name}')
                data.append(device_name)

            if (data_type == "type" or data_type == 2):
                if (verbose):
                    print(f'{device_type}')
                data.append(device_type)

            if (data_type == "id" or data_type == 3):
                if (verbose):
                    print(f'{device_id}')
                data.append(device_id)

    if (verbose):
        print(data)
    return data


# Check for a device id in the response and use it in ControlLamp.py to turn that lamp on or off
