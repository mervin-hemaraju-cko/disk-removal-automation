#!/usr/bin/env python3

import requests
import json
import os
import getpass
import utils.const as Const

# The template used in the lsit of drives
# template = {
#     "drive": "",
#     "disk": -1,
#     "offline": 0
# }

# Empty list of drives which will be filled.
drives = []
template = {
    "drives": drives
}


def generate_config_file():

    # Create and load file with drives
    with open(f'/home/{getpass.getuser()}/.diskremconf.json', 'w') as outfile:
        json.dump(template, outfile)

def load_drives(tasks):

    # Iterate through each tasks
    for task in tasks:

        # Fetch all tasks
        if(task["title"].lower().strip() == "drive" or task["title"].lower().strip() == "disk"):

            description = task["description"].lower().strip().split("-")
            disk_status = 0

            if(description[2] == "offline"):
                disk_status = 1

            drives.append(
                {
                    "drive": description[0].upper(),
                    "disk": description[1],
                    "offline": disk_status
                }
            )

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

    load_drives(filtered_tasks)

    generate_config_file()



if __name__ == "__main__":
    main()
