#!/usr/bin/env python3

import requests
import sys
import json
import os
import getpass
import utils.const as Const


# Define empty lists of disks, drives and volumes
# that will be filled at the end of the script execution
drives = []
disks = []
volumes = []

diskpart_config_file = ".diskpart.txt"
json_config_file = ".diskremconf.json"

template = {
    "diskpart_config_file": diskpart_config_file,
    "volumes": volumes
}


def generate_config_files():
    # Create diskpart file config
    with open(f'/home/{getpass.getuser()}/{diskpart_config_file}', 'w') as textfile:

        # Drive delete commands
        for drive in drives:
            textfile.write(f"select volume {drive} \n")
            textfile.write(f"delete volume \n")
        
        # Disk offline command
        disk_offline = filter(lambda x: x["offline"] == 1, disks)

        for disk in disk_offline:
            textfile.write(f"select disk {disk['disk']} \n")
            textfile.write(f"offline disk \n")

        # Final Exit command
        textfile.write(f"exit")

    # Create json file config
    with open(f'/home/{getpass.getuser()}/{json_config_file}', 'w') as jsonfile:
        json.dump(template, jsonfile)

def load_drives(tasks):
    # Define all glboal variables
    global drives
    global volumes
    global disks

    # Iterate through each tasks
    for task in tasks:

        # Get the task title and format
        task_title = task["title"].lower().strip()

        # Fetch drives
        if(task_title == "drive" or task_title == "drives"):

            description = task["description"].lower().strip().split(";")
            
            # Clean each drives and format
            for d in description:
                drives.append(d.strip().upper())


        # Fetch Disks
        if(task_title == "disk" or task_title == "disks"):
            description = task["description"].lower().strip().split(";")
            disk_actions = [d.strip() for d in description]

            for action in disk_actions:
                split_action = action.split(":")
                disk_status = 0

                if(split_action[1] == "offline"):
                    disk_status = 1

                disks.append(
                    {
                        "disk": split_action[0],
                        "offline": disk_status
                    }
                )
        
        # Fetch Volumes
        if(task_title == "volume" or task_title == "volumes"):

            description = task["description"].lower().strip().split(";")

            # Clean each volumes
            for v in description:
                volumes.append(v.strip())

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
    
def retrieve_ticket_number():
    
    if(len(sys.argv) < 2):
        raise Exception("Missing Arguments")

    return sys.argv[1]

def main():

    # TODO("Handle Errors")
    # TODO("Add Logging")
    # TODO("Handle different failing scenarios")

    ticket = retrieve_ticket_number()

    filtered_tasks = load_tasks(ticket)

    load_drives(filtered_tasks)

    generate_config_files()



if __name__ == "__main__":
    main()
