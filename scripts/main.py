#!/usr/bin/env python3
import requests
import json
import os
import utils.const as Const

template = {
    "drive": "",
    "disk": -1
}


def generate_config_file():
    with open('winpart_details.json', 'w') as outfile:
        json.dump(template, outfile)

def configure_template(tasks):

    # Iterate through each tasks
    for task in tasks:

        # Fetch the drive
        if(task["title"].lower() == "drive"):
            template["drive"] = task["description"]

        # Fetch the disk
        if(task["title"].lower() == "disk"):
            template["disk"] = task["description"]


def load_tasks(ticket):

    # Build Header
    headers = Const.require_headers_template(
        os.environ['ENV_FRESH_SERVICE_KEY_API_B64'])

    # Perform get requests to FreshService API
    response = requests.get(Const.VALUE_URL_BASE_FRESH_SERVICE_TASKS.format(
        os.environ['ENV_FRESH_SERVICE_URL'], ticket), headers=headers)

    # Check if get request is successful
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(
            Const.EXCEPTION_HTTP_ERROR_FRESHSERVICE)

    # Get all tasks
    tasks = json.loads(response.content)["tasks"]

    # Return a list of opened tasks ONLY
    return list(filter(lambda d: d["status"] == 1, tasks))

    

def main():

    # TODO("Handle Errors")
    # TODO("Add Logging")
    # TODO("Handle different failing scenarios")

    filtered_tasks = load_tasks("8156")

    configure_template(filtered_tasks)

    generate_config_file()



if __name__ == "__main__":
    main()
